import unittest


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        ...

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
