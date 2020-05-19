import streamlit as st
import numpy as np
import cv2 as cv
import sys

# Inpainting code copied from:
# https://docs.opencv.org/master/df/d3d/tutorial_py_inpainting.html

# st.write(cv)
# st.write(cv.__version__)
# st.write(dir(cv))

"""
# Inpainting
"""

# Let the user upload na image as the mask.
uploaded_file = st.file_uploader("Choose a base image",
        type=['png', 'jpg', 'gif', 'jpeg'])
if uploaded_file is not None:
    st.write(type(uploaded_file))
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv.imdecode(file_bytes, cv.IMREAD_COLOR)
    """Here is the image you uploaded:"""
    st.write(type(img), img.shape)
    st.image(img, use_column_width=True, channels='BGR')
else:
    """The uploader has no images right now."""
    sys.exit(0)

# Let the user select a mask:
img_width, img_height = img.shape[:2]
mask_width = st.slider('Mask width', 0, img_width // 2, img_width // 10)
mask_height = st.slider('Mask height', 0, img_height // 2, img_height // 10)
mask_x = st.slider('Mask x position', 0, img_width - mask_width, (img_width - mask_width) // 2)
mask_y = st.slider('Mask y position', 0, img_height - mask_height, (img_height - mask_height) // 2)
st.experimental_show(mask_width)
st.experimental_show(mask_height)
st.experimental_show(mask_x)
st.experimental_show(mask_y)

# Create the mask itself
mask = np.zeros((img_width, img_height), dtype=np.uint8)
mask[mask_x : mask_x + mask_width, mask_y : mask_y + mask_height] = 1
mask.shape
st.write(mask[:10,:10])
# mask = np.array([mask, mask, mask]).transpose((1, 2, 0))
mask.shape
st.image(mask, use_column_width=True)
'sum:', np.add.reduce(mask.flat)
#img = cv.imread('messi_2.jpg')
#mask = cv.imread('mask2.png',0)
#dst = cv.inpaint(img,mask,3,cv.INPAINT_TELEA)
#cv.imshow('dst',dst)
#cv.waitKey(0)
#cv.destroyAllWindows()img_width - mask_width, img_width - mask_width, img_width - mask_width, img_width - mask_width, img_width - mask_width, img_width - mask_width, 

