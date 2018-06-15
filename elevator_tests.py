import unittest
import elevator


class TestElevator(unittest.TestCase):

    def setUp(self):
        self.elevator = elevator.Elevator(1)

    def test_init(self):
        self.assertEqual(self.elevator.level, 1)
        self.assertEqual(self.elevator.target, 1)
        self.assertEqual(self.elevator.occupancy, 0)
        self.assertEqual(self.elevator.delay, 1)
        self.assertEqual(self.elevator.isMoving, False)

    def test_moving(self):
        self.elevator.move(1)
        self.assertEqual(self.elevator.level, 2)  # 1 + 1 = 2
        self.elevator.move(5)
        self.assertEqual(self.elevator.level, 7)  # 2 + 5 = 7
        self.elevator.move(-1)
        self.assertEqual(self.elevator.level, 6)  # 7 - 1 = 6
        self.elevator.move(-0.0)
        self.assertEqual(self.elevator.level, 6)  # 6 - 0 = 6

    def test_condition(self):
        self.elevator.stop()
        self.assertEqual(self.elevator.isMoving, False)
        self.elevator.go()
        self.assertEqual(self.elevator.isMoving, True)
        self.elevator.go()
        self.assertEqual(self.elevator.isMoving, True)
        self.elevator.stop()
        self.assertEqual(self.elevator.isMoving, False)


if __name__ == '__main__':
    unittest.main()
