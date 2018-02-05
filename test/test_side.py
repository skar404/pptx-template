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
        os.chdir(os.path.join(BASE_DIR, 'data4'))

        ppt = Presentation('in.pptx')
        process_all_slides(
            {
                "0": [
                    {
                        "string_0": '[DotNetBook] Stackalloc: забытая команда C#',
                        "string_1": 'С этой статьей я продолжаю публиковать целую серию статей, результатом которой будет '
                                    'книга по работе .NET CLR, и .NET в целом. Вся книга будет доступна на GitHub (ссылка '
                                    'в конце статьи).',
                    }, {
                        "string_0": '[DotNetBook] Stackalloc: забытая команда C#',
                        "string_1": 'С этой статьей я продолжаю публиковать целую серию статей, результатом которой будет '
                                    'книга по работе .NET CLR, и .NET в целом. Вся книга будет доступна на GitHub (ссылка '
                                    'в конце статьи).'
                    }
                ]
            }, ppt, True)
        ppt.save('out.pptx')

        if __name__ == '__main__':
            unittest.main()
