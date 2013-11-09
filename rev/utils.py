# -*- coding: utf-8 -*-

import docx
import lxml
import os
import zipfile


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