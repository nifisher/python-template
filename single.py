#!/usr/bin/python3
# Last-modified: 08 Feb 2022 09:43:21 PM
################################################################################

# Single file python template with main
# single.py
################################################################################


# Imports
################################################################################
import simplejson as json #json parsing
import argparse #command line arguments
import logging, logging.config #logging functions
import os #to create directories
import shutil #to manipulate files

# Globals
################################################################################
ver_major = "2"
ver_minor = "0"

config = {
    'version' : {
        'major' : int(ver_major),
        'minor' : int(ver_minor)
        },
    'key' : 'value',
    'list' : []
    }


logCfg = {
    'root': {
        'handlers': ['console-root'],
        'level': 'INFO'
        },
    'formatters': {
        'standard': {
            'format': \
            '%(asctime)s [%(levelname)s] %(funcName)s(%(lineno)d):: %(message)s'
            },
        'simple': {
            'format': '%(asctime)s [%(levelname)s]:: %(message)s'
            }
        },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'stream': 'ext://sys.stderr',
            'formatter': 'simple'
            },
    'console-root': {
        'class': 'logging.StreamHandler',
        'level': 'DEBUG',
        'stream': 'ext://sys.stdout',
        'formatter': 'simple'
        },
    'logFile': {
        'class': 'logging.handlers.RotatingFileHandler',
        'backupCount': 3,
        'filename': 'status.log',
        'maxBytes': 1024,
        'formatter': 'standard'
        }
    },
    'version': int(ver_major),
    'loggers': {
        'fileLogging': {
            'propagate': False,
            'handlers': ['logFile'],
            'level': 'DEBUG'
            },
        'baseLogging': {
            'propagate': False,
            'handlers': ['logFile', 'console'],
            'level': 'DEBUG'
            },
        'consoleLogging': {
            'propagate': False,
            'handlers': ['console'],
            'level': 'ERROR'
            }
        }
    }


# Funcitons
################################################################################



# Main()
################################################################################
# for running this suite as a script directly
if __name__ == "__main__":

    logCfgFile = 'log.cfg'
    cfgFile    = 'single.cfg'

    # Configure logging
    # Overwrite global config if config file exists
    try:
        with open(logCfgFile, 'r') as logCfgFD:
            logCfg = json.loads(logCfgFD.read())
    except json.JSONDecodeError:
        print("Error loading logging config file. Delete {0} and re-initialize".format(logCfgFile))
        exit(-1)
    except IOError:
        pass

    logging.config.dictConfig(logCfg)
    log = logging.getLogger()
    log.info('Program start')

    # Command line arguments
    argv = argparse.ArgumentParser(description="Single file python cript to do something")
    argv.add_argument("--initialize", action='store_true', default=False,
         help="Create intial configuration filesi and work directories")

    log.debug('Parse options')
    options = argv.parse_args()

    if options.initialize == True:
        # all local to current working dir
        # create general configuration file
        log.debug('Create config files')
        try:
            shutil.move(logCfgFile, '.'.join((logCfgFile,'old')))
            shutil.move(cfgFile, '.'.join((cfgFile,'old')))
            log.info('Existing files backed up')
        except (shutil.Error, IOError):
            pass

        # create logging config
        try:
            with open(logCfgFile, 'w') as logCfgFD:
                logCfgFD.write(json.dumps(logCfg, indent=3))
            with open(cfgFile, 'w') as cfgFD:
                cfgFD.write(json.dumps(config, indent=3))
            log.info('Config files created')
        except IOError:
            log.error('Error creating config files')
            pass

        # create any needed work directories
        log.info('Create directories')
        try:
            os.makedirs('tmpfiles')
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        exit(0)

    log.debug('nothing to do')


    log.info('Program finish')

    exit (0)
