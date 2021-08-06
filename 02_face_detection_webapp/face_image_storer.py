import cv2

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

Id = input('enter your id\n')
sampleNum = 0
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

while True:
    ret, img = cam.read()
    print(img.shape)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(x, y, w, h)
        cv2.putText(img, str(sampleNum), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 1)
        # saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User." + str(Id) + "." + str(sampleNum) + ".jpg",
                    gray[y:y + h, x:x + w])
        sampleNum = sampleNum + 1
        cv2.imshow('frame', img)
    # break if the sample number is morethan 20
    if (cv2.waitKey(10) & 0xFF == ord('q')) or (sampleNum > 100):
        break
print('--Capture Completed--')

cam.release()
cv2.destroyAllWindows()
