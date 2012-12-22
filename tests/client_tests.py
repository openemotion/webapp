# coding=utf8

import unittest
import test_utils.testapp as testapp
import test_utils.testobjects as testobjects

import logging
logging.disable(logging.INFO)

LOREM_IPSUM = open('lorem.txt').read().decode('utf8').splitlines()

testobjects.start_selenium()

class ClientTest(unittest.TestCase):
    def setUp(self):
        testapp.start_test_server()

    def tearDown(self):
        testapp.shutdown_test_server()

    def test_conversation(self):
        talker = testobjects.TestUser(testapp.SERVER_URL)
        listener = testobjects.TestUser(testapp.SERVER_URL)
        viewer = testobjects.TestUser(testapp.SERVER_URL)

        # register users
        talker.register(u'אלי', u'אלי', u'אלי')
        listener.register(u'גברי', u'גברי', u'גברי')

        # create conversation
        title = u"אני ממש אוהב בדיקות אוטומאטיות"
        talker.share(title,
            u"זה כל כך מגניב שאין לי מילים בכלל לתאר את זה!\n"
            u"וזו עוד שורה, סתם בשביל הקטע"
        )

        # accept conversation
        listener.open(title)

        # view conversation        
        viewer.open(title)

        # converse
        for i, ipsum in enumerate(LOREM_IPSUM[:6]):

            sender, receiver = (talker, listener) if i % 2 == 0 else (listener, talker)
            sender.send(ipsum)
            receiver.wait_updated()
            msg = receiver.receive()
            assert msg == ipsum

if __name__ == '__main__':
    import pytest
    pytest.main(["-s", __file__])
