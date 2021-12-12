#%%
from skimage.measure import block_reduce
#from functools import cached_property
from skimage.io import imread
from scipy.sparse import csr_matrix
import matplotlib.pyplot as plt
# import scipy.interpolate as itp
from operator import itemgetter
from functools import reduce
from itertools import chain
from glob import glob
from tqdm import tqdm
import pandas as pd
import numpy as np
import ffmpeg
import random
import time
import json

#import cv2

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
#%%

class Active_cell_finder(object):
    def __init__(self, frame_path, k=2, downsample=15, fs=25):
        self.frame_path = frame_path + "/*.tiff"
        #read tiff files
        Files = sorted(glob(self.frame_path))
        self.frames = np.array([imread(f) for f in Files])

        self.regionpath = "results.json"
        self.k = k
        self.downsample = (downsample, downsample)
        self.fs = fs


    def readjson(self):
        with open(self.regionpath) as f:
            regions = json.load(f)
        #return json file
        return regions


    def ROIs(self):
        # ROIs = {k: v for d in regions for k, v in d.items()}
        regions = self.readjson()
        regions = {list(i.items())[0][1]: list(i.items())[1][1] for i in regions}
        return regions


    def fluorescence_change(self, ):

        # calculate mean pixel value of each cell in each frame
        #this is the json file
        cellnumber = len(self.ROIs().items())
        print(cellnumber)
        T = self.frames.shape[0]
        output = np.zeros((cellnumber, T))
        loop = tqdm(self.frames, total=T, desc='extracting pixel intensity')
        
        for i, frame in enumerate(loop):
            for cell in self.ROIs().keys():
                position = self.ROIs()[cell]
                position = np.array(position)
                mean = np.mean(frame[position])
                output[cell, i] = mean

        # averaged pixel value of each cell
        output_del = np.delete(output, 0, 1)
        a = np.zeros((cellnumber, 1))
        output_new = np.c_[output_del, a]
        output = np.mat(output)
        average_value = np.mean(output, 1)

        # divide change level by the average pixel value of each cell
        average_value_new = np.tile(average_value, T)
        change_level = output_new - output
        change_signal = np.divide(change_level, average_value_new)

        # output the altered level of signal
        np.savetxt('./change_signal.csv', change_signal, delimiter=',')

        return np.asarray(change_signal)

    def filter(self, vector):

        # using binomial filter to smooth each cell signal
        bfilter = np.array([1, 2, 1])
        # add 0 to the start and the end
        vector_insert = np.insert(vector, 0, 0)
        vector_insert = np.append(vector_insert, 0)

        # dot product
        smoothed = []
        for i in range(0, len(vector_insert) - 2):
            smoothed = np.append(smoothed, np.dot(bfilter, vector_insert[i:i + 3]) / 4)
        # basline noise
        # return vector of same length
        substrate = vector - smoothed

        # calculate std and mean
        sd = np.std(substrate)
        mean = np.mean(substrate)

        # select original peaks that are 3std greater than mean
        # give them value 1
        # return a list of 0/1
        # filtered_vector = []
        filtered_vector = np.zeros_like(vector)
        filtered_vector[np.argwhere((substrate - mean) > self.k * sd)] = 1

        return filtered_vector

    def filter_mask(self, filtered_signal: np.ndarray):

        T = self.frames.shape[0]
        assert T == filtered_signal.shape[1]
        signal = pd.DataFrame(filtered_signal, index=self.ROIs().keys(), columns=list(range(T)))

        # get active ROIs in every frame
        sig_arr = np.array(signal)
        roi_ind, frame_ind = sig_arr.nonzero()
        roi_nz = signal.index.values[roi_ind]
        frame_nz = signal.columns.values[frame_ind]
        codebook = np.stack([roi_nz, frame_nz], axis=1)

        # get mask through codebook and generate video
        shape = self.frames.shape[1:]

        if len(shape) == 3:
            shape = shape[:-1]

        masks = []
        counts = []
        loop = tqdm(range(T), total=T, desc='finding active regions')
        for t in loop:
            active_roi_ind = codebook[codebook[:, 1] == t, 0]
            try:
                active_roi = itemgetter(*active_roi_ind)(self.ROIs())
                active_roi = list(chain.from_iterable(active_roi))
                rows, cols = zip(*active_roi)
            except TypeError:
                rows, cols = [], []

            mask = csr_matrix((np.ones_like(rows), (rows, cols)), shape).toarray()
            masks.append(mask)

            active_cell_count = len(active_roi_ind)
            counts.append(active_cell_count)

        masks = np.stack(masks)
        cumulative_mask = masks.sum(axis=0)

        return masks, counts, cumulative_mask

    def __call__(self, ):

        change_signal = self.fluorescence_change()

        filtered_signal = []
        for vector in change_signal:
            vector = np.squeeze(vector)
            filtered_vector = self.filter(vector)
            filtered_signal.append(filtered_vector)
        filtered_signal = np.stack(filtered_signal)

        M, C, CM = self.filter_mask(filtered_signal)
        T, height, width, *args = self.frames.shape

        process = (
            ffmpeg
                .input('pipe:', format='rawvideo', pix_fmt='gray8', s='{}x{}'.format(width, height))
                .output('active_cells.mp4', pix_fmt='gray8', vcodec='libx264', r=self.fs)
                .overwrite_output()
                .run_async(pipe_stdin=True)
                #.run(cmd='/anaconda3/lib/python3.7/site-packages/ffmpeg')
        )

        loop = tqdm(M, total=M.shape[0], desc='generating video')
        processed_masks = []
        for i, mask in enumerate(loop):
            mask *= 255
            mask_convert = Image.fromarray(mask)
            draw = ImageDraw.Draw(mask_convert)
            #** ImageFont模块**
            #选择文字字体和大小
            #setFont = ImageFont.truetype('C:/windows/fonts/Dengl.ttf', 20)，
            #设置文字颜色
            fillColor = "#ff0000"
            font = ImageFont.truetype('Times.ttf', 32)
            #写入文字
            draw.text((350, 50), 'frame {}: {} cells'.format(i, C[i]), fill=fillColor, font=font)
            mask = np.array(mask_convert)
            #cv2.rectangle(mask, (10, 50), (180, 76), 255, -1)
            #cv2.putText(mask, 'frame {}: {} cells'.format(i, C[i]), (10, 63), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))
            # mask = mask.astype(np.uint8)
            # while 1:
            #     cv2.imshow('src', mask)
            #     key = cv2.waitKey(30) & 0xFF
            #     if key == ord("q") or key == 27:
            process.stdin.write(
                mask.astype(np.uint8).tobytes()
            )
            processed_masks.append(mask)

        process.stdin.close()
        process.wait()

        CM_reduced = block_reduce(CM, block_size=(20, 20), func=np.mean, cval=CM.mean())
        plt.imshow(CM_reduced, cmap='magma', interpolation='bicubic')
        plt.colorbar()
        # plt.show()
        plt.savefig('./distribution')

        return np.stack(processed_masks)


#%%
ACF = Active_cell_finder('D:/zjuintl/Senior/BIA4/neurofinder.00.00/image2')
_ = ACF()


# %%
