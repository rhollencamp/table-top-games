from unittest import TestCase
from unittest.mock import patch
from unittest.mock import Mock
import json

from ttg import room


class TestRoom(TestCase):

    @patch("ttg.room._generate_room_code", return_value="ABCDEF")
    def test_create_room(self, _):
        wsock_mock = Mock()
        room.create_room({"name": "test"}, wsock_mock)
        self.assertEqual(json.dumps({"room": "ABCDEF"}),
                         wsock_mock.send.call_args[0][0])

    @patch("ttg.room._generate_room_code",
           side_effect=["BCDEFG", "BCDEFG", "CDEFGH"])
    def test_create_room_duplicate_code(self, _):
        """
        _generate_room_code is random and could generate a room code that is
        already in use; make sure create_room returns a unique code and not
        one that is already in use
        """
        wsock_mock = Mock()
        room.create_room({"name": "test"}, wsock_mock)
        self.assertEqual(json.dumps({"room": "BCDEFG"}),
                         wsock_mock.send.call_args[0][0])

        wsock_mock = Mock()
        room.create_room({"name": "test"}, wsock_mock)
        self.assertEqual(json.dumps({"room": "CDEFGH"}),
                         wsock_mock.send.call_args[0][0])
