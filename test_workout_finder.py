import unittest
from workout_finder import find_approx

class TestWorkoutFinder(unittest.TestCase):
    def test_find_approx(self):
        # Test case 1
        distance1 = 100
        distance2 = 200
        time1 = 10
        time2 = 20
        target_distance = 150
        expected_time = 15
        expected_distance = 150
        self.assertEqual(find_approx(distance1, distance2, time1, time2, target_distance), (expected_time, expected_distance))

        # Test case 2
        distance1 = 50
        distance2 = 100
        time1 = 5
        time2 = 10
        target_distance = 75
        expected_time = 7.5
        expected_distance = 75
        self.assertEqual(find_approx(distance1, distance2, time1, time2, target_distance), (expected_time, expected_distance))

        # Test case 3
        distance1 = 200
        distance2 = 300
        time1 = 20
        time2 = 30
        target_distance = 250
        expected_time = 25
        expected_distance = 250
        self.assertEqual(find_approx(distance1, distance2, time1, time2, target_distance), (expected_time, expected_distance))

if __name__ == '__main__':
    unittest.main()import unittest
from workout_finder import find_approx

class TestWorkoutFinder(unittest.TestCase):
    def test_find_approx(self):
        # Test case 1
        distance1 = 100
        distance2 = 200
        time1 = 10
        time2 = 20
        target_distance = 150
        expected_time = 15
        expected_distance = 150
        self.assertEqual(find_approx(distance1, distance2, time1, time2, target_distance), (expected_time, expected_distance))

        # Test case 2
        distance1 = 50
        distance2 = 100
        time1 = 5
        time2 = 10
        target_distance = 75
        expected_time = 7.5
        expected_distance = 75
        self.assertEqual(find_approx(distance1, distance2, time1, time2, target_distance), (expected_time, expected_distance))

        # Test case 3
        distance1 = 200
        distance2 = 300
        time1 = 20
        time2 = 30
        target_distance = 250
        expected_time = 25
        expected_distance = 250
        self.assertEqual(find_approx(distance1, distance2, time1, time2, target_distance), (expected_time, expected_distance))

if __name__ == '__main__':
    unittest.main()