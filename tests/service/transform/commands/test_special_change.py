import unittest


class TestSpecialChange(unittest.TestCase):

    def setUp(self) -> None:
        ...

    def test_fisica_1(self):
        self.assertEqual(1+1, 2)


if __name__ == '__main__':
    unittest.main()
