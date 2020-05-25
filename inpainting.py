# pylint: disable=E1101
# pylint: disable=E1120

import streamlit as st
import numpy as np
import base64
import cv2
import requests

### CONSTANTS ###

IMG_URL = "https://raw.githubusercontent.com/treuille/inpainting-hackathon/react-canvas-draw/data/emer-sleeping.png"

### FUNCTIONS ###

def register_mask_input(debug=True):
    """Declare the input mask component."""
    if debug:
        MaskInput = st.declare_component(url="http://localhost:3001")
    else:
        MaskInput = st.declare_component(path="component_template/build")
    MaskInput(create_mask_input)
    st.register_component("mask_input", MaskInput)

def create_mask_input(mask_input_component, imgUrl, key=None):
    """The MaskInput component returns a dictionary with two values:
    `value`, and optionally `consoleMsg`. The latter is a dictionary
    of debug information. This method strips out consoleMsg 
    (displaying it if it exists), then returns the underlying
    `value` object.
    """
    default_return_value = {'result': None}
    result = mask_input_component(imgUrl=imgUrl, key=key,
                default=default_return_value)
    if 'consoleMsg' in result:
        st.write('**consoleMsg:**', result['consoleMsg'])
    return result.get('value')

@st.cache
def load_image(url):
    """Load the image from the URL in RGB format and return
    it as a numpy array of type np.uint8."""
    response = requests.get(url)
    image = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = image[...,::-1].copy()
    return image


register_mask_input(debug=True)
value = st.mask_input(IMG_URL)
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


img = load_image(IMG_URL)
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
