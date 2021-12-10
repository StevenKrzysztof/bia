import cv2
import numpy as np
from skimage.morphology import disk, dilation, erosion
from skimage.filters.rank import minimum, median


class Rangefilter:

    def __init__(self, range_filter, frame, preview=True):
        self.filter = range_filter
        self.data_range = np.max(frame)
        self.image = frame
        self.preview = preview

    def callback(self, value):
        pass

    def setup_trackbars(self):
        cv2.namedWindow("set your threshold", 0)

        if self.filter != 'GREY':
            for i in ["MIN", "MAX"]:
                v = 0 if i == "MIN" else self.data_range
                for j in self.filter:
                    cv2.createTrackbar("%s_%s" % (j, i), "set your threshold", v, self.data_range, self.callback)
        else:
            cv2.createTrackbar('sigma', "set your threshold", 0, self.data_range, self.callback)

    def get_trackbar_values(self):
        values = []

        if self.filter != 'GREY':
            for i in ["MIN", "MAX"]:
                for j in self.filter:
                    v = cv2.getTrackbarPos("%s_%s" % (j, i), "set your threshold")
                    values.append(v)
        else:
            v = cv2.getTrackbarPos("sigma", "set your threshold")
            values.append(v)

        return values

    def _type_converter(self):

        if (len(self.image.shape) < 3) & (self.filter != 'GREY'):
            self.image = cv2.cvtColor(self.image, cv2.COLOR_GRAY2BGR)
            self.image = np.float32(self.image)

    def __call__(self):

        range_filter = self.filter.upper()
        self._type_converter()

        if self.filter != 'HSV':
            frame_to_thresh = self.image.copy()
        else:
            frame_to_thresh = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        self.setup_trackbars()

        while True:
            # v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = self.get_trackbar_values()
            args = self.get_trackbar_values()

            if self.filter != 'GREY':
                v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = self.get_trackbar_values()
                thresh = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
            else:
                Min = self.get_trackbar_values()
                # print(Min)
                # thresh = cv2.inRange(frame_to_thresh, Min, Max)
                thresh = (dilation(erosion(median(frame_to_thresh, selem=disk(4)), selem=disk(2)), selem=disk(2))) > Min

            if self.preview:
                preview = thresh.copy().astype(np.uint8) * 255
                # preview = cv2.bitwise_and(self.image, self.image, mask=thresh)
                # previewS = cv2.resize(preview, (540, 540))
                frame_to_thresh_s = frame_to_thresh.copy()/frame_to_thresh.max() * 255
                frame_to_thresh_s = frame_to_thresh_s.astype(np.uint8)
                cv2.imshow('frame', frame_to_thresh_s)
                cv2.imshow("mask", preview)
            else:
                cv2.imshow("Original", self.image)
                cv2.imshow("Thresh", thresh)

            if cv2.waitKey(1) & 0xFF is ord('s'):
                break

        return args
