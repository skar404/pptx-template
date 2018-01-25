import os
import unittest
import logging

from pptx import Presentation

from pptx_template.cli import process_all_slides

BASE_DIR = os.getcwd()

FORMAT = '%(filename)s[%(lineno)-3d] %(levelname)-2s [%(asctime)s]  %(message)s'
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
log.addHandler(handler)


class MyTest(unittest.TestCase):
    def tearDown(self):
        os.chdir(BASE_DIR)

    def test_create_table(self):
        os.chdir(os.path.join(BASE_DIR, 'test', 'data3'))

        ppt = Presentation('in.pptx')
        process_all_slides({
            "1": {
                "table0": '1',
                "table1": '1'
            }
        }, ppt, True)
        ppt.save('out.pptx')


if __name__ == '__main__':
    unittest.main()
