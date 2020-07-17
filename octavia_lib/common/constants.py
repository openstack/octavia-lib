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

# Codes the driver_agent can return to the octavia-lib driver_lib
DRVR_STATUS_CODE_FAILED = 500
DRVR_STATUS_CODE_OK = 200

STATUS_CODE = 'status_code'
FAULT_STRING = 'fault_string'
STATS_OBJECT = 'stats_object'
STATS_OBJECT_ID = 'stats_object_id'
STATS_RECORD = 'stats_record'
STATUS_OBJECT = 'status_object'
STATUS_OBJECT_ID = 'status_object_id'
STATUS_RECORD = 'status_record'

# Octavia objects
LOADBALANCERS = 'loadbalancers'
LISTENERS = 'listeners'
POOLS = 'pools'
HEALTHMONITORS = 'healthmonitors'
MEMBERS = 'members'
L7POLICIES = 'l7policies'
L7RULES = 'l7rules'
FLAVOR = 'flavor'
OBJECT = 'object'

# ID fields
ID = 'id'

# Octavia statistics fields
ACTIVE_CONNECTIONS = 'active_connections'
BYTES_IN = 'bytes_in'
BYTES_OUT = 'bytes_out'
REQUEST_ERRORS = 'request_errors'
TOTAL_CONNECTIONS = 'total_connections'

# Constants common to all Octavia provider drivers
HEALTH_MONITOR_PING = 'PING'
HEALTH_MONITOR_TCP = 'TCP'
HEALTH_MONITOR_HTTP = 'HTTP'
HEALTH_MONITOR_HTTPS = 'HTTPS'
HEALTH_MONITOR_TLS_HELLO = 'TLS-HELLO'
HEALTH_MONITOR_UDP_CONNECT = 'UDP-CONNECT'
HEALTH_MONITOR_SCTP = 'SCTP'
SUPPORTED_HEALTH_MONITOR_TYPES = (HEALTH_MONITOR_HTTP, HEALTH_MONITOR_HTTPS,
                                  HEALTH_MONITOR_PING, HEALTH_MONITOR_TCP,
                                  HEALTH_MONITOR_TLS_HELLO,
                                  HEALTH_MONITOR_UDP_CONNECT,
                                  HEALTH_MONITOR_SCTP)

HEALTH_MONITOR_HTTP_METHOD_GET = 'GET'
HEALTH_MONITOR_HTTP_METHOD_HEAD = 'HEAD'
HEALTH_MONITOR_HTTP_METHOD_POST = 'POST'
HEALTH_MONITOR_HTTP_METHOD_PUT = 'PUT'
HEALTH_MONITOR_HTTP_METHOD_DELETE = 'DELETE'
HEALTH_MONITOR_HTTP_METHOD_TRACE = 'TRACE'
HEALTH_MONITOR_HTTP_METHOD_OPTIONS = 'OPTIONS'
HEALTH_MONITOR_HTTP_METHOD_CONNECT = 'CONNECT'
HEALTH_MONITOR_HTTP_METHOD_PATCH = 'PATCH'
HEALTH_MONITOR_HTTP_DEFAULT_METHOD = HEALTH_MONITOR_HTTP_METHOD_GET
SUPPORTED_HEALTH_MONITOR_HTTP_METHODS = (
    HEALTH_MONITOR_HTTP_METHOD_GET, HEALTH_MONITOR_HTTP_METHOD_HEAD,
    HEALTH_MONITOR_HTTP_METHOD_POST, HEALTH_MONITOR_HTTP_METHOD_PUT,
    HEALTH_MONITOR_HTTP_METHOD_DELETE, HEALTH_MONITOR_HTTP_METHOD_TRACE,
    HEALTH_MONITOR_HTTP_METHOD_OPTIONS, HEALTH_MONITOR_HTTP_METHOD_CONNECT,
    HEALTH_MONITOR_HTTP_METHOD_PATCH)

L7POLICY_ACTION_REJECT = 'REJECT'
L7POLICY_ACTION_REDIRECT_TO_URL = 'REDIRECT_TO_URL'
L7POLICY_ACTION_REDIRECT_TO_POOL = 'REDIRECT_TO_POOL'
L7POLICY_ACTION_REDIRECT_PREFIX = 'REDIRECT_PREFIX'
SUPPORTED_L7POLICY_ACTIONS = (L7POLICY_ACTION_REJECT,
                              L7POLICY_ACTION_REDIRECT_TO_URL,
                              L7POLICY_ACTION_REDIRECT_TO_POOL,
                              L7POLICY_ACTION_REDIRECT_PREFIX)

L7RULE_COMPARE_TYPE_REGEX = 'REGEX'
L7RULE_COMPARE_TYPE_STARTS_WITH = 'STARTS_WITH'
L7RULE_COMPARE_TYPE_ENDS_WITH = 'ENDS_WITH'
L7RULE_COMPARE_TYPE_CONTAINS = 'CONTAINS'
L7RULE_COMPARE_TYPE_EQUAL_TO = 'EQUAL_TO'
SUPPORTED_L7RULE_COMPARE_TYPES = (L7RULE_COMPARE_TYPE_REGEX,
                                  L7RULE_COMPARE_TYPE_STARTS_WITH,
                                  L7RULE_COMPARE_TYPE_ENDS_WITH,
                                  L7RULE_COMPARE_TYPE_CONTAINS,
                                  L7RULE_COMPARE_TYPE_EQUAL_TO)

L7RULE_TYPE_HOST_NAME = 'HOST_NAME'
L7RULE_TYPE_PATH = 'PATH'
L7RULE_TYPE_FILE_TYPE = 'FILE_TYPE'
L7RULE_TYPE_HEADER = 'HEADER'
L7RULE_TYPE_COOKIE = 'COOKIE'
L7RULE_TYPE_SSL_CONN_HAS_CERT = 'SSL_CONN_HAS_CERT'
L7RULE_TYPE_SSL_VERIFY_RESULT = 'SSL_VERIFY_RESULT'
L7RULE_TYPE_SSL_DN_FIELD = 'SSL_DN_FIELD'
SUPPORTED_L7RULE_TYPES = (L7RULE_TYPE_HOST_NAME, L7RULE_TYPE_PATH,
                          L7RULE_TYPE_FILE_TYPE, L7RULE_TYPE_HEADER,
                          L7RULE_TYPE_COOKIE, L7RULE_TYPE_SSL_CONN_HAS_CERT,
                          L7RULE_TYPE_SSL_VERIFY_RESULT,
                          L7RULE_TYPE_SSL_DN_FIELD)
DISTINGUISHED_NAME_FIELD_REGEX = '^([a-zA-Z][A-Za-z0-9-]*)$'

LB_ALGORITHM_ROUND_ROBIN = 'ROUND_ROBIN'
LB_ALGORITHM_LEAST_CONNECTIONS = 'LEAST_CONNECTIONS'
LB_ALGORITHM_SOURCE_IP = 'SOURCE_IP'
LB_ALGORITHM_SOURCE_IP_PORT = 'SOURCE_IP_PORT'
SUPPORTED_LB_ALGORITHMS = (LB_ALGORITHM_LEAST_CONNECTIONS,
                           LB_ALGORITHM_ROUND_ROBIN,
                           LB_ALGORITHM_SOURCE_IP,
                           LB_ALGORITHM_SOURCE_IP_PORT)

OPERATING_STATUS = 'operating_status'
ONLINE = 'ONLINE'
OFFLINE = 'OFFLINE'
DEGRADED = 'DEGRADED'
ERROR = 'ERROR'
DRAINING = 'DRAINING'
NO_MONITOR = 'NO_MONITOR'
SUPPORTED_OPERATING_STATUSES = (ONLINE, OFFLINE, DEGRADED, ERROR, DRAINING,
                                NO_MONITOR)

PROTOCOL_TCP = 'TCP'
PROTOCOL_UDP = 'UDP'
PROTOCOL_HTTP = 'HTTP'
PROTOCOL_HTTPS = 'HTTPS'
PROTOCOL_TERMINATED_HTTPS = 'TERMINATED_HTTPS'
PROTOCOL_PROXY = 'PROXY'
PROTOCOL_SCTP = 'SCTP'
SUPPORTED_PROTOCOLS = (PROTOCOL_TCP, PROTOCOL_HTTPS, PROTOCOL_HTTP,
                       PROTOCOL_TERMINATED_HTTPS, PROTOCOL_PROXY, PROTOCOL_UDP,
                       PROTOCOL_SCTP)
LISTENER_SUPPORTED_PROTOCOLS = (PROTOCOL_TCP, PROTOCOL_HTTPS, PROTOCOL_HTTP,
                                PROTOCOL_TERMINATED_HTTPS, PROTOCOL_UDP,
                                PROTOCOL_SCTP)
POOL_SUPPORTED_PROTOCOLS = (PROTOCOL_TCP, PROTOCOL_HTTP, PROTOCOL_HTTPS,
                            PROTOCOL_PROXY, PROTOCOL_UDP, PROTOCOL_SCTP)

PROVISIONING_STATUS = 'provisioning_status'
# Amphora has been allocated to a load balancer
AMPHORA_ALLOCATED = 'ALLOCATED'
# Amphora is being built
AMPHORA_BOOTING = 'BOOTING'
# Amphora is ready to be allocated to a load balancer
AMPHORA_READY = 'READY'
ACTIVE = 'ACTIVE'
PENDING_DELETE = 'PENDING_DELETE'
PENDING_UPDATE = 'PENDING_UPDATE'
PENDING_CREATE = 'PENDING_CREATE'
DELETED = 'DELETED'
SUPPORTED_PROVISIONING_STATUSES = (ACTIVE, AMPHORA_ALLOCATED,
                                   AMPHORA_BOOTING, AMPHORA_READY,
                                   PENDING_DELETE, PENDING_CREATE,
                                   PENDING_UPDATE, DELETED, ERROR)

SESSION_PERSISTENCE_SOURCE_IP = 'SOURCE_IP'
SESSION_PERSISTENCE_HTTP_COOKIE = 'HTTP_COOKIE'
SESSION_PERSISTENCE_APP_COOKIE = 'APP_COOKIE'
SUPPORTED_SP_TYPES = (SESSION_PERSISTENCE_SOURCE_IP,
                      SESSION_PERSISTENCE_HTTP_COOKIE,
                      SESSION_PERSISTENCE_APP_COOKIE)

# List of HTTP headers which are supported for insertion
SUPPORTED_HTTP_HEADERS = ['X-Forwarded-For',
                          'X-Forwarded-Port',
                          'X-Forwarded-Proto']

# List of SSL headers for client certificate
SUPPORTED_SSL_HEADERS = ['X-SSL-Client-Verify', 'X-SSL-Client-Has-Cert',
                         'X-SSL-Client-DN', 'X-SSL-Client-CN',
                         'X-SSL-Issuer', 'X-SSL-Client-SHA1',
                         'X-SSL-Client-Not-Before', 'X-SSL-Client-Not-After']

# Client certification authorization options
CLIENT_AUTH_NONE = 'NONE'
CLIENT_AUTH_OPTIONAL = 'OPTIONAL'
CLIENT_AUTH_MANDATORY = 'MANDATORY'
SUPPORTED_CLIENT_AUTH_MODES = [CLIENT_AUTH_NONE, CLIENT_AUTH_OPTIONAL,
                               CLIENT_AUTH_MANDATORY]

# Constants from the provider driver API
ACTION = 'action'
ADDITIONAL_VIPS = 'additional_vips'
ADDRESS = 'address'
ADMIN_STATE_UP = 'admin_state_up'
ALLOWED_CIDRS = 'allowed_cidrs'
AVAILABILITY_ZONE = 'availability_zone'
BACKUP = 'backup'
CA_TLS_CONTAINER_DATA = 'ca_tls_container_data'
CA_TLS_CONTAINER_REF = 'ca_tls_container_ref'
CASCADE = 'cascade'
CERTIFICATE = 'certificate'
CLIENT_AUTHENTICATION = 'client_authentication'
CLIENT_CA_TLS_CONTAINER_DATA = 'client_ca_tls_container_data'
CLIENT_CA_TLS_CONTAINER_REF = 'client_ca_tls_container_ref'
CLIENT_CRL_CONTAINER_DATA = 'client_crl_container_data'
CLIENT_CRL_CONTAINER_REF = 'client_crl_container_ref'
COMPARE_TYPE = 'compare_type'
CONNECTION_LIMIT = 'connection_limit'
COOKIE_NAME = 'cookie_name'
CRL_CONTAINER_DATA = 'crl_container_data'
CRL_CONTAINER_REF = 'crl_container_ref'
DEFAULT_POOL = 'default_pool'
DEFAULT_POOL_ID = 'default_pool_id'
DEFAULT_TLS_CONTAINER_DATA = 'default_tls_container_data'
DEFAULT_TLS_CONTAINER_REF = 'default_tls_container_ref'
DELAY = 'delay'
DESCRIPTION = 'description'
DOMAIN_NAME = 'domain_name'
EXPECTED_CODES = 'expected_codes'
FALL_THRESHOLD = 'fall_threshold'
HEALTHMONITOR = 'healthmonitor'
HEALTHMONITOR_ID = 'healthmonitor_id'
HTTP_METHOD = 'http_method'
HTTP_VERSION = 'http_version'
INSERT_HEADERS = 'insert_headers'
INTERMEDIATES = 'intermediates'
INVERT = 'invert'
KEY = 'key'
L7POLICY_ID = 'l7policy_id'
L7RULE_ID = 'l7rule_id'
LB_ALGORITHM = 'lb_algorithm'
LISTENER_ID = 'listener_id'
LOADBALANCER_ID = 'loadbalancer_id'
MAX_RETRIES = 'max_retries'
MAX_RETRIES_DOWN = 'max_retries_down'
MEMBER_ID = 'member_id'
MONITOR_ADDRESS = 'monitor_address'
MONITOR_PORT = 'monitor_port'
NAME = 'name'
NETWORK_ID = 'network_id'
PASSPHRASE = 'passphrase'
PERSISTENCE_GRANULARITY = 'persistence_granularity'
PERSISTENCE_TIMEOUT = 'persistence_timeout'
POOL_ID = 'pool_id'
POSITION = 'position'
PRIMARY_CN = 'primary_cn'
PRIVATE_KEY = 'private_key'
PROJECT_ID = 'project_id'
PROTOCOL = 'protocol'
PROTOCOL_PORT = 'protocol_port'
REDIRECT_HTTP_CODE = 'redirect_http_code'
REDIRECT_POOL_ID = 'redirect_pool_id'
REDIRECT_PREFIX = 'redirect_prefix'
REDIRECT_URL = 'redirect_url'
RISE_THRESHOLD = 'rise_threshold'
RULES = 'rules'
SESSION_PERSISTENCE = 'session_persistence'
SNI_CONTAINER_DATA = 'sni_container_data'
SNI_CONTAINER_REFS = 'sni_container_refs'
SUBNET_ID = 'subnet_id'
TIMEOUT = 'timeout'
TIMEOUT_CLIENT_DATA = 'timeout_client_data'
TIMEOUT_MEMBER_CONNECT = 'timeout_member_connect'
TIMEOUT_MEMBER_DATA = 'timeout_member_data'
TIMEOUT_TCP_INSPECT = 'timeout_tcp_inspect'
TLS_CIPHERS = 'tls_ciphers'
TLS_CONTAINER_DATA = 'tls_container_data'
TLS_CONTAINER_REF = 'tls_container_ref'
TLS_ENABLED = 'tls_enabled'
TLS_VERSIONS = 'tls_versions'
SSL_VERSION_3 = 'SSLv3'
TLS_VERSION_1 = 'TLSv1'
TLS_VERSION_1_1 = 'TLSv1.1'
TLS_VERSION_1_2 = 'TLSv1.2'
TLS_VERSION_1_3 = 'TLSv1.3'
TYPE = 'type'
URL_PATH = 'url_path'
VALUE = 'value'
VIP_ADDRESS = 'vip_address'
VIP_NETWORK_ID = 'vip_network_id'
VIP_PORT_ID = 'vip_port_id'
VIP_SUBNET_ID = 'vip_subnet_id'
VIP_QOS_POLICY_ID = 'vip_qos_policy_id'
WEIGHT = 'weight'
