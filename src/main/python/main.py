"""Run main functions."""
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import (QApplication, QGroupBox, QLineEdit, QLabel,
                             QGridLayout, QPushButton, QMessageBox, QDialog,
                             QListWidget, QAbstractItemView, QProgressBar)
import sys
import text
import utils
import datetime
import os


class Gui(QDialog):
    """Perform Gui Functions."""

    def __init__(self, parent=None):
        """Perform the Main function."""
        super(Gui, self).__init__(parent)

        self.Env = utils.getEnv(envPath)
        mainLayout = QGridLayout()
        self.createTopLeftGroup()
        self.createBottomLeftGroup()
        self.createRightGroup()
        self.createMainProgressBarGroup()

        mainLayout.addWidget(self.TopLeftGroup, 0, 0)
        mainLayout.addWidget(self.BottomLeftGroup, 1, 0)
        mainLayout.addWidget(self.RightGroup, 0, 1, 2, 1)
        mainLayout.addWidget(self.MainProgressBar, 2, 0, 1, 2)
        self.setLayout(mainLayout)

    def createTopLeftGroup(self):
        """Create top left group containing text boxes and start button."""
        self.TopLeftGroup = QGroupBox()
        self.MonthField = QLineEdit()
        self.MonthField.setPlaceholderText('Month')
        self.MonthField.setMaxLength(2)

        self.DateField = QLineEdit()
        self.DateField.setPlaceholderText('Day')
        self.DateField.setMaxLength(2)

        self.YearField = QLineEdit()
        self.YearField.setPlaceholderText('Year')
        self.YearField.setMaxLength(4)

        self.StartButton = QPushButton('Start')

        layout = QGridLayout()
        layout.addWidget(self.MonthField, 0, 0, 1, 1)
        layout.addWidget(self.DateField, 0, 1, 1, 1)
        layout.addWidget(self.YearField, 0, 2, 1, 1)
        layout.addWidget(self.StartButton, 1, 0, 1, 3)
        self.TopLeftGroup.setLayout(layout)

        self.StartButton.clicked.connect(self.on_startButton_clicked)

    def on_startButton_clicked(self):
        """Take given day/month/year input and run main()."""
        # alert = QMessageBox()
        # alert.setText(self.MonthField.text() + ' ' + self.DateField.text() +
        #               ' ' + self.YearField.text())
        # alert.exec_()
        # reset output Fields
        self.reset()
        if(not os.path.isfile(self.Env['EXCEL'])):
            alert = QMessageBox()
            alert.setText("The spreadsheet can't be found.")
            alert.exec_()
            return
        # define date month and year local variables
        date = self.DateField.text()
        month = self.MonthField.text()
        year = self.YearField.text()
        # Make date month year integers
        if(date != ''):
            date = int(date)
        else:
            date = 0
        if(month != ''):
            month = int(month)
        else:
            month = 0
        if(year != ''):
            year = int(year)
        else:
            year = 0

        # Verify that date month and year are possible
        alertText = []
        if(date > 31 or date < 1):
            alertText.append('Date')
        if(month > 12 or month < 1):
            alertText.append('Month')
        if(year < 2010 or year > datetime.date.today().year + 2):
            alertText.append('Year')

        # format three date inputs as (M)M_(D)D_YYYY
        # if len(alertText) > 0:
        #     alert = QMessageBox()
        #     i = 0
        #     outputText = ''
        #     for string in alertText:
        #         if i == 0:
        #             outputText += string
        #             i = 1
        #         else:
        #             outputText += ' and ' + string
        #     alert.setText(outputText)
        #     alert.exec_()
        #     return
        if(len(alertText) > 0):
            alert = QMessageBox()
            if(len(alertText) == 1):
                alert.setText(alertText[0] + ' is invalid')

            if(len(alertText) == 2):
                alert.setText(alertText[0] + ' and ' + alertText[1] +
                              ' are invalid')
            if(len(alertText) == 3):
                alert.setText(alertText[0] + ', ' + alertText[1] +
                              ', and ' + alertText[2] + ' are invalid')
            alert.exec_()
            return
        mdy = str(month) + '_' + str(date) + '_' + str(year)

        # Start doing the work of main()
        files = text.findFiles(mdy, self.Env)
        if(files):
            (returnFiles, manualFiles) = files
            if(len(returnFiles) == 0):
                alert = QMessageBox()
                alert.setText('This day has already been run')
                alert.exec_()
                return
        else:
            alert = QMessageBox()
            alert.setText('Source is invalid')
            alert.exec_()
            return

        # returnFiles is a tuple (fileName, Num)
        # manualFiles is a tuple (fileName, Num)
        self.MainProgressBar.setRange(0, len(returnFiles))

        # Add manual files to ListWidget
        for fileArr in manualFiles:
            self.ManualFiles.addItem(fileArr[0])

        # Move and mark excel rows for returnFiles
        for fileArr in returnFiles:
            repeat = text.renameFile(fileArr, mdy, self.Env, 0)
            # if repeat is true, then files already exist at output
            if(repeat):
                alert = QMessageBox()
                alert.setText('Query has already been run')
                alert.exec_()
                break
            text.markExcelRow(fileArr[1], self.Env)
            self.advanceMainProgressBar()

    def createBottomLeftGroup(self):
        """Create bottom left group containing src and dest paths."""
        self.BottomLeftGroup = QGroupBox('Settings')

        srcLabel = QLabel('Source Folder')

        self.SrcField = QLineEdit()
        self.SrcField.setText(self.Env['SOURCE'])

        destLabel = QLabel('Destination Folder')

        self.DestField = QLineEdit()
        self.DestField.setText(self.Env['DEST'])

        excelLabel = QLabel('Excel File')
        self.excelField = QLineEdit()
        self.excelField.setText(self.Env['EXCEL'])

        self.saveEnvButton = QPushButton('Update Settings')

        self.saveEnvProgressBar = QProgressBar()

        layout = QGridLayout()
        layout.addWidget(srcLabel, 0, 0, 1, 2)
        layout.addWidget(self.SrcField, 1, 0, 1, 2)
        layout.addWidget(destLabel, 3, 0, 1, 2)
        layout.addWidget(self.DestField, 4, 0, 1, 2)
        layout.addWidget(excelLabel, 5, 0, 1, 2)
        layout.addWidget(self.excelField, 6, 0, 1, 2)
        layout.addWidget(self.saveEnvButton, 7, 0, 1, 1)
        layout.addWidget(self.saveEnvProgressBar, 7, 1, 1, 1)

        self.BottomLeftGroup.setLayout(layout)

        self.saveEnvButton.clicked.connect(self.on_saveEnv_clicked)
        self.SrcField.textChanged.connect(self.on_envText_changed)
        self.DestField.textChanged.connect(self.on_envText_changed)
        self.excelField.textChanged.connect(self.on_envText_changed)

    def on_saveEnv_clicked(self):
        """Update the env file based off of the new text."""
        self.saveEnvProgressBar.setValue(0)
        self.saveEnvProgressBar.setRange(0, 1)
        newEnv = {
            'SOURCE': self.SrcField.text(),
            'DEST': self.DestField.text(),
            'EXCEL': self.excelField.text()
        }
        self.Env = utils.updateEnv(newEnv, envPath)
        self.updateSettingsText()
        self.saveEnvProgressBar.setValue(1)

    def on_envText_changed(self):
        """Reset the env progress bar when text is changed."""
        self.saveEnvProgressBar.setValue(0)

    def createRightGroup(self):
        """Create the right group containing manaul files."""
        self.RightGroup = QGroupBox('Manual Files')

        self.ManualFiles = QListWidget()
        # Remove the edit cabability, need to see how this impacts copying
        self.ManualFiles.setEditTriggers(QAbstractItemView.NoEditTriggers)
        layout = QGridLayout()
        layout.addWidget(self.ManualFiles, 0, 0, 1, 1)
        self.RightGroup.setLayout(layout)

    def createMainProgressBarGroup(self):
        """Create a progress bar to update progress after pressing start."""
        self.MainProgressBarGroup = QGroupBox()
        self.MainProgressBar = QProgressBar()

        layout = QGridLayout()
        layout.addWidget(self.MainProgressBar)
        self.MainProgressBarGroup.setLayout(layout)

    def advanceMainProgressBar(self):
        """Advances the Main progress bar."""
        curVal = self.MainProgressBar.value()
        # maxVal = self.MainProgressBar.maximum()
        self.MainProgressBar.setValue(curVal + 1)
        QApplication.processEvents()
        # print('advancing Progress Bar')

    def updateSettingsText(self):
        """Update the text in the Source and Dest Fields."""
        self.SrcField.setText(self.Env['SOURCE'])
        self.DestField.setText(self.Env['DEST'])

    def reset(self):
        """Reset the app so that it can be used again for a different date."""
        self.MainProgressBar.setValue(0)
        self.ManualFiles.clear()


if __name__ == '__main__':
    appctxt = ApplicationContext()
    envPath = appctxt.get_resource('.env')
    Gui = Gui()
    Gui.show()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
