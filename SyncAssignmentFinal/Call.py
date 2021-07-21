# required libraries
import pytesseract
# pattern search library
import glob
# delete library
import os
from main import text_processing


if __name__ == "__main__":

    tesseract_loc = input("Enter the complete tesseract path: \n MACOS e.g. /usr/local/Cellar/tesseract/4.1.1/bin/tesseract OR Press Enter for Default") or "/usr/local/Cellar/tesseract/4.1.1/bin/tesseract"
    pytesseract.pytesseract.tesseract_cmd = tesseract_loc
    print("Current tesseract location on this machine is ", tesseract_loc)

    # parameterize input file
    Infilepath = input("\nEnter the complete input filepath: \n e.g. /Users/rachit/Desktop/images/ OR Press Enter for Default") or "/Users/rachit/Desktop/images/"
    Infilename = input("Enter the input filename pattern: \n e.g. *.png OR Press Enter for Default") or "*.png"
    Infullname = Infilepath + Infilename
    print("Full input path and file pattern is ", Infullname)

    # parameterize output file
    Outfilepath = input("\nEnter the complete output filepath: \n e.g. /Users/rachit/Desktop/images_output/ OR Press Enter for Default") or "/Users/rachit/Desktop/images_output/"
    check_dir = os.path.isdir(Outfilepath)
    if not check_dir:
        print("\nOutput dir does not exist please create it before running the program")
        exit(1)
    Outfilename = input("Enter the complete output filename: \n e.g. final_output.txt OR Leave empty for default value") or "final_output.txt"
    Outfullname = Outfilepath + Outfilename
    print("Full output path and filename is ", Outfullname)

    # delete any existing output file
    if os.path.exists(Outfullname):
        os.remove(Outfullname)
        print("\nPrevious job file has been deleted")
    else:
        print("\nCan not delete the file as it doesn't exists")

    # reading image using opencv
    print("\nStarting the Main text extraction function\n")
    path = glob.glob(Infullname)
    for img in path:
        print("processing image: ", img)
    # call the main function with the valid arguments
        text_processing(img, Outfullname, Outfilepath)
        print('success')
    print('\njob completed')
