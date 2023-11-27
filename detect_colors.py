import cv2
import sys
import numpy as np

class colorDetector:

    def __init__(self,control_window_name:str,initial_values:np.ndarray = None):
        """
        create the trackbars and so on to start detecting colors
        :param initial_values: a 1-D numpy array that contains the initial values in the order (hue min,hue max,sat min,sat max,vue min, vue max)
        NOTE: the numpy array given should have a dtype of int (of any kind) but not float
        :sub-param hue min/max: value between 0 and 179
        :sub-param sat min/max: value between 0 and 255
        :sub-param vue min/max: value between 0 and 255
        :return this function returns nothing
        """
        self.control_window_name = control_window_name

        # if no value is given we set them ourselves
        if initial_values is None:
            initial_values = np.array([0,179,0,255,0,255])
        
        # create a windows for controling the color that we want to detect
        cv2.namedWindow(control_window_name)
        # each time any parameter is updated the show_colors function will be called and it will update the image that show the color gradient accordingly
        cv2.createTrackbar('hue min',control_window_name,initial_values[0],179,lambda x : None)
        cv2.createTrackbar('hue max',control_window_name,initial_values[1],179,lambda x:None)
        cv2.createTrackbar('sat min',control_window_name,initial_values[2],255,lambda x:None)
        cv2.createTrackbar('sat max',control_window_name,initial_values[3],255,lambda x:None)
        cv2.createTrackbar('vue min',control_window_name,initial_values[4],255,lambda x:None)
        cv2.createTrackbar('vue max',control_window_name,initial_values[5],255,lambda x:None)


    def get_colors(self) -> tuple[int]:
        """
        a function that reads the values from the trackbar and return them back
        """

        # get the new values
        h_min = cv2.getTrackbarPos('hue min',self.control_window_name)
        h_max = cv2.getTrackbarPos('hue max',self.control_window_name)
        s_min = cv2.getTrackbarPos('sat min',self.control_window_name)
        s_max = cv2.getTrackbarPos('sat max',self.control_window_name)
        v_min = cv2.getTrackbarPos('vue min',self.control_window_name)
        v_max = cv2.getTrackbarPos('vue max',self.control_window_name)
        return h_min,h_max,s_min,s_max,v_min,v_max


    def detect_image(self,image_path:str,window_size:tuple[int]) -> None:
        """
        this function take the image path and detects the colors in the range specified in the control panel
        it will display 4 images as an overview of what is happening the images are :
        1. the original image
        2. the hsv version of the image
        3. the mask that is being applied in black and white
        4. the image after applying the mask

        :param image_path: string of the path of the image that we want to detect colors of
        :param window_size: tuple that specifies the heigh and width of the windows we want to display our out put at
        NOTE: windows_size should be in the format (height,width)
        """

        # define how much will we shrink each image
        scaling_factor = 0.5

        # get the size of each image according to the number or rows and columns
        size_of_one_image = ( int(window_size[0] * scaling_factor) , int(window_size[1] * scaling_factor))

        # load the image
        img = cv2.imread(image_path)

        # convert the image to HSV
        hsv_image = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

        img_resized = cv2.resize(img,size_of_one_image[::-1])
        hsv_image_resized = cv2.resize(hsv_image,size_of_one_image[::-1])

        # for more responsiveness i will concatenate the original and hsv version since they will no change
        concatenated_original_hsv_image  = np.hstack((img_resized,hsv_image_resized))


        while True:
            # get the new values
            h_min,h_max,s_min,s_max,l_min,l_max = self.get_colors()


            # create the mask
            mask = cv2.inRange(hsv_image_resized,np.array([h_min,s_min,l_min]),np.array([h_max,s_max,l_max]))

            # apply the mask to the image
            masked_image = cv2.bitwise_and(img_resized,img_resized,mask=mask)

            mask = cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)

            final = np.vstack((concatenated_original_hsv_image,np.hstack((masked_image,mask))))
            

            cv2.imshow('images',final)


            # quit if the user presses q

            if cv2.waitKey(1) == ord('q'):
                break



if __name__ == "__main__":
    cd = colorDetector('control')
    cd.detect_image(sys.argv[1],(600,800))
    cv2.destroyAllWindows()