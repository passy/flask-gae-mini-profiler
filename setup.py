"""
Flask-GAE-Mini-Profiler
-----------------------

A drop-in, ubiquitous, production profiling tool for
`Flask <http://flask.pocoo.org>`_ applications on Google App Engine using
`gae_mini_profiler <http://bjk5.com/post/6944602865/google-app-engine-mini-profiler>`_.

Links
`````

* `documentation <http://packages.python.org/Flask-GAE-Micro-Profiler>`_
* `development version
  <http://github.com/passy/flask-gae-mini-profiler/zipball/master#egg=Flask-GAE-Micro-Profiler-dev>`_
"""
from setuptools import setup


def run_tests():
    from tests import suite
    return suite()


setup(
    name='Flask-GAE-Mini-Profiler',
    version='0.1.1',
    url='http://packages.python.org/Flask-GAE-Micro-Profiler',
    license='MIT',
    author='Pascal Hartig',
    author_email='phartig@rdrei.net',
    description='Flask integration of gae_mini_profiler',
    long_description=__doc__,
    packages=['flaskext', 'flaskext.gae_mini_profiler'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    tests_require=['mock==0.7'],
    test_suite="__main__.run_tests",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
