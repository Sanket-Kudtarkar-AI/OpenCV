import streamlit as st
import cv2
from PIL import Image
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

rec = cv2.face.LBPHFaceRecognizer_create()
rec.read("trainingData.yml")


def detect_faces(our_image):
    img = np.array(our_image.convert('RGB'))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw rectangle around the faces
    # name = 'Unknown'

    for (x, y, w, h) in faces:
        # To draw a rectangle in a face
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)
        Id, uncertainty = rec.predict(gray[y:y + h, x:x + w])
        print("Id = ", Id, "Uncertainty = ", uncertainty)

        if uncertainty < 53:
            if Id == 1 or Id == 3 or Id == 5:
                name = "Me"
                cv2.putText(img, name, (x, y + h), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2.0, (0, 0, 255))
        else:
            cv2.putText(img, 'Unknown', (x, y + h), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2.0, (0, 0, 255))

    return img, gray[faces[0][1]:faces[0][1] + faces[0][3], faces[0][0]:faces[0][0] + faces[0][2]]


def main():
    """Face Recognition App"""

    st.title("Streamlit Tutorial")

    html_temp = """
    <body style="background-color:blue;">
    <div style="background-color:teal ;padding:10px">
    <h2 style="color:white;text-align:center;">Face Recognition WebApp</h2>
    </div>
    </body>
    """

    st.markdown(html_temp, unsafe_allow_html=True)

    image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    # If the image is uploaded
    if image_file is not None:
        our_image = Image.open(image_file)
        st.text("Original Image")
        # Display image on the WebPage
        st.image(our_image)

    # if the user clicks the recognise button
    if st.button("Recognise"):
        result_img, gray_img = detect_faces(our_image)
        st.image(result_img)
        st.image(gray_img)


if __name__ == '__main__':
    main()
