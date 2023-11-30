import numpy as np
import cv2

def main():


    scaling_factor = 0.25 # change this
    circle_radius = 5 # change this

    # define the ranges of the colors you want to detect in the form (lower,upper) for lower and higher bound of the color range
    ranges=  [
        (np.array([160,60,90]),np.array([179,255,255])), # (lower , upper)
        (np.array([65,71,36]),np.array([88,255,255])),

    ]
    painting_colors = [
        (0,0,255),  #BGR
        (0,255,0)
    ]

    # drawn image canvas



    capture = cv2.VideoCapture(0)
    ret , frame = capture.read()

    # get the dimenstions of the video stream
    if ret:
        frame = cv2.resize(frame,(0,0),fx = scaling_factor,fy= scaling_factor)
        height = frame.shape[0]
        width = frame.shape[1]



    # initialize the canvas that we will be drawing into
    canvas = np.zeros((height,width,3),dtype=np.uint8)


    # start capturing stream
    while True:

        # read the frame and success signal from the capture object
        ret, frame = capture.read()

        # if frame was captured successfully
        if ret:
            # resize frame to the desired size
            frame = cv2.resize(frame,(0,0),fx = scaling_factor,fy= scaling_factor)


            # conver frame to hsv because it is easier to detect colors through it
            hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

            # obtain color masks using the ranges defined above 
            masks=  [
                    cv2.inRange(hsv_frame,lower,upper) 
                    for lower,upper in ranges
                ]
            

            # kernel that will be used to fill out gaps in the mask
            kernel = np.ones((30,30),np.uint8)

            # fill out the gaps in the masks this will help in detecting edges and contours with less noise
            filled_masks = [
                cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
                for mask in masks
            ]

            # detect edges in preperation for contour detection and approximation
    
            edges = [
                cv2.Canny(filled_mask,100,200)
                for filled_mask in filled_masks
            ]
            

            # find contours for each edge
            contours_list = [
                    cv2.findContours(edge,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[0]  # [0] because findcontours() return two values
                    for edge in edges
                ]
            
            # calculate the perimeter of the contours that have an area greater than 100 only
            perimeters_list = [
                            [
                                (contour,cv2.arcLength(contour,True)) 
                                for contour in contours 
                                if cv2.contourArea(contour) > 100
                            ]
                            for contours in contours_list 
                        ]
            
            # after filtering out all of the noise and only get the proper size contours
            # we will only take on of them we do not need multiple contours for a mask one is a good enough approximation


            # approximate the contour (i.e. reduce the number of forming the contour)
            approximations = [

                    (i,cv2.approxPolyDP(contour,0.02 * perimeter,True))
                    for i,perimeters in enumerate(perimeters_list)
                        for contour,perimeter in perimeters[:1]
                ]
        
            
            
            
            # get the moments of the contour i.e. get the crucial points of the contour

            # NOTE: we are saving the index alongside with anything else to be able to draw the correct color on screen
            moments = [
                (i,cv2.moments(approximation))
                for i,approximation in approximations
            ]
            
            # calculate center point using moments
            centers = [
                (i,(int(moment['m10'] / (moment['m00'] + 1e-5)),int(moment['m01'] / (moment['m00'] + 1e-5))))
                for i,moment in moments
            ]

            # draw circles
            for i,center in centers:
                cv2.circle(canvas,center,circle_radius,painting_colors[i],cv2.FILLED)
            

            # create a mask out of the canvas
            gray_canvas = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)
            alpha = cv2.threshold(gray_canvas,1,255,cv2.THRESH_BINARY)[1] / 255

            # expand the canvas to 3 dimensional so that we can multiply it with the canvas to obtain the foreground
            bgr_alpha = np.repeat(alpha[:,:,np.newaxis],3,axis=2).astype(np.uint8)
            
            # since only the values that were drawn have 1 and the rest is 0 when we multiply by 1 - alpha we get the opposite and make all of the 
            # places where something was drawn on the canvas equal to 0 in the frame preparing them to be replaced by the canvas values
            background = cv2.multiply(1 - bgr_alpha,frame)
            # since we have 0's in the places where something was drawn onto the canvas when we add the canvas those places will be filled with the values
            # in the canvas meaning we will draw on top of the canvas
            result = cv2.add(canvas,background)


            cv2.imshow('frame',frame)
            cv2.imshow('result',result)
            cv2.imshow('canvas',canvas)

            if cv2.waitKey(1) == ord('q'):
                break

            
    capture.release()





if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()

