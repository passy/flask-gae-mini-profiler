"""
Flask-GAE-Mini-Profiler
-----------------------

Description goes here...

Links
`````

* `documentation <http://packages.python.org/Flask-GAE-Micro-Profiler>`_
* `development version
  <http://github.com/USERNAME/REPOSITORY/zipball/master#egg=Flask-GAE-Micro-Profiler-dev>`_

"""
from setuptools import setup


setup(
    name='Flask-GAE-Mini-Profiler',
    version='0.1',
    url='<enter URL here>',
    license='MIT',
    author='Pascal Hartig',
    author_email='your-email-here@example.com',
    description='<enter short description here>',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask'
    ],
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
