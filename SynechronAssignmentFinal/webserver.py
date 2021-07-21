#   library for web apps
from flask import Flask, render_template, request
#   required libraries
import pytesseract
#   pattern search library
import glob
#   os library
import os
#   import function from other py program
from main import text_processing

app = Flask("my website")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit')
def submit():
    # using GET method
    Infilename = request.args.get("Infilename")
    Tesseract_loc = request.args.get("Tesseract_loc")
    Infilepath = request.args.get("Infilepath")
    Outfilepath = request.args.get("Outfilepath")
    Outfilename = request.args.get("Outfilename")
    return render_template('submit.html', Infilename=Infilename, Tesseract_loc=Tesseract_loc, Infilepath=Infilepath,
                           Outfilepath=Outfilepath, Outfilename=Outfilename)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
