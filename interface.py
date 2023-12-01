import camera_painter
import streamlit as st
import numpy as np

# ----------------------------------------------------

# ----------------------
# ADJUSTABLE VALUES
# ----------------------

# color ranges that will be detected in hsv format
ranges=  [
    (np.array([160,60,90]),np.array([179,255,255])), # (lower , upper) [hue,saturation,value]
    (np.array([65,71,36]),np.array([88,255,255])),

]

# the painting color corresponding to the range i.e. if a color in the range index 0 is detected it will paint with the color of index 0 etc...
painting_colors = [
    (0,0,255),  #BGR
    (0,255,0)
]

# how much should we scale the video stream up or down
scaling_factor = 0.4

# what is the radius of the circle that will be drawn in the center of the pen or in other words what is the thickness of the painting stroke
circle_radius = 10

# ----------------------------------------------------

def stopper():
    camera_painter.CONTINUE = False


def web_app():
    """
    a function that creates a webpage that has controls and can display the images
    """


    st.title("Camera Painter")
    st.write("This is a web app that allows you to paint on a camera feed.")

    # places where the video streams will be displayed
    frame_placeholder = st.empty()
    canvas_placeholder = st.empty()
    result_placeholder = st.empty()



    st.button("Stop webcam",key= "stop",on_click=stopper)


# get the video stream
    for frame,canvas,result in camera_painter.color_detector(scaling_factor,circle_radius,ranges,painting_colors):
        frame_placeholder.image(frame,channels="BGR",)
        canvas_placeholder.image(canvas,channels="BGR")
        result_placeholder.image(result,channels="BGR")


st.session_state()

if __name__ == "__main__":
    web_app()