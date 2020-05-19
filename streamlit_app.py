import streamlit as st
import numpy as np
import cv2 as cv

for i in range(100):
    st.write(i, 'Hello, world!!!')

# Inpainting code copied from:
# https://docs.opencv.org/master/df/d3d/tutorial_py_inpainting.html

#img = cv.imread('messi_2.jpg')
#mask = cv.imread('mask2.png',0)
#dst = cv.inpaint(img,mask,3,cv.INPAINT_TELEA)
#cv.imshow('dst',dst)
#cv.waitKey(0)
#cv.destroyAllWindows()
