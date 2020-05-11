from unittest import TestCase

from ttg.room import create_room


class TestRoom(TestCase):

    def test_create_room(self):
        """creating a room generates a unique code"""

        # method under test
        room_code = create_room('test')

        # make sure room code looks sane
        self.assertEqual(6, len(room_code))
