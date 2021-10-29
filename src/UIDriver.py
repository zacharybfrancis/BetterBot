from PyQt5.QtCore import *
import BetterBot
import Page

# Class to handle different pages in the main window
class UIDriver:

    def __init__(self):
        self.bot = BetterBot.BetterBot()

    # Initial setup of window
    def setupUI(self, mainWindow):
        self.mainWindow = mainWindow
        self.mainWindow.setFixedSize(700, 800)
        self.mainWindow.setWindowTitle("Better Bot")
        self.mainWindow.setStyleSheet("background-color: white;")

    # Sets the page the user is looking at
    def setPage(self, page):
        if page == "welcome":
            welcomePage = Page.WelcomePage(self, self.mainWindow)
            welcomeWidget = welcomePage.getWidget()
            self.mainWindow.setCentralWidget(welcomeWidget)
            welcomePage.setupUI()
        elif page == "info":
            infoPage = Page.InfoPage(self, self.mainWindow)
            infoWidget = infoPage.getWidget()
            self.mainWindow.setCentralWidget(infoWidget)
            infoPage.setupUI()
        elif page == "shipping":
            shippingPage = Page.ShippingInfoPage(self, self.mainWindow)
            shippingWidget = shippingPage.getWidget()
            self.mainWindow.setCentralWidget(shippingWidget)
            shippingPage.setupUI()
        elif page == "payment":
            paymentPage = Page.PaymentPage(self, self.mainWindow)
            paymentWidget = paymentPage.getWidget()
            self.mainWindow.setCentralWidget(paymentWidget)
            paymentPage.setupUI()
        elif page == "runBot":
            runnerPage = Page.BotRunnerPage(self, self.mainWindow)
            runnerWidget = runnerPage.getWidget()
            self.mainWindow.setCentralWidget(runnerWidget)
            runnerPage.setupUI()

    # Creating a new instance of the bot to get new thread to start
    def resetBot(self):
        self.bot = BetterBot.BetterBot()
