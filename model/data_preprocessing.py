import tensorflow as tf
import numpy as np
import pandas as pd
import time
from tqdm import tqdm
from scipy import misc
import glob
import os
import random



def final_labels(label_file):
    final_labels =[]
    for val in label_file:
        aw = [0 for i in range(23)]
        aw[val] = 1
        final_labels.append(aw)
    return final_labels

def get_raw(path_to_csv):
    df = pd.read_csv(path_to_csv)
    print df.columns
    aw2s= df.images
    aw1s = df[df.columns[1]]
    im_id=[];im_label=[]
    for val in aw2s:
        im_id.append(val.lstrip("data/ima"))
    for val in aw1s:
        im_label.append(val)
    return im_id,im_label



def image_labels(im_id,im_label):
    print("length of id is",len(im_id))
    print("length of id is",len(im_label))
    final_label=[]
    final_images=[]
    cvg=0
    for fil in tqdm(glob.glob("/home/prayalankar/Downloads/anahita/images/*.png")):
        ax = fil
        op=ax.lstrip("/home/prayalankar/Downloads/anahita")
        #print op
        if op in im_id:
            cvg+=1
            idx = im_id.index(op)
            final_label.append(im_label[idx])
            rt = misc.imread(fil)
            final_images.append(rt)
        if cvg==1000:
            break
    print("length of id is",len(final_images))
    print("length of id is",len(final_images))
    return final_images , final_label
