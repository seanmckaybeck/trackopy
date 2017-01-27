trackopy
========

Overview
--------

``trackopy`` is a Python 3 wrapper library for the `Track-o-bot`_ API.
It requires the ``requests`` module and Python 3. No, it does not
support Python 2.

Installation
------------

``pip install trackopy``

Usage
-----

The library relies on the ``Trackobot`` class. All methods are
documented and easy to use.

::

    import trackopy
    # from trackopy import *
    # from trackopy import Trackobot
    # All of the above are valid

    # You can create new users if you do not already have an account
    # The returned data will look like {'username': 'foo-bar-1234', 'password': 'abcdefgh'}
    user = trackopy.Trackobot.create_user()

    trackobot = trackopy.Trackobot(user['username'], user['password'])

    # Generate a profile link
    url = trackobot.one_time_auth()

    # Get your stats by arena, class, or deck
    stats = trackobot.stats(stats_type='decks')
    stats = trackobot.stats(stats_type='classes')
    stats = trackobot.stats(stats_type='arena')

    # Get supported deck archetypes
    decks = trackobot.decks()

    # Reset your account
    trackobot.reset()

    # Get game history
    history = trackobot.history()
    arena_history = trackobot.arena_history()

In addition to the above, you can upload games, modify game metadata,
delete games, or toggle automatic deck tracking. To learn more about the
available functionality, please `read the docs`_.

Please ensure you are using your Trackobot **password**, not your
Trackobot API key. You can get your password from the Trackobot desktop
app by exporting your user data to a file. Your password will be the
second string in the file with spaces between each character. Remove the
spaces and you should have a password of length 8.

CLI
===

Starting with v2.0, there is an included CLI utility for interacting with trackobot.com.
It serves as an example of how to use the library as well as a convenient way of getting data quickly.
Some people may only need simple functionality from this library, and this utility provides that.
It implements all available commands in ``trackopy``.
It is installed with the library and can be run with the ``tb`` command.
See all arguments and functionality with ``tb --help``.

License
-------

This project is licensed under the MIT license. You can read more in the
LICENSE file.

.. _Track-o-bot: https://trackobot.com
.. _read the docs: https://trackopy.readthedocs.io/en/latest/
