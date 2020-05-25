# pylint: disable=E1101
# pylint: disable=E1120

import streamlit as st
import numpy as np
import base64
import cv2

# Declare a Streamlit component.
# It will be served by the local webpack dev server that you can
# run via `npm run start`.
MyComponent = st.declare_component(url="http://localhost:3001")

# Alternately, if you've built a production version of the component,
# you can register the component's static files via the `path` param:
# MyComponent = st.declare_component(path="component_template/build")

"MyComponent", type(MyComponent)

# This is an optional step that enables you to customize your component's
# API, pre-process its input args, and post-process its output value.
@MyComponent
def create_instance(f, name, key=None):
    return f(name=name, key=key, default=0)

"MyComponent (again)", type(MyComponent), MyComponent

# Register the component. This assigns it a name within the Streamlit
# namespace. "Declaration" and "registration" are separate steps:
# generally, the component *creator* will do the declaration part,
# and a component *user* will do the registration.
st.register_component("my_component", MyComponent)

"What did we register?", st.my_component

# Create an instance of the component. Arguments we pass here will be
# available in an "args" dictionary in the component. "default" is a special
# argument that specifies the initial return value of my_component, before the
# user has interacted with it.
result = st.my_component("World")
'state:', result['value']['state']
'consoleMsg:', result['consoleMsg']

dataurl = result['value']['canvas']
image_b64 = dataurl.split(",")[1]
binary = base64.b64decode(image_b64)
image = np.asarray(bytearray(binary), dtype="uint8")
image = cv2.imdecode(image, cv2.IMREAD_COLOR)

'image:', type(image), image.shape 
st.image(image)
'mininum', np.amin(image.flat)
'maximum', np.amax(image.flat)

mask = np.zeros(image.shape[:2], dtype=np.int32)
mask[image[:,:,0] > 0] = 255
'mask:', mask.dtype
st.image(mask)

raise RuntimeError('Early stopping.')

# # It can live in the sidebar.
# num_clicks = st.sidebar.my_component("Sidebar")
# st.sidebar.markdown("You've clicked %s times!" % int(num_clicks))
# 
# name_input = st.text_input("Enter a name", value="Streamlit")
# 
# # Use the special "key" argument to assign your component a fixed identity
# # if you want to change its arguments over time and not have it be
# # re-created. (If you remove the "key" argument here, then the component will
# # be re-created whenever a new name is entered in 'name_input', which means
# # it will lose its current state.)
# num_clicks = st.my_component(name_input, key="foo")
# st.markdown("You've clicked %s times!" % int(num_clicks))
