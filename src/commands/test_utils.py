import unittest
from random import seed

from utils import shuffle


class ShuffleTests(unittest.TestCase):

    def test_shuffle(self):
        # Set a seed for predictable results
        seed(42)

        # Test case 1: Shuffle a list of numbers
        context1 = {
            "data": [1, 2, 3, 4, 5]
        }

        data1 = shuffle(context1)

        # Assert that the result is a shuffled version of the input list
        self.assertNotEqual(data1, [1, 2, 3, 4, 5])
        self.assertEqual(set(data1), {1, 2, 3, 4, 5})

        # Test case 2: Shuffle a list of strings
        context2 = {
            "data": ["apple", "banana", "cherry", "date", "elderberry"]
        }

        data2 = shuffle(context2)

        # Assert that the result is a shuffled version of the input list
        self.assertNotEqual(data2, ["apple", "banana", "cherry", "date", "elderberry"])
        self.assertEqual(set(data2), {"apple", "banana", "cherry", "date", "elderberry"})

        # Test case 3: Shuffle an empty list
        context3 = {
            "data": []
        }

        data3 = shuffle(context3)

        # Assert that the result is an empty list
        self.assertEqual(data3, [])

        # Test case 4: Shuffle a list with a single element
        context4 = {
            "data": [42]
        }

        data4 = shuffle(context4)

        # Assert that the result is the same as the input list (since there's only one element)
        self.assertEqual(data4, [42])


if __name__ == "__main__":
    unittest.main()
