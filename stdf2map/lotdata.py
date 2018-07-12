###########################################################
# $File: lotdata.py $
# $Author: daf $
# $Date: 2018-01-20 03:24:26 -0800 (Sat, 20 Jan 2018) $
# $Revision: 202 $
###########################################################
import demodata
import logging
import constants
from config import App
#from Dumper import Dumper

#from config import App
# from legend import Legend
# from PIL import Image, ImageDraw
#from stdfparser import parser
#from wafer import Wafer, WaferDie
from util import check_bindict, log_duplicate_die
from stdfdata import stdfdata


log = logging.getLogger(__name__)

def lotdata(options):
    
    # Options.demo will contain the count of demo 
    # wafers to make
    if options.demo:
        lot = demodata.generate_lot(int(options.demo))
        
    elif options.infile:
        log.info("Processing input file - '{}'".format(options.infile))
        lot = stdfdata(options.infile)   
    
    else:
        log.info("Bug alert... Should never see this! (options.demo = False AND options.infile = False)")
        
     
    # Some of the sample stdf files I have were created by a software analysis program and
    # do not include a WCR.  Ensure we at least have a WF_FLAT entry...  
    if 'WF_FLAT' not in lot.wcr:
        lot.wcr['WF_FLAT'] = ''
        
    # set multitest flags
    mybin = App.cfg['binmap']
    for wfr in lot.wafers:
        for eachEntry in wfr.diedict:
        
            wfr.diedict[eachEntry]['flags']=0
            binlist = wfr.diedict[eachEntry][mybin]
#             print binlist
            if len(binlist) > 1:
                wfr.diedict[eachEntry]['flags'] |= constants.FLAG_MULTITEST       
                if min(binlist) != max(binlist):  
                    wfr.diedict[eachEntry]['flags'] |= constants.FLAG_SPLIT_BIN  
                else:
                    wfr.diedict[eachEntry]['flags'] |= constants.FLAG_DUPLICATE_BIN     

        # Check the wfr.dielist bin dictionary to ensure there is an entry 
        # for every bin. (Only a few are specified in config.py, though
        # others may be present from optional conf files) 
        # If a bin is not found in the dielist, add one with a random 
        # color value

        check_bindict(wfr.dielist)
    
        # Check wafer flags to see if any duplicate bin data should be logged
        if App.cfg['duplicate_die_warnings']:
            log_duplicate_die(wfr)
        
#         dumper=Dumper(max_depth=3)
#         print (dumper.dump(wfr))
        
    return lot