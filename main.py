from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import numpy as np
import os
import vlc
from tts.tts_functions import speakTextSSML, speakText
import time


class gamePage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.player = vlc.MediaPlayer()
        self.correctCount = 0
        self.incorrectCount = 0
        self.pageLayout = QGridLayout()
        self.setFixedSize(QSize(800, 480))
        self.pictures = [
            x.split('.')[0] for x in os.listdir('animal_bgs')
            if (x.endswith('.png'))
        ]
        self.randomSix = np.random.permutation(len(self.pictures))[:6]
        self.index = 0
        # set the background image of the main window to  self.pictures[self.randomSix[self.index]].png
        self.parent().setStyleSheet(
            "QMainWindow {border-image: url(animal_bgs/" +
            self.pictures[self.randomSix[self.index]] +
            ".png) 0 0 0 0 stretch stretch;}")

        # generate two random choices not including the correct one
        randomChoices = np.random.permutation(len(self.pictures))[:2]
        # make sure the correct choice is not one of the random choices
        while self.randomSix[self.index] in randomChoices:
            randomChoices = np.random.permutation(len(self.pictures))[:2]
        # add the correct choice to the random choices
        randomChoices = np.append(randomChoices, self.randomSix[self.index])
        # shuffle the choices
        randomChoices = np.random.permutation(randomChoices)

        self.correctButtonStyle = (
            "QToolButton"
            "{"
            "border-radius: 15; border: none; background-color: rgba(255, 255, 255, 0.75); color: black; font-size: 60px; font-family: Opun;"
            "}"
            "QToolButton::pressed"
            "{"
            "border-radius: 15; border: none; background-color: green;"
            "}")

        self.inCorrectButtonStyle = (
            "QToolButton"
            "{"
            "border-radius: 15; border: none; background-color: rgba(255, 255, 255, 0.75); color: black; font-size: 60px; font-family: Opun;"
            "}"
            "QToolButton::pressed"
            "{"
            "border-radius: 15; border: none; background-color: red;"
            "}")

        self.buttons = [QToolButton() for i in range(3)]
        self.buttonLabel = ('A', 'B', 'C')
        for i in range(3):
            picTemp = QPixmap('animal_pics/' +
                              self.pictures[randomChoices[i]] + '.png')
            picTemp = picTemp.scaledToHeight(145)
            self.buttons[i].setIcon(QIcon(picTemp))
            self.buttons[i].setIconSize(picTemp.size())
            self.buttons[i].setText(self.buttonLabel[i])
            self.buttons[i].setToolButtonStyle(
                Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
            self.buttons[i].setFixedSize(QSize(175, 250))
            if randomChoices[i] == self.randomSix[self.index]:
                self.buttons[i].setStyleSheet(self.correctButtonStyle)
                self.buttons[i].clicked.connect(self.correct)
            else:
                self.buttons[i].setStyleSheet(self.inCorrectButtonStyle)
                self.buttons[i].clicked.connect(self.incorrect)
            self.buttons[i].setShortcut(str(i + 1))
            self.pageLayout.addWidget(self.buttons[i], 1, i,
                                      Qt.AlignmentFlag.AlignBottom)

        self.playSoundShortcut = QShortcut(QKeySequence('4'), self)
        self.playSoundShortcut.activated.connect(self.playAnimalSound)

        self.restartGameShortcut = QShortcut(QKeySequence('5'), self)
        self.restartGameShortcut.activated.connect(self.restartGame)

        self.setLayout(self.pageLayout)

    def correct(self):
        print('correct')
        self.correctCount += 1
        self.nextCard()

    def incorrect(self):
        print('incorrect')
        self.incorrectCount += 1
        self.nextCard()

    def nextCard(self):
        self.index += 1
        if self.index < 6:
            # self.currentWordLabel.setText(
            #     self.pictures[self.randomSix[self.index]][0])
            self.parent().setStyleSheet(
                "QMainWindow {border-image: url(animal_bgs/" +
                self.pictures[self.randomSix[self.index]] +
                ".png) 0 0 0 0 stretch stretch;}")
            # generate two random choices not including the correct one
            randomChoices = np.random.permutation(len(self.pictures))[:2]
            # make sure the correct choice is not one of the random choices
            while self.randomSix[self.index] in randomChoices:
                randomChoices = np.random.permutation(len(self.pictures))[:2]
            # add the correct choice to the random choices
            randomChoices = np.append(randomChoices,
                                      self.randomSix[self.index])
            # shuffle the choices
            randomChoices = np.random.permutation(randomChoices)

            for i in range(3):
                self.buttons[i].disconnect()
                picTemp = QPixmap('animal_pics/' +
                                  self.pictures[randomChoices[i]] + '.png')
                picTemp = picTemp.scaledToHeight(145)
                self.buttons[i].setIcon(QIcon(picTemp))
                self.buttons[i].setIconSize(picTemp.size())
                self.buttons[i].setText(self.buttonLabel[i])
                self.buttons[i].setToolButtonStyle(
                    Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
                if randomChoices[i] == self.randomSix[self.index]:
                    self.buttons[i].setStyleSheet(self.correctButtonStyle)
                    self.buttons[i].clicked.connect(self.correct)
                else:
                    self.buttons[i].setStyleSheet(self.inCorrectButtonStyle)
                    self.buttons[i].clicked.connect(self.incorrect)
                self.buttons[i].setShortcut(str(i + 1))
            # self.playAnimalSound()
        else:
            self.parent().setCentralWidget(
                summaryWidget1(self.correctCount,
                               self.incorrectCount,
                               self.parent(),
                               randomSix=self.randomSix))

            # self.parent().setCentralWidget(
            #     advancedGamePage(self.parent(), self.randomSix))

    def playAnimalSound(self):
        print('playing sound')
        speakTextSSML(self.pictures[self.randomSix[self.index]])
        self.player.stop()
        self.player.set_mrl('animal_sounds/' +
                            self.pictures[self.randomSix[self.index]] + '.mp3')
        self.player.play()

    def readAnimalName(self):
        speakTextSSML(self.pictures[self.randomSix[self.index]])

    def restartGame(self):
        # self.parent().setCentralWidget(gamePage(self.parent()))
        self.parent().setStyleSheet(
            "QMainWindow {border-image: url(black.jpeg) 0 0 0 0 stretch stretch;}"
        )
        self.parent().setCentralWidget(blackPage(self.parent()))


class summaryWidget1(QWidget):
    def __init__(self, correct, incorrect, parent=None, randomSix=None):
        super().__init__(parent=parent)
        self.parent().setStyleSheet('QMainWindow {background-color: white;}')
        self.setFixedSize(QSize(800, 480))
        self.randomSix = randomSix
        self.correctCount = correct
        self.incorrectCount = incorrect
        self.correctLabel = QLabel(f'\tCorrect: {self.correctCount}')
        self.correctLabel.setStyleSheet(
            'font-size: 35px; font-family: Opun; color: green;')
        self.incorrectLabel = QLabel(f'\tIncorrect: {self.incorrectCount}')
        self.incorrectLabel.setStyleSheet(
            'font-size: 35px; font-family: Opun; color: red;')
        self.pageLayout = QVBoxLayout(self)
        self.textLabel = QLabel('Press Any Button to Play Advanced Mode')
        self.textLabel.setStyleSheet(
            'font-size: 35px; font-family: Opun; color: black;')
        self.textLabel.setAlignment(Qt.AlignmentFlag.AlignCenter
                                    | Qt.AlignmentFlag.AlignTop)
        self.pageLayout.addWidget(self.textLabel)
        self.correctBox = QHBoxLayout(self)
        self.incorrectBox = QHBoxLayout(self)
        self.correctPic = QPixmap('correct.png')
        self.correctPic = self.correctPic.scaledToHeight(100)
        self.correctPicLabel = QLabel()
        self.correctPicLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.correctPicLabel.setPixmap(self.correctPic)
        self.incorrectPic = QPixmap('incorrect.png')
        self.incorrectPic = self.incorrectPic.scaledToHeight(100)
        self.incorrectPicLabel = QLabel()
        self.incorrectPicLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.incorrectPicLabel.setPixmap(self.incorrectPic)
        self.correctBox.addWidget(self.correctPicLabel)
        self.correctBox.addWidget(self.correctLabel)
        self.correctBox.setAlignment(Qt.AlignmentFlag.AlignCenter
                                     | Qt.AlignmentFlag.AlignTop)
        self.incorrectBox.addWidget(self.incorrectPicLabel)
        self.incorrectBox.addWidget(self.incorrectLabel)
        self.incorrectBox.setAlignment(Qt.AlignmentFlag.AlignCenter
                                       | Qt.AlignmentFlag.AlignTop)
        self.pageLayout.addLayout(self.correctBox)
        self.pageLayout.addLayout(self.incorrectBox)

        self.restartGameShortcut = []
        for i in range(1, 5):
            self.restartGameShortcut.append(
                QShortcut(QKeySequence(str(i)), self))
            self.restartGameShortcut[i - 1].activated.connect(
                self.continueGame)

        self.setLayout(self.pageLayout)

    def continueGame(self):
        self.parent().setCentralWidget(
            advancedGamePage(self.parent(), self.randomSix))


class summaryWidget2(QWidget):
    def __init__(self, correct, incorrect, parent=None):
        super().__init__(parent=parent)
        self.parent().setStyleSheet('QMainWindow {background-color: white;}')
        self.setFixedSize(QSize(800, 480))
        self.correctCount = correct
        self.incorrectCount = incorrect
        self.correctLabel = QLabel(f'\tCorrect: {self.correctCount}')
        self.correctLabel.setStyleSheet(
            'font-size: 35px; font-family: Opun; color: green;')
        self.incorrectLabel = QLabel(f'\tIncorrect: {self.incorrectCount}')
        self.incorrectLabel.setStyleSheet(
            'font-size: 35px; font-family: Opun; color: red;')
        self.pageLayout = QVBoxLayout(self)

        self.textLabel = QLabel('Press Any Button to Restart')
        self.textLabel.setStyleSheet(
            'font-size: 35px; font-family: Opun; color: black;')
        self.textLabel.setAlignment(Qt.AlignmentFlag.AlignCenter
                                    | Qt.AlignmentFlag.AlignTop)
        self.pageLayout.addWidget(self.textLabel)

        self.correctBox = QHBoxLayout(self)
        self.incorrectBox = QHBoxLayout(self)
        self.correctPic = QPixmap('correct.png')
        self.correctPic = self.correctPic.scaledToHeight(100)
        self.correctPicLabel = QLabel()
        self.correctPicLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.correctPicLabel.setPixmap(self.correctPic)
        self.incorrectPic = QPixmap('incorrect.png')
        self.incorrectPic = self.incorrectPic.scaledToHeight(100)
        self.incorrectPicLabel = QLabel()
        self.incorrectPicLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.incorrectPicLabel.setPixmap(self.incorrectPic)
        self.correctBox.addWidget(self.correctPicLabel)
        self.correctBox.addWidget(self.correctLabel)
        self.correctBox.setAlignment(Qt.AlignmentFlag.AlignCenter
                                     | Qt.AlignmentFlag.AlignTop)
        self.incorrectBox.addWidget(self.incorrectPicLabel)
        self.incorrectBox.addWidget(self.incorrectLabel)
        self.incorrectBox.setAlignment(Qt.AlignmentFlag.AlignCenter
                                       | Qt.AlignmentFlag.AlignTop)
        self.pageLayout.addLayout(self.correctBox)
        self.pageLayout.addLayout(self.incorrectBox)

        self.restartGameShortcut = []
        for i in range(1, 5):
            self.restartGameShortcut.append(
                QShortcut(QKeySequence(str(i)), self))
            self.restartGameShortcut[i - 1].activated.connect(
                self.continueGame)

        self.setLayout(self.pageLayout)

    def continueGame(self):
        self.parent().setCentralWidget(gamePage(self.parent()))


class advancedGamePage(QWidget):
    def __init__(self, parent=None, cardSet=None):
        super().__init__(parent=parent)
        self.player = vlc.MediaPlayer()
        self.setFixedSize(QSize(800, 480))
        self.correctCount = 0
        self.incorrectCount = 0
        self.pageLayout = QGridLayout()
        self.pictures = [
            x.split('.')[0] for x in os.listdir('animal_bgs2')
            if (x.endswith('.png'))
        ]
        if cardSet is None:
            self.randomSix = np.random.permutation(len(self.pictures))[:6]
        else:
            self.randomSix = cardSet
        self.index = 0
        # set the background image of the main window to  self.pictures[self.randomSix[self.index]].png
        self.parent().setStyleSheet(
            "QMainWindow {border-image: url(animal_bgs2/" +
            self.pictures[self.randomSix[self.index]] +
            ".png) 0 0 0 0 stretch stretch;}")

        # generate two random choices not including the correct one
        randomChoices = np.random.permutation(len(self.pictures))[:2]
        # make sure the correct choice is not one of the random choices
        while self.randomSix[self.index] in randomChoices:
            randomChoices = np.random.permutation(len(self.pictures))[:2]
        # add the correct choice to the random choices
        randomChoices = np.append(randomChoices, self.randomSix[self.index])
        # shuffle the choices
        randomChoices = np.random.permutation(randomChoices)

        self.correctButtonStyle = (
            "QPushButton"
            "{"
            "border-radius: 15; border: none; background-color: rgba(255, 255, 255, 0.75); color: black; font-size: 35px; font-family: Opun;"
            "}"
            "QPushButton::pressed"
            "{"
            "border-radius: 15; border: none; background-color: green;"
            "}")

        self.inCorrectButtonStyle = (
            "QPushButton"
            "{"
            "border-radius: 15; border: none; background-color: rgba(255, 255, 255, 0.75); color: black; font-size: 35px; font-family: Opun;"
            "}"
            "QPushButton::pressed"
            "{"
            "border-radius: 15; border: none; background-color: red;"
            "}")

        self.buttons = [QPushButton() for i in range(3)]
        for i in range(3):
            self.buttons[i].setText(
                self.pictures[randomChoices[i]].title().upper())

            self.buttons[i].setFixedSize(QSize(250, 100))
            if randomChoices[i] == self.randomSix[self.index]:
                self.buttons[i].setStyleSheet(self.correctButtonStyle)
                self.buttons[i].clicked.connect(self.correct)
            else:
                self.buttons[i].setStyleSheet(self.inCorrectButtonStyle)
                self.buttons[i].clicked.connect(self.incorrect)
            self.buttons[i].setShortcut(str(i + 1))
            self.pageLayout.addWidget(self.buttons[i], 1, i,
                                      Qt.AlignmentFlag.AlignBottom)
        self.playSoundShortcut = QShortcut(QKeySequence('4'), self)
        self.playSoundShortcut.activated.connect(self.playAnimalSound)

        self.restartGameShortcut = QShortcut(QKeySequence('5'), self)
        self.restartGameShortcut.activated.connect(self.restartGame)

        self.setLayout(self.pageLayout)

    def correct(self):
        print('correct')
        self.correctCount += 1
        self.nextCard()

    def incorrect(self):
        print('incorrect')
        self.incorrectCount += 1
        self.nextCard()

    def nextCard(self):
        self.index += 1
        if self.index < 6:
            # self.currentWordLabel.setText(
            #     self.pictures[self.randomSix[self.index]][0])
            self.parent().setStyleSheet(
                "QMainWindow {border-image: url(animal_bgs2/" +
                self.pictures[self.randomSix[self.index]] +
                ".png) 0 0 0 0 stretch stretch;}")
            # generate two random choices not including the correct one
            randomChoices = np.random.permutation(len(self.pictures))[:2]
            # make sure the correct choice is not one of the random choices
            while self.randomSix[self.index] in randomChoices:
                randomChoices = np.random.permutation(len(self.pictures))[:2]
            # add the correct choice to the random choices
            randomChoices = np.append(randomChoices,
                                      self.randomSix[self.index])
            # shuffle the choices
            randomChoices = np.random.permutation(randomChoices)

            for i in range(3):
                self.buttons[i].disconnect()
                self.buttons[i].setText(
                    self.pictures[randomChoices[i]].title().upper())
                if randomChoices[i] == self.randomSix[self.index]:
                    self.buttons[i].setStyleSheet(self.correctButtonStyle)
                    self.buttons[i].clicked.connect(self.correct)
                else:
                    self.buttons[i].setStyleSheet(self.inCorrectButtonStyle)
                    self.buttons[i].clicked.connect(self.incorrect)
                self.buttons[i].setShortcut(str(i + 1))

        else:
            self.parent().setCentralWidget(
                summaryWidget2(self.correctCount, self.incorrectCount,
                               self.parent()))

    def playAnimalSound(self):
        print('playing sound')
        # speakTextSSML(self.pictures[self.randomSix[self.index]])
        self.player.stop()
        self.player.set_mrl('animal_sounds/' +
                            self.pictures[self.randomSix[self.index]] + '.mp3')
        self.player.play()

    def restartGame(self):
        # self.parent().setCentralWidget(gamePage(self.parent()))
        self.parent().setStyleSheet(
            "QMainWindow {border-image: url(black.jpeg) 0 0 0 0 stretch stretch;}"
        )
        self.parent().setCentralWidget(blackPage(self.parent()))


class blackPage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.restartGameShortcut = QShortcut(QKeySequence('6'), self)
        self.restartGameShortcut.activated.connect(self.restartGame)
        self.setFixedSize(QSize(800, 480))

    def restartGame(self):
        self.parent.setCentralWidget(gamePage(self.parent))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spy K🔍ds")
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet('QMainWindow {background-color: white;}')
        # self.setFixedSize(QSize(800, 480))
        self.setBaseSize(QSize(800, 480))
        self.showMaximized()


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('spykid.png'))
    window = MainWindow()
    window.setStyleSheet(
        "QMainWindow {border-image: url(black.jpeg) 0 0 0 0 stretch stretch;}")
    window.setCentralWidget(blackPage(window))

    screen_count = app.screens()
    if len(screen_count) > 1:
        second_screen = screen_count[1]
        geometry = second_screen.geometry()
        window = MainWindow()
        window.move(geometry.x(), geometry.y())

    window.show()
    window.showFullScreen()

    # window.setCentralWidget(gamePage(window))
    # window.setCentralWidget(advancedGamePage(window))
    # window.setCentralWidget(summaryWidget2(6, 0, window))
    app.exec()