import streamlit as st
import numpy as np
import cv2 as cv
import sys

# Inpainting code copied from:
# https://docs.opencv.org/master/df/d3d/tutorial_py_inpainting.html

"""
# Inpainting
"""

"""
## Input image
"""

# Let the user upload na image as the mask.
uploaded_file = st.file_uploader("Choose a base image",
        type=['png', 'jpg', 'gif', 'jpeg'])

if uploaded_file is not None:
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv.imdecode(file_bytes, cv.IMREAD_COLOR)
    st.image(img, use_column_width=True, channels='BGR')

    """
    ## Input parameters
    """

    # Let the user select a mask:
    img_width, img_height = img.shape[:2]
    mask_width = st.slider('Mask width', 0, img_width // 2, img_width // 10)
    mask_height = st.slider('Mask height', 0, img_height // 2, img_height // 10)
    mask_x = st.slider('Mask x position', 0, img_width - mask_width, (img_width - mask_width) // 2)
    mask_y = st.slider('Mask y position', 0, img_height - mask_height, (img_height - mask_height) // 2)

    # Ask the user for the inpainting method.
    inpainting_methods = [
        ('Navier-Stokes based method', cv.INPAINT_NS),
        ('Method by Alexandru Telea [Telea04]', cv.INPAINT_TELEA),
    ]
    method = st.selectbox('Inpainting method', inpainting_methods, format_func=lambda x: x[0])[1]
    """
    ## Result
    """

    # Create the mask itself
    mask = np.zeros((img_width, img_height), dtype=np.uint8)
    mask[mask_x : mask_x + mask_width, mask_y : mask_y + mask_height] = 255
    result = cv.inpaint(img, mask, 3, method)
    mask = np.array([mask, mask, mask]).transpose((1, 2, 0))
    st.image([mask, result], caption=['mask', 'result'], use_column_width=True, channels='BGR')

else:
    st.warning('To get started, click above to upload an image.')
