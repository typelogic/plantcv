# display instances in an image
import cv2
from matplotlib.patches import Polygon
import colorsys
import random
from skimage.measure import find_contours
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import patches, lines
from matplotlib.patches import Polygon
from plantcv import plantcv as pcv
from plantcv.plantcv import fatal_error
from plantcv.plantcv import params
from plantcv.plantcv import plot_image
from plantcv.plantcv import print_image
import os

def _overlay_mask_on_image(image, mask, color, alpha=0.5):
    """ apply a mask to an input image with a user defined color
    :param image: input RGB or grayscale image
    :param mask: desired mask
    :param color: (a tuple) desired color to show the mask on top of the image
    :param alpha: (a value between 0 and 1) transparency value when blending mask and image, by default 0.5
    :return: image with an mask with desired color on top of it
    """
    if len(image.shape) == 2:
        image = cv2.cvtColor(image.astype(np.uint8), cv2.COLOR_GRAY2BGR)
    for c in range(image.shape[-1]):
        image[:, :, c] = np.where(mask == 1,
                                  image[:, :, c] *
                                  (1 - alpha) + alpha * color[c] * 255,
                                  image[:, :, c])
    return image

# def _random_colors(num, bright=True):
#     """
#     Generate desired number of random colors. To get visually distinct colors, generate them in HSV space then convert to RGB.
#     :param num: number of colors to be generated
#     :param bright: True or False, if true, the brightness would be 1.0; if False, the brightness would be 0.7. By default it would be True (brightness 0.7)
#     :return: generated colors (a list of tuples)
#     """
#
#     brightness = 1.0 if bright else 0.7
#     hsv = [(i / num, 1, brightness) for i in range(num)]
#     colors = list(map(lambda c: colorsys.hsv_to_rgb(*c), hsv))
#     random.shuffle(colors)
#     return colors

def display_instances(image, masks, figsize=(16, 16), title="", ax=None, colors=None, captions=None, show_bbox=True):
    """
    This function is inspired by the same function used in mrcnn, showing different instances with different colors on top of the original image
    Users also have the option to specify the color for every instance, as well as the caption for every instance. Showing bounding boxes is another option.
    :param image: (required, ndarray)
    :param masks: (required, ndarray)
    :param figsize: (optional, tuple) the size of the generated figure
    :param title: (optional, str) the title of the figure
    :param ax: (optional, matplotlib.axes._subplots.AxesSubplot) the axis to plot on. If no axis is passed, create one and automatically call show()
    :param colors: (optional, list of tuples, every value should be in the range of [0.0,1.0]) a list of colors to use with each object. If no value is passed, a set of random colors would be used
    :param captions: (optional, str) a list of strings to use as captions for each object. If no list of captions is provided, show the local index of the instance
    :param show_bbox: (optional, bool) indicator of whether showing the bounding-box
    :return:masked_image
    :return:colors: colors used to show the instances (same as number of instances)
    """

    params.device += 1

    debug = params.debug
    params.debug = None

    if image.shape[0:2] != masks.shape[0:2]:
        fatal_error("Sizes of image and mask mismatch!")
    #
    # auto_show = False
    if not ax:
        _, ax = plt.subplots(1, figsize=figsize)
        # auto_show = True

    num_insts = masks.shape[2]
    # Generate random colors
    #     colors = colors or _random_colors(num_insts)

    if colors is not None:
        if max(max(colors)) > 1 or min(min(colors)) < 0:
            fatal_error("RGBA values should be within 0-1 range!")
    else:
        colors_ = pcv.color_palette(num_insts)
        colors = [tuple([ci / 255 for ci in c]) for c in colors_]

    if len(colors) < num_insts:
        fatal_error("Not enough colors provided to show all instances!")
    if len(colors) > num_insts:
        colors = colors[0:num_insts]

    # Show area outside image boundaries.
    height, width = image.shape[:2]
    ax.set_ylim(height + 10, -10)
    ax.set_xlim(-10, width + 10)
    ax.axis('off')
    ax.set_title(title)

    masked_image = image.astype(np.uint32).copy()

    for i in range(num_insts):
        color = colors[i]

        # Mask
        mask = masks[:, :, i]
        masked_image = _overlay_mask_on_image(masked_image, mask, color)

        ys, xs = np.where(mask > 0)
        x1, x2 = min(xs), max(xs)
        y1, y2 = min(ys), max(ys)
        if show_bbox:
            p = patches.Rectangle((x1, y1), x2 - x1, y2 - y1, linewidth=2, alpha=0.7, linestyle="dashed", edgecolor=color, facecolor='none')
            ax.add_patch(p)

        # Mask Polygon
        # Pad to ensure proper polygons for masks that touch image edges.
        padded_mask = np.zeros((mask.shape[0] + 2, mask.shape[1] + 2), dtype=np.uint8)
        padded_mask[1:-1, 1:-1] = mask
        contours = find_contours(padded_mask, 0.5)
        for verts in contours:
            # Subtract the padding and flip (y, x) to (x, y)
            verts = np.fliplr(verts) - 1
            p = Polygon(verts, facecolor="none", edgecolor=color)
            ax.add_patch(p)
        if not captions:
            caption = str(i)
        else:
            caption = captions[i]
        ax.text(x1, y1 + 8, caption, color='w', size=13, backgroundcolor="none")

    params.debug = debug
    if params.debug is not None:
        if params.debug == "plot":
            ax.imshow(masked_image)

        if params.debug == "print":
            ax.imshow(masked_image.astype(np.uint8))
            plt.savefig(os.path.join(params.debug_outdir, str(params.device) + "_displayed_instances.png"))
            plt.close("all")
    return masked_image, colors