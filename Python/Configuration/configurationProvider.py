import json
import yaml
import configparser
import io
from bs4 import BeautifulSoup
import xmltodict

import Utilities.Logger_LocalDiskLogging as logger
import config as baseConfig

def get_json_configuration(self, filename):
    with open(filename) as json_data_file:
        data = json.load(json_data_file)

    # create common dictionary of configuration
    global_configuration = json.load(data)

    logger.logging_rest_service.info('JSon configuration retrieved : {}'.format(data))

    return global_configuration

def get_yaml_configuration(filename):
    with open(filename, 'r') as ymlfile:
        global_configuration = yaml.load(ymlfile)

    return global_configuration

def get_ini_configuration(filename):
    # Load the configuration file
    with open(filename) as f:
        sample_config = f.read()
    config = configparser.RawConfigParser(allow_no_value=True)
    config.readfp(io.BytesIO(sample_config))

    global_configuration = {}

    # List all contents
    logger.logging_rest_service.info('INI configuration : {}'.format("List all contents"))
    for section in config.sections():
        logger.logging_rest_service.info('INI configuration : {}'.format("Section: %s" % section))
        global_configuration[section] = {}
        for option in config.options(section):
            global_configuration[section][option] = config.get(section,option)

    return global_configuration

def get_xml_configuration(filename):
    with open(filename) as f:
        content = f.read()

    y = BeautifulSoup(content)
    logger.logging_rest_service.info('SML configuration : {}'.format(y.mysql.host.contents[0]))
    for tag in y.other.preprocessing_queue:
        logger.logging_rest_service.info('XML configuration : {}'.format(tag))

    global_configuration = xmltodict.parse(content, process_namespaces=True)
    return global_configuration