import json
import os.path
import numpy as np
import keras
from keras.preprocessing.image import img_to_array, load_img

MODEL_PATH = os.path.abspath('../baseline.h5')
CLASS_INDICES_PATH = os.path.abspath('../class_indices.json')


def classify_doc_pic(image_path, model=None, class_indices=None):
    """
    Args:
      image_path (str): file path of the image
      model (Keras Model)
      class_indices (dict): e.g. {"0": "doc_template_01", "1": "doc_template_02", "2": "doc_template_03", "3": "doc_template_04"}

    Returns:
      {
        'class_index': class_index, # e.g. 0
        'class_name': class_indices[class_index] # e.g. "doc_template_01"
      }

    """
    img = load_img(image_path)
    img_arr = np.expand_dims(img_to_array(img), 0)

    # load model if it is not load
    if model is None:
        model = keras.models.load_model(MODEL_PATH)
        print('model loaded from: {}'.format(MODEL_PATH))

    if class_indices is None:
        class_indices = json.load(open(CLASS_INDICES_PATH, 'r'))
        print('class indices loaded from: {}'.format(CLASS_INDICES_PATH))

    class_index = np.asscalar(model.predict_classes(img_arr))

    return {
        'class_index': class_index,
        'class_name': class_indices[class_index]
    }
