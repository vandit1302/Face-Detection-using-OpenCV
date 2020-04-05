from flask import Flask,render_template,url_for,request
import os
from skimage import io
import sys
import dlib
import cv2


app = Flask(__name__)

port = int(os.environ.get('PORT', 5000))

@app.route('/index')
def index():
	return render_template('index2.html')


@app.route('/index2',methods=['GET','POST'])
def index2():
    if request.method == 'POST' or request.method == 'GET':
        
        #loads the Cascade with data of faces
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        #Sets the video source to the webcam (value = 0)
        video_capture = cv2.VideoCapture(0)

        while True:
            
            # Capture frame-by-frame
            ret, frame = video_capture.read()
            
            #converts image to Grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            #detectMultiScale is the function that detects Faces. Declaring the parameters for the function. Returns the list of Rectangles.
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
                #flags=cv2.cv2.CV_HAAR_SCALE_IMAGE
                flags=cv2.CASCADE_SCALE_IMAGE
            )

            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # Display the resulting frame
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # When everything is done, release the capture
        video_capture.release()
        cv2.destroyAllWindows()
    return render_template('index2.html')




@app.route('/image',methods=['GET','POST'])
def detect():
    fc=0
    if request.method == 'POST':
        user = request.form['file']
        image = io.imread(user)
        detected_faces = my_detect(image)
        detected2 = enumerate(detected_faces)
    return render_template('result2.html',detected_faces = detected2,l = len(detected_faces))



    
def my_detect(image):
    # Take the image array from the command line

    # Create a HOG face detector using the built-in dlib class
    face_detector = dlib.get_frontal_face_detector()

    win = dlib.image_window()

    # Run the HOG face detector on the image data.
    # The result will be the bounding boxes of the faces in our image.
    detected_faces = face_detector(image, 1)

    print("I found {} faces in the file ".format(len(detected_faces)))

    # Open a window on the desktop showing the image
    win.set_image(image)

    # Loop through each face we found in the image
    for i, face_rect in enumerate(detected_faces): 
        
        # Detected faces are returned as an object with the coordinates 
        # of the top, left, right and bottom edges
        print("- Face #{} found at Left: {} Top: {} Right: {} Bottom: {}".format(i, face_rect.left(), face_rect.top(), face_rect.right(), face_rect.bottom()))
        # Draw a box around each face we found
        win.add_overlay(face_rect)
        print(face_rect.left())
        
    # Wait until the user hits <enter> to close the window	        
    dlib.hit_enter_to_continue()
    return detected_faces
    

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)