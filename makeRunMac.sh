#!/bin/sh


sudo pyinstaller -i ./source/images/common/icon.icns -w --clean --add-data source:source --add-data yanglabMFuns:yanglabMFuns --add-binary='/System/Library/Frameworks/Tk.framework/Tk':'tk' --add-binary='/System/Library/Frameworks/Tcl.framework/Tcl':'tcl' --noconfirm --k=as2gaFgWE1weA2a --hidden-import pkg_resources.py2_warn run.py

echo "start to codesign the app"

APP_PATH="/Users/Zy/PycharmProjects/ptbGui/dist/run.app"
sudo codesign --deep -f -s B1B17CC1866C978FE90BA83228B6D4045A1081A8  "$APP_PATH"