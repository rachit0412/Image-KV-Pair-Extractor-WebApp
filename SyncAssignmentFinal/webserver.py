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

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit',methods=['GET','POST'])
def submit():
    if request.method == 'GET':
        return render_template('submit.html')
    elif request.method == 'POST':
        Infilename = request.form.get("Infilename")
        Tesseract_loc = request.form.get("Tesseract_loc")
        Infilepath = request.form.get("Infilepath")
        outfilepath = request.form.get("Outfilepath")
        Outfilename = request.form.get("Outfilename")
        if not Infilename or not Infilepath:
            path = Infilepath + "*.png"
            print("No value passed. All png files would be processed")
        else:
            path = Infilepath + Infilename + "*.png"
            print("Only png files with suffix", Infilename, "would be processed")
        if not outfilepath or not Outfilename or not Tesseract_loc:
            print("Values missing. Job will not run")
            breakpoint()
        else:
            outfullname = outfilepath + Outfilename
            print("Output would be written to: ", outfullname)

        text_processing(path=path, Outfullname=outfullname, Outfilepath=outfilepath)
        return render_template('submit.html', result='Success!')


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')
