from PyQt6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QGridLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize

correct = 11
incorrect = 2


class summaryWidget(QWidget):
    def __init__(self, correct, incorrect):
        super().__init__()
        self.correctCount = correct
        self.incorrectCount = incorrect
        self.correctLabel = QLabel(f'\tCorrect: {self.correctCount}')
        self.correctLabel.setStyleSheet(
            'font-size: 80px; font-family: Comic Sans MS; color: green;')
        self.incorrectLabel = QLabel(f'\tIncorrect: {self.incorrectCount}')
        self.incorrectLabel.setStyleSheet(
            'font-size: 80px; font-family: Comic Sans MS; color: red;')
        self.pageLayout = QVBoxLayout(self)
        self.correctBox = QHBoxLayout(self)
        self.incorrectBox = QHBoxLayout(self)
        self.correctPic = QPixmap('correct.png')
        self.correctPic = self.correctPic.scaledToHeight(200)
        self.correctPicLabel = QLabel()
        self.correctPicLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.correctPicLabel.setPixmap(self.correctPic)
        self.incorrectPic = QPixmap('incorrect.png')
        self.incorrectPic = self.incorrectPic.scaledToHeight(200)
        self.incorrectPicLabel = QLabel()
        self.incorrectPicLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.incorrectPicLabel.setPixmap(self.incorrectPic)
        self.correctBox.addWidget(self.correctPicLabel)
        self.correctBox.addWidget(self.correctLabel)
        self.correctBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.incorrectBox.addWidget(self.incorrectPicLabel)
        self.incorrectBox.addWidget(self.incorrectLabel)
        self.incorrectBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pageLayout.addLayout(self.correctBox)
        self.pageLayout.addLayout(self.incorrectBox)
        self.setLayout(self.pageLayout)


class MainWindow(QMainWindow):
    #create a widget summarizing correct and incorrect answers, use correct and incorrect pngs
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flashcard App")
        self.showMaximized()
        self.setStyleSheet('background-color: white;')
        # self.correctCount = correct
        # self.incorrectCount = incorrect
        # self.correctLabel = QLabel(f'\tCorrect: {self.correctCount}')
        # self.correctLabel.setStyleSheet(
        #     'font-size: 80px; font-family: Comic Sans MS; color: green;')
        # self.incorrectLabel = QLabel(f'\tIncorrect: {self.incorrectCount}')
        # self.incorrectLabel.setStyleSheet(
        #     'font-size: 80px; font-family: Comic Sans MS; color: red;')
        # self.pageLayout = QVBoxLayout(self)
        # self.correctBox = QHBoxLayout(self)
        # self.incorrectBox = QHBoxLayout(self)
        # self.correctPic = QPixmap('correct.png')
        # self.correctPic = self.correctPic.scaledToHeight(200)
        # self.correctPicLabel = QLabel()
        # self.correctPicLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.correctPicLabel.setPixmap(self.correctPic)
        # self.incorrectPic = QPixmap('incorrect.png')
        # self.incorrectPic = self.incorrectPic.scaledToHeight(200)
        # self.incorrectPicLabel = QLabel()
        # self.incorrectPicLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.incorrectPicLabel.setPixmap(self.incorrectPic)
        # self.correctBox.addWidget(self.correctPicLabel)
        # self.correctBox.addWidget(self.correctLabel)
        # self.correctBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.incorrectBox.addWidget(self.incorrectPicLabel)
        # self.incorrectBox.addWidget(self.incorrectLabel)
        # self.incorrectBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.pageLayout.addLayout(self.correctBox)
        # self.pageLayout.addLayout(self.incorrectBox)
        # self.widget = QWidget()
        # self.widget.setLayout(self.pageLayout)
        self.setCentralWidget(summaryWidget(correct, incorrect))


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
