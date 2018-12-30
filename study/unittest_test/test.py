import unittest
from study.unittest_test.name_function import get_formatted_name


class NamesTestCase(unittest.TestCase):
    """测试"""

    def test_fist_last_name(self):
        formatted_name = get_formatted_name('janis', 'joplin')
        self.assertEqual(formatted_name, 'Janis Joplin')


unittest.main()