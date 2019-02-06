#    Copyright 2018 Rackspace, US Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import mock

from octavia_lib.api.drivers import driver_lib
from octavia_lib.api.drivers import exceptions as driver_exceptions
from octavia_lib.tests.unit import base


class TestDriverLib(base.TestCase):
    def setUp(self):
        self.driver_lib = driver_lib.DriverLibrary()

        super(TestDriverLib, self).setUp()

    @mock.patch('six.moves.builtins.memoryview')
    def test_recv(self, mock_memoryview):
        mock_socket = mock.MagicMock()
        mock_socket.recv.side_effect = [b'1', b'\n']
        mock_socket.recv_into.return_value = 1
        mv_mock = mock.MagicMock()
        mock_memoryview.return_value = mv_mock
        mv_mock.tobytes.return_value = b'"test data"'

        response = self.driver_lib._recv(mock_socket)

        calls = [mock.call(1), mock.call(1)]

        mock_socket.recv.assert_has_calls(calls)
        mock_socket.recv_into.assert_called_once_with(
            mv_mock.__getitem__(), 1)
        self.assertEqual('test data', response)

    @mock.patch('octavia_lib.api.drivers.driver_lib.DriverLibrary._recv')
    def test_send(self, mock_recv):
        mock_socket = mock.MagicMock()
        mock_recv.return_value = 'fake_response'

        with mock.patch('socket.socket') as socket_mock:
            socket_mock.return_value = mock_socket
            response = self.driver_lib._send('fake_path', 'test data')

        mock_socket.connect.assert_called_once_with('fake_path')
        mock_socket.send.assert_called_once_with(b'11\n')
        mock_socket.sendall.assert_called_once_with(b'"test data"')
        mock_socket.close.assert_called_once()
        self.assertEqual(mock_recv.return_value, response)

    @mock.patch('octavia_lib.api.drivers.driver_lib.DriverLibrary._send')
    def test_update_loadbalancer_status(self, mock_send):
        error_dict = {'status_code': 500, 'fault_string': 'boom',
                      'status_object': 'balloon', 'status_object_id': '1',
                      'status_record': 'tunes'}
        mock_send.side_effect = [{'status_code': 200}, Exception('boom'),
                                 error_dict]

        # Happy path
        self.driver_lib.update_loadbalancer_status('fake_status')

        mock_send.assert_called_once_with('/var/run/octavia/status.sock',
                                          'fake_status')

        # Test general exception
        self.assertRaises(driver_exceptions.UpdateStatusError,
                          self.driver_lib.update_loadbalancer_status,
                          'fake_status')

        # Test bad status code returned
        self.assertRaises(driver_exceptions.UpdateStatusError,
                          self.driver_lib.update_loadbalancer_status,
                          'fake_status')

    @mock.patch('octavia_lib.api.drivers.driver_lib.DriverLibrary._send')
    def test_update_listener_statistics(self, mock_send):
        error_dict = {'status_code': 500, 'fault_string': 'boom',
                      'status_object': 'balloon', 'status_object_id': '1',
                      'status_record': 'tunes'}
        mock_send.side_effect = [{'status_code': 200}, Exception('boom'),
                                 error_dict]

        # Happy path
        self.driver_lib.update_listener_statistics('fake_stats')

        mock_send.assert_called_once_with('/var/run/octavia/stats.sock',
                                          'fake_stats')

        # Test general exception
        self.assertRaises(driver_exceptions.UpdateStatisticsError,
                          self.driver_lib.update_listener_statistics,
                          'fake_stats')

        # Test bad status code returned
        self.assertRaises(driver_exceptions.UpdateStatisticsError,
                          self.driver_lib.update_listener_statistics,
                          'fake_stats')
