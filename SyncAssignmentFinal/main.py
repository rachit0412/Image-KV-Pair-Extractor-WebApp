# import the required libraries
import cv2
import pytesseract
import csv
# reg ex library
import re
# delete library
import os


def text_processing(path, Outfullname, Outfilepath):
    """
    function will extract the necessary fields
    """
    if not os.path.exists(path):
        print("Image does not exists")
        quit()
    # converting image into gray scale image
    image = cv2.imread(path)
    # height, width, channel = image.shape
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # converting it to binary image by Thresholding, especially needed for colored images
    convert, thresh_img = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Find contours
    # contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # configuring parameters for tesseract, oem is engine, psm is page segmentation methods
    # psm 6: Assume a single uniform block of text
    # oem 3: Legacy + LSTM mode only

    custom_config = r'--oem 3 --psm 6'

    # now feeding image to tesseract
    details = pytesseract.image_to_data(thresh_img, output_type=pytesseract.Output.DICT, config=custom_config, lang="eng")
    # print(details.keys())

    # now feeding image to tesseract for string outout
    # details2 = pytesseract.image_to_string(thresh_img, config=custom_config, lang="eng")
    # print(details2)

    # draw boxes on text area detected by Tesseract. Using the detail dictionary.
    total_boxes = len(details['text'])
    for sequence_number in range(total_boxes):
        if int(details['conf'][sequence_number]) > 30:
            (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number],
                            details['width'][sequence_number], details['height'][sequence_number])
            image = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # parse and arrange the formatted data
    parse_text = []
    word_list = []
    last_word = ''
    for word in details['text']:
        if word != '':
            word_list.append(word)
            last_word = word
        if (last_word != '' and word == '') or (word == details['text'][-1]):
            parse_text.append(word_list)
            word_list = []

    # write to a temp file
    tempfile = Outfilepath + "temp_csv_file.csv'"
    with open(tempfile, 'w', newline="") as file:
        csv.writer(file, delimiter=" ").writerows(parse_text)

    read_csv = open(tempfile, "r")
    sometext = read_csv.read()
    company_type = re.search('Company Type (.*?)\n', sometext).group(1).strip()
    status = re.search('Status (.*?)\s', sometext).group(1).strip()
    registration_date = re.search('Registration Date (.*?)\s', sometext).group(1).strip()
    company_period = re.search('Company Period (.*?)\s', sometext).group(1).strip()
    req_dict = {'Company Type': company_type, 'Status': status, 'Registration Date': registration_date,
                'Company Period': company_period}

    # write the data to a file
    output_file = open(Outfullname, "a")
    print(req_dict, file=output_file)
    if os.path.exists(tempfile):
        read_csv.close()
        os.remove(tempfile)
