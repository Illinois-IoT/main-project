 #Import necessary libraries
from flask import Flask, render_template, Response
import cv2
import project
#Initialize the Flask app
app = Flask(__name__)

@app.route("/")
def start():
    return "Hello World"

@app.route("/take_picture")
def picture():
    project.capture_images("test")
    img = cv2.imread("../images/test.jpg")
    
    print(img)
    return "Picture Taken"
if __name__ == "__main__":
    app.run(debug=True)
