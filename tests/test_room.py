"""
Unit tests against room logic
"""

from unittest import TestCase
from unittest.mock import Mock
import json

from ttg import room


class TestRoom(TestCase):

    def test_create_room(self):
        # setup
        wsock_mock = Mock()

        # method under test
        room.create_room('test', wsock_mock)

        # verify response was sent to the web socket
        msg = self.__find_msg(wsock_mock, 'room-created')
        self.assertIsNotNone(msg)
        # make sure room code looks sane
        self.assertIsInstance(msg['room'], str)
        self.assertEqual(6, len(msg['room']))

    def test_join_room_player_broadcast(self):
        """when someone joins a room make sure player list is broadcast"""
        # setup
        wsock_foo_mock = Mock()
        wsock_bar_mock = Mock()

        # methods under test
        room.create_room('foo', wsock_foo_mock)
        room_code = self.__extract_room_code(wsock_foo_mock)
        room.join_room('bar', room_code, wsock_bar_mock)

        # make sure foo got the broadcast
        msg = self.__find_msg(wsock_foo_mock, 'player-list')
        self.assertIsNotNone(msg)
        self.assertEqual(['foo', 'bar'], msg['players'])
        # make sure bar got the broadcast
        msg = self.__find_msg(wsock_bar_mock, 'player-list')
        self.assertIsNotNone(msg)
        self.assertEqual(['foo', 'bar'], msg['players'])

    @staticmethod
    def __extract_room_code(mock):
        msg = mock.send.call_args[0][0]
        msg = json.loads(msg)
        return msg['room']

    @staticmethod
    def __find_msg(mock, msg):
        for x in mock.send.call_args:
            x = json.loads(x[0])
            if x['msg'] == msg:
                return x
        return None
