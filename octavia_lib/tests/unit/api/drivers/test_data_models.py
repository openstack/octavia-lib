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

from copy import deepcopy

from oslo_utils import uuidutils

from octavia_lib.api.drivers import data_models
from octavia_lib.common import constants
from octavia_lib.tests.unit import base


class TestProviderDataModels(base.TestCase):

    def setUp(self):
        super(TestProviderDataModels, self).setUp()

        self.loadbalancer_id = uuidutils.generate_uuid()
        self.project_id = uuidutils.generate_uuid()
        self.vip_address = '192.0.2.83'
        self.vip_network_id = uuidutils.generate_uuid()
        self.vip_port_id = uuidutils.generate_uuid()
        self.vip_subnet_id = uuidutils.generate_uuid()
        self.listener_id = uuidutils.generate_uuid()
        self.vip_qos_policy_id = uuidutils.generate_uuid()
        self.default_tls_container_ref = uuidutils.generate_uuid()
        self.sni_container_ref_1 = uuidutils.generate_uuid()
        self.sni_container_ref_2 = uuidutils.generate_uuid()
        self.pool_id = uuidutils.generate_uuid()
        self.session_persistence = {"cookie_name": "sugar",
                                    "type": "APP_COOKIE"}
        self.member_id = uuidutils.generate_uuid()
        self.mem_subnet_id = uuidutils.generate_uuid()
        self.healthmonitor_id = uuidutils.generate_uuid()
        self.l7policy_id = uuidutils.generate_uuid()
        self.l7rule_id = uuidutils.generate_uuid()
        self.availability_zone = uuidutils.generate_uuid()

        self.ref_l7rule = data_models.L7Rule(
            admin_state_up=True,
            compare_type='STARTS_WITH',
            invert=True,
            key='cookie',
            l7policy_id=self.l7policy_id,
            l7rule_id=self.l7rule_id,
            type='COOKIE',
            project_id=self.project_id,
            value='chocolate')

        self.ref_l7policy = data_models.L7Policy(
            action='REJECT',
            admin_state_up=False,
            description='A L7 Policy',
            l7policy_id=self.l7policy_id,
            listener_id=self.listener_id,
            name='l7policy',
            position=1,
            redirect_pool_id=self.pool_id,
            redirect_url='/test',
            rules=[self.ref_l7rule],
            project_id=self.project_id,
            redirect_prefix='http://example.com',
            redirect_http_code=301)

        self.ref_listener = data_models.Listener(
            admin_state_up=True,
            connection_limit=5000,
            default_pool=None,
            default_pool_id=None,
            default_tls_container_data='default_cert_data',
            default_tls_container_ref=self.default_tls_container_ref,
            description=data_models.Unset,
            insert_headers={'X-Forwarded-For': 'true'},
            l7policies=[self.ref_l7policy],
            listener_id=self.listener_id,
            loadbalancer_id=self.loadbalancer_id,
            name='super_listener',
            project_id=self.project_id,
            protocol='avian',
            protocol_port=42,
            sni_container_data=['sni_cert_data_1', 'sni_cert_data_2'],
            sni_container_refs=[self.sni_container_ref_1,
                                self.sni_container_ref_2],
            timeout_client_data=3,
            timeout_member_connect=4,
            timeout_member_data=5,
            timeout_tcp_inspect=6,
            client_authentication=None,
            client_ca_tls_container_data=None,
            client_ca_tls_container_ref=None,
            client_crl_container_data=None,
            client_crl_container_ref=None,
            allowed_cidrs=None,
            tls_versions=[constants.SSL_VERSION_3,
                          constants.TLS_VERSION_1,
                          constants.TLS_VERSION_1_1,
                          constants.TLS_VERSION_1_2,
                          constants.TLS_VERSION_1_3],
            tls_ciphers=None)

        self.ref_lb = data_models.LoadBalancer(
            admin_state_up=False,
            description='One great load balancer',
            flavor={'cake': 'chocolate'},
            listeners=[self.ref_listener],
            loadbalancer_id=self.loadbalancer_id,
            name='favorite_lb',
            project_id=self.project_id,
            vip_address=self.vip_address,
            vip_network_id=self.vip_network_id,
            vip_port_id=self.vip_port_id,
            vip_subnet_id=self.vip_subnet_id,
            vip_qos_policy_id=self.vip_qos_policy_id,
            availability_zone=self.availability_zone)

        self.ref_vip = data_models.VIP(
            vip_address=self.vip_address,
            vip_network_id=self.vip_network_id,
            vip_port_id=self.vip_port_id,
            vip_subnet_id=self.vip_subnet_id,
            vip_qos_policy_id=self.vip_qos_policy_id)

        self.ref_member = data_models.Member(
            address='192.0.2.10',
            admin_state_up=True,
            member_id=self.member_id,
            monitor_address='192.0.2.11',
            monitor_port=8888,
            name='member',
            pool_id=self.pool_id,
            project_id=self.project_id,
            protocol_port=80,
            subnet_id=self.mem_subnet_id,
            weight=1,
            backup=False)

        self.ref_healthmonitor = data_models.HealthMonitor(
            admin_state_up=False,
            delay=1,
            expected_codes='200,202',
            healthmonitor_id=self.healthmonitor_id,
            http_method='GET',
            max_retries=2,
            max_retries_down=3,
            name='member',
            pool_id=self.pool_id,
            project_id=self.project_id,
            timeout=4,
            type='HTTP',
            url_path='/test',
            http_version=1.1,
            domain_name='testdomainname.com')

        self.ref_pool = data_models.Pool(
            admin_state_up=True,
            description='A pool',
            healthmonitor=None,
            lb_algorithm='fast',
            loadbalancer_id=self.loadbalancer_id,
            members=[self.ref_member],
            name='pool',
            pool_id=self.pool_id,
            project_id=self.project_id,
            listener_id=self.listener_id,
            protocol='avian',
            session_persistence=self.session_persistence,
            tls_versions=[constants.SSL_VERSION_3,
                          constants.TLS_VERSION_1,
                          constants.TLS_VERSION_1_1,
                          constants.TLS_VERSION_1_2,
                          constants.TLS_VERSION_1_3],
            tls_ciphers=None)

        self.ref_l7rule_dict = {'admin_state_up': True,
                                'compare_type': 'STARTS_WITH',
                                'invert': True,
                                'key': 'cookie',
                                'l7policy_id': self.l7policy_id,
                                'l7rule_id': self.l7rule_id,
                                'type': 'COOKIE',
                                'project_id': self.project_id,
                                'value': 'chocolate'}

        self.ref_l7policy_dict = {'action': 'REJECT',
                                  'admin_state_up': False,
                                  'description': 'A L7 Policy',
                                  'l7policy_id': self.l7policy_id,
                                  'listener_id': self.listener_id,
                                  'name': 'l7policy',
                                  'position': 1,
                                  'project_id': self.project_id,
                                  'redirect_pool_id': self.pool_id,
                                  'redirect_url': '/test',
                                  'rules': [self.ref_l7rule_dict],
                                  'redirect_prefix': 'http://example.com',
                                  'redirect_http_code': 301}

        self.ref_lb_dict = {'project_id': self.project_id,
                            'flavor': {'cake': 'chocolate'},
                            'vip_network_id': self.vip_network_id,
                            'admin_state_up': False,
                            'loadbalancer_id': self.loadbalancer_id,
                            'vip_port_id': self.vip_port_id,
                            'vip_address': self.vip_address,
                            'description': 'One great load balancer',
                            'vip_subnet_id': self.vip_subnet_id,
                            'name': 'favorite_lb',
                            'vip_qos_policy_id': self.vip_qos_policy_id,
                            'availability_zone': self.availability_zone}

        self.ref_listener_dict = {
            'admin_state_up': True,
            'connection_limit': 5000,
            'default_pool': None,
            'default_pool_id': None,
            'default_tls_container_data': 'default_cert_data',
            'default_tls_container_ref': self.default_tls_container_ref,
            'description': None,
            'insert_headers': {'X-Forwarded-For': 'true'},
            'listener_id': self.listener_id,
            'l7policies': [self.ref_l7policy_dict],
            'loadbalancer_id': self.loadbalancer_id,
            'name': 'super_listener',
            'project_id': self.project_id,
            'protocol': 'avian',
            'protocol_port': 42,
            'sni_container_data': ['sni_cert_data_1', 'sni_cert_data_2'],
            'sni_container_refs': [self.sni_container_ref_1,
                                   self.sni_container_ref_2],
            'timeout_client_data': 3,
            'timeout_member_connect': 4,
            'timeout_member_data': 5,
            'timeout_tcp_inspect': 6,
            'client_authentication': None,
            'client_ca_tls_container_data': None,
            'client_ca_tls_container_ref': None,
            'client_crl_container_data': None,
            'client_crl_container_ref': None,
            'allowed_cidrs': None,
            'tls_versions': [constants.SSL_VERSION_3,
                             constants.TLS_VERSION_1,
                             constants.TLS_VERSION_1_1,
                             constants.TLS_VERSION_1_2,
                             constants.TLS_VERSION_1_3],
            'tls_ciphers': None}

        self.ref_lb_dict_with_listener = {
            'admin_state_up': False,
            'description': 'One great load balancer',
            'flavor': {'cake': 'chocolate'},
            'listeners': [self.ref_listener_dict],
            'loadbalancer_id': self.loadbalancer_id,
            'name': 'favorite_lb',
            'project_id': self.project_id,
            'vip_address': self.vip_address,
            'vip_network_id': self.vip_network_id,
            'vip_port_id': self.vip_port_id,
            'vip_subnet_id': self.vip_subnet_id,
            'vip_qos_policy_id': self.vip_qos_policy_id,
            'availability_zone': self.availability_zone}

        self.ref_vip_dict = {
            'vip_address': self.vip_address,
            'vip_network_id': self.vip_network_id,
            'vip_port_id': self.vip_port_id,
            'vip_subnet_id': self.vip_subnet_id,
            'vip_qos_policy_id': self.vip_qos_policy_id}

        self.ref_member_dict = {
            'address': '192.0.2.10',
            'admin_state_up': True,
            'member_id': self.member_id,
            'monitor_address': '192.0.2.11',
            'monitor_port': 8888,
            'name': 'member',
            'pool_id': self.pool_id,
            'project_id': self.project_id,
            'protocol_port': 80,
            'subnet_id': self.mem_subnet_id,
            'weight': 1,
            'backup': False}

        self.ref_healthmonitor_dict = {
            'admin_state_up': False,
            'delay': 1,
            'expected_codes': '200,202',
            'healthmonitor_id': self.healthmonitor_id,
            'http_method': 'GET',
            'max_retries': 2,
            'max_retries_down': 3,
            'name': 'member',
            'pool_id': self.pool_id,
            'project_id': self.project_id,
            'timeout': 4,
            'type': 'HTTP',
            'url_path': '/test',
            'http_version': 1.1,
            'domain_name': 'testdomainname.com'}

        self.ref_pool_dict = {
            'admin_state_up': True,
            'description': 'A pool',
            'healthmonitor': self.ref_healthmonitor_dict,
            'lb_algorithm': 'fast',
            'loadbalancer_id': self.loadbalancer_id,
            'members': [self.ref_member_dict],
            'name': 'pool',
            'pool_id': self.pool_id,
            'project_id': self.project_id,
            'listener_id': self.listener_id,
            'protocol': 'avian',
            'session_persistence': self.session_persistence,
            'tls_versions': [constants.SSL_VERSION_3,
                             constants.TLS_VERSION_1,
                             constants.TLS_VERSION_1_1,
                             constants.TLS_VERSION_1_2,
                             constants.TLS_VERSION_1_3],
            'tls_ciphers': None}

    def test_equality(self):
        second_ref_lb = deepcopy(self.ref_lb)

        self.assertEqual(self.ref_lb, second_ref_lb)

        second_ref_lb.admin_state_up = True

        self.assertNotEqual(self.ref_lb, second_ref_lb)

        self.assertNotEqual(self.ref_lb, self.loadbalancer_id)

    def test_inequality(self):
        second_ref_lb = deepcopy(self.ref_lb)

        self.assertEqual(self.ref_lb, second_ref_lb)

        second_ref_lb.admin_state_up = True

        self.assertNotEqual(self.ref_lb, second_ref_lb)

        self.assertNotEqual(self.ref_lb, self.loadbalancer_id)

    def test_to_dict(self):
        ref_lb_converted_to_dict = self.ref_lb.to_dict()
        ref_listener_converted_to_dict = self.ref_listener.to_dict()
        ref_pool_converted_to_dict = self.ref_pool.to_dict()
        ref_member_converted_to_dict = self.ref_member.to_dict()
        ref_healthmon_converted_to_dict = self.ref_healthmonitor.to_dict()
        ref_l7policy_converted_to_dict = self.ref_l7policy.to_dict()
        ref_l7rule_converted_to_dict = self.ref_l7rule.to_dict()
        ref_vip_converted_to_dict = self.ref_vip.to_dict()

        # This test does not recurse, so remove items for the reference
        # that should not be rendered
        ref_list_dict = deepcopy(self.ref_listener_dict)
        ref_list_dict.pop('l7policies', None)
        ref_list_dict.pop('sni_container_data', None)
        ref_list_dict.pop('sni_container_refs', None)
        ref_list_dict.pop('tls_versions', None)
        ref_pool_dict = deepcopy(self.ref_pool_dict)
        ref_pool_dict['healthmonitor'] = None
        ref_pool_dict.pop('members', None)
        ref_pool_dict.pop('tls_versions', None)
        ref_l7policy_dict = deepcopy(self.ref_l7policy_dict)
        ref_l7policy_dict.pop('rules', None)

        # This test does not render unsets, so remove those from the reference
        ref_list_dict.pop('description', None)

        self.assertEqual(self.ref_lb_dict, ref_lb_converted_to_dict)
        self.assertEqual(ref_list_dict, ref_listener_converted_to_dict)
        self.assertEqual(ref_pool_dict, ref_pool_converted_to_dict)
        self.assertEqual(self.ref_member_dict, ref_member_converted_to_dict)
        self.assertEqual(self.ref_healthmonitor_dict,
                         ref_healthmon_converted_to_dict)
        self.assertEqual(ref_l7policy_dict, ref_l7policy_converted_to_dict)
        self.assertEqual(self.ref_l7rule_dict, ref_l7rule_converted_to_dict)
        self.assertEqual(self.ref_vip_dict, ref_vip_converted_to_dict)

    def test_to_dict_private_attrs(self):
        private_dict = {'_test': 'foo'}
        ref_lb_converted_to_dict = self.ref_lb.to_dict(**private_dict)

        self.assertEqual(self.ref_lb_dict, ref_lb_converted_to_dict)

    def test_to_dict_partial(self):
        ref_lb = data_models.LoadBalancer(loadbalancer_id=self.loadbalancer_id)
        ref_lb_dict = {'loadbalancer_id': self.loadbalancer_id}
        ref_lb_converted_to_dict = ref_lb.to_dict()

        self.assertEqual(ref_lb_dict, ref_lb_converted_to_dict)

    def test_to_dict_render_unsets(self):

        ref_lb_converted_to_dict = self.ref_lb.to_dict(render_unsets=True)

        new_ref_lib_dict = deepcopy(self.ref_lb_dict)
        new_ref_lib_dict['pools'] = None
        new_ref_lib_dict['listeners'] = None
        new_ref_lib_dict['additional_vips'] = None

        self.assertEqual(new_ref_lib_dict, ref_lb_converted_to_dict)

    def test_to_dict_recursive(self):
        # Render with unsets is not set, so remove the Unset description
        ref_lb_dict_with_listener = deepcopy(self.ref_lb_dict_with_listener)
        ref_lb_dict_with_listener['listeners'][0].pop('description', None)

        ref_lb_converted_to_dict = self.ref_lb.to_dict(recurse=True)

        self.assertEqual(ref_lb_dict_with_listener,
                         ref_lb_converted_to_dict)

    def test_to_dict_recursive_partial(self):
        ref_lb = data_models.LoadBalancer(
            loadbalancer_id=self.loadbalancer_id,
            listeners=[self.ref_listener])

        ref_lb_dict_with_listener = {
            'loadbalancer_id': self.loadbalancer_id,
            'listeners': [self.ref_listener_dict]}

        # Render with unsets is not set, so remove the Unset description
        ref_lb_dict_with_listener = deepcopy(ref_lb_dict_with_listener)
        ref_lb_dict_with_listener['listeners'][0].pop('description', None)

        ref_lb_converted_to_dict = ref_lb.to_dict(recurse=True)

        self.assertEqual(ref_lb_dict_with_listener, ref_lb_converted_to_dict)

    def test_to_dict_recursive_render_unset(self):
        ref_lb = data_models.LoadBalancer(
            admin_state_up=False,
            description='One great load balancer',
            flavor={'cake': 'chocolate'},
            listeners=[self.ref_listener],
            loadbalancer_id=self.loadbalancer_id,
            project_id=self.project_id,
            vip_address=self.vip_address,
            vip_network_id=self.vip_network_id,
            vip_port_id=self.vip_port_id,
            vip_subnet_id=self.vip_subnet_id,
            vip_qos_policy_id=self.vip_qos_policy_id,
            availability_zone=self.availability_zone)

        ref_lb_dict_with_listener = deepcopy(self.ref_lb_dict_with_listener)
        ref_lb_dict_with_listener['pools'] = None
        ref_lb_dict_with_listener['name'] = None
        ref_lb_dict_with_listener['additional_vips'] = None

        ref_lb_converted_to_dict = ref_lb.to_dict(recurse=True,
                                                  render_unsets=True)

        self.assertEqual(ref_lb_dict_with_listener,
                         ref_lb_converted_to_dict)

    def test_from_dict(self):
        lb_object = data_models.LoadBalancer.from_dict(self.ref_lb_dict)

        self.assertEqual(self.ref_lb, lb_object)

    def test_unset_bool(self):
        self.assertFalse(data_models.Unset)

    def test_unset_repr(self):
        self.assertEqual('Unset', repr(data_models.Unset))
