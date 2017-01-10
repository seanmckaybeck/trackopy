trackopy
========

`trackopy` is a Python 3 wrapper library for the `Track-o-bot <https://trackobot.com>`_ API.
It requires the `requests` module and Python 3.
No, it does not support Python 2.


Installation
------------

Install trackopy with the command::

    $ pip install trackopy

Usage
-----

The library relies on the `Trackobot` class.
All methods are documented and easy to use.

.. code-block:: python

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

In addition to the above, you can upload games, modify game metadata, delete games, or toggle automatic deck tracking.


API
---

.. autoclass:: trackopy.Trackobot
    :members:
