# Copyright 2018 Rackspace, US Inc.
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

import socket

from oslo_serialization import jsonutils

from octavia_lib.api.drivers import exceptions as driver_exceptions
from octavia_lib.common import constants

DEFAULT_STATUS_SOCKET = '/var/run/octavia/status.sock'
DEFAULT_STATS_SOCKET = '/var/run/octavia/stats.sock'
SOCKET_TIMEOUT = 5


class DriverLibrary(object):

    def __init__(self, status_socket=DEFAULT_STATUS_SOCKET,
                 stats_socket=DEFAULT_STATS_SOCKET, **kwargs):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(SOCKET_TIMEOUT)
        self.status_socket = status_socket
        self.stats_socket = stats_socket

        super(DriverLibrary, self).__init__(**kwargs)

    def _recv(self):
        size_str = ''
        char = self.sock.recv(1)
        while char != '\n':
            size_str += char
            char = self.sock.recv(1)
        payload_size = int(size_str)
        mv_buffer = memoryview(bytearray(payload_size))
        next_offset = 0
        while payload_size - next_offset > 0:
            recv_size = self.sock.recv_into(mv_buffer[next_offset:],
                                            payload_size - next_offset)
            next_offset += recv_size
        return jsonutils.loads(mv_buffer.tobytes())

    def _send(self, socket_path, data):
        self.sock.connect(socket_path)
        try:
            json_data = jsonutils.dumps(data)
            self.sock.send('%d\n' % len(json_data))
            self.sock.sendall(json_data)
            response = self._recv()
        finally:
            self.sock.close()
        return response

    def update_loadbalancer_status(self, status):
        """Update load balancer status.

        :param status: dictionary defining the provisioning status and
            operating status for load balancer objects, including pools,
            members, listeners, L7 policies, and L7 rules.
            iod (string): ID for the object.
            provisioning_status (string): Provisioning status for the object.
            operating_status (string): Operating status for the object.
        :type status: dict
        :raises: UpdateStatusError
        :returns: None
        """
        try:
            response = self._send(self.status_socket, status)
        except Exception as e:
            raise driver_exceptions.UpdateStatusError(fault_string=str(e))

        if response[constants.STATUS_CODE] != constants.DRVR_STATUS_CODE_OK:
            raise driver_exceptions.UpdateStatusError(
                fault_string=response.pop(constants.FAULT_STRING, None),
                status_object=response.pop(constants.STATUS_OBJECT, None),
                status_object_id=response.pop(constants.STATUS_OBJECT_ID,
                                              None),
                status_record=response.pop(constants.STATUS_RECORD, None))

    def update_listener_statistics(self, statistics):
        """Update listener statistics.

        :param statistics: Statistics for listeners:
              id (string): ID for listener.
              active_connections (int): Number of currently active connections.
              bytes_in (int): Total bytes received.
              bytes_out (int): Total bytes sent.
              request_errors (int): Total requests not fulfilled.
              total_connections (int): The total connections handled.
        :type statistics: dict
        :raises: UpdateStatisticsError
        :returns: None
        """
        try:
            response = self._send(self.stats_socket, statistics)
        except Exception as e:
            raise driver_exceptions.UpdateStatisticsError(
                fault_string=str(e), stats_object=constants.LISTENERS)

        if response[constants.STATUS_CODE] != constants.DRVR_STATUS_CODE_OK:
            raise driver_exceptions.UpdateStatisticsError(
                fault_string=response.pop(constants.FAULT_STRING, None),
                stats_object=response.pop(constants.STATS_OBJECT, None),
                stats_object_id=response.pop(constants.STATS_OBJECT_ID, None),
                stats_record=response.pop(constants.STATS_RECORD, None))
