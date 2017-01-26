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


def _logging(v):
    if v > 4:
        v = 4
    level = 50 - v*10
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='tb.log')
    return logging.getLogger(__name__)


def _check_creds(config):
    if config.trackobot is None:
        click.echo('Please supply a username and password')
        config.logger.error('No username or password supplied')
        sys.exit(1)
    config.logger.debug('Trackobot object properly created')


@click.group()
@click.option('-v', '--verbose', count=True, help='Logging verbosity')
@click.option('-u', '--username', help='Your Trackobot username')
@click.option('-p', '--password', help='Your Trackobot password')
@pass_config
def cli(config, verbose, username, password):
    v = int(verbose)
    config.logger = _logging(v)
    if username and password:
        try:
            config.trackobot = trackopy.Trackobot(username, password)
        except ValueError as e:
            click.echo(str(e))
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
@pass_config
def history(config, num_pages, start, output):
    """Get your game history"""
    _check_creds(config)
    games = []
    count = 0
    while count != num_pages:
        config.logger.debug('Getting page %d of history', start)
        history = config.trackobot.history(page=start)
        config.logger.debug('Extending games list')
        games.extend(history['history'])
        count += 1
        start += 1
    config.logger.debug('Dumping game history to %s', output)
    with open(output, 'w') as f:
        json.dump(games, f)
    click.echo('Wrote {} games to {}'.format(len(games), output))


@cli.command()
@click.option('-i', '--id', help='The ID of the game to delete', type=int)
@pass_config
def delete(config, id):
    """Delete the specified game from trackobot"""
    _check_creds(config)
    config.logger.debug('Deleting the game')
    config.trackobot.delete_game(id)
    config.logger.info('Game %d deleted', id)
    click.echo('Game deleted')


@cli.command()
@click.option('-o', '--output', help='The file to write decks to', default='decks.json')
@pass_config
def decks(config, output):
    """Get a list of the currently supported deck archetypes for Trackobot and write them to disk"""
    _check_creds(config)
    config.logger.debug('Getting decks list')
    decks = config.trackobot.decks()
    with open(output, 'w') as f:
        json.dump(decks, f)
    config.logger.info('Wrote decks to %s', output)
    click.echo('Wrote decks to {}'.format(output))


@cli.command()
@pass_config
def one_time_auth(config):
    _check_creds(config)
    config.logger.debug('Getting profile link')
    url = config.trackobot.one_time_auth()
    config.logger.info('Retrieved profile url: %s', url)
    click.echo(url)


if __name__ == '__main__':
    cli()

