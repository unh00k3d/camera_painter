import cv2
import sys
import numpy as np

class colorDetectorAdjustable:

    def __init__(self,control_window_name:str,color_count:int = 1,initial_values:np.ndarray = None):
        """
        create the trackbars and so on to start detecting colors
        :param initial_values: a 1-D numpy array that contains the initial values in the order (hue min,hue max,sat min,sat max,vue min, vue max)
        NOTE: the numpy array given should have a dtype of int (of any kind) but not float
        :sub-param hue min/max: value between 0 and 179
        :sub-param sat min/max: value between 0 and 255
        :sub-param vue min/max: value between 0 and 255

        :param color_count: the number of colors that we want to detect (default is 1)
        :return this function returns nothing
        """
        self.control_window_name = control_window_name
        self.color_count = color_count

        # if no value is given we set them ourselves
        if initial_values is None:
            initial_values = np.array([[0,179,0,255,0,255] for _ in range(color_count)])
        
        # create a windows for controling the color that we want to detect
        cv2.namedWindow(control_window_name)
        # each time any parameter is updated the show_colors function will be called and it will update the image that show the color gradient accordingly
        for i in range(color_count):

            cv2.createTrackbar(f'{i} hue min',control_window_name,initial_values[i][0],179,lambda x : None)
            cv2.createTrackbar(f'{i} hue max',control_window_name,initial_values[i][1],179,lambda x:None)
            cv2.createTrackbar(f'{i} sat min',control_window_name,initial_values[i][2],255,lambda x:None)
            cv2.createTrackbar(f'{i} sat max',control_window_name,initial_values[i][3],255,lambda x:None)
            cv2.createTrackbar(f'{i} vue min',control_window_name,initial_values[i][4],255,lambda x:None)
            cv2.createTrackbar(f'{i} vue max',control_window_name,initial_values[i][5],255,lambda x:None)


    def get_colors(self) -> list[tuple[np.ndarray]]:
        """
        a function that reads the values from the trackbar and return them back
        """

        result = []

        for i in range(self.color_count):

            # get the new values
            h_min = cv2.getTrackbarPos(f'{i} hue min',self.control_window_name)
            h_max = cv2.getTrackbarPos(f'{i} hue max',self.control_window_name)
            s_min = cv2.getTrackbarPos(f'{i} sat min',self.control_window_name)
            s_max = cv2.getTrackbarPos(f'{i} sat max',self.control_window_name)
            v_min = cv2.getTrackbarPos(f'{i} vue min',self.control_window_name)
            v_max = cv2.getTrackbarPos(f'{i} vue max',self.control_window_name)
            result.append((np.array([h_min,s_min,v_min]),np.array([h_max,s_max,v_max])))
        
        return result


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
        original_stacked  = np.hstack((img_resized,hsv_image_resized))
        while True:
            # get the new values
            values = self.get_colors()

            # initialize a value for the the mask_final variable to updated automatically later
            mask = cv2.inRange(hsv_image_resized,values[0][0],values[0][1])
            masked_image = cv2.bitwise_and(img_resized,img_resized,mask=mask)
            mask_stacked = np.hstack((masked_image,cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)))

            # add any other color masks if any
            for lower,upper in values[1:]:

                # create the mask
                mask = cv2.inRange(hsv_image_resized,lower,upper)

                # apply the mask to the image
                masked_image = cv2.bitwise_and(img_resized,img_resized,mask=mask)

                mask_stacked = np.vstack((mask_stacked,np.hstack((masked_image,cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)))))

            

            # combine 
            final = np.vstack((original_stacked,mask_stacked))

            
            cv2.imshow('images',final)



            # quit if the user presses q

            if cv2.waitKey(1) == ord('q'):
                break


    def detect_video(self,video_path:str) -> None:
        """
        this function take the video path and detects the colors in the range specified in the control panel
        it will display 4 video streams as an overview of what is happening the video which are :
        1. the original stream
        2. the hsv version of the stream
        3. the mask that is being applied in black and white
        4. the stream after applying the mask

        :param video_path: string of the path of the video that we want to detect colors of alternatively you can also put and integer for a webcam
        0 will be the defulat built-in webcam and if you have any other pluggen in webcam specify the number

        """

        # get the video capture object
        capture = cv2.VideoCapture(video_path)
        
        # get the dimensions of the video stream
        window_size = (int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)))

        # define how much will we shrink each image
        scaling_factor = 0.5

        # get the size of each image according to the number or rows and columns
        size_of_one_frame = ( int(window_size[0] * scaling_factor) , int(window_size[1] * scaling_factor))

        # we will continue doing this until the user presses q or the video stream ends
        while True:
            # get the frame
            ret , frame = capture.read()
            # if reading wasn't successful we break from the loop
            if not ret:
                break

            # resize image to be the size of one frame
            frame = cv2.resize(frame,size_of_one_frame[::-1])

            # convert to hsv
            hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

            # get the new values
            values = self.get_colors()

            original_stacked = np.hstack((frame,hsv_frame))

            # initialize a value for the the mask_final variable to updated automatically later
            mask = cv2.inRange(hsv_frame,values[0][0],values[0][1])
            masked_image = cv2.bitwise_and(frame,frame,mask=mask)
            mask_stacked = np.hstack((masked_image,cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)))

            for lower,upper in values[1:]:
                mask = cv2.inRange(hsv_frame,lower,upper)

                masked_image = cv2.bitwise_and(frame,frame,mask = mask)

                mask_stacked = np.vstack((mask_stacked,np.hstack((masked_image,cv2.cvtColor(mask,cv2.COLOR_GRAY2BGR)))))
            
            # display the streams
            final = np.vstack((original_stacked,mask_stacked))
            cv2.imshow('images',final)

            if cv2.waitKey(1) == ord('q'):
                break

        capture.release()



if __name__ == "__main__":
    cd = colorDetector('control',color_count=int(sys.argv[2]))
    cd.detect_image(sys.argv[1],(600,800))
    # try:
    #     cd.detect_video(int(sys.argv[1]))
    # except ValueError:
    #     cd.detect_video(sys.argv[1])
    cv2.destroyAllWindows()