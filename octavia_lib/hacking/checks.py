# Copyright (c) 2014 OpenStack Foundation.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""
Guidelines for writing new hacking checks

 - Use only for Octavia specific tests. OpenStack general tests
   should be submitted to the common 'hacking' module.
 - Pick numbers in the range O3xx. Find the current test with
   the highest allocated number and then pick the next value.
 - Keep the test method code in the source file ordered based
   on the O3xx value.
 - List the new rule in the top level HACKING.rst file
 - Add test cases for each new rule to
   octavia_lib/tests/unit/test_hacking.py

"""


import re

from hacking import core

_all_log_levels = {'critical', 'error', 'exception', 'info', 'warning'}
_all_hints = {'_LC', '_LE', '_LI', '_', '_LW'}

_log_translation_hint = re.compile(
    r".*LOG\.(%(levels)s)\(\s*(%(hints)s)\(" % {
        'levels': '|'.join(_all_log_levels),
        'hints': '|'.join(_all_hints),
    })

assert_trueinst_re = re.compile(
    r"(.)*assertTrue\(isinstance\((\w|\.|\'|\"|\[|\])+, "
    r"(\w|\.|\'|\"|\[|\])+\)\)")
assert_equal_in_end_with_true_or_false_re = re.compile(
    r"assertEqual\((\w|[][.'\"])+ in (\w|[][.'\", ])+, (True|False)\)")
assert_equal_in_start_with_true_or_false_re = re.compile(
    r"assertEqual\((True|False), (\w|[][.'\"])+ in (\w|[][.'\", ])+\)")
assert_equal_with_true_re = re.compile(
    r"assertEqual\(True,")
assert_equal_with_false_re = re.compile(
    r"assertEqual\(False,")
mutable_default_args = re.compile(r"^\s*def .+\((.+=\{\}|.+=\[\])")
assert_equal_end_with_none_re = re.compile(r"(.)*assertEqual\(.+, None\)")
assert_equal_start_with_none_re = re.compile(r".*assertEqual\(None, .+\)")
assert_not_equal_end_with_none_re = re.compile(
    r"(.)*assertNotEqual\(.+, None\)")
assert_not_equal_start_with_none_re = re.compile(
    r"(.)*assertNotEqual\(None, .+\)")
revert_must_have_kwargs_re = re.compile(
    r'[ ]*def revert\(.+,[ ](?!\*\*kwargs)\w+\):')
untranslated_exception_re = re.compile(r"raise (?:\w*)\((.*)\)")
no_basestring_re = re.compile(r"\bbasestring\b")
no_eventlet_re = re.compile(r'(import|from)\s+[(]?eventlet')
no_line_continuation_backslash_re = re.compile(r'.*(\\)\n')
no_logging_re = re.compile(r'(import|from)\s+[(]?logging')
namespace_imports_dot = re.compile(r"import[\s]+([\w]+)[.][^\s]+")
namespace_imports_from_dot = re.compile(r"from[\s]+([\w]+)[.]")
namespace_imports_from_root = re.compile(r"from[\s]+([\w]+)[\s]+import[\s]+")


def _check_imports(regex, submatch, logical_line):
    m = re.match(regex, logical_line)
    if m and m.group(1) == submatch:
        return True
    return False


def _check_namespace_imports(failure_code, namespace, new_ns, logical_line,
                             message_override=None):
    if message_override is not None:
        msg_o = "%s: %s" % (failure_code, message_override)
    else:
        msg_o = None

    if _check_imports(namespace_imports_from_dot, namespace, logical_line):
        msg = ("%s: '%s' must be used instead of '%s'.") % (
            failure_code,
            logical_line.replace('%s.' % namespace, new_ns),
            logical_line)
        return (0, msg_o or msg)
    if _check_imports(namespace_imports_from_root, namespace, logical_line):
        msg = ("%s: '%s' must be used instead of '%s'.") % (
            failure_code,
            logical_line.replace(
                'from %s import ' % namespace, 'import %s' % new_ns),
            logical_line)
        return (0, msg_o or msg)
    if _check_imports(namespace_imports_dot, namespace, logical_line):
        msg = ("%s: '%s' must be used instead of '%s'.") % (
            failure_code,
            logical_line.replace('import', 'from').replace('.', ' import '),
            logical_line)
        return (0, msg_o or msg)
    return None


def _translation_checks_not_enforced(filename):
    # Do not do these validations on tests
    return any(pat in filename for pat in ["/tests/", "rally-jobs/plugins/"])


@core.flake8ext
def assert_true_instance(logical_line):
    """Check for assertTrue(isinstance(a, b)) sentences

    O316
    """
    if assert_trueinst_re.match(logical_line):
        yield (0, "O316: assertTrue(isinstance(a, b)) sentences not allowed. "
               "Use assertIsInstance instead.")


@core.flake8ext
def assert_equal_or_not_none(logical_line):
    """Check for assertEqual(A, None) or assertEqual(None, A) sentences,

    assertNotEqual(A, None) or assertNotEqual(None, A) sentences

    O318
    """
    msg = ("O318: assertEqual/assertNotEqual(A, None) or "
           "assertEqual/assertNotEqual(None, A) sentences not allowed")
    res = (assert_equal_start_with_none_re.match(logical_line) or
           assert_equal_end_with_none_re.match(logical_line) or
           assert_not_equal_start_with_none_re.match(logical_line) or
           assert_not_equal_end_with_none_re.match(logical_line))
    if res:
        yield (0, msg)


@core.flake8ext
def assert_equal_true_or_false(logical_line):
    """Check for assertEqual(True, A) or assertEqual(False, A) sentences

    O323
    """
    res = (assert_equal_with_true_re.search(logical_line) or
           assert_equal_with_false_re.search(logical_line))
    if res:
        yield (0, "O323: assertEqual(True, A) or assertEqual(False, A) "
               "sentences not allowed")


@core.flake8ext
def no_mutable_default_args(logical_line):
    msg = "O324: Method's default argument shouldn't be mutable!"
    if mutable_default_args.match(logical_line):
        yield (0, msg)


@core.flake8ext
def assert_equal_in(logical_line):
    """Check for assertEqual(A in B, True), assertEqual(True, A in B),

    assertEqual(A in B, False) or assertEqual(False, A in B) sentences

    O338
    """
    res = (assert_equal_in_start_with_true_or_false_re.search(logical_line) or
           assert_equal_in_end_with_true_or_false_re.search(logical_line))
    if res:
        yield (0, "O338: Use assertIn/NotIn(A, B) rather than "
               "assertEqual(A in B, True/False) when checking collection "
               "contents.")


@core.flake8ext
def no_log_warn(logical_line):
    """Disallow 'LOG.warn('

    O339
    """
    if logical_line.startswith('LOG.warn('):
        yield(0, "O339:Use LOG.warning() rather than LOG.warn()")


@core.flake8ext
def no_translate_logs(logical_line, filename):
    """O341 - Don't translate logs.

    Check for 'LOG.*(_(' and 'LOG.*(_Lx('

    Translators don't provide translations for log messages, and operators
    asked not to translate them.

    * This check assumes that 'LOG' is a logger.

    :param logical_line: The logical line to check.
    :param filename: The file name where the logical line exists.
    :returns: None if the logical line passes the check, otherwise a tuple
              is yielded that contains the offending index in logical line
              and a message describe the check validation failure.
    """
    if _translation_checks_not_enforced(filename):
        return

    msg = "O341: Log messages should not be translated!"
    match = _log_translation_hint.match(logical_line)
    if match:
        yield (logical_line.index(match.group()), msg)


@core.flake8ext
def check_raised_localized_exceptions(logical_line, filename):
    """O342 - Untranslated exception message.

    :param logical_line: The logical line to check.
    :param filename: The file name where the logical line exists.
    :returns: None if the logical line passes the check, otherwise a tuple
              is yielded that contains the offending index in logical line
              and a message describe the check validation failure.
    """
    if _translation_checks_not_enforced(filename):
        return

    logical_line = logical_line.strip()
    raised_search = untranslated_exception_re.match(logical_line)
    if raised_search:
        exception_msg = raised_search.groups()[0]
        if exception_msg.startswith("\"") or exception_msg.startswith("\'"):
            msg = "O342: Untranslated exception message."
            yield (logical_line.index(exception_msg), msg)


@core.flake8ext
def check_no_basestring(logical_line):
    """O343 - basestring is not Python3-compatible.

    :param logical_line: The logical line to check.
    :returns: None if the logical line passes the check, otherwise a tuple
              is yielded that contains the offending index in logical line
              and a message describe the check validation failure.
    """
    if no_basestring_re.search(logical_line):
        msg = ("O343: basestring is not Python3-compatible, use "
               "str instead.")
        yield(0, msg)


@core.flake8ext
def check_no_eventlet_imports(logical_line):
    """O345 - Usage of Python eventlet module not allowed.

    :param logical_line: The logical line to check.
    :returns: None if the logical line passes the check, otherwise a tuple
              is yielded that contains the offending index in logical line
              and a message describe the check validation failure.
    """
    if no_eventlet_re.match(logical_line):
        msg = 'O345 Usage of Python eventlet module not allowed'
        yield logical_line.index('eventlet'), msg


@core.flake8ext
def check_line_continuation_no_backslash(logical_line, tokens):
    """O346 - Don't use backslashes for line continuation.

    :param logical_line: The logical line to check. Not actually used.
    :param tokens: List of tokens to check.
    :returns: None if the tokens don't contain any issues, otherwise a tuple
              is yielded that contains the offending index in the logical
              line and a message describe the check validation failure.
    """
    backslash = None
    for token_type, text, start, end, orig_line in tokens:
        m = no_line_continuation_backslash_re.match(orig_line)
        if m:
            backslash = (start[0], m.start(1))
            break

    if backslash is not None:
        msg = 'O346 Backslash line continuations not allowed'
        yield backslash, msg


@core.flake8ext
def check_no_logging_imports(logical_line):
    """O348 - Usage of Python logging module not allowed.

    :param logical_line: The logical line to check.
    :returns: None if the logical line passes the check, otherwise a tuple
              is yielded that contains the offending index in logical line
              and a message describe the check validation failure.
    """
    if no_logging_re.match(logical_line):
        msg = 'O348 Usage of Python logging module not allowed, use oslo_log'
        yield logical_line.index('logging'), msg


@core.flake8ext
def check_no_octavia_namespace_imports(logical_line):
    """O501 - Direct octavia imports not allowed.

    :param logical_line: The logical line to check.
    :returns: None if the logical line passes the check, otherwise a tuple
        is yielded that contains the offending index in logical line and a
        message describe the check validation failure.
    """
    x = _check_namespace_imports(
        'O501', 'octavia', 'octavia_lib.', logical_line,
        message_override="O501 Direct octavia imports not allowed")
    if x is not None:
        yield x
