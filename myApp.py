import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QGridLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
from tts.tts_functions import speakTextSSML, speakText
import time
import json

flashcard_set = ['food_pics']


def getCategoryData(set):
    # store the json file of the category in a variable then return
    with open(f'{flashcard_set[set]}.json') as f:
        data = json.load(f)
    return list(data.items())


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Flashcard App")
        self.showMaximized()
        self.setStyleSheet('background-color: white;')
        self.setCentralWidget(cardsWidget())


class cardsWidget(QWidget):
    def __init__(self, set=0):
        super().__init__()
        self.data = self.getCategoryData(set)
        self.numCards = len(self.data)
        self.randomOrder = np.random.permutation(self.numCards)
        # print(self.randomOrder)
        self.index = 0
        self.picPath = self.data[self.randomOrder[self.index]][0]
        self.correctCount = 0
        self.incorrectCount = 0

        page_layout = QGridLayout()
        button_layout = QHBoxLayout()
        self.pic = QPixmap(self.picPath)
        self.pic = self.pic.scaledToHeight(800)
        self.pic_label = QLabel()
        self.pic_label.setPixmap(self.pic)
        # self.pic_label.setFixedSize(QSize(600, 800))
        # self.pic_label.setScaledContents(True)

        self.choices = self.data[self.randomOrder[self.index]][1]
        self.choice_buttons = [
            QPushButton(text=self.choices['choices'][i]) for i in range(3)
        ]

        self.correctButtonStyle = (
            "QPushButton"
            "{"
            "border-radius: 15; border: 1px solid black; color: black; font-size: 60px; font-family: Comic Sans MS; background-color: white"
            "}"
            "QPushButton::pressed"
            "{"
            "border-radius: 15; border: 1px solid black; color: white; font-size: 60px; font-family: Comic Sans MS; background-color: green"
            "}")

        self.inCorrectButtonStyle = (
            "QPushButton"
            "{"
            "border-radius: 15; border: 1px solid black; color: black; font-size: 60px; font-family: Comic Sans MS; background-color: white"
            "}"
            "QPushButton::pressed"
            "{"
            "border-radius: 15; border: 1px solid black; color: white; font-size: 60px; font-family: Comic Sans MS; background-color: red"
            "}")

        for i in range(3):
            self.choice_buttons[i].setShortcut(f'{i+1}')
            if self.choices['correct'] == i:
                self.choice_buttons[i].clicked.connect(self.correctChoice)
                self.choice_buttons[i].setStyleSheet(self.correctButtonStyle)
            else:
                self.choice_buttons[i].clicked.connect(self.incorrectChoice)
                self.choice_buttons[i].setStyleSheet(self.inCorrectButtonStyle)
            button_layout.addWidget(self.choice_buttons[i])

        page_layout.addWidget(self.pic_label, 0, 0,
                              Qt.AlignmentFlag.AlignCenter)
        page_layout.addLayout(button_layout, 1, 0)
        # page_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        page_layout.setRowStretch(1, 3)
        self.setLayout(page_layout)

    def nextCard(self):
        self.index += 1
        if self.index < self.numCards:
            self.picPath = self.data[self.randomOrder[self.index]][0]
            self.pic = QPixmap(self.picPath)
            self.pic = self.pic.scaledToHeight(800)
            self.pic_label.setPixmap(self.pic)
            self.choices = self.data[self.randomOrder[self.index]][1]
            i = 0
            self.choiceOrder = np.random.permutation(3)
            for n in self.choiceOrder:
                self.choice_buttons[i].disconnect()
                self.choice_buttons[i].setText(self.choices['choices'][n])
                self.choice_buttons[i].setShortcut(f'{i+1}')
                if self.choices['correct'] == n:
                    self.choice_buttons[i].clicked.connect(self.correctChoice)
                    self.choice_buttons[i].setStyleSheet(
                        self.correctButtonStyle)
                else:
                    self.choice_buttons[i].clicked.connect(
                        self.incorrectChoice)
                    self.choice_buttons[i].setStyleSheet(
                        self.inCorrectButtonStyle)
                i += 1

        else:
            # change into summary page
            self.setCentralWidget(
                summaryWidget(self.correctCount, self.incorrectCount))
            # unbind all the buttons
            for i in range(3):
                self.choice_buttons[i].disconnect()
                self.choice_buttons[i].clicked.connect(lambda: None)

    def correctChoice(self):
        speakTextSSML('Correct! The answer is' + self.sender().text() + '!')
        print("Correct")
        # time.sleep(.3)
        self.correctCount += 1
        self.nextCard()

    def incorrectChoice(self):
        speakTextSSML('Wrong! The correct answer is ' +
                      self.choices['choices'][self.choices['correct']] + '!')
        print("Incorrect")
        # time.sleep(.3)
        self.incorrectCount += 1
        self.nextCard()

    def getCategoryData(self, set):
        # store the json file of the category in a variable then return
        with open(f'{flashcard_set[set]}.json') as f:
            data = json.load(f)
        return list(data.items())


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
