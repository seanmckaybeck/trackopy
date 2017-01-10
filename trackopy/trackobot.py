import requests


class Trackobot:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._params = {'username': username, 'password': password}
        self._auth = requests.auth.HTTPBasicAuth(username, password)
        self._url = 'https://trackobot.com/'
        self._allowed_params = ['added', 'mode', 'win', 'hero', 'opponenet',
                                'coin', 'duration', 'rank', 'legend', 'deck_id',
                                'opponent_deck_id', 'note']
    @staticmethod
    def create_user(self) -> dict:
        """
        Create a new username and password in Trackobot.
        Returns JSON of the format {'username': 'newuser', 'password': 'password}

        :return: Dictionary of new user data
        :raises: requests.exceptions.HTTPError on error
        """
        url = 'https://trackobot.com/users.json'
        r = requests.post(url)
        r.raise_for_status()
        return r.json()

    def rename_user(self, user_id: int):
        """
        Rename your user to something else.
        Not yet implemented because user ID is not available in an API call

        :param int user_id: The ID representing your user in the trackobot database
        :return:
        """
        # endpoint = '/users/{}/rename'.format(str(user_id))
        # url = self._url + endpoint
        raise NotImplemented('Not yet implemented because user ID unavailable')

    def one_time_auth(self) -> str:
        """
        Generate a one-time URL for opening your profile

        :return: Profile URL
        :rtype: str
        :raises: requests.exceptions.HTTPError on error
        """
        endpoint = '/one_time_auth.json'
        url = self._url + endpoint
        r = requests.post(url, auth=self._auth)
        r.raise_for_status()
        return r.json()['url'] if 'error' not in r.json() else r.json()['error']

    def modify_metadata(game_id: int, param: str, value: str) -> bool:
        """
        Modify the metadata of a specified game.
        Possible parameters that can be changed are: added, mode, win,
          hero, opponent, coin, duration, rank, legend, deck_id,
          opponent_deck_id, note
        It is up to the user to know the correct possible values for each
        of these parameters.

        :param int game_id: The ID of the game to be modified
        :param str param: The name of the parameter to be modified
        :param str value: The new value for the parameter
        :return: True if successfully changed, False otherwise
        :rtype: bool
        """
        if param not in self._allowed_params:
            raise ValueError('param must be one of ' + ', '.join(self._allowed_params))
        endpoint = '/profile/results/'
        url = self._url + endpoint + str(game_id)
        data = {param: value}
        r = requests.put(url, auth=self._auth, json=data)
        if r.status_code == 204:
            return True
        else:
            return False

    def stats(self, stats_type: str='decks') -> dict:
        """
        Get the user's statistics by deck, class, or for arena.
        You must specify one of "decks", "classes", or "arena" for
          the stats_type.
        This will return a dictionary with statistics associated with
          the requested type.

        :param str stats_type: The type of stats you want to see. One of decks, classes, arena
        :return: Dictionary of stats
        :rtype: dict
        :raises: requests.exceptions.HTTPError on error
        """
        allowed = ['classes', 'decks', 'arena']
        if stats_type not in allowed:
            raise ValueError('stats_type must be one of ' + ', '.join(allowed))
        endpoint = '/profile/stats/{}.json'.format(stats_type)
        url = self._url + endpoint
        r = requests.get(url, auth=self._auth)
        r.raise_for_status()
        return r.json()

    def decks(self) -> dict:
        """
        Get the deck archetypes supported by Track-o-bot.

        :return: Dictionary listing each archetype by class
        :rtype: dict
        :raises: requests.exceptions.HTTPError on error
        """
        endpoint = '/profile/settings/decks.json'
        url = self._url + endpoint
        r = requests.get(url, auth=self._auth)
        r.raise_for_status()
        return r.json()

    def reset(self, modes: list=None):
        """
        Reset the user's account data for the specified game modes.
        Supported modes values are "ranked", "casual", "practice",
          "arena", and "friendly".

        :param list modes: A list of the modes to reset
        :return: None
        :raises: requests.exceptions.HTTPError on error
        """
        allowed = ['ranked', 'casual', 'practice', 'arena', 'friendly']
        if modes is None:
            modes = allowed
        if any(mode not in allowed for mode in modes):
            raise ValueError('modes list can only contain ' + ', '.join(allowed))
        endpoint = '/profile/settings/account/reset'
        url = self._url + endpoint
        data = {'reset_modes': modes}
        r = requests.post(url, auth=self._auth, data=data)
        r.raise_for_status()

    def history(self, page: int=1) -> dict:
        """
        Get game history for the user by page.
        Each page contains 15 games.
        Returns JSON as a dictionary representing each game.

        :param int page: The page number
        :return: Dictionary of game data
        :rtype: dict
        :raises: requests.exceptions.HTTPError on error
        """
        endpoint = '/profile.json' 
        url = self._url + endpoint
        params = {'page': page}
        r = requests.get(url, auth=self._auth, params=params)
        r.raise_for_status()
        return r.json()

