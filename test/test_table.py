import os
import unittest
import logging

from pptx import Presentation

from pptx_template.cli import process_all_slides


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FORMAT = '%(filename)s[%(lineno)-3d] %(levelname)-2s [%(asctime)s]  %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


class MyTest(unittest.TestCase):
    def test_create_table(self):
        ppt = Presentation(BASE_DIR + '/data3/in.pptx')
        process_all_slides({
            "1": {
                "table0": '1',
                "table1": '1'
            }
        }, ppt, True)
        ppt.save(BASE_DIR + '/data3/out.pptx')


if __name__ == '__main__':
    from .test_cli import *

    unittest.main()
