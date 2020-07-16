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

import os
import socket
import time

from oslo_serialization import jsonutils
import tenacity

from octavia_lib.api.drivers import data_models
from octavia_lib.api.drivers import exceptions as driver_exceptions
from octavia_lib.common import constants

DEFAULT_STATUS_SOCKET = '/var/run/octavia/status.sock'
DEFAULT_STATS_SOCKET = '/var/run/octavia/stats.sock'
DEFAULT_GET_SOCKET = '/var/run/octavia/get.sock'
SOCKET_TIMEOUT = 5
DRIVER_AGENT_TIMEOUT = 30


class DriverLibrary():

    @tenacity.retry(
        stop=tenacity.stop_after_attempt(30), reraise=True,
        wait=tenacity.wait_exponential(multiplier=1, min=1, max=5),
        retry=tenacity.retry_if_exception_type(
            driver_exceptions.DriverAgentNotFound))
    def _check_for_socket_ready(self, socket):
        if not os.path.exists(socket):
            raise driver_exceptions.DriverAgentNotFound(
                fault_string=('Unable to open the driver agent '
                              'socket: {}'.format(socket)))

    def __init__(self, status_socket=DEFAULT_STATUS_SOCKET,
                 stats_socket=DEFAULT_STATS_SOCKET,
                 get_socket=DEFAULT_GET_SOCKET, **kwargs):
        self.status_socket = status_socket
        self.stats_socket = stats_socket
        self.get_socket = get_socket

        self._check_for_socket_ready(status_socket)
        self._check_for_socket_ready(stats_socket)
        self._check_for_socket_ready(get_socket)

        super(DriverLibrary, self).__init__(**kwargs)

    def _recv(self, sock):
        size_str = b''
        char = sock.recv(1)
        begin = time.time()
        while char != b'\n':
            size_str += char
            char = sock.recv(1)
            if time.time() - begin > DRIVER_AGENT_TIMEOUT:
                raise driver_exceptions.DriverAgentTimeout(
                    fault_string=('The driver agent did not respond in {} '
                                  'seconds.'.format(DRIVER_AGENT_TIMEOUT)))
            # Give the CPU a break from polling
            time.sleep(0.01)
        payload_size = int(size_str)
        mv_buffer = memoryview(bytearray(payload_size))
        next_offset = 0
        begin = time.time()
        while payload_size - next_offset > 0:
            recv_size = sock.recv_into(mv_buffer[next_offset:],
                                       payload_size - next_offset)
            next_offset += recv_size
            if time.time() - begin > DRIVER_AGENT_TIMEOUT:
                raise driver_exceptions.DriverAgentTimeout(
                    fault_string=('The driver agent did not respond in {} '
                                  'seconds.'.format(DRIVER_AGENT_TIMEOUT)))
            # Give the CPU a break from polling
            time.sleep(0.01)
        return jsonutils.loads(mv_buffer.tobytes())

    def _send(self, socket_path, data):
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.settimeout(SOCKET_TIMEOUT)
        sock.connect(socket_path)
        try:
            json_data = jsonutils.dump_as_bytes(data)
            len_str = '{}\n'.format(len(json_data)).encode('utf-8')
            sock.send(len_str)
            sock.sendall(json_data)
            response = self._recv(sock)
        finally:
            sock.close()
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

    def _get_resource(self, resource, id):
        try:
            return self._send(self.get_socket, {constants.OBJECT: resource,
                                                constants.ID: id})
        except driver_exceptions.DriverAgentTimeout:
            raise
        except Exception:
            raise driver_exceptions.DriverError()

    def get_loadbalancer(self, loadbalancer_id):
        """Get a load balancer object.

        :param loadbalancer_id: The load balancer ID to lookup.
        :type loadbalancer_id: UUID string
        :raises DriverAgentTimeout: The driver agent did not respond
          inside the timeout.
        :raises DriverError: An unexpected error occurred.
        :returns: A LoadBalancer object or None if not found.
        """
        data = self._get_resource(constants.LOADBALANCERS, loadbalancer_id)
        if data:
            return data_models.LoadBalancer.from_dict(data)
        return None

    def get_listener(self, listener_id):
        """Get a listener object.

        :param listener_id: The listener ID to lookup.
        :type listener_id: UUID string
        :raises DriverAgentTimeout: The driver agent did not respond
          inside the timeout.
        :raises DriverError: An unexpected error occurred.
        :returns: A Listener object or None if not found.
        """
        data = self._get_resource(constants.LISTENERS, listener_id)
        if data:
            return data_models.Listener.from_dict(data)
        return None

    def get_pool(self, pool_id):
        """Get a pool object.

        :param pool_id: The pool ID to lookup.
        :type pool_id: UUID string
        :raises DriverAgentTimeout: The driver agent did not respond
          inside the timeout.
        :raises DriverError: An unexpected error occurred.
        :returns: A Pool object or None if not found.
        """
        data = self._get_resource(constants.POOLS, pool_id)
        if data:
            return data_models.Pool.from_dict(data)
        return None

    def get_healthmonitor(self, healthmonitor_id):
        """Get a health monitor object.

        :param healthmonitor_id: The health monitor ID to lookup.
        :type healthmonitor_id: UUID string
        :raises DriverAgentTimeout: The driver agent did not respond
          inside the timeout.
        :raises DriverError: An unexpected error occurred.
        :returns: A HealthMonitor object or None if not found.
        """
        data = self._get_resource(constants.HEALTHMONITORS, healthmonitor_id)
        if data:
            return data_models.HealthMonitor.from_dict(data)
        return None

    def get_member(self, member_id):
        """Get a member object.

        :param member_id: The member ID to lookup.
        :type member_id: UUID string
        :raises DriverAgentTimeout: The driver agent did not respond
          inside the timeout.
        :raises DriverError: An unexpected error occurred.
        :returns: A Member object or None if not found.
        """
        data = self._get_resource(constants.MEMBERS, member_id)
        if data:
            return data_models.Member.from_dict(data)
        return None

    def get_l7policy(self, l7policy_id):
        """Get a L7 policy object.

        :param l7policy_id: The L7 policy ID to lookup.
        :type l7policy_id: UUID string
        :raises DriverAgentTimeout: The driver agent did not respond
          inside the timeout.
        :raises DriverError: An unexpected error occurred.
        :returns: A L7Policy object or None if not found.
        """
        data = self._get_resource(constants.L7POLICIES, l7policy_id)
        if data:
            return data_models.L7Policy.from_dict(data)
        return None

    def get_l7rule(self, l7rule_id):
        """Get a L7 rule object.

        :param l7rule_id: The L7 rule ID to lookup.
        :type l7rule_id: UUID string
        :raises DriverAgentTimeout: The driver agent did not respond
          inside the timeout.
        :raises DriverError: An unexpected error occurred.
        :returns: A L7Rule object or None if not found.
        """
        data = self._get_resource(constants.L7RULES, l7rule_id)
        if data:
            return data_models.L7Rule.from_dict(data)
        return None
