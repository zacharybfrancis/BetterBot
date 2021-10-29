from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

# Parent class to create pages that the user will access
class Page:

    # Initialization
    def __init__(self, driver, win):
        self.driver = driver
        self.win = win
        self.MAX_SIZE = 16777215 # Max size for any given widget
        self.font = QFont('Courier New', 10)

    # Returns the central widget for a given page
    def getWidget(self):
        self.centralWidget = QWidget(self.win)
        return self.centralWidget

    # Sets up UI for the page
    def setupUI(self):
        self.setupVerticalLayout()
        self.setupWidgets()

    # Sets up the vertical layout properties that are consistent with each page
    def setupVerticalLayout(self):
        self.verticalLayoutWidget = QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QRect(0, 0, 700, 800))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(10)

    def setupWidgets(self):
        for i in range(self.verticalLayout.count()):
            self.verticalLayout.itemAt(i).widget().setFont(self.font)

# Class to display the welcome page
class WelcomePage(Page):

    # Sets welcome page margins for vertical layout
    def setupVerticalLayout(self):
        super().setupVerticalLayout()
        self.verticalLayout.setContentsMargins(75, 300, 75, 300)

    # Sets up the widgets for the page
    def setupWidgets(self):

        # Set up title label
        self.titleLabel = QLabel(self.verticalLayoutWidget)
        self.titleLabel.setMaximumSize(QSize(self.MAX_SIZE, 20))
        self.titleLabel.setText("Welcome to Better Bot for Supreme!")
        self.verticalLayout.addWidget(self.titleLabel, 0, Qt.AlignHCenter)

        # Set up start button
        self.startButton = QPushButton(self.verticalLayoutWidget)
        self.startButton.setStyleSheet("background-color: red;"
            + "color: white;")
        self.startButton.setText("Get Started")
        self.startButton.clicked.connect(lambda:
            self.driver.setPage("info"))
        self.verticalLayout.addWidget(self.startButton, 0, Qt.AlignHCenter)

        super().setupWidgets()

# Class to display the info page
class InfoPage(Page):

    # Sets info page margins for vertical layout
    def setupVerticalLayout(self):
        super().setupVerticalLayout()
        self.verticalLayout.setContentsMargins(75, 150, 75, 150)

    # Sets up the widgets for the page
    def setupWidgets(self):

        # Set up title label
        self.titleLabel = QLabel(self.verticalLayoutWidget)
        self.titleLabel.setMaximumSize(QSize(self.MAX_SIZE, 375))
        self.titleLabel.setText("Before you start here's\na few things to note:"
            + "\n\n-All the information you provide here will be\n kept "
            + "private."
            + "\n\n-You are fully responsible for entering in the\n correct "
            + "information. We have some features\n to make sure that your "
            + "information is\n consistent. If the bot fails due to mistakes\n"
            + " with your input, we are NOT responsible."
            + "\n\n-This bot is semi-manual. This means that once\n the bot has"
            + " automated the cart-adding and\n checkout, YOU will have to fill"
            + " out the\n Recaptcha form in order to complete the\n purchase.")
        self.titleLabel.setAlignment(Qt.AlignLeft)
        self.verticalLayout.addWidget(self.titleLabel, 0, Qt.AlignHCenter)

        # Set up start button
        self.continueButton = QPushButton(self.verticalLayoutWidget)
        self.continueButton.setStyleSheet("background-color: red;"
            + "color: white;")
        self.continueButton.setText("Continue")
        self.continueButton.clicked.connect(lambda:
            self.driver.setPage("shipping"))
        self.verticalLayout.addWidget(self.continueButton, 0, Qt.AlignHCenter)

        super().setupWidgets()

# Class to display shipping information form
class ShippingInfoPage(Page):

    # Sets shipping info page margins for vertical layout
    def setupVerticalLayout(self):
        super().setupVerticalLayout()
        self.verticalLayout.setContentsMargins(105, 55, 105, 55)

    # Sets up the widgets for the page
    def setupWidgets(self):

        # Set up the title label
        self.titleLabel = QLabel(self.verticalLayoutWidget)
        self.titleLabel.setMaximumSize(QSize(self.MAX_SIZE, 20))
        self.titleLabel.setText("Fill out your shipping info:")
        self.verticalLayout.addWidget(self.titleLabel, 0, Qt.AlignHCenter)

        # Set up all the info entry lines
        self.nameLine = QLineEdit(self.verticalLayoutWidget)
        self.nameLine.setPlaceholderText("Name (First and Last)")
        self.verticalLayout.addWidget(self.nameLine)

        self.emailLine = QLineEdit(self.verticalLayoutWidget)
        self.emailLine.setPlaceholderText("Email")
        # From emailregex.com
        emailReg = QRegExp("[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
        self.emailLine.setValidator(QRegExpValidator(emailReg, self.emailLine))
        self.verticalLayout.addWidget(self.emailLine)

        self.phoneLine = QLineEdit(self.verticalLayoutWidget)
        self.phoneLine.setPlaceholderText("Phone")
        phoneReg = QRegExp("\d{10}")
        self.phoneLine.setValidator(QRegExpValidator(phoneReg, self.phoneLine))
        self.verticalLayout.addWidget(self.phoneLine)

        self.addressLine = QLineEdit(self.verticalLayoutWidget)
        self.addressLine.setPlaceholderText("Address")
        self.verticalLayout.addWidget(self.addressLine)

        self.aptLine = QLineEdit(self.verticalLayoutWidget)
        self.aptLine.setPlaceholderText("Apt, Unit, etc. (Optional)")
        self.verticalLayout.addWidget(self.aptLine)

        self.cityLine = QLineEdit(self.verticalLayoutWidget)
        self.cityLine.setPlaceholderText("City")
        self.verticalLayout.addWidget(self.cityLine)

        self.setupStateBox()

        self.zipLine = QLineEdit(self.verticalLayoutWidget)
        self.zipLine.setPlaceholderText("Zip Code")
        zipReg = QRegExp("\d{5}")
        self.zipLine.setValidator(QRegExpValidator(zipReg, self.zipLine))
        self.verticalLayout.addWidget(self.zipLine)

        self.countryBox = QComboBox(self.verticalLayoutWidget)
        self.countryBox.setPlaceholderText("Country")
        self.countryBox.addItem("USA")
        self.verticalLayout.addWidget(self.countryBox)

        # Set up the submit button
        self.submitButton = QPushButton(self.verticalLayoutWidget)
        self.submitButton.setStyleSheet("background-color: red;\n"
            + "color: white;")
        self.submitButton.clicked.connect(lambda: self.submit())
        self.submitButton.setText("Submit")
        self.verticalLayout.addWidget(self.submitButton, 0, Qt.AlignHCenter)

        # Set up error label
        self.errorLabel = QLabel(self.verticalLayoutWidget)
        self.errorLabel.setMaximumSize(QSize(self.MAX_SIZE, 70))
        self.errorLabel.setStyleSheet("color: red;")
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.errorLabel, 0, Qt.AlignHCenter)

        super().setupWidgets()

    # Helper that sets up the state dropdown menu
    def setupStateBox(self):
        self.stateBox = QComboBox(self.verticalLayoutWidget)
        self.stateBox.setPlaceholderText("State")
        self.stateBox.addItem("AL")
        self.stateBox.addItem("AK")
        self.stateBox.addItem("AS")
        self.stateBox.addItem("AZ")
        self.stateBox.addItem("AR")
        self.stateBox.addItem("CA")
        self.stateBox.addItem("CO")
        self.stateBox.addItem("CT")
        self.stateBox.addItem("DE")
        self.stateBox.addItem("DC")
        self.stateBox.addItem("FM")
        self.stateBox.addItem("FL")
        self.stateBox.addItem("GA")
        self.stateBox.addItem("GU")
        self.stateBox.addItem("HI")
        self.stateBox.addItem("ID")
        self.stateBox.addItem("IL")
        self.stateBox.addItem("IN")
        self.stateBox.addItem("IA")
        self.stateBox.addItem("KS")
        self.stateBox.addItem("KY")
        self.stateBox.addItem("LA")
        self.stateBox.addItem("ME")
        self.stateBox.addItem("MH")
        self.stateBox.addItem("MD")
        self.stateBox.addItem("MA")
        self.stateBox.addItem("MI")
        self.stateBox.addItem("MN")
        self.stateBox.addItem("MS")
        self.stateBox.addItem("MO")
        self.stateBox.addItem("MT")
        self.stateBox.addItem("NE")
        self.stateBox.addItem("NV")
        self.stateBox.addItem("NH")
        self.stateBox.addItem("NJ")
        self.stateBox.addItem("NM")
        self.stateBox.addItem("NY")
        self.stateBox.addItem("NC")
        self.stateBox.addItem("ND")
        self.stateBox.addItem("MP")
        self.stateBox.addItem("OH")
        self.stateBox.addItem("OK")
        self.stateBox.addItem("OR")
        self.stateBox.addItem("PA")
        self.stateBox.addItem("PR")
        self.stateBox.addItem("RI")
        self.stateBox.addItem("SC")
        self.stateBox.addItem("SD")
        self.stateBox.addItem("TN")
        self.stateBox.addItem("TX")
        self.stateBox.addItem("UT")
        self.stateBox.addItem("VT")
        self.stateBox.addItem("VI")
        self.stateBox.addItem("VA")
        self.stateBox.addItem("WA")
        self.stateBox.addItem("WV")
        self.stateBox.addItem("WI")
        self.stateBox.addItem("WY")
        self.verticalLayout.addWidget(self.stateBox)

    # Function that is called when the submit button is clicked
    def submit(self):
        error = self.validateFields()
        if not error:
            self.errorLabel.setStyleSheet("color: black;")
            self.errorLabel.setText("Please make sure all of the information"
                + "\nyou put is correct.\nPress confirm when ready.")
            self.submitButton.setText("Confirm")
            self.submitButton.clicked.disconnect()
            self.submitButton.clicked.connect(lambda: self.saveData())
        else:
            self.displayError(error)

    # Partially validates the info before it is saved
    def validateFields(self):
        name = self.nameLine.text().strip()
        email = self.emailLine.text().strip()
        phone = self.phoneLine.text()
        address = self.addressLine.text().strip()
        apt = self.aptLine.text().strip()
        city = self.cityLine.text().strip()
        state = self.stateBox.currentText()
        zip = self.zipLine.text()
        country = self.countryBox.currentText()

        if (not name or not email or not phone or not address or not city
            or state == "State" or not zip or country == "Country"):
            return "Please make sure all required fields have\nbeen filled."
        elif not " " in name:
             return "You need to include both your\nfirst and last name."
        elif not "@" in email or not "." in email:
            return "That isn't a valid email."
        elif len(phone) < 10:
            return "That isn't a valid phone number."
        elif len(zip) < 5:
            return "That isn't a valid zip code."
        return ""

    # Displays the error from the validate fields function
    def displayError(self, error):
        self.errorLabel.setStyleSheet("color: red;")
        self.errorLabel.setText(error)
        self.submitButton.setText("Submit")

    # Saves info passed from user to the bot instance
    def saveData(self):
        name = self.nameLine.text().strip()
        email = self.emailLine.text().strip()
        phone = self.phoneLine.text()
        address = self.addressLine.text().strip()
        apt = self.aptLine.text().strip()
        city = self.cityLine.text().strip()
        state = self.stateBox.currentText()
        zip = self.zipLine.text()
        country = self.countryBox.currentText()

        self.driver.bot.updateShipping(name, email, phone, address, apt,
            city, state, zip, country)

        self.driver.setPage("payment")

# Class to display payment info form
class PaymentPage(Page):

    # Sets payment info page margins for vertical layout
    def setupVerticalLayout(self):
        super().setupVerticalLayout()
        self.verticalLayout.setContentsMargins(105, 100, 105, 100)

    # Sets up the widgets for the page
    def setupWidgets(self):

        # Set up title label
        self.titleLabel = QLabel(self.verticalLayoutWidget)
        self.titleLabel.setMaximumSize(QSize(self.MAX_SIZE, 20))
        self.titleLabel.setText("Fill out your payment info:")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.titleLabel, 0, Qt.AlignHCenter)

        # Set up input forms
        self.cardLine = QLineEdit(self.verticalLayoutWidget)
        self.cardLine.setPlaceholderText("Card Number")
        cardReg = QRegExp("\d{19}")
        self.cardLine.setValidator(QRegExpValidator(cardReg, self.cardLine))
        self.verticalLayout.addWidget(self.cardLine)

        self.monthBox = QComboBox(self.verticalLayoutWidget)
        self.monthBox.setPlaceholderText("Month")
        for i in range(1, 13):
            if i < 10: self.monthBox.addItem("0%d" % i)
            else: self.monthBox.addItem("%d" % i)
        self.verticalLayout.addWidget(self.monthBox)

        self.yearBox = QComboBox(self.verticalLayoutWidget)
        self.yearBox.setPlaceholderText("Year")
        for i in range(11): self.yearBox.addItem("%d" % (2020 + i))
        self.verticalLayout.addWidget(self.yearBox)

        self.cvvLine = QLineEdit(self.verticalLayoutWidget)
        self.cvvLine.setPlaceholderText("CVV")
        cvvReg = QRegExp("\d{4}")
        self.cvvLine.setValidator(QRegExpValidator(cvvReg, self.cvvLine))
        self.verticalLayout.addWidget(self.cvvLine)

        # Set up submit button
        self.submitButton = QPushButton(self.verticalLayoutWidget)
        self.submitButton.setStyleSheet("background-color: red;\n"
            + "color: white;")
        self.submitButton.clicked.connect(lambda: self.submit())
        self.submitButton.setText("Submit")
        self.verticalLayout.addWidget(self.submitButton, 0, Qt.AlignHCenter)

        # Set up error label
        self.errorLabel = QLabel(self.verticalLayoutWidget)
        self.errorLabel.setMaximumSize(QSize(self.MAX_SIZE, 70))
        self.errorLabel.setStyleSheet("color: red;")
        self.errorLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.errorLabel, 0, Qt.AlignHCenter)

        super().setupWidgets()

    # Function for submit button
    def submit(self):
        error = self.validateFields()
        if not error:
            self.errorLabel.setStyleSheet("color: black;")
            self.errorLabel.setText("Please make sure all of the information"
                + "\nyou put is correct.\nPress confirm when ready.")
            self.submitButton.setText("Confirm")
            self.submitButton.clicked.disconnect()
            self.submitButton.clicked.connect(lambda: self.saveData())
        else:
            self.displayError(error)

    # Partially validates payment info
    def validateFields(self):
        card = self.cardLine.text()
        month = self.monthBox.currentText()
        year = self.yearBox.currentText()
        cvv = self.cvvLine.text()

        if not card or month == "Month" or year == "Year" or not cvv:
            return "Please make sure all required fields have\nbeen filled."
        elif not len(card) == 16 and not len(card) == 19:
            return "That isn't a valid card number."
        elif len(cvv) < 3:
            return "That isn't a valid cvv code."
        return ""

    # Displays error from validate field
    def displayError(self, error):
        self.errorLabel.setStyleSheet("color: red;")
        self.errorLabel.setText(error)
        self.submitButton.setText("Submit")

    # Saves data to bot instance
    def saveData(self):
        card = self.cardLine.text()
        month = self.monthBox.currentText()
        year = self.yearBox.currentText()
        cvv = self.cvvLine.text()

        self.driver.bot.updatePayment(card, month, year, cvv)

        self.driver.setPage("runBot")

# Class to display and handle running bot
class BotRunnerPage(Page):

    # Set up margins for vertical layout
    def setupVerticalLayout(self):
        super().setupVerticalLayout()
        self.verticalLayout.setContentsMargins(75, 250, 75, 250)

    # Set up widgets
    def setupWidgets(self):

        self.titleLabel = QLabel(self.verticalLayoutWidget)
        self.titleLabel.setMaximumSize(QSize(self.MAX_SIZE, 250))
        self.titleLabel.setText("Better Bot is ready to go!"
            + "\n\nIf you realized you input something wrong,\nrestart the"
            + " program and use the\ncorrect information."
            + "\n\nDon't forget about filling out the Recaptcha\nat the end!"
            + "\n\nGood luck!")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.verticalLayout.addWidget(self.titleLabel, 0, Qt.AlignHCenter)

        self.operationButton = QPushButton(self.verticalLayoutWidget)
        self.operationButton.setStyleSheet("background-color: red;\n"
            + "color: white;")
        self.operationButton.clicked.connect(lambda: self.activateBot())
        self.operationButton.setText("Start")
        self.verticalLayout.addWidget(self.operationButton, 0, Qt.AlignHCenter)

        super().setupWidgets()

    # Activates the bot when the button is pressed
    def activateBot(self):

        # Change button style and function
        self.operationButton.setEnabled(False)
        self.operationButton.clicked.disconnect()
        self.operationButton.setStyleSheet("background-color: #ff6161;\n"
            + "color: white;")
        self.operationButton.setText("Stop")
        self.operationButton.clicked.connect(lambda: self.stopBot())

        # Connecting the page and starting bot
        self.driver.bot.connectPage(self)
        self.driver.bot.start()

    # Updates title label as bot runs
    def updateInfo(self, info):
        self.titleLabel.setText(info)

    # Changes button style once bot driver has loaded
    def updateButton(self):
        self.titleLabel.setText("Better Bot is active!")
        self.operationButton.setStyleSheet("background-color: red;\n"
            + "color: white;")
        self.operationButton.setEnabled(True)

    # Stops the bot, quits if theres an error thrown, quits when done
    def stopBot(self):
        self.operationButton.clicked.disconnect()
        self.driver.bot.stop()
        if self.driver.bot.errorThrown:
            self.updateInfo("Quitting...")
            sys.exit()
        elif self.driver.bot.endReached:
            self.updateInfo("Quitting...")
            self.driver.bot.quit()
            sys.exit()
        self.resetButton()

    # Resets the button style in case you stop
    def resetButton(self):
        self.driver.resetBot()
        self.titleLabel.setText("Better Bot is ready to go!"
            + "\n\nIf you realized you input something wrong,\nrestart the"
            + " program and use the\ncorrect information."
            + "\n\nDon't forget about filling out the Recaptcha\nat the end!"
            + "\n\nGood luck!")
        self.operationButton.setText("Start")
        self.operationButton.clicked.connect(lambda: self.activateBot())

    # Changes button text when needed
    def changeButtonText(self, text):
        self.operationButton.setText(text)
