# pylint: disable=E1101
# pylint: disable=E1120

import streamlit as st
import numpy as np
import base64
import cv2
import requests


### CONSTANTS ###


IMG_URL = "https://raw.githubusercontent.com/treuille/inpainting-hackathon/master/data/emer-sleeping.png"


### FUNCTIONS ###


def register_mask_input(debug=True):
    """Declare the input mask component."""
    if debug:
        MaskInput = st.declare_component(url="http://localhost:3001")
    else:
        MaskInput = st.declare_component(path="frontend/build")
    MaskInput(mask_input_wrapper)
    st.register_component("mask_input", MaskInput)


def mask_input_wrapper(mask_input_component, imgUrl, key=None):
    """Decodes information from the MaskInput component, including
    decoding a png image into a numpy array of the mask."""

    # Get raw data back from the MaskInput component.
    result = mask_input_component(imgUrl=imgUrl, key=key, default={})

    # Debug information is stored in the 'consoleMsg' entry.
    if 'consoleMsg' in result:
        st.write('**consoleMsg:**', result['consoleMsg'])

    # The return value is stored in 'value' which we will convert
    # from an encoded png image into a numpy array.
    if 'value' in result:
        # The mask comes in as a base64 encoded png image.
        mask_image_b64 = result['value']
        binary = base64.b64decode(mask_image_b64.split(",")[1])
        image = np.asarray(bytearray(binary), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)

        # The mask itself is a single-channel uint8 image which is white
        # where inpainting should occur, and black everywhere else.
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        mask[image[:,:,0] > 0] = 255
        return mask
    else:
        # No mask has been created to return None
        return None


@st.cache
def load_image(url):
    """Load the image from the URL in RGB format and return
    it as a numpy array of type np.uint8."""
    response = requests.get(url)
    image = np.asarray(bytearray(response.content), dtype=np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = image[...,::-1].copy()
    return image

def get_user_input():
    """Returns a bunch of input from the sidebar UI."""
    # The image we're inpainting is hard-coded right now.
    img = load_image(IMG_URL)

    # As the user how they'd like to inpaint.
    inpainting_methods = [
        ('Navier-Stokes based method', cv2.INPAINT_NS),
        ('Method by Alexandru Telea [Telea04]', cv2.INPAINT_TELEA),
    ]
    inpainting_method = \
            st.sidebar.selectbox('Inpainting method', inpainting_methods, format_func=lambda x: x[0])[1]

    # Ask the user if they'd like to see the mask image.
    show_mask = st.sidebar.checkbox('Show mask')

    # Return this back
    return (img, inpainting_method, show_mask)

def main():
    """Execution starts here."""
    # Register the new mask_input custom component.
    register_mask_input(debug=True)

    # Title
    "# Adrien's Inpainting Demo"

    # Ask the user for input
    img, inpainting_method, show_mask = get_user_input()

    # Get the mask.
    '## Input'
    mask = st.mask_input(IMG_URL)

    # Perform the inpainting.
    if type(mask) != np.ndarray:
        # Issue a warning if there's no mask.
        st.warning('Draw on the image above to perform inpainting.')
    else:
        # Show the mask if the user requested so.
        if show_mask:
            '## Mask'
            st.image(mask)

        # Where all the magic happens.
        '## Result'
        inpainted_image = cv2.inpaint(img, mask, 3, inpainting_method)
        st.image(inpainted_image)

if __name__ == '__main__':
    main()
