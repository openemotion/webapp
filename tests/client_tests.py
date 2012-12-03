# coding=utf8

import re
import sys
import time
import urllib
import random
import logging
import unittest
import threading
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

sys.path.append("..")

from webapp import app
from flask import request
from db import Database

logging.disable(logging.INFO)

# Configuration
app.config['DATABASE']  = 'test_data.db'
app.config['UPDATE_INTERVAL'] = 1000
app.config['ENABLE_LONG_POLL'] = False
UPDATE_INTERVAL = app.config['UPDATE_INTERVAL'] / 1000.0
HOST = 'localhost'
PORT = 5001
ROOT_URL = 'http://%s:%s/' % (HOST, PORT)
LEAVE_CHROME_OPEN = False

# Load lorem ipsum
LOREM_IPSUM = open('lorem.txt').read().decode('utf8').splitlines()

# Create chromedriver service
import atexit
import selenium.webdriver.chrome.service as service
CHROME_SERVICE = service.Service('/usr/bin/chromedriver')
CHROME_SERVICE.start()
def stop_chrome_service():
    try:
        CHROME_SERVICE.stop()
    except:
        pass
atexit.register(stop_chrome_service)

def run_server():
    try:
        app.run(host=HOST, port=PORT, debug=False)
    except IOError:
        pass

@app.route("/shutdown")
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError("Not running with the Werkzeug Server")
    func()
    return ""

class ClientTest(unittest.TestCase):
    def setUp(self):
        # setting up testing web server and browser
        Database(app.config["DATABASE"]).init()
        self.appthread = threading.Thread(target=run_server)
        self.appthread.setDaemon(True)
        self.appthread.start()
        self.driver1 = webdriver.Remote(CHROME_SERVICE.service_url, {'chrome.detach': LEAVE_CHROME_OPEN})
        self.driver1.set_window_size(800,500)
        self.driver1.set_window_position(0,0)
        self.driver2 = webdriver.Remote(CHROME_SERVICE.service_url, {'chrome.detach': LEAVE_CHROME_OPEN})
        self.driver2.set_window_size(800,500)
        self.driver2.set_window_position(800,0)
        self.driver3 = webdriver.Remote(CHROME_SERVICE.service_url, {'chrome.detach': LEAVE_CHROME_OPEN})
        self.driver3.set_window_size(800,500)
        self.driver3.set_window_position(800,500)

    def tearDown(self):
        # killing server
        urllib.urlopen(ROOT_URL + 'shutdown')
        self.appthread.join()

    def test_two_new_users(self):
        talker = self.driver1
        listener = self.driver2
        viewer = self.driver3

        # register talker

        self.register_user(talker, u'אלי', u'אלי', u'אלי')
        assert talker.current_url == ROOT_URL
        assert talker.find_element_by_id('login-links').text == u"מחובר כ-אלי | התנתק"

        # register listener

        self.register_user(listener, u'גברי', u'גברי', u'גברי')
        assert listener.current_url == ROOT_URL
        assert listener.find_element_by_id('login-links').text == u"מחובר כ-גברי | התנתק"

        # talker shares something

        talker.find_element_by_id('new_share').click()
        talker.find_element_by_id('message').send_keys(u"אני ממש אוהב בדיקות אוטומאטיות")
        # header should change to first line of text
        assert talker.find_element_by_tag_name('h1').text == u"אני ממש אוהב בדיקות אוטומאטיות"
        talker.find_element_by_id('message').send_keys(Keys.RETURN)
        talker.find_element_by_id('message').send_keys(Keys.RETURN)
        talker.find_element_by_id('message').send_keys(u"זה כל כך מגניב שאין לי מילים בכלל לתאר את זה!")
        talker.find_element_by_id('message').send_keys(Keys.RETURN)
        talker.find_element_by_id('message').send_keys(u"וזו עוד שורה, סתם בשביל הקטע.")
        talker.find_element_by_id('submit').click()
        assert talker.current_url.startswith("http://localhost:5001/conversations/1/")

        # listener goes to conversation and accepts it

        self.goto_conversation(listener, u"אני ממש אוהב בדיקות אוטומאטיות")
        listener.find_element_by_id('submit_listen').click()

        # viewer goes to conversation

        self.goto_conversation(viewer, u"אני ממש אוהב בדיקות אוטומאטיות")

        # start conversation

        time.sleep(UPDATE_INTERVAL)

        for i, ipsum in enumerate(LOREM_IPSUM[:6]):
            #FIXME: add asserts that the messages are actually being shown
            # submitter = random.choice([talker, talker, listener])
            submitter = talker if i % 2 == 0 else listener
            submitter.find_element_by_id('message').send_keys(ipsum)
            submitter.find_element_by_id('message').send_keys(Keys.RETURN)
            submitter.find_element_by_id('message').send_keys(Keys.RETURN)
            time.sleep(UPDATE_INTERVAL)

    @staticmethod
    def register_user(driver, name, password, password2):
        driver.get(ROOT_URL)
        driver.find_element_by_link_text(u'הרשמה').click()
        driver.find_element_by_id('name').send_keys(name)
        driver.find_element_by_id('password').send_keys(password)
        driver.find_element_by_id('password2').send_keys(password2)
        driver.find_element_by_id('register').click()

    @staticmethod
    def goto_conversation(driver, title):
        driver.get(ROOT_URL)
        for i in range(3):
            convs = driver.find_elements_by_class_name('conversation_link')
            for conv in convs:
                if title in conv.text:
                    conv.find_element_by_class_name('title').find_element_by_tag_name('a').click()
                    return
            # conversations haven't updated yet
            time.sleep(UPDATE_INTERVAL)
        raise AssertionError("can't find conversation '%s'" % title)

if __name__ == '__main__':
    import pytest
    pytest.main(["-s", __file__])
