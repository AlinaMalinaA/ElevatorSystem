import unittest
import controller as c


class TestController(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.controller = c.Controller(1)

    def test_init(self):
        self.assertEqual(self.controller.where_are_we_now(), 1)
        self.assertEqual(self.controller.where_do_we_go(), 1)
        self.assertEqual(self.controller.how_much_people_inside(), 0)
        self.assertFalse(self.controller.is_elev_moving())

    def test_of_loading_people(self):
        self.controller.load_people(1)
        self.assertEqual(self.controller.how_much_people_inside(), 1)
        self.assertFalse(self.controller.if_elevator_empty())
        self.controller.load_people(-1)
        self.assertEqual(self.controller.how_much_people_inside(), 0)
        self.assertTrue(self.controller.if_elevator_empty())
        self.controller.load_people(1.0)
        self.assertEqual(self.controller.how_much_people_inside(), 1)
        self.assertFalse(self.controller.if_elevator_empty())

    def test_of_elevator_preparing(self):
        target = 5
        self.controller.prepare_elevator(5)
        self.assertEqual(self.controller.where_do_we_go(), target)
        self.assertTrue(self.controller.is_elev_moving())
        self.controller.stop_the_elevator()
        temp_of_actual_level = self.controller.where_are_we_now()
        self.controller.prepare_elevator(temp_of_actual_level)
        self.assertFalse(self.controller.is_elev_moving())
        self.assertEqual(self.controller.where_do_we_go(), temp_of_actual_level)
        self.assertNotEqual(self.controller.where_are_we_now(), target)

    def test_of_moving(self):
        target = 3
        self.assertFalse(self.controller.is_elev_moving())
        self.controller.prepare_elevator(target)
        self.assertTrue(self.controller.is_elev_moving())
        self.assertNotEqual(self.controller.where_are_we_now(), target)
        self.assertEqual(self.controller.where_do_we_go(), target)
        self.assertTrue(self.controller.is_that_not_our_target(target-1))
        self.controller.move(target)
        self.assertFalse(self.controller.is_elev_moving())
        self.assertEqual(self.controller.where_are_we_now(), target)
        self.assertFalse(self.controller.is_that_not_our_target(target))

    def test_of_left_levels_range(self):
        target = 10
        self.controller.prepare_elevator(target)
        a, b = self.controller.give_the_range_of_levels_that_left()
        self.assertLess(a, b)
        temp_actual_level = self.controller.where_are_we_now()
        if temp_actual_level < target:
            self.assertEqual(a, temp_actual_level)
            self.assertEqual(b, target)
        else:
            self.assertEqual(b, temp_actual_level)
            self.assertEqual(a, target)
        self.controller.stop_the_elevator()


if __name__ == '__main__':
    unittest.main()
