from pytz import timezone
from selenium import webdriver
from selenium import common
from time import sleep
import ctypes
import datetime
import threading

class BetterBot(threading.Thread):

    # Initialization with desired product's xpath saved
    def __init__(self):
        threading.Thread.__init__(self)
        self.errorThrown = False
        self.endReached = False

        # Info to be changed based on customer's desired product
        self.product = "//img[@alt='2cfbpnh2oq8']"
        self.sizedItem = False
        self.size = "Medium"

    # Saves user's shipping info
    def updateShipping(self, name, email, phone, address, apt, city,
        state, zip, country):
        self.fullName = name
        self.email = email
        self.phone = phone
        self.address = address
        self.apt = apt
        self.city = city
        self.state = state
        self.zip = zip
        self.country = country

    # Saves user's payment info
    def updatePayment(self, card, month, year, cvv):
        self.card = card
        self.month = month
        self.year = year
        self.cvv = cvv

    # Save user's size if the item is sized
    def updateSize(self, size):
        self.size = size

    # Connecting the bot with the UI page to display updates
    # as to what the bot is doing
    def connectPage(self, page):
        self.page = page

    # Runs the script to automate your checkout
    def run(self):
        try:
            self.page.updateInfo("Launching Better Bot...")

            # Setting options to have no print outs in console
            # From https://stackoverflow.com/questions/47392423/python-selenium-devtools-listening-on-ws-127-0-0-1
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches',
                ['enable-logging'])

            # Launching WebDriver and proceeding to shop URL
            PATH = "C:\Program Files (x86)\chromedriver.exe"
            self.driver = webdriver.Chrome(PATH, options=options)

            self.page.updateButton()

            self.driver.get("https://www.supremenewyork.com/shop/all")

            # Waiting for the scheduled drop time to begin refreshing the page
            tz = timezone("US/Eastern")
            DROP_TIME = datetime.time(11, 0, 0, 0)

            count = 0
            while datetime.datetime.now(tz).time() < DROP_TIME:
                if count % 600000 == 0:
                    self.page.updateInfo("Waiting for drop time\n.")
                elif count % 600000 == 200000:
                    self.page.updateInfo("Waiting for drop time\n..")
                elif count % 600000 == 400000:
                    self.page.updateInfo("Waiting for drop time\n...")
                if count == 6000000:
                    count = 0
                    continue
                count += 1

            self.page.updateInfo("Looking for drop...")

            # Refreshes page until it finds the right product
            while True:
                try:
                    element = self.driver.find_element_by_xpath(self.product)
                    element.click()
                    break
                except common.exceptions.NoSuchElementException:
                    self.driver.refresh()

            startTime = datetime.datetime.now()
            self.page.updateInfo("DROP! Detected at "
                + str(startTime.time())[:8] + ".\n Attempting to cop...")

            # If the item is sized, then select the right size
            if self.sizedItem:
                while True:
                    try:
                        element = self.driver.find_element_by_xpath("//select"
                            + "[@name='s']")
                        selector = webdriver.support.select.Select(element)
                        selector.select_by_visible_text(self.size)
                        break
                    except common.exceptions.NoSuchElementException:
                        continue

            self.page.updateInfo("Adding product to cart...")

            # Add to cart and wait until it was added
            while True:
                try:
                    element = self.driver.find_element_by_xpath("//*[@id='add-"
                        + "remove-buttons']/input")
                    element.click()
                    break
                except common.exceptions.NoSuchElementException:
                    continue

            while True:
                try:
                    element = self.driver.find_element_by_xpath("//*[@id='cart"
                        + "-remove']")
                    break
                except common.exceptions.NoSuchElementException:
                    continue

            self.page.updateInfo("Added product to cart!\nProceeding to "
                + "checkout...")

            # Go to checkout
            self.driver.get("https://www.supremenewyork.com/checkout")

            self.page.updateInfo("Filling out checkout details...\n"
                + "Be ready to fill out the Recaptcha!")

            # Fill out the billing/shipping info field by field
            element = self.driver.find_element_by_xpath("//*[@id='order_"
                + "billing_name']")
            element.click()
            element.send_keys(self.fullName)

            element = self.driver.find_element_by_xpath("//*[@id='order_"
                + "email']")
            element.click()
            element.send_keys(self.email)

            element = self.driver.find_element_by_xpath("//*[@id='order_tel']")
            element.click()
            for char in self.phone:
                element.send_keys(char)
                sleep(.001)

            element = self.driver.find_element_by_xpath("//*[@placeholder="
                + "'address']")
            element.click()
            element.send_keys(self.address)

            element = self.driver.find_element_by_xpath("//*[@id='order"
                + "_billing_zip']")
            element.click()
            element.send_keys(self.zip)

            element = self.driver.find_element_by_xpath("//*[@id='order"
                + "_billing_city']")
            element.click()
            element.send_keys(self.city)

            element = self.driver.find_element_by_xpath("//*[@id='order"
                + "_billing_state']")
            selector = webdriver.support.select.Select(element)
            selector.select_by_value(self.state)

            element = self.driver.find_element_by_xpath("//*[@id="
                + "'credit_card_type']")
            selector = webdriver.support.select.Select(element)
            selector.select_by_visible_text("Credit Card")

            element = self.driver.find_element_by_xpath("//*[@id='rnsnckrn']")
            element.click()
            for char in self.card:
                element.send_keys(char)
                sleep(.001)

            element = self.driver.find_element_by_xpath("//*[@id='credit_"
                + "card_month']")
            selector = webdriver.support.select.Select(element)
            selector.select_by_visible_text(self.month)

            element = self.driver.find_element_by_xpath("//*[@id='credit_"
                + "card_year']")
            selector = webdriver.support.select.Select(element)
            selector.select_by_visible_text(self.year)

            element = self.driver.find_element_by_xpath("//*[@placeholder"
                + "='CVV']")
            element.click()
            element.send_keys(self.cvv)

            element = self.driver.find_element_by_xpath("//*[@id='cart-cc']"
                + "/fieldset/p/label/div")
            element.click()

            element = self.driver.find_element_by_xpath("//*[@id='pay']/input")
            element.click()

            # Done!
            endTime = datetime.datetime.now()
            processingTime = endTime - startTime

            self.page.updateInfo("The drop occured at "
                + str(startTime.time())[:8] + ".\nThe bot was able to reach"
                + " the final stage of\ncheckout in "
                + str(processingTime)[5:] + "s."
                + "\n\nFeel free to quit when you have secured your"
                + " purchase.\n\nThanks for using Better Bot!")

            self.endReached = True

        except Exception as e:
            self.errorThrown = True
            self.page.updateInfo("Something went wrong...\n"
                + "Try restarting the program :/")
            self.page.changeButtonText("Quit")

        finally:
            if self.endReached:
                self.page.changeButtonText("Quit")
            else:
                self.quit()

    # Helper function to retrieve id of thread
    def getId(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    # Throws error to interrupt thread
    def stop(self):
        if not self.errorThrown and not self.endReached:
            thread_id = self.getId()
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                  ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
                print('Exception raise failure')

    # Quits
    def quit(self):
        self.driver.quit()
