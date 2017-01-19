import datetime
import unittest

import requests
from trackopy import Trackobot


USERNAME = 'twilight-squirrel-3676'
PASSWORD = 'e8fb91349a'


class TestTB(unittest.TestCase):
    def setUp(self):
        self.t = Trackobot(USERNAME, PASSWORD)

    def test_one_time_auth(self):
        url = self.t.one_time_auth()
        assert 'trackobot' in url

    def test_stats(self):
        stats = self.t.stats(stats_type='classes')
        assert 'stats' in stats
        stats = self.t.stats(stats_type='decks')
        assert 'stats' in stats
        stats = self.t.stats(stats_type='arena')
        assert 'stats' in stats
        stats = self.t.stats(mode='ranked')
        assert 'stats' in stats
        stats = self.t.stats(mode='arena')
        assert 'stats' in stats
        stats = self.t.stats(mode='casual')
        assert 'stats' in stats
        stats = self.t.stats(mode='friendly')
        assert 'stats' in stats
        stats = self.t.stats(time_range='current_month')
        assert 'stats' in stats
        stats = self.t.stats(time_range='last_3_days')
        assert 'stats' in stats
        stats = self.t.stats(time_range='last_24_hours')
        assert 'stats' in stats
        today = datetime.datetime.now()
        yesterday = today - datetime.timedelta(days=1)
        stats = self.t.stats(time_range='custom', start=yesterday, end=today)
        assert 'stats' in stats
        stats = self.t.stats(stats_type='classes', as_hero='shaman', vs_hero='warrior')
        assert 'stats' in stats
        stats = self.t.stats(stats_type='decks', as_deck=2, vs_deck=5)
        assert 'stats' in stats
        with self.assertRaises(ValueError):
            self.t.stats(stats_type='badstr')
        with self.assertRaises(ValueError):
            self.t.stats(mode='badstr')
        with self.assertRaises(ValueError):
            self.t.stats(time_range='badstr')
        # end is None
        with self.assertRaises(TypeError):
            self.t.stats(time_range='custom', start=today)
        # start is None
        with self.assertRaises(TypeError):
            self.t.stats(time_range='custom', end=today)
        # type(start) != datetime.datetime
        with self.assertRaises(TypeError):
            self.t.stats(time_range='custom', start='', end=today)
        # type(end) != datetime.datetime
        with self.assertRaises(TypeError):
            self.t.stats(time_range='custom', end='', start=today)

    def test_decks(self):
        decks = self.t.decks()
        assert 'decks' in decks

    def test_reset(self):
        with self.assertRaises(ValueError):
            self.t.reset(modes=['foobar'])
        self.upload()
        self.upload()
        self.t.reset()  # default is all modes
        history = self.t.history()
        assert len(history['history']) == 0
        self.upload()
        self.upload(mode='arena')
        self.t.reset(modes=['ranked'])
        r_history = self.t.history()
        a_history = self.t.arena_history()
        l = [g for g in r_history['history'] if g['mode'] != 'arena']
        assert len(l) == 0
        assert len(a_history['arena']) != 0

    def test_modify_metadata(self):
        with self.assertRaises(ValueError):
            self.t.modify_metadata(111, 'foo', 'bar')
        game = self.upload()
        game = game['result']
        value = 15
        ret = self.t.modify_metadata(game['id'], 'rank', value)
        assert ret is True
        history = self.t.history()
        for g in history['history']:
            if g['id'] == game['id']:
                assert g['rank'] == value
                break

    def test_history(self):
        self.upload(**{'deck_id': 'aggro', 'opponent_deck_id': 'pirate'})
        history = self.t.history()
        assert 'history' in history
        assert len(history['history']) != 0
        history = self.t.history(query='Shaman')
        assert 'history' in history

    def test_arena_history(self):
        self.upload(mode='arena')
        history = self.t.arena_history()
        assert 'arena' in history
        assert len(history['arena']) != 0

    def test_toggle_tracking(self):
        try:
            self.t.toggle_tracking(enabled=False)
        except requests.exceptions.HTTPError:
            self.fail('toggle_tracking() raised an exception')
        try:
            self.t.toggle_tracking(enabled=True)
        except requests.exceptions.HTTPError:
            self.fail('toggle_tracking() raised an exception')

    def test_delete_game(self):
        game = self.upload()
        game = game['result']
        self.t.delete_game(game['id'])
        history = self.t.history()
        ids = [g['id'] for g in history['history']]
        assert game['id'] not in ids

    def upload(self, mode='ranked', **kwargs):
        data = {'result': {'hero': 'Shaman', 'opponent': 'Warrior', 'mode': mode,
            'coin': False, 'win': True }}
        if kwargs:
            data.update(**kwargs)
        game = self.t.upload_game(data)
        return game

    def test_upload_game(self):
        game = self.upload()
        game = game['result']
        assert 'id' in game

    def test_create_user(self):
        data = Trackobot.create_user()
        assert 'username' in data
        assert 'password' in data

    def test_rename_user(self):
        try:
            self.t.rename_user('stan darsh')
        except requests.exceptions.HTTPError:
            self.fail('rename_user() raised an exception')


if __name__ == '__main__':
    unittest.main()

