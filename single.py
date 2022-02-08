#!/usr/bin/python3
# Last-modified: 07 Feb 2022 11:23:46 PM
################################################################################

# Single file python template with main
# single.py
################################################################################

# Version History
################################################################################
# 0.   - initial version
# 1.   - argument parsinge and logging

# Imports
################################################################################
import argparse #command line arguments
import logging, logging.config #logging functions

# Globals
################################################################################
ver_major = "1"
ver_minor = "0"

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

    # Configure logging
    logging.config.dictConfig(logCfg)
    log = logging.getLogger()
    log.info('Program start')

    # Command line arguments
    argv = argparse.ArgumentParser(description="Single file python cript to do something")
    argv.add_argument("--bool", action='store_true', default=False,
         help="basic option, true on existance")

    log.debug('Parse options')
    options = argv.parse_args()

    if options.bool == True:
        log.debug('option is set')
        exit(0)

    log.debug('no option is set')


    log.info('Program finish')

exit (0)
