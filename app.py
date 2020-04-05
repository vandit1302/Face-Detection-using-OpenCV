from flask import Flask,render_template,url_for,request
import os
from skimage import io
import sys
import dlib


app = Flask(__name__)

port = int(os.environ.get('PORT', 5000))

@app.route('/index')
def index():
	return render_template('index.html')
""""
@app.route('/back')
def back():
	return render_template('index.html')"""

@app.route('/image',methods=['GET','POST'])
def detect():
    fc=0
    if request.method == 'POST':
        user = request.form['file']
        image = io.imread(user)
        fc = my_detect(image)

    return render_template('result.html',faces = fc)
    
def my_detect(image):
    # Take the image file name from the command line
    # image = sys.argv[1]

    # Create a HOG face detector using the built-in dlib class
    face_detector = dlib.get_frontal_face_detector()

    win = dlib.image_window()

    # Load the image into an array
    #image = io.imread(file_name)

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
        
    #im = Image.fromarray(face_rect)
    #im.save("your_file.jpeg")
        
    # Wait until the user hits <enter> to close the window	        
    dlib.hit_enter_to_continue()
    return len(detected_faces)
    

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)