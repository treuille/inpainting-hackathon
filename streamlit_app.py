import streamlit as st
import numpy as np
import cv2 as cv

# Inpainting code copied from:
# https://docs.opencv.org/master/df/d3d/tutorial_py_inpainting.html

# st.write(cv)
# st.write(cv.__version__)
# st.write(dir(cv))

"""
# Inpainting
"""

#st.file_uploader
uploaded_file = st.file_uploader("Choose a base image",
        type=['png', 'jpg', 'gif', 'jpeg'])
if uploaded_file is not None:
    st.write(type(uploaded_file))
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv.imdecode(file_bytes, cv.IMREAD_COLOR)
    #img = cv.imread(uploaded_file.read())
    """Here is the image you uploaded:"""
    st.write(type(img), img.shape)
    st.image(img, use_column_width=True, channels='BGR')
    # st.image
    #ata = pd.read_csv(uploaded_file)
    #st.write(data)
else:
    """The uploader has no images right now."""

#img = cv.imread('messi_2.jpg')
#mask = cv.imread('mask2.png',0)
#dst = cv.inpaint(img,mask,3,cv.INPAINT_TELEA)
#cv.imshow('dst',dst)
#cv.waitKey(0)
#cv.destroyAllWindows()
