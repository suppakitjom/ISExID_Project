import sys
from random import randint
import numpy as np
from PyQt6.QtWidgets import (QApplication, QLabel, QMainWindow, QPushButton,
                             QVBoxLayout, QHBoxLayout, QWidget, QGridLayout)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QSize
import time
import json

flashcard_set = ['food_pics']


def getCategoryData(set):
    # store the json file of the category in a variable then return
    with open(f'{flashcard_set[set]}.json') as f:
        data = json.load(f)
    return list(data.items())


class MainWindow(QMainWindow):
    def __init__(self, set=0):
        super().__init__()
        self.setWindowTitle("Flashcard App")
        self.showMaximized()
        self.setStyleSheet('background-color: white;')
        self.data = getCategoryData(set)
        self.numCards = len(self.data)
        self.randomOrder = np.random.permutation(self.numCards)
        print(self.randomOrder)
        self.index = 0
        self.picPath = self.data[self.randomOrder[self.index]][0]
        self.correctCount = 0
        self.incorrectCount = 0

        page_layout = QGridLayout()
        button_layout = QHBoxLayout()
        self.pic = QPixmap(self.picPath)
        self.pic_label = QLabel()
        self.pic_label.setPixmap(self.pic)
        self.pic_label.setFixedSize(QSize(600, 800))
        self.pic_label.setScaledContents(True)

        self.choices = self.data[self.randomOrder[self.index]][1]

        self.choice_buttons = [
            QPushButton(text=self.choices['choices'][i]) for i in range(3)
        ]

        self.correctButtonStyle = (
            "QPushButton"
            "{"
            "border: 1px solid black; color: black; font-size: 60px; font-family: Comic Sans MS; background-color: white"
            "}"
            "QPushButton::pressed"
            "{"
            "border: 1px solid black; color: white; font-size: 60px; font-family: Comic Sans MS; background-color: green"
            "}")

        self.inCorrectButtonStyle = (
            "QPushButton"
            "{"
            "border: 1px solid black; color: black; font-size: 60px; font-family: Comic Sans MS; background-color: white"
            "}"
            "QPushButton::pressed"
            "{"
            "border: 1px solid black; color: white; font-size: 60px; font-family: Comic Sans MS; background-color: red"
            "}")
        self.choiceOrder = [0, 1, 2]
        for i in range(3):
            if self.choices['correct'] == i:
                self.choice_buttons[i].clicked.connect(self.correctChoice)
                self.choice_buttons[i].setStyleSheet(self.correctButtonStyle)
            else:
                self.choice_buttons[i].clicked.connect(self.incorrectChoice)
                self.choice_buttons[i].setStyleSheet(self.inCorrectButtonStyle)

        #randomly add the button to the frame
        for n in np.random.permutation(3):
            button_layout.addWidget(self.choice_buttons[n])

        page_layout.addWidget(self.pic_label, 0, 0,
                              Qt.AlignmentFlag.AlignCenter)
        page_layout.addLayout(button_layout, 1, 0)
        # page_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        page_layout.setRowStretch(1, 3)
        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

    def nextCard(self):
        self.index += 1
        if self.index < self.numCards:
            self.picPath = self.data[self.randomOrder[self.index]][0]
            self.pic = QPixmap(self.picPath)
            self.pic_label.setPixmap(self.pic)
            self.choices = self.data[self.randomOrder[self.index]][1]
            i = 0
            self.choiceOrder = np.random.permutation(3)
            for n in self.choiceOrder:
                self.choice_buttons[i].disconnect()
                self.choice_buttons[i].setText(self.choices['choices'][n])
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
            self.pic_label.setText(
                f"Correct: {self.correctCount} Incorrect: {self.incorrectCount}"
            )
            self.pic_label.setScaledContents(False)
            self.pic_label.setFixedSize(QSize(1000, 800))
            self.pic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.pic_label.setStyleSheet(
                "border: 1px solid black; color: black; font-size: 60px; font-family: Comic Sans MS; background-color: white"
            )
            for i in range(3):
                self.choice_buttons[i].hide()

    def correctChoice(self):
        # change the button color to green
        correctStyle = "border: 1px solid black; color: black; font-size: 60px; font-family: Comic Sans MS; background-color: black"
        self.choice_buttons[self.choices['correct']].setStyleSheet(
            correctStyle)
        print("Correct")
        time.sleep(.3)
        self.correctCount += 1
        self.nextCard()

    def incorrectChoice(self):
        print("Incorrect")
        time.sleep(.3)
        self.incorrectCount += 1
        self.nextCard()

    def keyPressEvent(self, event):
        print(self.choiceOrder)
        if event.key() == Qt.Key.Key_1:
            self.centralWidget().layout().itemAt(1).layout().itemAt(
                0).widget().click()
        elif event.key() == Qt.Key.Key_2:
            self.centralWidget().layout().itemAt(1).layout().itemAt(
                1).widget().click()
        elif event.key() == Qt.Key.Key_3:
            self.centralWidget().layout().itemAt(1).layout().itemAt(
                2).widget().click()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
