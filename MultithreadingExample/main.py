#!/usr/bin/env python
import re
import time
import logging
import subprocess
import uuid
import argparse
from multiprocessing import Pool



def run_cmd(cmd):
    try:
        success = subprocess.check_call(cmd, shell = True)
    except Exception, e:
        success = 1
        print e
    return success


class generateQT(object):
	def __init__(self):
		self.formats = ['internal_format1', 'client_format1', 'client_format2']
		self.input = 'input.%05d.exr' # Sequence of input files
		self.outdir = '/.'


	def getFlags(self):
		pass

	def getTemplate(self):
		pass

	def runCodec(self):
	    formats = self.formats
	    flags = self.getFlags()
	    template = self.getTemplate()
	    cmd_list = []
	    for i in range(len(formats)):
	        format = formats[i]
	        if format != '':
	            cmd = 'run_qt_terminal -f %s %s -t %s -i %s -o %s'%(format, flags, template, in_path, out_base)
	            cmd_list.append(cmd)


	    pool = Pool(processes = len(formats))
	    calls = pool.map(run_cmd, cmd_list)

	    calls_success = sum(calls)

	    if calls_success == 0:       
	        print "CALLS SUCCESSFUL!!!"
	    else:
	        raise OSError("CALLS UNSUCCESSFUL!!!")    


class App(object):
    def __init__(self):
        desc = ""
        usage = ""
        
        parser = argparse.ArgumentParser(description=__doc__,
                formatter_class=argparse.RawDescriptionHelpFormatter)

        parser.add_argument("-o", "--output_path", 
            dest="output_path",
            default=os.getcwd(),
            help="path of output location [default is current location]",
            required = False)

        parser.add_argument("-f", "--format", nargs = '+',
            dest="format",
            default=["prores"],
            help="type of movie codec to run [prores|dnxhd|etc...]",
            required = True)

        parser.add_argument("-v", "--version",
            dest="version",
            default=None,
            nargs = '+',
            help="a list of version names [0903_0040_main_comp_output_v003 ect...]",
            required = False)

        parser.add_argument("-p", "--playlist",
            dest = "playlist",
            default = None,
            nargs = '+',
            help = "copy by playlist id",
            required = False)



        options = parser.parse_args()
        self.format = options.format
        self.output_path = options.output_path
        if options.version:
            self.version = options.version
        else:
            self.version = None
        if options.playlist:
            self.playlist = [int(f) for f in options.playlist]
        else:
            self.playlist = None 
    
    def getPlaylistVersions(self, playlist_id = 5436):
    
        Playlist = {'type' : 'Playlist', 'id' : int(playlist_id)}

        entity_type = 'Version'
        if not entity_type and 'AF_ENTITY_TYPE' in os.environ:
            entity_type = os.environ['AF_ENTITY_TYPE']
            
        if entity_type:
            entities = self.sg.find(entity_type.capitalize(), 
                                [["playlists", "is", Playlist]], 
                                ['code'])

            if entities:
                return sorted(entities, key=lambda a: a['code'])
        
        return []


    def getQTEntities(self):
        qts = []
        entities = []
        if self.playlist != None:

            versions = []
            for arg in self.playlist:
                playlist_id = arg
                print "Playlist:", arg
                versions+=getPlaylistVersions(playlist_id = playlist_id)

            print "Versions:"
            for version in versions:
                print version['code']
                qts.append(version['code'])

        elif self.version:
            for arg in self.version:
                qts.append(arg)

        for qt in qts:
            entity_type = 'Version'
              
            entity = self.sg.find_one(entity_type.capitalize(), 
                                [["code", "is", qt]], 
                                ['code', 'project'])

            if entity:
                entities.append(entity)
            else:
                print "ERROR: COULDN'T FIND VERSION %s"%qt

        return entities



if __name__ == '__main__':
    a = App()
    for entity in a.getQTEntities():
        qt = generateQT(entity, a.format, a.output_path)
        qt.run()





