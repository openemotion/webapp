# coding=utf8

import time
import atexit
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import selenium.webdriver.chrome.service as service

SLEEP_INTERVAL = 1.0

LEAVE_CHROME_OPEN = False
CHROME_SERVICE = service.Service('/usr/bin/chromedriver')
def start_selenium():
    CHROME_SERVICE.start()
    def stop_chrome_service():
        try:
            CHROME_SERVICE.stop()
        except:
            pass
    atexit.register(stop_chrome_service)
CHROME_INSTANCES = 0
PLACEMENTS = [
    dict(position=(0,0), size=(800,500)),
    dict(position=(800,0), size=(800,500)),
    dict(position=(800,500), size=(800,500)),
    dict(position=(0,500), size=(800,500)),
]

class TestUser(object):
    def __init__(self, url):
        # start chrome via selenium
        global CHROME_INSTANCES
        self.driver = webdriver.Remote(CHROME_SERVICE.service_url, {'chrome.detach': LEAVE_CHROME_OPEN})
        place = PLACEMENTS[CHROME_INSTANCES % 4]
        self.driver.set_window_size(*place['size'])
        self.driver.set_window_position(*place['position'])
        CHROME_INSTANCES += 1

        self.url = url
        self.driver.get(self.url)

    def register(self, name, password, password2):
        self.driver.find_element_by_link_text(u'הרשמה').click()
        self.driver.find_element_by_id('name').send_keys(name)
        self.driver.find_element_by_id('password').send_keys(password)
        self.driver.find_element_by_id('password2').send_keys(password2)
        self.driver.find_element_by_id('register').click()
        assert self.driver.current_url == self.url
        assert self.driver.find_element_by_id('login-links').text == u"מחובר כ-%s | התנתק" % name

    def login(self, name, password):
        pass

    def logout(self):
        pass

    def share(self, title, text):
        self.driver.find_element_by_id('new_share').click()
        self.driver.find_element_by_id('message').send_keys(title)
        self.driver.find_element_by_id('message').send_keys(Keys.RETURN)
        self.driver.find_element_by_id('message').send_keys(Keys.RETURN)
        for line in text.splitlines():
            self.driver.find_element_by_id('message').send_keys(line)
            self.driver.find_element_by_id('message').send_keys(Keys.RETURN)
        self.driver.find_element_by_id('submit').click()
        assert self.driver.find_element_by_tag_name('h1').text == title
        assert self.driver.current_url.startswith(self.url + "conversations/1/")

    def open(self, title):
        for i in xrange(10):
            convs = self.driver.find_elements_by_class_name('conversation_link')
            for conv in convs:
                if title in conv.text:
                    try:
                        conv.find_element_by_class_name('title').find_element_by_tag_name('a').click()
                    except StaleElementReferenceException:
                        pass
                    else:
                        return
            time.sleep(SLEEP_INTERVAL)
        raise AssertionError("can't find conversation '%s'" % title)

    def send(self, message):
        self.driver.find_element_by_id('message').send_keys(message)
        self.driver.find_element_by_id('message').send_keys(Keys.RETURN)
        self.driver.find_element_by_id('message').send_keys(Keys.RETURN)

    def wait_updated(self):
        prev_history = self.driver.find_element_by_id('history').text
        for i in xrange(10):
            if prev_history != self.driver.find_element_by_id('history').text:
                return
            time.sleep(SLEEP_INTERVAL)
        raise AssertionError("no updates received")

    def receive(self):
        messages = self.driver.find_elements_by_class_name('message')
        if messages:
            last_message = messages[-1]
            return last_message.find_elements_by_class_name("text")[0].text
        else:
            return None
