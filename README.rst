=======================
Flask-GAE-Mini-Profiler
=======================

This Flask extension provides easy integration of the excellent
`gae_mini_profiler
<http://bjk5.com/post/6944602865/google-app-engine-mini-profiler>`_.

Usage::

    from flask import Flask
    from flaskext.gae_mini_profiler import GAEMiniProfiler

    app = Flask(__name__)
    GAEMiniProfiler(app)
