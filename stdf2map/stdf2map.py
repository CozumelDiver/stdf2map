#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Copyright (C) 2017 D. Fish
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------
###########################################################
# $File: stdf2map.py $
# $Author: daf $
# $Date: 2018-07-07 22:52:37 -0700 (Sat, 07 Jul 2018) $
# $Revision: 213 $
###########################################################
import sys
import copy
import logging
import logging.handlers
import os.path
import glob
import pprint


from _version import __version__
from optparse import OptionParser, OptionGroup
from lotdata import lotdata
from optconfig import partconfig, userconfig, democonfig
from wafermap import WaferMap
from util import lotinfo, wfr_equivalence, is_int
from mapviewer import Mapviewer
from util import get_outfile, dump_lotdata, check_infile, map_yield
from config import App


def do_map (options):
    
    log = logging.getLogger()    

    # NOTE: if options.testset is used with options.demo, it has a 
    # different meaning... it SETS the number of testcounts to 
    # build into the wafer.  
    if options.testset:
        if options.demo:
            App.cfg['demo']['testcount'] = options.testset
            options.testset = None  #Force maps for all demo test sets
        else:
            App.cfg['testset'] = int(options.testset)
     
#     print "test count: {}, testset={}".format(App.cfg['demo']['testcount'], App.cfg['testset']) 
    
    # Get wafer data, depending on the options, it could be
    # demo data or stdf data
    lot = lotdata(options)
    
    # If we have the --info command line option, show lot
    # information and exit
    if options.lotinfo:
        lotinfo(lot)
        return
    
    #Check to make sure we found some data...
    if len(lot.wafers) == 0:
        log.error("No valid data found in '{}'".format(os.path.basename(options.infile)))
        return
    
    #--------------------------------------------------------
    # Check for optional configuration files...
    # ORDER is IMPORTANT here!  Each successive configuration
    # file will overwrite the same settings specified in an 
    # earlier config file.
    #--------------------------------------------------------
        
    # Check for optional theme configuration file
    # typically used to set visual display aspects.
    if '_theme' in App.cfg:
       userconfig(App.cfg['_theme'])
    
    if options.theme:
       userconfig(options.theme)
    
    # Check for optional part-based configuration file
    # NOTE: Any options specifed in the part config file 
    # will override built-in defaults
    partconfig(lot.mir['PART_TYP'])
    
    # Check for demo configuration file
    if options.demo:
        democonfig()
    
    # Check for optional user specified configuration file   
    # NOTE: Any options specifed in the user config file 
    # will override built-in defaults AND the part config 
    # file (if it exists...)   
    if options.user_conf:
        userconfig(options.user_conf)
          
    #--------------------------------------------------------
        
    # Command line options should supersede any of the prior
    # config file options...
       
    if options.baseWidth:
        App.cfg['image']['basewidth'] = int(options.baseWidth)
        
    if options.baseHeight:
        App.cfg['image']['baseheight'] = int(options.baseHeight)
    
    if options.autosize == False:
        App.cfg['image']['autosize'] = False
        
    if options.symbols == False:
        App.cfg['enable_symbols'] = False     
    
    if options.flag == False:
        App.cfg['flag']['show'] = False
        
    if options.binmap:
        if options.binmap.lower() not in ['s','h','sbin','hbin']:
            raise ValueError("Binmap must be 'sbin' or 'hbin'")
        if options.binmap.lower() in ['s','sbin']:
            App.cfg['binmap'] = 'sbin'
        if options.binmap.lower() in ['h','hbin']:
            App.cfg['binmap'] = 'hbin'         
    
    dataflag = False
    
    # Create a map for EACH wafer in the lot AND each testset in a wafer unless explicitly
    # directed to a specify combo with the -t and -w options.
    for wfr in lot.wafers:
#         print wfr.testcounts
        for tset in sorted(wfr.testcounts.keys(),reverse=True):
            
            App.cfg['testset'] = tset
            
            wfr.map_yield = map_yield(wfr, tset)
                    
            # Skip if not explicity requested test number
            if options.testset and tset != int(options.testset):
                continue
            
            # Skip if not explicity requested wafer
            if options.waferid:
                if not wfr_equivalence(options.waferid, wfr.wafer_id):
                    continue
            
            # Build wafermap
            dataflag = True
            wmap = WaferMap()
            img = wmap.buildmap(lot, wfr, tset)
    
            # Construct output filename
            outfile = get_outfile(options,lot,wfr)

            log.info("Writing output file - '{}'".format(outfile))
            img.save(outfile)
        
    log.info("--------------------- End of File Processing -----------------------")   
   
    # If dataflag is still false, an explicitly requested combo of 
    # wafer and/or testset was not found, log a warning and return
    if not dataflag:
        log.warn("No data matching input wafer_id or testset!")
        return
       
    if options.dump_lotdata:
        dump_lotdata(lot)
 
    # Launch viewer and feed it the image if option was given
    if options.viewer:
        mv=Mapviewer()       
        wximage=mv.PilImageToWxImage(img, False)
        mv.show(wximage)
        mv.MainLoop()
    
    
    #Reset to default config for next file
    App.cfg = copy.deepcopy(App.default_cfg)
     
    #Delete the lot data
    del lot
    del wmap
    
    

def main():
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version=__version__)
    
    parser.add_option("-a", "--autosize",
                      action="store_false",
                      dest="autosize",
                      default=True,
                      help="Disable autosize mode")
        
    parser.add_option("-b", "--binmap",
                      action="store",
                      dest="binmap",
                      default=None,
                      help="Binmap should be either 'sbin' or 'hbin'")
    
    parser.add_option("-c", "--conf",
                      action="store",
                      dest="user_conf",
                      default=None,
                      help="Load a user configuration file")
    
    parser.add_option("-d", "--demo",
                      action="store",
                      dest="demo",
                      default=None,
                      help="Generate a Demo WaferMap, integer argument is number of wafers (1-99)")
    
    parser.add_option("-e", "--theme",
                      action="store",
                      dest="theme",
                      default=None,
                      help="Specify a theme configuration file")
    
    parser.add_option("-f", "--flag",
                      action="store_false",
                      dest="flag",
                      default=True,
                      help="Disable flagging multiple die results")
    
    parser.add_option("-g", "--good",
                      action="store",
                      dest="good_die",
                      default=None,
                      help="Specify Good Die Percentage - Applies to Demo ONLY")
    
    parser.add_option("-i", "--info",
                      action="store_true",
                      dest="lotinfo",
                      default=None,
                      help="Print Data Summary Info - Does not create map")
        
    parser.add_option("-l", "--loglevel",
                      action="store",
                      dest="loglevel",
                      default=None,
                      help="Override default Log Level")
    
    parser.add_option("-o", "--output",
                      action="store",
                      dest="outfile",
                      default=None,
                      help="Specify output image file")
                    
    parser.add_option("-q", "--quiet",
                      action="store_false", 
                      dest="verbose",
                      default=True,
                      help="Suppress messages")
    
    parser.add_option("-s", "--symbols",
                      action="store_false", 
                      dest="symbols",
                      default=True,
                      help="Disable Symbols")
    
    parser.add_option("-t", "--testset", 
                       action="store", 
                       dest="testset",
                       help="Select testset number - First test is 1, retests are 2,3 ...etc.")
      
    parser.add_option("-v", "--viewer",
                      action="store_true", 
                      dest="viewer",
                      default=False,
                      help="Launch MapViewer")
    
    parser.add_option("-w", "--wafer",
                      action="store", 
                      dest="waferid",
                      default=False,
                      help="Specify a single wafer ID within file")          
    
    parser.add_option("-x", "--width",
                      action="store", 
                      dest="baseWidth",
                      default=None,
                      help="Base Width of map (overrides default)")
    
    parser.add_option("-y", "--height",
                      action="store", 
                      dest="baseHeight",
                      default=None,
                      help="Base Height of map (overrides default)")
    
    parser.add_option("-z", "--dump",
                      action="store_true", 
                      dest="dump_lotdata",
                      default=None,
                      help="Dump lot data to screen")
    
    (options, args) = parser.parse_args()

   # Set application default configuration options
    App.autocfg(options)
    
    # Set up logger
    log = logging.getLogger()
    default_loglevel = 'logging.' + App.cfg['_loglevel'].upper()
    log.setLevel(eval(default_loglevel))
    
    if options.loglevel:
        if options.loglevel.upper() in ['NOTSET','DEBUG','INFO','WARNING','ERROR','CRITICAL']:
            logging.getLogger().setLevel(options.loglevel.upper())
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handler = logging.handlers.RotatingFileHandler( App.cfg['file']['logfile'], 
            maxBytes = App.cfg['file']['logfile_size'],
            backupCount = App.cfg['file']['logfile_rotates'])
    handler.setFormatter(formatter)
    log.addHandler(handler)
    
    # Add a stream handler to print messages to stdout
    if(options.verbose): 
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        log.addHandler(ch)
        
    log.info("Configuration information loaded from: {}".format(App.cfg['_config_file'])) 
    
    pp = pprint.PrettyPrinter(depth=6)
    if sys.platform == "win32" and args:
        for arg in args:
            if '*' in arg: 
                myargs = glob.glob(arg)
                args.remove(arg)
                args.extend(myargs)           
    
    pp.pprint(args)
    

    if(args):          
        for eachArg in args:
            App.cfg['runmode']='stdf'
 
            infile = check_infile(eachArg)
            if infile == None:
                continue
            options.infile = infile
            do_map(options)  #Demo = False, make a real map
    
    elif options.demo:
        if not is_int(options.demo, True):
            parser.error("-d argument must be an integer > 0!")        
        if options.good_die:
            App.cfg['demo']['random_yield'] = False
            App.cfg['demo']['fixed_yield'] = float(options.good_die)
            
        App.cfg['runmode']='demo'
        do_map(options)
            
    elif options.viewer:
        mv=Mapviewer()       
        mv.MainLoop()
        
    else: #nothing to do
        parser.print_help()
        exit(1)
        
    for handler in log.handlers:
        handler.close() 
        
 
if __name__ == '__main__':
    main()
