## Read and preprocess data
import os as os
import numpy as np
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array

def read_imgs(path_base, dir_categories):
    """
    Base path: str, must have trailing slash
    dirs: str, also label categories, no slashes
    """

    # path_categories = map(lambda x: path_base+x, dir_categories)


    # get file numbers for each category
    
    X = []
    y = []
    y_label_numeric = []

    for idx, dctg in enumerate(dir_categories):
        
        path_categories = path_base+dctg

        files_cat = os.listdir(path_categories)

        for i, fc in enumerate(files_cat):

            X.append(img_to_array(load_img(os.path.join(path_categories, fc))))
            y.append(dctg)
            y_label_numeric.append(idx)

    return {'X' : np.array(X), 'y' : np.array(y), 'y_label_numeric' : np.array(y_label_numeric)}
