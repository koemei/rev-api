# -*- coding: utf-8 -*-

import docx
import lxml
import os
import zipfile
import traceback

from ConfigParser import SafeConfigParser
from ConfigParser import Error as ConfigParserError

from rev.exceptions import SettingsFileNotFoundError


def docx_to_txt(source, dest):
    """
    Don't ask...
    """
    try:
        document = docx.opendocx(source)
    except:
        print "Exception opening docx %s" %source
        return False
    paratextlist = docx.getdocumenttext(document=document)

    # Make explicit unicode version
    newparatextlist = []
    for paratext in paratextlist:
        newparatextlist.append(paratext.encode("utf-8").strip())

    # Print out text of document with two newlines under each paragraph
    with open(dest, "wb") as txt_file:
        txt = '\n'.join(newparatextlist)\
            .replace('’', '\'')\
            .replace('“', '\"')\
            .replace('”', '\"')\
            .replace('…', '...')\
            .replace('Speaker 1:', '')\
            .replace('\t', '')
        txt_file.write(txt)


def read_settings_file():
    """
    Read the settings.ini file located at the root of this project
    """
    # read settings
    settings_file_path = "settings.ini"
    settings = None
    try:
        if os.path.exists(settings_file_path):
            settings = SafeConfigParser()
            settings.read(settings_file_path)
        else:
            raise SettingsFileNotFoundError("Settings file not found, please copy settings.example.ini to settings.ini and fill in your details")
    except ConfigParserError, e:
        print "Error parsing settings file: "
        print e
        print traceback.format_exc()
        raise e
    return settings