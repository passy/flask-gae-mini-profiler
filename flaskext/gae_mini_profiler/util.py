"""
    gae_mini_profiler.util
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2011 - 2013, Ben Kamens
    :url: https://github.com/kamens/gae_mini_profiler
    :license: MIT, see LICENSE for more details
"""


def seconds_fmt(f, n=0):
    return milliseconds_fmt(f * 1000, n)

def milliseconds_fmt(f, n=0):
    return decimal_fmt(f, n)

def decimal_fmt(f, n=0):
    format = "%." + str(n) + "f"
    return format % f

def short_method_fmt(s):
    return s[s.rfind("/") + 1:]

def short_rpc_file_fmt(s):
    if not s:
        return ""
    return s[s.find("/"):]