import cv2
import pytesseract
import re

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

img = cv2.imread('pan1.jpg')
hImg, wImg, dummy = img.shape

boxes = pytesseract.image_to_data(img, lang='eng')
panNo = []
dob = []
for x, b in enumerate(boxes.splitlines()):
    if x != 0:
        b = b.split('\t')

        if b[-1] == "":
            b.pop(-1)

        if len(b) == 12 and len(b[11]) == 10 and (re.findall("\w\w\w\w\w\d\d\d\d\w", b[11]) or re.findall("\d\d/\d\d/\d\d\d\d", b[11])):
            x, y, w, h = int(b[6]), int(b[7]), int(b[8]), int(b[9])
            cv2.putText(img, b[11], (x, y - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (100, 255, 255), 2)
            if re.findall('\w\w\w\w\w\d\d\d\d\w', b[11]):
                panNo.append(b[11])
            if re.findall('\d\d/\d\d/\d\d\d\d', b[11]):
                dob.append(b[11])

if panNo:
    print("Pan card no. is {}.".format(panNo[0]))
else:
    print("Pan card no. no found.")

if dob:
    print("DOB is {}.".format(dob[0]))
else:
    print("DOB not found.")
cv2.imshow('Result', img)
cv2.waitKey(0)
