# pylint: disable=E1101
# pylint: disable=E1120

import streamlit as st
import numpy as np
import base64
import cv2
import requests

# Declare a Streamlit component.
# It will be served by the local webpack dev server that you can
# run via `npm run start`.
MaskInput = st.declare_component(url="http://localhost:3001")

# Alternately, if you've built a production version of the component,
# you can register the component's static files via the `path` param:
# MaskInput = st.declare_component(path="component_template/build")

"MaskInput", type(MaskInput)

# This is an optional step that enables you to customize your component's
# API, pre-process its input args, and post-process its output value.
@MaskInput
def create_instance(f, imgUrl, key=None):
    result = f(imgUrl=imgUrl, key=key) 
    if 'consoleMsg' in result:
        st.write('**consoleMsg:**', result['consoleMsg'])
    return result.get('value')

"MaskInput (again)", type(MaskInput), MaskInput

# Register the component. This assigns it a name within the Streamlit
# namespace. "Declaration" and "registration" are separate steps:
# generally, the component *creator* will do the declaration part,
# and a component *user* will do the registration.
st.register_component("mask_input", MaskInput)


"What did we register?", st.mask_input

# Create an instance of the component. Arguments we pass here will be
# available in an "args" dictionary in the component. "default" is a special
# argument that specifies the initial return value of mask_input, before the
# user has interacted with it.
img_url = "https://raw.githubusercontent.com/treuille/inpainting-hackathon/react-canvas-draw/data/emer-sleeping.png"
value = st.mask_input(img_url)
'value:', value

image_b64 = value['canvas'].split(",")[1]
binary = base64.b64decode(image_b64)
image = np.asarray(bytearray(binary), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)

'image:', type(image), image.shape 
st.image(image)
'mininum', np.amin(image.flat)
'maximum', np.amax(image.flat)

mask = np.zeros(image.shape[:2], dtype=np.uint8)
mask[image[:,:,0] > 0] = 255
'mask:', mask.dtype
st.image(mask)

st.image('https://github.com/treuille/inpainting-hackathon/raw/react-canvas-draw/data/emer-sleeping.png')

# Ask the user for the inpainting method.
inpainting_methods = [
    ('Navier-Stokes based method', cv2.INPAINT_NS),
    ('Method by Alexandru Telea [Telea04]', cv2.INPAINT_TELEA),
]

method = st.selectbox('Inpainting method', inpainting_methods, format_func=lambda x: x[0])[1]

def url_to_image(url):
    # download the image, convert it to a NumPy array, and then read
    # it into OpenCV format

    # resp = urllib.urlopen(url)
    # image = np.asarray(bytearray(resp.read()), dtype="uint8")

    r = requests.get(img_url)
    image = np.asarray(bytearray(r.content), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    'image shape before', image.shape
    image = image[...,::-1].copy()
    'image shape after', image.shape
    # return the image
    return image

img = url_to_image(img_url)
"the loaded image"
st.image(img)

"""
## Result
"""

# Create the mask itself
# mask = np.zeros((img_width, img_height), dtype=np.uint8)
# mask[mask_x : mask_x + mask_width, mask_y : mask_y + mask_height] = 255
'mask before', mask.shape
st.image(mask)
# mask = np.array([mask, mask, mask]).transpose((1, 2, 0))
'mask after', mask.shape
st.image(mask)
'image shape', img.shape
result = cv2.inpaint(img, mask, 3, method)
'result'
st.image(result)


raise RuntimeError('Early stopping.')

# # It can live in the sidebar.
# num_clicks = st.sidebar.mask_input("Sidebar")
# st.sidebar.markdown("You've clicked %s times!" % int(num_clicks))
# 
# name_input = st.text_input("Enter a name", value="Streamlit")
# 
# # Use the special "key" argument to assign your component a fixed identity
# # if you want to change its arguments over time and not have it be
# # re-created. (If you remove the "key" argument here, then the component will
# # be re-created whenever a new name is entered in 'name_input', which means
# # it will lose its current state.)
# num_clicks = st.mask_input(name_input, key="foo")
# st.markdown("You've clicked %s times!" % int(num_clicks))
