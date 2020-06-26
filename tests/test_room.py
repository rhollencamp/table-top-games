from unittest import TestCase

from ttg.room import create_room
from ttg.room import Room


class TestRoom(TestCase):

    def test_create_room(self):
        """creating a room generates a unique code"""

        # method under test
        room_code = create_room('test')

        # make sure room code looks sane
        self.assertEqual(6, len(room_code))

    def test_add_entities(self):
        """test adding an entity to a room"""

        room = Room("ABC123")
        room.process_entity_defs({
            "entities": [{
                "img": "test",
                "width": 1,
                "height": 2,
                "pos_x": 3,
                "pos_y": 4
            }]})

        self.assertEqual(1, len(room.entities))
        for entity in room.entities.values():
            self.assertEqual("test", entity.img)
            self.assertEqual(1, entity.width)
            self.assertEqual(2, entity.height)
            self.assertEqual(3, entity.pos_x)
            self.assertEqual(4, entity.pos_y)
