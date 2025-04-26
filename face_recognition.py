from tkinter import *
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
import mysql.connector
from datetime import datetime
from time import strftime


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        self.root.configure(bg="blue")  # Set background color to blue

        # Title Label
        title_lbl = Label(self.root, text="FACE RECOGNITION", font=("times new roman", 35, "bold"), bg="blue", fg="white")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # Left Image (Static Display)
        img_top = Image.open(r"college_image/2.jpg")
        img_top = img_top.resize((650, 700), Image.Resampling.NEAREST)
        self.photoimg_top = ImageTk.PhotoImage(img_top)

        f_lbl = Label(self.root, image=self.photoimg_top)
        f_lbl.place(x=0, y=55, width=650, height=700)

        # Right Image (For Video Feed)
        self.video_frame = Label(self.root, bg="black")
        self.video_frame.place(x=650, y=55, width=950, height=700)

        # Face Recognition Button
        b1 = Button(self.root, text="FACE RECOGNITION", command=self.face_recog, cursor="hand2",
                    font=("times new roman", 18, "bold"), bg="red", fg="white")
        b1.place(x=1000, y=680, width=250, height=40)

    def mark_attendance(self, i, r, n, d):
        """Marks attendance in the CSV file."""
        with open("deepak.csv", "r+", newline="\n") as f:
            myDatalist = f.readlines()
            name_list = [line.split(",")[0] for line in myDatalist]

            if i not in name_list:
                now = datetime.now()
                d1 = now.strftime("%Y-%m-%d")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Present")

    def face_recog(self):
        """Handles face recognition and displays the live feed."""
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        classifier = cv2.face.LBPHFaceRecognizer_create()
        classifier.read("classifier.xml")

        video_cap = cv2.VideoCapture(0)
        self.update_video(video_cap, faceCascade, classifier)

    def update_video(self, cap, faceCascade, classifier):
        """Continuously updates the video feed inside the Tkinter frame."""
        ret, img = cap.read()
        if ret:
            img = cv2.resize(img, (950, 700))  # Resize to fit the Tkinter frame
            img, detected = self.recognize(img, classifier, faceCascade)

            # Convert frame for Tkinter display
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_frame.imgtk = imgtk
            self.video_frame.configure(image=imgtk)
            self.video_frame.after(10, lambda: self.update_video(cap, faceCascade, classifier))
        else:
            cap.release()
            cv2.destroyAllWindows()

    def recognize(self, img, classifier, faceCascade):
        """Detects faces and recognizes students."""
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray_image, 1.1, 10)
        detected = False

        for (x, y, w, h) in faces:
            detected = True
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            id, predict = classifier.predict(gray_image[y:y + h, x:x + w])
            confidence = int((100 * (1 - predict / 300)))

            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Deepak@7846",
                database="face_recognition",
                auth_plugin='mysql_native_password'
            )
            my_cursor = conn.cursor()

            my_cursor.execute("SELECT Student_id, Name, Roll, Dep FROM student WHERE Student_id=%s", (id,))
            student = my_cursor.fetchone()

            if student and confidence > 77:
                i, n, r, d = student
                cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(img, f"Name: {n}", (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(img, f"Roll: {r}", (x, y - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                cv2.putText(img, f"Dept: {d}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
                self.mark_attendance(i, r, n, d)
            else:
                cv2.putText(img, "Unknown", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        return img, detected


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()
