======
prolog
======

Tools and convenience methods to simplify and expedite Python logging.

* Simple - though opinionated - setup for common use-cases
* Extensively and easily configurable via user and local files, as well as environ variables
* Comes with full featured formatters and handlers that can also be used
  in normal ``logging`` situations

Usage
=====

The easiest way to begin using ``prolog`` is to add the following to your application
code::

    import prolog
    prolog.basic_config()

will configure the ``root`` logger for the default level ``logging.INFO`` and
set up two handlers: a colorized, console streaming handler, as well as a file
handler set to log to the default file - ``pypro.log`` - in the main app's directory.



Develop and testing
===================

    $ pip install invoke
    $ inv develop
    $ inv test
