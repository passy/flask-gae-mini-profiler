# -*- coding: utf-8 -*-
"""
    Unit and integration tests for the gae-mini-profiler flask extension.

    :copyright: (c) 2011 by Pascal Hartig.
    :license: MIT, see LICENSE for more details.
"""

import unittest
import mock
import sys
import os

# Messy hack to remove google modules from the cache. Unfortunately, google is
# not using namespaces and thus may be installed multiple times.
try:
    del sys.modules['google']
except KeyError:
    pass


class GAETestCase(unittest.TestCase):
    """TestCase that mocks out common GAE imports."""

    def setUp(self):
        """Load our own stub-library that allows us to run the test suite
        without having the gae sdk installed. This messes around with the
        module internals quite badly, but it simplifies the later use a lot.
        """

        self.mocklib_path = os.path.realpath(
            os.path.join(
                os.path.dirname(__file__),
                'gaemock'
            )
        )
        sys.path.insert(0, self.mocklib_path)

    def tearDown(self):
        sys.path.remove(self.mocklib_path)


class FunctionTestCase(GAETestCase):

    def test_replace_insensitive(self):
        from flaskext.gae_mini_profiler import replace_insensitive

        string = "Hello, World. Replace me."
        result = replace_insensitive(string, "wORld", "GAE")
        self.assertEquals("Hello, GAE. Replace me.", result)


class MiddlewareTestCase(GAETestCase):

    def _get_middleware(self, app_config=None):
        from flaskext.gae_mini_profiler import GAEMiniProfilerWSGIMiddleware

        with mock.patch('flaskext.gae_mini_profiler.profiler'):
            app = mock.MagicMock(name='app')
            if app_config:
                app.config = app_config

            wsgi_app = mock.Mock(name='wsgi_app')
            return GAEMiniProfilerWSGIMiddleware(app, wsgi_app)

    def test_is_admin(self):
        middleware = self._get_middleware()

        with mock.patch('google.appengine.api.users') as users_mock:
            users_mock.is_current_user_admin.return_value = True

            self.assertTrue(middleware.should_profile({'PATH_INFO': ""}))
            users_mock.is_current_user_admin.assert_called_once()

    def test_has_allowed_email(self):
        email = "test@example.com"
        config = {
            'GAEMINIPROFILER_PROFILER_EMAILS': [email],
            'GAEMINIPROFILER_PROFILER_ADMINS': False
        }

        middleware = self._get_middleware(app_config=config)

        with mock.patch('google.appengine.api.users') as users_mock:
            users_mock.get_current_user.return_value.email.return_value = \
                    email

            self.assertTrue(middleware.should_profile({'PATH_INFO': ""}))

    def test_has_unauthorized_email(self):
        email = "test@example.com"
        config = {
            'GAEMINIPROFILER_PROFILER_EMAILS': [email],
            'GAEMINIPROFILER_PROFILER_ADMINS': False
        }

        middleware = self._get_middleware(app_config=config)

        with mock.patch('google.appengine.api.users') as users_mock:
            email = "test@evilbadguys.com"
            users_mock.get_current_user.return_value.email.return_value = \
                    email

            self.assertFalse(middleware.should_profile({'PATH_INFO': ""}))

def suite():
    suite = unittest.TestSuite()
    for case in [FunctionTestCase, MiddlewareTestCase]:
        suite.addTest(unittest.makeSuite(case))

    return suite


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
    unittest.main(defaultTest='suite')
