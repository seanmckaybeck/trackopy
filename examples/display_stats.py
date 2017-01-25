import trackopy


USERNAME = 'ooga-booga-1234'
PASSWORD = 'abcdefgh'


t = trackopy.Trackobot(USERNAME, PASSWORD)

stats = t.stats(stats_type='classes', time_range='current_month', as_hero='warrior')
total = stats['stats']['overall']['total']
wins = stats['stats']['overall']['wins']
losses = stats['stats']['overall']['losses']
print('Stats for the current month as Warrior:\n{} total games, with {} wins and {} losses'.format(total, wins, losses))

stats = t.stats(stats_type='decks', time_range='last_3_days', as_hero='shaman', as_deck='aggro', mode='ranked')
total = stats['stats']['overall']['total']
wins = stats['stats']['overall']['wins']
losses = stats['stats']['overall']['losses']
print('Stats for the last 3 days as Aggro Shaman:\n{} total games, with {} wins and {} losses'.format(total, wins, losses))

