import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import warnings
import json

from skimage import io
from skimage import img_as_uint, img_as_float
from skimage import measure, color 
from skimage.filters import gaussian, threshold_otsu
from skimage.filters.rank import minimum, median
from skimage.morphology import disk,dilation,erosion
from skimage.exposure import rescale_intensity, equalize_hist
from skimage.measure import label, regionprops
from skimage.segmentation import watershed
from skimage.feature import peak_local_max
from scipy.ndimage import distance_transform_edt
from skimage.color import label2rgb
from tqdm import tqdm
from glob import glob
from numpy import array


warnings.filterwarnings("ignore")


#导入所有images合成3Dimage

def seg(input_filepath):
    
    files = sorted(glob(input_filepath+'/*.tiff'))
    im3d = array([io.imread(f) for f in files])
    #print(im3d.shape)
    #print(im3d.dtype)

    #3D取max成2D

    imax = np.max(im3d, axis=0)
    #plt.imshow(imax, cmap="gray")


#定义 对图片进行亮度调整+filter处理+thresholding 的函数

    loop = tqdm(im3d, total=im3d.shape[0], desc='thresholding')
    image3D_threshold = np.zeros_like(im3d, dtype=bool)
    for i, img in enumerate(loop): 
        image3D_threshold[i] = (dilation(erosion(median(img,selem = disk(4)),selem = disk(2)),selem = disk(2))) > 980
    
    #return(image3D_threshold)

# threshold 最好能根据图片的average intensity改变，例如：> X * np.median(imax), 但X具体为多少待定


#运行modify_image函数，得到每帧图的mask

#im3d_threshold = modify_image(im3d)
#print(im3d_threshold.shape)
#print(im3d_threshold.dtype)


#将3D mask取max成2D

    threshold_mask = np.max(image3D_threshold,axis=0)
    #plt.imshow(final_threshold,cmap="gray")


#定义 进行watershed segmentation 的函数


    # apply the distance transform and find the maxima
    image3D_edt = distance_transform_edt(threshold_mask)
    peak_idx = peak_local_max(image3D_edt, min_distance=2, exclude_border=False)
    #print(peak_idx.shape)
    
    #Peaks are returned as coordinates in the original image space, so we need to transform them back to the image shape
    peak_mask = np.zeros_like(imax, dtype=bool)
    peak_mask[tuple(peak_idx.T)] = True
    
    # Lable the peaks and apply the watershed algorithm
    watershed_mask = watershed(-image3D_edt, markers = label(peak_mask), mask = threshold_mask)
    io.imsave('./mask.jpg', watershed_mask)



    #运行produce_watershed_mask函数，得到最终的watershed mask


    #plt.imshow(label2rgb(watershed_mask, image=imax, bg_label=0, alpha = 1))

    #这里同时保存mask文件至本地

    # 创建dictionary{cell index : 每个cell中所有pixel的坐标}

    props=measure.regionprops(watershed_mask)
    results=[]
    count=0
    for prop in props:
        result = {'id': count, 'coordinates':prop.coords.tolist()}
        results = np.append(results, result)
        count = count+1


    results = results.tolist()


    #将dictionary写进jason文件

    with open('results.json', 'w') as f:
        f.write(json.dumps(results))
    
    print("success")
#run file

#seg('D:/zjuintl/Senior/BIA4/neurofinder.00.00/image2')
#%%
#files = sorted(glob('D:/zjuintl/Senior/BIA4/neurofinder.00.00/*.tiff'))
#im3d = array([io.imread(f) for f in files])