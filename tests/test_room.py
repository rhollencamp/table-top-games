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
        mock_calls = wsock_mock.method_calls
        self.assertEqual(1, len(mock_calls))
        self.assertEqual('send', mock_calls[0][0])

        # verify response contained the right msg and a valid looking room code
        msg = json.loads(mock_calls[0][1][0])
        self.assertEqual('room-created', msg['msg'])
        self.assertIsInstance(msg['room'], str)
        self.assertEqual(6, len(msg['room']))
