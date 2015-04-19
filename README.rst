=======================
Flask-GAE-Mini-Profiler
=======================

Deprecation Note
================

I know longer have any apps on GAE myself and don't intend to
maintain this library. If anyone is interested in picking this
up want me to point to an alternative here, please let me know.

Description
===========

This Flask extension provides easy integration of the excellent
`gae_mini_profiler
<http://bjk5.com/post/6944602865/google-app-engine-mini-profiler>`_.

Usage::

    from flask import Flask
    from flaskext.gae_mini_profiler import GAEMiniProfiler

    app = Flask(__name__)
    GAEMiniProfiler(app)
