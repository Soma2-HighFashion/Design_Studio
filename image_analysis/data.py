try:
    import cPickle as pickle
except:
    import pickle
import os
from PIL import Image
import numpy as np

GEOMETRY = (128, 42)
PATCH_GEOMETRY = (42, 42)

def img2numpy_arr(img_path):
	return np.array(Image.open(img_path))

def generate_patches(ndarr, patch_count):
	step = (GEOMETRY[0] - PATCH_GEOMETRY[0]) / (patch_count-1)
	return [ndarr[i*step:i*step+PATCH_GEOMETRY[0], :, : ] for i in range(patch_count)]

def save2p(data, fname):
    try:
        with open(fname, "wb") as fh:
            pickle.dump(data, fh)
    except IOError as ioerr:
        print ("File Error: %s" % str(ioerr))
    except pickle.PickleError as pklerr:
        print ("Pickle Error: %s" % str(pklerr))

def load(fname):
    savedItems = []
    try:
        with open(fname, "rb") as fh:
            savedItems = pickle.load(fh)
    except IOError as ioerr:
        save2p(savedItems, fname)
    except pickle.PickleError as pklerr:
        print ("Pickle Error: %s" % str(pklerr))
    finally:
        return savedItems
