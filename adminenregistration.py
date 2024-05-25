import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLineEdit
import cv2
import os
import time
from PyQt5.QtCore import QFile, QTextStream, Qt

class CaptureWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Capture Face")
        self.resize(600, 300)  # Initial size
        self.setMinimumSize(300, 150)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Enter your name")
        self.layout.addWidget(self.name_input)
        self.capture_button = QPushButton("Capture Face", self)
        self.capture_button.clicked.connect(self.capture_face_with_name)
        self.layout.addWidget(self.capture_button)
        self.stop_button = QPushButton("Stop Capturing", self)
        self.stop_button.setObjectName("stopButton")  # Ajout de l'identifiant
        self.stop_button.clicked.connect(self.stop_capture)
        self.layout.addWidget(self.stop_button)
        self.stop_button.setEnabled(False)
        self.is_capturing = False
        self.apply_stylesheet("stylesheet.css")

    def apply_stylesheet(self, filename):
        style_sheet = QFile(filename)
        if not style_sheet.open(QFile.ReadOnly | QFile.Text):
            return

        stream = QTextStream(style_sheet)
        self.setStyleSheet(stream.readAll())

    def capture_face_with_name(self):
        name = self.name_input.text().strip()
        if not name:
            print("Please enter a name.")
            return

        output_directory = "captures_faces"
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        name_directory = os.path.join(output_directory, name)
        if not os.path.exists(name_directory):
            os.makedirs(name_directory)

        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        if not cap.isOpened():
            print("Error: Cannot open webcam.")
            return

        self.capture_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.is_capturing = True

        while self.is_capturing:
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read frame.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                roi_color = frame[y:y + h, x:x + w]
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                cv2.imwrite(f"{name_directory}/{name}_{timestamp}.png", roi_color)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw rectangle around face

            cv2.imshow('Webcam with Face Capture', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def stop_capture(self):
        self.is_capturing = False
        self.capture_button.setEnabled(True)
        self.stop_button.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    window = CaptureWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
