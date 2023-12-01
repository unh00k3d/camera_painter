import camera_painter
import streamlit as st
import numpy as np

ranges=  [
    (np.array([160,60,90]),np.array([179,255,255])), # (lower , upper)
    (np.array([65,71,36]),np.array([88,255,255])),

]
painting_colors = [
    (0,0,255),  #BGR
    (0,255,0)
]


scaling_factor = 0.4
circle_radius = 10



def stopper():
    camera_painter.CONTINUE = False
def web_app():
    """
    a function that creates a webpage that has controls and can display the images
    """
    st.title("Camera Painter")
    st.write("This is a web app that allows you to paint on a camera feed.")
    # st.write("To paint on the camera feed, simply click on the canvas.")
    # st.write("To save the image, click on the save button.")
    # st.write("To clear the canvas, click on the clear button.")
    # st.write("To undo the last action, click on the undo button.")



    frame_placeholder = st.empty()
    canvas_placeholder = st.empty()
    result_placeholder = st.empty()
    st.button("Stop webcam",key= "stop",on_click=stopper)


# get the video stream
    for frame,canvas,result in camera_painter.color_detector(scaling_factor,circle_radius,ranges,painting_colors):
        frame_placeholder.image(frame,channels="BGR")
        canvas_placeholder.image(canvas,channels="BGR")
        result_placeholder.image(result,channels="BGR")



if __name__ == "__main__":

    try:
        web_app()

    except KeyboardInterrupt:
        camera_painter.CONTINUE = False
        st.write("Exiting...")