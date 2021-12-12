import qtawesome
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from copy import deepcopy
from glob import glob
from tqdm import tqdm
from abc import ABC
import pandas as pd
import numpy as np
import warnings
import json
import sys

import os

# from range_filter import Rangefilter
from skimage.io import imread, imsave
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
import matplotlib.pyplot as plt


class DisplayImageWidget(QWidget):
    def __init__(self, parent=None):
        super(DisplayImageWidget, self).__init__(parent)

        self.image_frame = QLabel()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.image_frame)
        self.setLayout(self.layout)

    @QtCore.pyqtSlot()
    def show_image(self, image):
        image = QtGui.QImage(image.data, image.shape[1], image.shape[0],
                             QImage.Format_Grayscale8)  # .rgbSwapped()
        self.image_frame.setPixmap(QtGui.QPixmap.fromImage(image))


class Thresholding(QThread):

    signal = pyqtSignal(int, str, np.ndarray)

    def __init__(self, filter_type, stack, Min, Range):
        super(Thresholding, self).__init__()
        self.Min = Min
        self.Range = Range
        self.filter = filter_type
        self.stack = stack

    def run(self):

        warnings.filterwarnings("ignore")

        loop = tqdm(self.stack, total=self.stack.shape[0], desc='thresholding')
        for i, frame in enumerate(loop):

            # preprocess
            if len(frame.shape) == 3:
                frame = np.float32(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) if self.filter == 'HSV' else frame

            # thresholding and morpho
            if self.filter != 'GREY':
                v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = self.Range
                fgMask = cv2.inRange(frame, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
            else:
                fgMask = (dilation(erosion(median(frame, selem=disk(4)), selem=disk(2)), selem=disk(2))) > self.Min

            if i == len(loop) - 1:
                self.signal.emit(i, 'mask extracted!', fgMask)
            else:
                self.signal.emit(i, 'processing...', fgMask)


class Segmentation(QWidget):

    def __init__(self, range_filter, frame_path):
        super(Segmentation, self).__init__()

        Files = sorted(glob(frame_path + '/*.tiff'))
        frames = np.array([imread(f) for f in Files])[0: 1000, :, :]

        self.stack = frames
        self.filter = range_filter
        self.imax = np.max(self.stack, axis=0)

        frame = frames[0]
        self.data_range = np.max(frame)

        # preprocessing displayed image
        if (len(frame.shape) < 3) & (self.filter != 'GREY'):
            raise TypeError('should not apply GREY filter to RGB image!')
        else:
            self.frame_to_thresh = frame.copy()

        if len(self.frame_to_thresh.shape) == 3:
            self.frame_to_thresh = np.float32(self.frame_to_thresh)
            if self.filter == 'HSV':
                self.frame_to_thresh = cv2.cvtColor(self.frame_to_thresh, cv2.COLOR_RGB2HSV)

        # layouts
        if self.filter == 'GREY':
            self._setup_spinbox_grey()
        else:
            raise TypeError('Currently only GREY filter is supported')
            # self._setup_spinbox_nongrey()

    def _setup_spinbox_nongrey(self):

        # set window
        self.setWindowTitle('Threshold')
        self.resize(800, 700)
        # cv2.namedWindow("set your threshold", 0)

        slider = []
        Qboxs = []
        slider_label = []
        Qbox_label = []
        for i in ["MIN", "MAX"]:

            v = 0 if i == "MIN" else self.data_range
            _s = QSlider(Qt.Horizontal)
            _s.setMinimum(0)
            _s.setMaximum(self.data_range)
            _s.setSingleStep(10)
            _s.setValue(v)
            _s.setTickPosition(QSlider.TicksBelow)
            _s.setTickInterval(5)
            # _s.valueChanged.connect(self._valuechange)
            slider.append(_s)

            _s_label = QLabel('{}'.format(i))
            slider_label.append(_s_label)

            for j in self.filter:
                # cv2.createTrackbar("%s_%s" % (j, i), "set your threshold", v, self.data_range, self.callback)
                sp1 = QSpinBox()
                sp1.setRange(0, self.data_range)
                sp1.setSingleStep(10)
                sp1.setWrapping(True)
                sp1.setValue(v)
                sp1.valueChanged.connect(self._preview)
                Qboxs.append(sp1)

                sp_label = QLabel('{}_{}'.format(i, j))
                Qbox_label.append(sp_label)

        self.s1, self.s2 = slider
        self.s1.valueChanged.connect(self._s1_changevalue)
        self.s2.valueChanged.connect(self._s2_changevalue)

        self.sp1, self.sp2, self.sp3, self.sp4, self.sp5, self.sp6 = Qboxs
        self.sl1, self.sl2 = slider_label
        self.spl1, self.spl2, self.spl3, self.spl4, self.spl5, self.spl6 = Qbox_label

        self.getmaskbutton = QtWidgets.QPushButton(qtawesome.icon('fa.heart', color='white'), "Get Mask")
        # self.left_label_4.setObjectName('left_label')
        self.getmaskbutton.clicked.connect(self._thresholding)

        self.pbar = QProgressBar(self)

        # img displayer
        self.displayer_orig = DisplayImageWidget()
        self.displayer_mask = DisplayImageWidget()

        # display original at the start
        frame_to_thresh_s = self.frame_to_thresh.copy() / self.frame_to_thresh.max() * 255
        frame_to_thresh_s = frame_to_thresh_s.astype(np.uint8)
        self.displayer_orig.show_image(frame_to_thresh_s)

        # layout
        layout = QGridLayout()
        for i, (l, p) in enumerate(zip(Qbox_label, Qboxs)):
            layout.addWidget(l, i, 0, 1, 2)
            layout.addWidget(p, i, 2, 1, 6)

        for i, (l, p) in enumerate(zip(slider_label, slider)):
            layout.addWidget(l, i + 6, 1, 1, 2)
            layout.addWidget(p, i + 6, 3, 1, 3)

        layout.addWidget(self.displayer_orig, 9, 0, 4, 4)
        layout.addWidget(self.displayer_mask, 9, 4, 4, 4)
        layout.addWidget(self.getmaskbutton, 10, 0, 1, 2)
        layout.addWidget(self.pbar, 10, 4, 1, 4)
        self.pbar = QProgressBar(self)

        self.setLayout(layout)

    def _setup_spinbox_grey(self):

        # set window
        self.setWindowTitle('Threshold')
        self.resize(800, 700)
        layout = QGridLayout()

        self.s = QSlider(Qt.Horizontal)
        self.s.setMinimum(0)
        self.s.setMaximum(self.data_range)
        self.s.setSingleStep(10)
        self.s.setValue(0)
        self.s.setTickPosition(QSlider.TicksBelow)
        self.s.setTickInterval(5)
        self.s.valueChanged.connect(self._s_changevalue)
        self.l_s = QLabel('Threshold')

        self.sp = QSpinBox()
        self.sp.setRange(0, self.data_range)
        self.sp.setSingleStep(10)
        self.sp.setWrapping(True)
        self.sp.setValue(0)
        self.sp.valueChanged.connect(self._preview)
        self.l_sp = QLabel('Threshold')

        self.getmaskbutton = QtWidgets.QPushButton(qtawesome.icon('fa.heart', color='white'), "Get Mask")
        # self.left_label_4.setObjectName('left_label')
        self.getmaskbutton.clicked.connect(self._thresholding)

        self.pbar = QProgressBar(self)

        # img displayer
        self.displayer_orig = DisplayImageWidget()
        self.displayer_mask = DisplayImageWidget()

        # display original at the start
        frame_to_thresh_s = self.frame_to_thresh.copy() / self.frame_to_thresh.max()
        frame_to_thresh_s *= 255
        # plt.imshow(frame_to_thresh_s, cmap='gray')
        # plt.show()
        frame_to_thresh_s = frame_to_thresh_s.astype(np.uint8)
        self.displayer_orig.show_image(frame_to_thresh_s)

        # layout
        layout.addWidget(self.l_sp, 0, 0, 1, 2)
        layout.addWidget(self.sp, 0, 2, 1, 6)
        layout.addWidget(self.l_s, 1, 1, 1, 2)
        layout.addWidget(self.s, 1, 3, 1, 3)
        layout.addWidget(self.displayer_orig, 2, 0, 4, 4)
        layout.addWidget(self.displayer_mask, 2, 4, 4, 4)
        layout.addWidget(self.getmaskbutton, 6, 0, 1, 1)
        layout.addWidget(self.pbar, 6, 3, 1, 5)

        self.setLayout(layout)

    def _s1_changevalue(self):
        self.sp1.setValue(self.s1.value())
        self.sp2.setValue(self.s1.value())
        self.sp3.setValue(self.s1.value())
        self._preview()

    def _s2_changevalue2(self):
        self.sp4.setValue(self.s2.value())
        self.sp5.setValue(self.s2.value())
        self.sp6.setValue(self.s2.value())
        self._preview()

    def _s_changevalue(self):
        self.sp.setValue(self.s.value())
        self._preview()

    def _preview(self):

        if self.filter != 'GREY':
            v1_min, v2_min, v3_min = self.sp1.value(), self.sp2.value(), self.sp3.value()
            v1_max, v2_max, v3_max = self.sp4.value(), self.sp5.value(), self.sp6.value()
            thresh = cv2.inRange(self.frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
            self._range = [v1_min, v2_min, v3_min, v1_max, v2_max, v3_max]
        else:
            # print(Min)
            # thresh = cv2.inRange(frame_to_thresh, Min, Max)
            Min = self.sp.value()
            thresh = (
                         dilation(
                             erosion(
                                 median(
                                     self.frame_to_thresh,
                                     selem=disk(4)
                                 ),
                                 selem=disk(2)
                             ),
                             selem=disk(2)
                         )
                     ) > Min
            # print(Min)
            # print(thresh.nonzero()[0].shape)
            self._Min = Min

        if self.filter == 'GREY':
            preview = (thresh.copy() / thresh.max()) * 255
            preview = preview.astype(np.uint8)
        else:
            preview = cv2.bitwise_and(self.frame_to_thresh, self.frame_to_thresh, mask=thresh)

        # # cv2.imshow("mask", preview)
        self.displayer_mask.show_image(preview)

    @property
    def Min(self):
        Min = getattr(self, '_Min', None)
        if Min is None:
            if self.filter != 'GREY':
                return None
            else:
                return self.sp.value()
        else:
            return Min

    @property
    def Range(self):
        Range = getattr(self, '_Range', None)
        if Range is None:
            if self.filter == 'GREY':
                return None
            else:
                return [
                    self.sp1.value(),
                    self.sp2.value(),
                    self.sp3.value(),
                    self.sp4.value(),
                    self.sp5.value(),
                    self.sp6.value()
                ]
        else:
            return Range

    def _thresholding(self):

        # Min, Range = None, None
        # if self.filter == 'GREY':
        #     assert self.Min is not None
        #     Min = deepcopy(self.Min)
        # else:
        #     assert self.Range is not None
        #     Range = deepcopy(self.Range)

        self._mask_stack = []
        self.thread = Thresholding(self.filter, self.stack, self.Min, self.Range)
        self.thread.signal.connect(self._call_backlog)
        self.thread.start()

    def _call_backlog(self, i, string, mask):

        self._mask_stack.append(mask)

        self.pbar.setValue(i)
        self.pbar.setFormat(string)
        self.pbar.setAlignment(Qt.AlignCenter)

        if string == 'mask extracted!':
            self._postprocess()

    def _postprocess(self):

        print('!!')
        mask_stack = np.stack(self._mask_stack)
        mask = np.max(mask_stack, axis=0)
        watershed_mask = self._produce_watershed_mask(mask)
        rgb_labeled_mask = label2rgb(watershed_mask, image=self.imax, bg_label=0, alpha=1) * 255
        rgb_labeled_mask = rgb_labeled_mask.astype(np.uint8)
        print('!!')

        # save final mask
        imsave('./mask.png', rgb_labeled_mask)

    # def _thresholding(self):
    #
    #     warnings.filterwarnings("ignore")
    #
    #     Min, Range = None, None
    #     if self.filter == 'GREY':
    #         assert self.Min is not None
    #         Min = deepcopy(self.Min)
    #     else:
    #         assert self.Range is not None
    #         Range = deepcopy(self.Range)
    #
    #     loop = tqdm(self.stack, total=self.stack.shape[0], desc='thresholding')
    #     mask_stack = []
    #     for i, frame in enumerate(loop):
    #
    #         # preprocess
    #         if len(frame.shape) == 3:
    #             frame = np.float32(frame)
    #             frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) if self.filter == 'HSV' else frame
    #
    #         # thresholding and morpho
    #         if self.filter != 'GREY':
    #             v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = Range
    #             fgMask = cv2.inRange(frame, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
    #         else:
    #             fgMask = (dilation(erosion(median(frame, selem=disk(4)), selem=disk(2)), selem=disk(2))) > Min
    #
    #         mask_stack.append(fgMask)
    #         QApplication.processEvents()
    #         self.pbar.setValue(i)
    #
    #     # tricky stuff
    #     self.pbar.setFormat('Mask extracted!')
    #     self.pbar.setAlignment(Qt.AlignCenter)
    #
    #     mask_stack = np.stack(mask_stack)
    #     mask = np.max(mask_stack, axis=0)
    #     watershed_mask = self._produce_watershed_mask(mask)
    #     rgb_labeled_mask = label2rgb(watershed_mask, image=self.imax, bg_label=0, alpha=1) * 255
    #     rgb_labeled_mask = rgb_labeled_mask.astype(np.uint8)
    #
    #     # save final mask
    #     imsave('./final_mask.png', rgb_labeled_mask)

    def _produce_watershed_mask(self, mask):

        # apply the distance transform and find the maxima
        image3D_edt = distance_transform_edt(mask)
        peak_idx = peak_local_max(image3D_edt, min_distance=2, exclude_border=False)
        print(peak_idx.shape)

        # Peaks are returned as coordinates in the original image space, so we need to
        # transform them back to the image shape
        peak_mask = np.zeros_like(self.imax, dtype=bool)
        peak_mask[tuple(peak_idx.T)] = True

        # Lable the peaks and apply the watershed algorithm
        watershed_mask = watershed(-image3D_edt, markers=label(peak_mask), mask=mask)
        return watershed_mask


# files = sorted(glob('neurofinder.00.00/images/*.tiff'))
# frams = np.array([imread(f) for f in files])

# app = QApplication(sys.argv)
# demo = Rangefilter('GREY', 'neurofinder.00.00/images/*.tiff')
# demo.show()
# # demo = DisplayImageWidget()
# # demo.show_image(img)
# # demo.show()
# sys.exit(app.exec_())
