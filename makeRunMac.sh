#!/bin/sh


sudo pyinstaller -i ./source/images/common/icon.icns -w -F --clean --add-data source:source --add-data yanglabMFuns:yanglabMFuns --noconfirm --k=as2gaFgWE1weA2a --hidden-import pkg_resources.py2_warn run.py
