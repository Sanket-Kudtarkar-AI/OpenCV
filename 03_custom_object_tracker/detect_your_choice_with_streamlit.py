import cv2
import streamlit as st

st.title("Webcam Live Feed")

FRAME_WINDOW = st.image([])

cap = cv2.VideoCapture(1)

run = st.checkbox("Run")


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

tracker.init(img, bbox)


def drawBox(img, bbox):
    x, y, w, h = bbox
    x, y, w, h = int(x), int(y), int(w), int(h)
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
    cv2.putText(img, 'Tracking', (75, 75), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)


while True and run:

    if cv2.waitKey(20) & 0xff == ord('y'):
        img, bbox, tracker = check_region()
        tracker.init(img, bbox)

    timer = cv2.getTickCount()
    success, img = cap.read()

    success2, bbox = tracker.update(img)
    if success2:
        drawBox(img, bbox)
    else:
        cv2.putText(img, 'Lost', (75, 75), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)
        cv2.putText(img, 'Press \'y\' to try Again', (75, 100), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    cv2.putText(img, str(int(fps)), (75, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 1)
    FRAME_WINDOW.image(img)

    if cv2.waitKey(10) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()