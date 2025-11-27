
import requests
from PySide6 import QtWidgets,QtCore
from PySide6.QtGui import QPixmap , QFont
import sys
import API_KEYS
import json

class mywidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
        QWidget {
            background-color: #121212;
            color: white;
            font-family: Arial;
        }

        QPushButton {
            background-color: #2a2a2a;
            border: 1px solid #444;
            padding: 6px;
            border-radius: 5px;
        }

        QPushButton:hover {
            background-color: #3a3a3a;
        }
    """)
        #basic widgets 
        self.image_pos = 0
        self.download_counter = 0
        self.download_url = ""
        #LINEEDIT
        self.inputquery = QtWidgets.QLineEdit()
        self.button = QtWidgets.QPushButton("Find Image!")
        self.nextButton = QtWidgets.QPushButton("Next")
        self.prevButton = QtWidgets.QPushButton("Previous")
        self.downloadButton = QtWidgets.QPushButton("Download")
        self.image = QtWidgets.QLabel("No image loaded!")
        self.image.setMaximumWidth(300)
        self.image.setMaximumHeight(150)
        #BUTTON
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.inputquery)
        layout.addWidget(self.button)
        hlay = QtWidgets.QHBoxLayout(self)
        hlay.addWidget(self.nextButton)
        hlay.addWidget(self.prevButton)
        layout.addLayout(hlay)
        layout.addWidget(self.image)
        layout.addWidget(self.downloadButton)
        #LAYOUT

        #EVENT HANDLING
        self.button.clicked.connect(self.fetchImage)
        self.nextButton.clicked.connect(self.NextImage)
        self.prevButton.clicked.connect(self.PrevImage)
        self.downloadButton.clicked.connect(self.download_image)

    def NextImage(self):
        self.image_pos += 1
        self.fetchImage()

    def PrevImage(self):
        self.image_pos -= 1
        self.fetchImage()
    
    def fetchImage(self):
        image_pos = 0
        
        query = self.inputquery.text().strip()
        
        url = f"https://api.pexels.com/v1/search?query={query}"
        
        
        headers = {
            "Authorization":API_KEYS.api_key,
        }
        
        response = requests.get(url,headers=headers)
        
        Image = QPixmap() #creating a image from the raw image bytes

        data = json.loads(response.text)
        getImageURL = data["photos"][self.image_pos]["src"]["small"]
        self.download_url = data["photos"][self.image_pos]["src"]["large"]
        getImageresponse = requests.get(getImageURL)
        Image.loadFromData(getImageresponse.content)
        self.image.setPixmap(Image)
    
    def download_image(self):

        response = requests.get(self.download_url)
        filename = f"image_{self.download_counter}.png"
        with open(filename,"wb") as f:
            f.write(response.content)
        print(f"{filename} is saved!")
        self.download_counter += 1

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = mywidget()
    window.setWindowTitle("Free Images Finder")
    window.setWindowIcon(QPixmap('icon.png'))
    window.setFont(QFont('pixelify sans',16))
    
    window.show()

    sys.exit(app.exec())

    # "https://api.pexels.com/v1/search?query=people"
