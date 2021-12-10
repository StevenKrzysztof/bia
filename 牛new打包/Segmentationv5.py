import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from abc import ABC
import os
import warnings
import json
from glob import glob
import cv2
from tqdm import tqdm

from range_filter import Rangefilter
from skimage import io
from skimage import img_as_uint, img_as_float
from skimage import measure, color
from skimage.filters import gaussian, threshold_otsu
from skimage.filters.rank import minimum, median
from skimage.morphology import disk, dilation, erosion
from skimage.exposure import rescale_intensity, equalize_hist
from skimage.measure import label, regionprops, regionprops_table
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from scipy.ndimage import distance_transform_edt
from skimage.color import label2rgb


class Segmentation(object):
    def __init__(self, Filter):
        super().__init__()
        self.filter = Filter

    @property
    def mask(self):
        return self._mask

    @property
    def imax(self):
        return self._imax

    def _threholding(self, stack):

        Rf = Rangefilter(self.filter, stack[0])
        Min, v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = [None] * 7
        if self.filter != 'GREY':
            v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = Rf()
        else:
            Min = Rf()
        cv2.destroyAllWindows()

        loop = tqdm(stack, total=stack.shape[0], desc='thresholding')
        mask_stack = []
        for img in loop:

            # preprocess
            if len(img.shape) == 3:
                img = np.float32(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) if self.filter == 'HSV' else img

            # thresholding and morpho
            if self.filter != 'GREY':
                fgMask = cv2.inRange(img, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
            else:
                fgMask = (dilation(erosion(median(img, selem=disk(4)), selem=disk(2)), selem=disk(2))) > Min
            # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
            # fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)
            # fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_CLOSE, kernel)
            mask_stack.append(fgMask)

        return np.stack(mask_stack)

    def produce_watershed_mask(self, ):
        # apply the distance transform and find the maxima
        image3D_edt = distance_transform_edt(self.mask)
        peak_idx = peak_local_max(image3D_edt, min_distance=2, exclude_border=False)
        print(peak_idx.shape)

        # Peaks are returned as coordinates in the original image space, so we need to
        # transform them back to the image shape
        peak_mask = np.zeros_like(self.imax, dtype=bool)
        peak_mask[tuple(peak_idx.T)] = True

        # Lable the peaks and apply the watershed algorithm
        watershed_mask = watershed(-image3D_edt, markers=label(peak_mask), mask=self.mask)
        return watershed_mask

    def __call__(self, stack):
        self._imax = np.max(stack, axis=0)
        while True:
            mask_stack = self._threholding(stack)
            mask = np.max(mask_stack, axis=0)
            self._mask = mask
            watershed_mask = self.produce_watershed_mask()
            rgb_labeled_mask = label2rgb(watershed_mask, image=self.imax, bg_label=0, alpha=1)

            ok = False
            while 1:
                _mask = rgb_labeled_mask * 255
                _mask = _mask.astype(np.uint8)
                cv2.imshow('processed mask', _mask)
                key = cv2.waitKey(30) & 0xFF
                if key == ord("s"):
                    ok = True
                    break
                if key == ord("q") or key == 27:
                    break

            if not ok:
                continue
            else:
                break
        cv2.destroyAllWindows()

        # save mask as json
        props = measure.regionprops(watershed_mask)
        results = []
        count = 0
        for prop in props:
            result = {'id': count, 'coordinates': prop.coords.tolist()}
            results = np.append(results, result)
            count = count + 1

        results = results.tolist()
        with open('./results.json', 'w') as f:
            f.write(json.dumps(results))

        return results


def get_mask(img_path):

    warnings.filterwarnings("ignore")
    Seg = Segmentation('GREY')

    files = sorted(glob(img_path))
    im3d = np.array([io.imread(f) for f in files])
    res = Seg(im3d)
    return res
