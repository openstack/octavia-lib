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
from unittest import mock

from octavia_lib.api.drivers import driver_lib
from octavia_lib.api.drivers import exceptions as driver_exceptions
from octavia_lib.common import constants
from octavia_lib.tests.unit import base


class TestDriverLib(base.TestCase):

    @mock.patch('octavia_lib.api.drivers.driver_lib.DriverLibrary.'
                '_check_for_socket_ready')
    def setUp(self, mock_check_ready):
        self.driver_lib = driver_lib.DriverLibrary()

        super(TestDriverLib, self).setUp()

    @mock.patch('octavia_lib.api.drivers.driver_lib.DriverLibrary.'
                '_check_for_socket_ready.retry.sleep')
    @mock.patch('os.path.exists')
    def test_check_for_socket_ready(self, mock_path_exists, mock_sleep):
        mock_path_exists.return_value = True

        # should not raise an exception
        self.driver_lib._check_for_socket_ready('bogus')

        mock_path_exists.return_value = False
        self.assertRaises(driver_exceptions.DriverAgentNotFound,
                          self.driver_lib._check_for_socket_ready,
                          'bogus')

    @mock.patch('builtins.memoryview')
    def test_recv(self, mock_memoryview):
        mock_socket = mock.MagicMock()
        mock_socket.recv.side_effect = [b'1', b'\n', b'2', b'\n', b'3', b'\n']
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

        # Test size recv timeout
        with mock.patch('octavia_lib.api.drivers.driver_lib.'
                        'time') as mock_time:
            mock_time.time.side_effect = [0, 1000, 0, 0, 0, 0, 1000]
            self.assertRaises(driver_exceptions.DriverAgentTimeout,
                              self.driver_lib._recv, mock_socket)

            # Test payload recv timeout
            self.assertRaises(driver_exceptions.DriverAgentTimeout,
                              self.driver_lib._recv, mock_socket)

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

    @mock.patch('octavia_lib.api.drivers.driver_lib.DriverLibrary._send')
    def test_get_resource(self, mock_send):
        fake_resource = 'fake resource'
        fake_id = 'fake id'

        mock_send.side_effect = ['some result',
                                 driver_exceptions.DriverAgentTimeout,
                                 Exception('boom')]

        result = self.driver_lib._get_resource(fake_resource, fake_id)

        data = {constants.OBJECT: fake_resource, constants.ID: fake_id}
        mock_send.assert_called_once_with('/var/run/octavia/get.sock', data)
        self.assertEqual('some result', result)

        # Test with driver_exceptions.DriverAgentTimeout
        self.assertRaises(driver_exceptions.DriverAgentTimeout,
                          self.driver_lib._get_resource,
                          fake_resource, fake_id)

        # Test with random exception
        self.assertRaises(driver_exceptions.DriverError,
                          self.driver_lib._get_resource,
                          fake_resource, fake_id)

    @mock.patch('octavia_lib.api.drivers.driver_lib.DriverLibrary.'
                '_get_resource')
    def _test_get_object(self, get_method, name, mock_from_dict,
                         mock_get_resource):

        mock_get_resource.side_effect = ['some data', None]
        mock_from_dict.return_value = 'object'

        result = get_method('fake id')

        mock_get_resource.assert_called_once_with(name, 'fake id')
        mock_from_dict.assert_called_once_with('some data')
        self.assertEqual('object', result)

        # Test not found
        result = get_method('fake id')

        self.assertIsNone(result)

    @mock.patch('octavia_lib.api.drivers.data_models.LoadBalancer.from_dict')
    def test_get_loadbalancer(self, mock_from_dict):
        self._test_get_object(self.driver_lib.get_loadbalancer,
                              constants.LOADBALANCERS, mock_from_dict)

    @mock.patch('octavia_lib.api.drivers.data_models.Listener.from_dict')
    def test_get_listener(self, mock_from_dict):
        self._test_get_object(self.driver_lib.get_listener,
                              constants.LISTENERS, mock_from_dict)

    @mock.patch('octavia_lib.api.drivers.data_models.Pool.from_dict')
    def test_get_pool(self, mock_from_dict):
        self._test_get_object(self.driver_lib.get_pool,
                              constants.POOLS, mock_from_dict)

    @mock.patch('octavia_lib.api.drivers.data_models.HealthMonitor.from_dict')
    def test_get_healthmonitor(self, mock_from_dict):
        self._test_get_object(self.driver_lib.get_healthmonitor,
                              constants.HEALTHMONITORS, mock_from_dict)

    @mock.patch('octavia_lib.api.drivers.data_models.Member.from_dict')
    def test_get_member(self, mock_from_dict):
        self._test_get_object(self.driver_lib.get_member,
                              constants.MEMBERS, mock_from_dict)

    @mock.patch('octavia_lib.api.drivers.data_models.L7Policy.from_dict')
    def test_get_l7policy(self, mock_from_dict):
        self._test_get_object(self.driver_lib.get_l7policy,
                              constants.L7POLICIES, mock_from_dict)

    @mock.patch('octavia_lib.api.drivers.data_models.L7Rule.from_dict')
    def test_get_l7rule(self, mock_from_dict):
        self._test_get_object(self.driver_lib.get_l7rule,
                              constants.L7RULES, mock_from_dict)
