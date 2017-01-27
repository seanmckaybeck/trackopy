import json
import logging
import pprint
import sys

import click
import trackopy


class Config:
    def __init__(self):
        self.logger = None
        self.trackobot = None


pass_config = click.make_pass_decorator(Config, ensure=True)


def _logging(v, logfile):
    if v > 4:
        v = 4
    level = 50 - v*10
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename=logfile)
    return logging.getLogger(__name__)


def _check_creds(config):
    """Check if credentials were supplied. Used for commands requiring credentials, which
    is all of them except for create"""
    if config.trackobot is None:
        click.secho('Please supply a username and password', fg='red')
        config.logger.error('No username or password supplied')
        sys.exit(1)
    config.logger.debug('Trackobot object properly created')


@click.group()
@click.option('-v', '--verbose', count=True, help='Logging verbosity. Add more v to increase, i.e. -vvvv')
@click.option('-u', '--username', help='Your Trackobot username')
@click.option('-p', '--password', help='Your Trackobot password')
@click.option('-l', '--log', help='The name of your desired log file. Defaults to tb.log', default='tb.log')
@pass_config
def cli(config, verbose, username, password, log):
    v = int(verbose)
    config.logger = _logging(v, log)
    if username and password:
        try:
            config.trackobot = trackopy.Trackobot(username, password)
        except ValueError as e:
            click.secho(str(e), fg='red')
            sys.exit(1)


@cli.command()
@pass_config
def create(config):
    """Create a new user on trackobot.com"""
    user = trackopy.Trackobot.create_user()
    click.echo('Username: {}\nPassword: {}'.format(user['username'], user['password']))


@cli.command()
@click.option('-n', '--num-pages', default=1, help='The number of pages of history to get')
@click.option('-s', '--start', default=1, help='The page to start from')
@click.option('-o', '--output', help='The file to write game history to', default='history.json')
@click.option('--arena/--no-arena', default=False, help='Whether to get all history or only arena')
@pass_config
def history(config, num_pages, start, output, arena):
    """Get your game history"""
    _check_creds(config)
    games = []
    count = 0
    while count != num_pages:
        config.logger.debug('Getting page %d of history', start)
        if arena:
            history = config.trackobot.arena_history(page=start)
        else:
            history = config.trackobot.history(page=start)
        config.logger.debug('Extending games list')
        games.extend(history['history'])
        count += 1
        start += 1
        if start > history['meta']['total_pages']:
            config.logger.info('Hit max pages on account')
            break
    config.logger.debug('Dumping game history to %s', output)
    with open(output, 'w') as f:
        json.dump(games, f)
    click.secho('Wrote {} games to {}'.format(len(games), output), fg='green')


@cli.command()
@click.option('-i', '--id', help='The ID of the game to delete', type=int)
@pass_config
def delete(config, id):
    """Delete the specified game from trackobot"""
    _check_creds(config)
    if not id:
        click.secho('You need to specify an ID!', fg='red')
        sys.exit(1)
    config.logger.debug('Deleting the game')
    config.trackobot.delete_game(id)
    config.logger.info('Game %d deleted', id)
    click.secho('Game deleted', fg='green')


@cli.command()
@click.option('-o', '--output', help='The file to write decks to', default='decks.json')
@pass_config
def decks(config, output):
    """Get a list of the currently supported deck archetypes for Trackobot and write them to disk.
    Default file name is decks.json"""
    _check_creds(config)
    config.logger.debug('Getting decks list')
    decks = config.trackobot.decks()
    with open(output, 'w') as f:
        json.dump(decks, f)
    config.logger.info('Wrote decks to %s', output)
    click.secho('Wrote decks to {}'.format(output), fg='green')


@cli.command()
@pass_config
def one_time_auth(config):
    """Generate a one-time use profile link for your user"""
    _check_creds(config)
    config.logger.debug('Getting profile link')
    url = config.trackobot.one_time_auth()
    config.logger.info('Retrieved profile url: %s', url)
    click.secho(url, fg='green')


@cli.command()
@click.option('-n', '--name', default='hue-jass', help='The new username')
@pass_config
def rename(config, name):
    """Rename your user. Default name is hue-jass."""
    _check_creds(config)
    config.logger.debug('Renaming...')
    config.trackobot.rename_user(name)
    click.secho('Done', fg='green')


@cli.command()
@click.argument('modes', nargs=-1, type=click.Choice(['ranked', 'casual', 'practice', 'arena', 'friendly']))
@pass_config
def reset(config, modes):
    """Reset game data for the specified <MODES>. If none given, reset everything"""
    _check_creds(config)
    if modes:
        modes = list(modes)
    config.logger.debug('Resetting modes: ' + ', '.join(modes))
    config.trackobot.reset(modes=modes)
    click.secho('Reset!', fg='green')


@cli.command()
@click.option('--track/--no-track', default=True, help='Whether to enable tracking')
@pass_config
def toggle(config, track):
    """Toggle automatic deck tracking"""
    _check_creds(config)
    config.logger.debug('Tracking enabled is %s', track)
    config.trackobot.toggle_tracking(enabled=track)
    click.secho('Done!', fg='green')


@cli.command()
@click.option('-i', '--id', type=int, help='The ID of the game to modify', required=True)
@click.option('-p', '--param', required=True,
              help='The name of the game metadata variable to change, i.e. "rank", "win", etc.',
              type=click.Choice(['added', 'mode', 'win', 'hero', 'opponenet',
                                 'coin', 'duration', 'rank', 'legend', 'deck_id',
                                 'opponent_deck_id', 'note']))
@click.option('-v', '--value', help='The new value for the given parameter', required=True)
@pass_config
def modify(config, id, param, value):
    """Modify the game metadata for the specified game"""
    _check_creds(config)
    try:
        config.logger.debug('Submitting modify request...')
        ret = config.trackobot.modify_metadata(id, param, value)
    except ValueError as e:
        click.secho(str(e), fg='red')
        config.logger.error(str(e))
        sys.exit(1)
    if ret:
        click.secho('Success!', fg='green')
    else:
        click.secho('Failed :(', fg='red')


@cli.command()
@click.option('-t', '--type', type=click.Choice(['classes', 'decks', 'arena']), help='The type of stats',
              default='decks')
@click.option('-r', '--range', type=click.Choice(['current_month', 'all', 'last_3_days', 'last_24_hours']),
              help='The range of time to grab', default='current_month')
@click.option('-m', '--mode', type=click.Choice(['ranked', 'arena', 'casual', 'friendly', 'all']),
              help='The game mode to check', default='ranked')
@click.option('-h', '--hero', type=click.Choice(['rogue', 'paladin', 'warrior', 'warlock',
                                                 'druid', 'priest', 'shaman', 'mage', 'hunter']),
              help='The hero to get stats for', default=None)
@click.option('-o', '--opponent', type=click.Choice(['rogue', 'paladin', 'warrior', 'warlock',
                                                 'druid', 'priest', 'shaman', 'mage', 'hunter']),
              help='The opposing hero to get stats for', default=None)
@click.option('-d', '--deck', type=int, help='The deck ID to get stats for', default=None)
@click.option('-v', '--versus-deck', type=int, help='The opponent deck ID to get stats for', default=None)
@click.option('-f', '--file', help='The name of the file to write the stats to. Defaults to stats.json',
              default='stats.json')
@pass_config
def stats(config, type, range, mode, hero, opponent, deck, versus_deck, file):
    """Retrieve player stats. Note that a custom date range is not supported in this application"""
    _check_creds(config)
    try:
        config.logger.debug('Getting player stats')
        stats = config.trackobot.stats(stats_type=type, time_range=range, mode=mode, as_hero=hero,
                                       vs_hero=opponent, as_deck=deck, vs_deck=versus_deck)
    except ValueError as e:
        click.secho(str(e), fg='red')
        config.logger.error(str(e))
        sys.exit(1)
    with open(file, 'w') as f:
        json.dump(stats, f)
    click.secho('Wrote stats to {}'.format(file), fg='green')


@cli.command()
@click.argument('file')
@click.option('-o', '--output', default='game.json', help='The file to write the resulting game JSON to')
@pass_config
def upload(config, file, output):
    """Upload a new game for the player using information specified in <FILE>"""
    _check_creds(config)
    with open(file) as f:
        game = json.load(f)
        config.logger.debug('Loaded the game data')
    config.logger.debug('Uploading...')
    data = config.trackobot.upload_game(game)
    with open(output, 'w') as f:
        json.dump(data, f)
        config.logger.debug('Wrote the game')
    click.secho('Done!', fg='green')


if __name__ == '__main__':
    cli()

