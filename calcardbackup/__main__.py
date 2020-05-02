"""calcardbackup

Backup calendar data from nextcloud. Use the CLI arguments to override settings from the config file.

Usage:
    calcardbackup [options]

Options:
  -c FILE --configfile=FILE             Config file. Read configuration from FILE. [default: config.ini]
  -d FORMAT --date=FORMAT               Use FORMAT as file name extension for backup directory or compressed backup file. Check 'man date' for more info about different formats and syntax.
  -o DIRECTORY --output=DIRECTORY       Use directory DIRECTORY to store backups.

Other options:
  -h --help         Show this screen.
  --version         Show version.
  --loglevel LEVEL  Set the loglevel. This override the configfile.

"""

VERSION = '0.1.0'

from docopt import docopt
from . import logger
import configparser
import sys
import logging

config = configparser.ConfigParser()

def debugShowConfig(config, logger):
    """Show all values from configparser in the DEBUG log

    """
    for section in config.sections():
        for key in config[section]:
            logger.debug('Load {}:{} = {}'.format(section, key, config.get(section, key, fallback=None)))

def debugShowCLIArgs(args, logger):
    """Show all values from the CLI input in the DEBUG log

    """
    for key, value in args.items():
        if value:
            logger.debug('CLI {} = {}'.format(key, value))

def addLogFile(config, logger):
    """Add a FileHandler for the logger.

    """
    logfile = config.get('global', 'logfile', fallback='calcardbackup.log')
    try:
        fh = logging.FileHandler(logfile)
    except PermissionError as e:
        logger.error(e)
        logger.warning('Cannot write logfile. Check file permission for {}'.format(logfile))
    except Exception as e:
        logger.error(e)
    else:
        fh.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S'))
        logger.addHandler(fh)
        logger.debug('Write log to {}'.format(logfile))

if __name__ == '__main__':
    args = docopt(__doc__, version=VERSION)
    configfile = args['--configfile']
    config.read(configfile)
    if len(config.sections()) == 0:
        logger.error('{} seems to be empty or is missing the required settings!'.format(configfile))
        logger.error('The config file is required. Aborting...')
        sys.exit(1)
    logger.setLevel(args['--loglevel'] or config.get('global', 'loglevel', fallback=logging.DEBUG))
    addLogFile(config, logger)
    debugShowCLIArgs(args, logger)
    debugShowConfig(config, logger)
