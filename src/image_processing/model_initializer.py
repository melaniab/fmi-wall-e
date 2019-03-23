import os
import sys

ROOT_DIR = './Mask_RCNN'
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

assert os.path.exists(ROOT_DIR)
sys.path.append(ROOT_DIR)

from mrcnn.config import Config
import mrcnn.utils as utils
from mrcnn import visualize
import mrcnn.model as modellib
import skimage
import numpy as np


class CigButtsConfig(Config):
    """Configuration for training on the cigarette butts dataset.
    Derives from the base Config class and overrides values specific
    to the cigarette butts dataset.
    """
    # Give the configuration a recognizable name
    NAME = "cig_butts"

    # Train on 1 GPU and 1 image per GPU. Batch size is 1 (GPUs * images/GPU).
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 1  # background + 1 (cig_butt)

    # All of our training images are 512x512
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512

    # You can experiment with this number to see if it improves training
    STEPS_PER_EPOCH = 500

    # This is how often validation is run. If you are using too much hard drive space
    # on saved models (in the MODEL_DIR), try making this value larger.
    VALIDATION_STEPS = 5
    
    # Matterport originally used resnet101, but I downsized to fit it on my graphics card
    BACKBONE = 'resnet50'

    # To be honest, I haven't taken the time to figure out what these do
    RPN_ANCHOR_SCALES = (8, 16, 32, 64, 128)
    TRAIN_ROIS_PER_IMAGE = 32
    MAX_GT_INSTANCES = 50 
    POST_NMS_ROIS_INFERENCE = 500 
    POST_NMS_ROIS_TRAINING = 1000 
    
config = CigButtsConfig()


class InferenceConfig(CigButtsConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    IMAGE_MIN_DIM = 512
    IMAGE_MAX_DIM = 512
    DETECTION_MIN_CONFIDENCE = 0.85


# model_path: path to the coco model
def load_model_train(model_path):
    model = modellib.MaskRCNN(mode="training", config=config,
                              model_dir=MODEL_DIR)
    model.load_weights(model_path, by_name=True,
                           exclude=["mrcnn_class_logits", "mrcnn_bbox_fc", 
                                "mrcnn_bbox", "mrcnn_mask"])
    return model


# model_path: path to the coco model
def load_model_infer(model_path):
    inference_config = InferenceConfig()
    # Recreate the model in inference mode
    model = modellib.MaskRCNN(mode="inference", 
                          config=inference_config,
                          model_dir=MODEL_DIR)
    # Load trained weights (fill in path to trained weights here)
    assert model_path != "", "Provide path to trained weights"
    print("Loading weights from ", model_path)
    model.load_weights(model_path, by_name=True)
    return model


# real_test_dir: dir of the pictures to be predicted
# model: trained model
def _make_predictions_test(real_test_dir, model=None, model_dir=None):
    if not model:
        model = load_model_infer(model_dir)

    image_paths = []
    predictions = []

    for filename in os.listdir(real_test_dir):
        if os.path.splitext(filename)[1].lower() in ['.png', '.jpg', '.jpeg']:
            image_paths.append(os.path.join(real_test_dir, filename))

    for image_path in image_paths:
        img = skimage.io.imread(image_path)
        img_arr = np.array(img)
        results = model.detect([img_arr], verbose=1)
        predictions.append(results[0])
    return predictions

COCO_MODEL_PATH = '../../datasets/trained_weights/mask_rcnn_cig_butts_0008.h5'
real_test_dir = '../../datasets/cig_butts/real_test/'

# Use this to load a model!
load_model = lambda: load_model_infer(COCO_MODEL_PATH)

# Use this to make predictions!
make_predictions_test = lambda: _make_predictions_test(real_test_dir, model_dir=COCO_MODEL_PATH)
