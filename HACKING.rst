Octavia-lib Style Commandments
==============================
This project was ultimately spawned from work done on the Neutron project.
As such, we tend to follow Neutron conventions regarding coding style.

- We follow the OpenStack Style Commandments:
  https://docs.openstack.org/hacking/latest

-- Read the OpenStack Octavia style guide:
-  https://docs.openstack.org/octavia/latest/contributor/HACKING.html

Octavia Specific Commandments
-----------------------------
- [O316] Change assertTrue(isinstance(A, B)) by optimal assert like
  assertIsInstance(A, B).
- [O318] Change assert(Not)Equal(A, None) or assert(Not)Equal(None, A)
  by optimal assert like assertIs(Not)None(A).
- [O319] Validate that debug level logs are not translated.
- [O321] Validate that jsonutils module is used instead of json
- [O322] Don't use author tags
- [O323] Change assertEqual(True, A) or assertEqual(False, A) to the more
  specific assertTrue(A) or assertFalse(A)
- [O324] Method's default argument shouldn't be mutable
- [O338] Change assertEqual(A in B, True), assertEqual(True, A in B),
  assertEqual(A in B, False) or assertEqual(False, A in B) to the more
  specific assertIn/NotIn(A, B)
- [O339] LOG.warn() is not allowed. Use LOG.warning()
- [O340] Don't use xrange()
- [O341] Don't translate logs.
- [0342] Exception messages should be translated
- [O343] Python 3: do not use basestring.
- [O344] Python 3: do not use dict.iteritems.
- [O345] Usage of Python eventlet module not allowed
- [O346] Don't use backslashes for line continuation.
- [O501] Direct octavia imports not allowed.

Creating Unit Tests
-------------------
For every new feature, unit tests should be created that both test and
(implicitly) document the usage of said feature. If submitting a patch for a
bug that had no unit test, a new passing unit test should be added. If a
submitted bug fix does have a unit test, be sure to add a new one that fails
without the patch and passes with the patch.

Everything is python
--------------------
Although OpenStack apparently allows either python or C++ code, at this time
we don't envision needing anything other than python (and standard, supported
open source modules) for anything we intend to do in Octavia-lib.

Idempotency
-----------
With as much as is going on inside Octavia-lib, its likely that certain
messages and commands will be repeatedly processed. It's important that this
doesn't break the functionality of the load balancing service. Therefore, as
much as possible, algorithms and interfaces should be made as idempotent as
possible.

Avoid premature optimization
----------------------------
Understand that being "high performance" is often not the same thing as being
"scalable." First get the thing to work in an intelligent way. Only worry about
making it fast if speed becomes an issue.

Don't repeat yourself
---------------------
Octavia-lib strives to follow DRY principles. There should be one source of
truth, and repetition of code should be avoided.

Security is not an afterthought
-------------------------------
The load balancer is often both the most visible public interface to a given
user application, but load balancers themselves often have direct access to
sensitive components and data within the application environment. Security bugs
will happen, but in general we should not approve designs which have known
significant security problems, or which could be made more secure by better
design.

Octavia-lib should follow industry standards
--------------------------------------------
By "industry standards" we either mean RFCs or well-established best practices.
We are generally not interested in defining new standards if a prior open
standard already exists. We should also avoid doing things which directly
or indirectly contradict established standards.
