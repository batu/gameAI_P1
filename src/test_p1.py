import unittest
import  p1, p1_support

class Test_P1(unittest.TestCase):

        src_waypoint, dst_waypoint = "a", "e"
        def test_trivial(self):
            filename = "../input/test_trivial.txt"
            path = p1.unit_test_route(filename, self.src_waypoint, self.dst_waypoint)
            correct_path = [(1,1)]

            path.sort()
            correct_path.sort()
            self.assertEqual(path, correct_path)


        def test_simple(self):
            filename = "../input/test_simple.txt"
            path = p1.unit_test_route(filename, self.src_waypoint, self.dst_waypoint)
            correct_path = [(1,1), (1,2), (1,3), (2,4)]

            path.sort()
            correct_path.sort()
            self.assertEqual(path, correct_path)


        def test_no_path(self):
            filename = "../input/test_nopath.txt"
            path = p1.unit_test_route(filename, self.src_waypoint, self.dst_waypoint)
            correct_path = []

            path.sort()
            correct_path.sort()
            self.assertEqual(path, correct_path)



if __name__ == '__main__':
        unittest.main()