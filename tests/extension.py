# -*- coding: utf-8 -*-
"""
    Unit and integration tests for the gae-mini-profiler flask extension.

    :copyright: (c) 2011 by Pascal Hartig.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import with_statement
import unittest
import mock
import sys
import os

# Messy hack to remove google modules from the cache. Unfortunately, google is
# not using proper namespaces and thus may be installed multiple times.
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


class ExtensionTestCase(GAETestCase):


    def setUp(self):
        self.environ_patcher = mock.patch('flaskext.gae_mini_profiler.'
                                          'Environment')
        self.middleware_patcher = mock.patch('flaskext.gae_mini_profiler.'
                                        'GAEMiniProfilerWSGIMiddleware')

        self.environ_patcher.start()
        self.middleware_patcher.start()

    def tearDown(self):

        self.environ_patcher.stop()
        self.middleware_patcher.stop()

    def test_response_processing(self, *mocks):
        from flaskext.gae_mini_profiler import GAEMiniProfiler

        app = mock.Mock()
        rendering = "GAEMiniProfiler"

        class Response(object):
            """Mock response"""

            status_code = 200
            is_sequence = True
            charset = "utf-8"

            data = u"<body>Hello World!</body>"


        with mock.patch_object(GAEMiniProfiler, '_render') as render_mock:
            render_mock.return_value = rendering
            ext = GAEMiniProfiler(app)

            new_response = ext._process_response(Response())

        self.assertEquals([u"<body>Hello World!GAEMiniProfiler</body>"],
                          new_response.response)

    def test_request_view(self):
        request_patcher = mock.patch('flaskext.gae_mini_profiler.request',
                                     spec=True)
        profiler_patcher = mock.patch('flaskext.gae_mini_profiler.profiler',
                                      spec=True)
        jsonify_patcher = mock.patch('flaskext.gae_mini_profiler.jsonify',
                                     spec=True)

        request = request_patcher.start()
        profiler = profiler_patcher.start()
        jsonify = jsonify_patcher.start()

        try:
            from flaskext.gae_mini_profiler import GAEMiniProfiler
            properties = ['a', 'b', 'c']

            request_id = mock.Sentinel()
            request.args = {'request_id': request_id}

            stats = profiler.RequestStats.get.return_value
            stats.__getattribute__ = lambda x: x
            profiler.RequestStats.serialized_properties = properties
            app = mock.Mock()
            ext = GAEMiniProfiler(app)
            ext._request_view()

            profiler.RequestStats.get.assertCalledOnceWith(request_id)
            jsonify.assert_called_once_with(
                dict(zip(properties, properties)))
        finally:
            request_patcher.stop()
            profiler_patcher.stop()
            jsonify_patcher.stop()


def suite():
    suite = unittest.TestSuite()
    for case in [FunctionTestCase, MiddlewareTestCase, ExtensionTestCase]:
        suite.addTest(unittest.makeSuite(case))

    return suite


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), os.path.pardir))
    unittest.main(defaultTest='suite')
