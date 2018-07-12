###########################################################
# $File: util.py $
# $Author: daf $
# $Date: 2018-01-20 01:45:55 -0800 (Sat, 20 Jan 2018) $
# $Revision: 197 $
###########################################################
import random
import logging
import constants
import os.path
import datetime
import pprint

from demofail import demofail
from filename import make_filename

import re

#from wafer import Wafer
from config import App

log = logging.getLogger(__name__)

def _clamp(x): 
    return max(0, min(x, 255))        

def randcolor(websafe=True):
    r=(random.randint(0,255))
    g=(random.randint(0,255))
    b=(random.randint(0,255))
    
    if websafe:
        r = int( (float(r)/255) * 5)  * 51
        g = int( (float(g)/255) * 5)  * 51
        b = int( (float(b)/255) * 5)  * 51
        
    return("#{0:02x}{1:02x}{2:02x}".format(_clamp(r), _clamp(g), _clamp(b)))

'''
Check the bin dictionary to ensure there is an entry for every bin in the 
dielist.  If there isn't add one with a random color value
'''
def check_bindict(dielist):
    
    for eachDie in dielist:
        mybin = getattr(eachDie,App.cfg['binmap'])
        if str(mybin) in App.cfg['bin']:
            pass    #Bin exists, don't need to do anything
        else:
            if App.cfg['runmode'] == 'demo':
                App.cfg['bin'][str(mybin)]={'color':randcolor(),'label':random.choice(demofail)} 
            else:
                App.cfg['bin'][str(mybin)]={'color':randcolor(),'label':'-'}
        
def log_duplicate_die(wfr):
    
    for eachDie in wfr.dielist:
        
        if eachDie.flags & constants.FLAG_DUPLICATE_BIN:
            log.info('%s: duplicate die probed at (%d.%d) resulting in SAME bin failure [%d]' % 
                     (wfr.waferid,eachDie.X, eachDie.Y, eachDie.sbin))

        if eachDie.flags & constants.FLAG_SPLIT_BIN:
            log.warn('%s: duplicate die probed at (%d.%d) resulting in DIFFERENT bin failures' % 
                     (wfr.waferid,eachDie.X, eachDie.Y))
        


def get_outfile(options, lot, wfr):
    
    if(options.outfile):
        head, tail = os.path.split(options.outfile)
        if(head):
            if not os.path.exists(os.path.abspath(head)):
                os.makedirs(os.path.abspath(head))  
        outfile = make_filename(lot.mir, wfr, head, tail)
    else:
        outpath = App.cfg['file']['map_path']       
        outfile = make_filename(lot.mir, wfr, outpath, basefile=None, thumb_mode=App.cfg['file']['thumb_mode'])     
        
    return outfile

def check_infile(filename):
    
#     print "filename = {}".format(filename)
    
    tmpfile = os.path.abspath(filename)
    filelist = []
    
    # First check for file exactly as entered
    filelist.append(filename)
    if os.path.isfile(filename):
#         print "1:returning...{}".format(filename)
        return filename
    
    # Next, add .stdf if it doesn't exist and try again
    if  not re.search('\.stdf$',filename,flags=re.IGNORECASE):
        stdffile = tmpfile + '.stdf'
        filelist.append(stdffile)
        if os.path.isfile(stdffile):
#             print "2:returning...{}".format(stdffile)
            return stdffile
    
    # Check for file in stdf directory
    tmpfile = os.path.join(App.cfg['file']['stdf_path'], filename)
    filelist.append(tmpfile)
    if os.path.isfile(tmpfile):
#         print "3:returning...{}".format(tmpfile)
        return tmpfile
    
    # Add .stdf if it doesn't exist and try again
    if  not re.search('\.stdf$',tmpfile,flags=re.IGNORECASE):
        stdffile = tmpfile + '.stdf'
        filelist.append(stdffile)
        if os.path.isfile(stdffile):
#             print "4:returning...{}".format(stdffile)
            return stdffile
    
    #Give up!
    log.error("Cannot locate input file - '{}'".format(filename))
    log.info("Failed to find files: {}".format(filelist))
    
    return(None) 

# Test to see if wafer_id specified by -w command line option 
# is equivalent to actual wafer_id in stdf file.  
# Test #1 - Case insensitive string comparison, returns true if strings equal
# Test #2 - If input is convertible to int and numbers are equal, return true
# Return False if either test fails
def wfr_equivalence(str1,str2):
    
    if str1.lower() == str2.lower():
        return True
    
    if is_int(str1) and is_int(str2):
        if int(str1) == int(str2):
            return True
        
    return False

# Try to convert an input string to an integer. 
def is_int(input, posval=False):
    try:
        num = int(input)
    except ValueError:
        return False
    
    if posval and num < 1:
        return False
    
    return True

def map_yield(wfr, testset):
    
    passcount=0
    totalcount=0
    
    for eachDie in wfr.dielist: 
        if eachDie.testset != testset:
            continue
        totalcount +=1
        mybin = getattr(eachDie,App.cfg['binmap'])
        if mybin == App.cfg['good_die_bin']:
            passcount +=1
    
    if totalcount > 0:
        yieldpct = float(passcount)/float(totalcount) * 100
    else:
        yieldpct = 0.0
        
    return (yieldpct)


# Debugging aid to show center            
#         dr.point([cx,cy],fill='black')
      
def lotinfo(lot):
    pp = pprint.PrettyPrinter(indent=4)
    units = {'0':'Unknown', '1':'Inches', '2':'Centimeters', '3':'Millimeters', '4':'Mils'}
    
    print "MIR:PART_TYP ....... {}".format(lot.mir['PART_TYP'] )   
    print "MIR:LOT_ID ......... {}".format(lot.mir['LOT_ID'] )
    print "MIR:TSTR_TYP   ..... {}".format(lot.mir['TSTR_TYP'] )
    print "MIR:SETUP_T ........ {}".format(datetime.datetime.fromtimestamp(float(lot.mir['SETUP_T'])).strftime('%Y-%m-%d  %H:%M'))
    print "MIR:START_T ........ {}".format(datetime.datetime.fromtimestamp(float(lot.mir['START_T'])).strftime('%Y-%m-%d  %H:%M'))    
    print "MIR:MODE_COD ....... {}".format(lot.mir['MODE_COD'])
    print "-----------------------------------------"
    print "WCR:WAFR_SIZ ....... {}".format(lot.wcr['WAFR_SIZ'])
    print "WCR:WF_FLAT ........ {}".format(lot.wcr['WF_FLAT'])
    print "WCR:WF_UNITS ....... {} ({})".format(lot.wcr['WF_UNITS'],units[str(lot.wcr['WF_UNITS']) ])
    print "WCR:DIE_HT ......... {}".format(lot.wcr['DIE_HT'])
    print "WCR:DIE_WID ........ {}".format(lot.wcr['DIE_WID'])
    print "WCR:CENTER_X ....... {}".format(lot.wcr['CENTER_X'])
    print "WCR:CENTER_Y ....... {}".format(lot.wcr['CENTER_Y'])
    print "WCR:POS_X .......... {}".format(lot.wcr['POS_X'])
    print "WCR:POS_Y .......... {}".format(lot.wcr['POS_Y'])    
    print "    ------------------------------------------"     
    for w in lot.wafers:
        print "    WIR:WAFER_ID ........... {}".format(w.wafer_id)
        print "    WIR:START_T ............ {}".format(datetime.datetime.fromtimestamp(float(w.start_t)).strftime('%Y-%m-%d  %H:%M'))
        print "    WRR:FINISH_T ........... {}".format(datetime.datetime.fromtimestamp(float(w.finish_t)).strftime('%Y-%m-%d  %H:%M'))
        print "    WRR:PART_CNT ........... {}".format(w.part_cnt)
        print "    WRR:GOOD_CNT ........... {}".format(w.good_cnt)
        print "    WRR:RTST_CNT ........... {}".format(w.rtst_cnt)        
        print "      >> Die Found  ........ {}".format(len(w.dielist))
        print "      >> Die Test Counts ... {}".format(w.testcounts)
        print "    ------------------------------------------"

    print "HBR: {}".format("FOUND" if lot.hbr else "NOT FOUND")
    print "SBR: {}".format("FOUND" if lot.sbr else "NOT FOUND")    
    print "MRR:FINISH_T ....... {}".format(datetime.datetime.fromtimestamp(float(lot.mrr['FINISH_T'])).strftime('%Y-%m-%d  %H:%M'))
    print "MRR:DISP_COD ....... {}".format(lot.mrr["DISP_COD"])
    print "MRR:USR_DESC ....... {}".format(lot.mrr['USR_DESC'])
    print "MRR:EXC_DESC ....... {}".format(lot.mrr['EXC_DESC'])              
              
def dump_lotdata(lot):
    
    pp = pprint.PrettyPrinter(indent=4)
    print "=================================================================="
    print " Lot Data Dump"
    print "=================================================================="   
    print "Lot ID......... {}".format(lot.mir['LOT_ID'])
    print "Part........... {}".format(lot.mir['PART_TYP'])
    print "Date........... {} ({})".format(lot.mir['START_T'], datetime.datetime.fromtimestamp(float(lot.mir['START_T'])).strftime('%Y-%m-%d  %H:%M'))
    print "Flat........... {}".format(lot.wcr['WF_FLAT'])

    print "==================================================================" 
    print " "     
    for wfr in lot.wafers:
        print '----------------------------'
        print ' Wafer_ID ...... {}                Dielist:'.format(wfr.wafer_id)
        print '----------------------------'      
        print '      Count      X    Y  HBIN      SBIN      Flags     PartFlag       Testset'
        print '     ----------------------------------------------------------------------------'
        idx = 0
        for eachDie in wfr.dielist:

            idx+=1
            print '      {:0>5d}:  {:-4d},{:-4d}  hbin={:3d}  sbin={:3d}  flags={:2d}  partflag={}  testset={:2d} '.format(
                idx, eachDie.X, eachDie.Y, eachDie.hbin, eachDie.sbin, eachDie.flags, eachDie.partflag, eachDie.testset)
        
        print " "
        print '     ----------------------------------------------------------------------------'
        print "                               Die Bin Dictionary "
        print '     ----------------------------------------------------------------------------'
        print '      Count     X|Y      HBIN Array              SBIN Array         Flags ' 
        print '     ----------------------------------------------------------------------------'
        idx = 0      
        for i in wfr.diedict:
            idx+=1
            print "      {:0>5d}:  {:>6}  hbin={:>15}    sbin={:>15}  flags={}".format(
                idx, i, wfr.diedict[i]['hbin'], wfr.diedict[i]['sbin'], wfr.diedict[i]['flags'])
    
    print " "
    print "==================================================================" 
    print " Configuraton for last wafer ran "
    print "------------------------------------------------------------------"      

    pp.pprint(App.cfg)
    
    print " "
    print "==================================================================" 
    print " Default Configuraton (may be different than above...)"
    print "------------------------------------------------------------------"      

    pp.pprint(App.default_cfg)    
 
    print " "    
    print "--------------------------- END -----------------------------------" 
    
