import cv2

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)


# tracker = cv2.legacy.TrackerMOSSE_create() # less accurate

# Select region of interest

def check_region():
    # detect the first frame for object selection
    tracker = cv2.legacy.TrackerCSRT_create()  # more accurate
    success, img = cap.read()
    bbox = cv2.selectROI('Tracking', img, False)
    while bbox[0] == bbox[1] == bbox[2] == bbox[3] == 0:
        success, img = cap.read()
        cv2.putText(img, 'Try Again', (75, 75),
                    cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (255, 0, 0), 1)
        bbox = cv2.selectROI('Tracking', img, False)
    return img, bbox, tracker


img, bbox, tracker = check_region()
# Initialize tracking
tracker.init(img, bbox)


def drawBox(img, bbox):
    x, y, w, h = bbox
    x, y, w, h = int(x), int(y), int(w), int(h)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.putText(img, 'Tracking', (75, 75), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)


while True:

    if cv2.waitKey(20) & 0xff == ord('y'):
        img, bbox, tracker = check_region()
        tracker.init(img, bbox)

    timer = cv2.getTickCount()
    success, img = cap.read()

    success2, bbox = tracker.update(img)
    print(success2)
    if success2:
        drawBox(img, bbox)
    else:
        cv2.putText(img, 'Lost', (75, 75), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
        cv2.putText(img, 'Press \'y\' to try Again', (75, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 1)
    cv2.imshow('Tracking', img)

    if cv2.waitKey(10) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

# import cv2
# import numpy as np

#
# def drawBox(img, bbox):
#     x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
#     cv2.rectangle(img, (x, y), ((x + w), (y + h)), (0, 0, 255), 3, 1)
#     cv2.putText(img, "Tracking", (50, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 1)
#
#
# # load video from camera
#
# cap = cv2.VideoCapture(1)
#
# # tracker for opencv
#
# tracker = cv2.legacy.TrackerMOSSE_create()
# # tracker = cv2.TrackerCRST.create()
# success, img = cap.read()
# print("success", success)
#
# bbox = cv2.selectROI("Tracking", img, False, False)
#
# tracker.init(img, bbox)
#
# while True:
#     timer = cv2.getTickCount()
#
#     success, img = cap.read()
#
#     success, bbox = tracker.update(img)
#
#     if success:
#         drawBox(img, bbox)
#     else:
#         cv2.putText(img, "Lost", (50, 60), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 1)
#
#     fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
#     cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 1)
#
#     cv2.imshow("Tracking", img)
#
#     if cv2.waitKey(1) & 0xff == ord('q'):
#         cv2.destroyAllWindows()
#         break
