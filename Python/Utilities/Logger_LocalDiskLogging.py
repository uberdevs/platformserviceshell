from os import path, remove
import logging
import logging.config
import json
import sys
from logging.handlers import RotatingFileHandler

with open('A:\Work\Python\Vagrant\\api_server\\Configuration\\rest_api_logging_configuration.json', 'r') as logging_configuration_file:
    config_dict = json.load(logging_configuration_file)

consoleHandler = logging.StreamHandler(sys.stdout)

logging.config.dictConfig(config_dict)
# capture formatted warning seperately and to the log
logging.captureWarnings(True)

max_log_size = (1048576*5)





def getALog(name, path, maxBytes, backupCount, addConsole):
    # format log strings
    formatter = logging.Formatter("%(asctime)s [%(name)s] %(levelname)s: %(message)s")
    consoleHandler.setFormatter(formatter)

    makeALog_fileHandler = logging.FileHandler(path)
    makeALog_fileHandler.setFormatter(formatter)
    makeALog = logging.getLogger(name)
    makeALog.addHandler(makeALog_fileHandler)

    if (addConsole):
        makeALog.addHandler(consoleHandler)
        #print('Added log hanlder {} with console'.format(name))
        #logging.info('Added log hanlder {} with console'.format(name))
    else:
        pass
        #print('Added log hanlder {} without console'.format(name))
        #logging.info('Added log hanlder {} without console'.format(name))

    # control number of bytes and files for logs
    makeALog.addHandler(
        RotatingFileHandler(path, maxBytes=maxBytes,
                            backupCount=backupCount))


    return makeALog

# service logs
logging_rest_service = getALog('rest_service_log','A:\\Work\\Python\\Vagrant\\api_server\\Logs\\rest_service.log', max_log_size, 10, True)

# tester module logs
logging_test = getALog('testers_log','A:\\Work\\Python\\Vagrant\\api_server\\Logs\\testers.log', max_log_size, 10, True)

# database logs
logging_database = getALog('database_log','A:\\Work\\Python\\Vagrant\\api_server\\Logs\\database.log',max_log_size, 10, True)

# security logs
logging_security = getALog('security_log','A:\\Work\\Python\\Vagrant\\api_server\\Logs\\security.log', max_log_size, 10, True)

# Log that the logger was configured
logging.info('Completed configuring logger() based on file configuration values! ' + json.dumps(config_dict, indent=1))


def deleteTheLog(self, path):
    remove(path)

def closeTheLog(self):
    logging.shutdown()