#!/usr/bin/env python

import os
import sys


class BashScript(object):
    def __init__(self, filename = '', command = ''):
        self.command = command
        self.filename = filename

    @classmethod
    def writeBash(cls, filename, content):
            
        f = open(filename, 'w')
        f.write('#!/bin/bash\n')    

        # Make the home directory if it doesn't exist

        f.write('\n')
        f.write('if [ ! -d "$HOME" ] ; then\n')
        f.write('    sudo mkdir $HOME\n')
        f.write('    sudo chown $USER $HOME\n')
        f.write('fi\n')
        f.write('\n')
        
        # Write the content

        f.write(content + "\n")
        f.close()
        
        try:
            os.chmod(filename, 0777)
        except:
            pass
        
        if os.name == 'nt':
            subprocess.call('dos2unix.exe %s'%filename)

    def setFilename(self, path):
        baseName, typeExt = os.path.splitext(path)
        if typeExt != "sh":
            raise Exception, "File is not a .sh file: '%s'" % path
        else:
            self.filename = path

    def setCommand(self, command):
        self.command = command


    def generateScript(self):
        shfile = self.filename
        self.writeBash(self.filename, self.command)
        return shfile


def Test():
    b = BashScript('/Users/Amber/test.sh')
    b.setCommand("echo $USER ")
    b.generateScript()

if __name__ == "__main__":
    Test()