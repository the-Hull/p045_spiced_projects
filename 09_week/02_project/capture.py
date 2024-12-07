import sys
import logging
import os
import cv2
from utils import write_image, key_action, init_cam, write_text_cam, get_predicted_label
import tensorflow as tf



if __name__ == "__main__":

    # folder to write images to
    out_folder = sys.argv[1]

    # maybe you need this
    os.environ['KMP_DUPLICATE_LIB_OK']='True'

    logging.getLogger().setLevel(logging.INFO)
   
    # also try out this resolution: 640 x 360
    webcam = init_cam(640, 480)
    key = None
    frame_count = 0
    cols = [(0,0,0)] * 3
    classes = ['here', 'we', 'go...']


    model = tf.keras.models.load_model('../../02_project/vgg_retrained.h5')

    try:
        # q key not pressed 

        pred_mode = False
        while key != 'q':
            # Capture frame-by-frame
            ret, frame = webcam.read()
            # fliping the image 
            frame = cv2.flip(frame, 1)
   
            # draw a [224x224] rectangle into the frame, leave some space for the black border 
            offset = 2
            width = 224
            x = 160
            y = 120
            cv2.rectangle(img=frame, 
                          pt1=(x-offset,y-offset), 
                          pt2=(x+width+offset, y+width+offset), 
                          color=(0, 0, 0), 
                          thickness=2
            )

           
            
            # get key event
            key = key_action()
            
            if key == 'space':
                # write the image without overlay
                # extract the [224x224] rectangle out of it
                image = frame[y:y+width, x:x+width, :]
                write_image(out_folder, image) 

            if key == 'p':
                pred_mode = not pred_mode

            # cols = [(0,0,0)] * 3
            if pred_mode:

                image = frame[y:y+width, x:x+width, :]

                classes = os.listdir('../../00_data')
                if frame_count % 30 == 0:
                    pred_class, pred_idx = get_predicted_label(
                        model=model, 
                        image=image, 
                        classes=classes)
                    cols = [(0,0,0)] * 3
                    cols[pred_idx] = (0,0,255)
                    
                xs = [60, 300, 460]
                for i,v in enumerate(xs):
                    write_text_cam(
                        text=classes[i],
                        frame=frame,
                        col=cols[i],
                        offset=offset-10,
                        y=y-10,
                        x=v
                    )

                # write_text_cam(
                # text=pred_class,
                # frame=frame,
                # col=(255,0,0),
                # offset=offset-10,
                # y=y,
                # x=x
                # # )

            # disable ugly toolbar
            cv2.namedWindow('frame', flags=cv2.WINDOW_GUI_NORMAL)              
            
            # display the resulting frame
            cv2.imshow('frame', frame)    

            frame_count += 1        
            
    finally:
        # when everything done, release the capture
        logging.info('quit webcam')
        webcam.release()
        cv2.destroyAllWindows()
