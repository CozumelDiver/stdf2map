###########################################################
# $File: demodata.py $
# $Author: daf $
# $Date: 2018-01-22 12:03:01 -0800 (Mon, 22 Jan 2018) $
# $Revision: 207 $
###########################################################
import random
import math
import time
import logging
from wafer import DemoLot, Wafer, WaferDie
from config import App


log = logging.getLogger(__name__)

#Check if point is within a circle
def _in_radius(cx, cy, r, x, y):
    return math.hypot(cx - x, cy - y) <= r

#Check if a box is fully within a circle
def _box_in_radius(x1,y1,x2,y2,cx,cy,r):
    if not _in_radius(cx,cy,r,x1,y1):
        return False
    if not _in_radius(cx,cy,r,x2,y1):
        return False
    if not _in_radius(cx,cy,r,x1,y2):
        return False
    if not _in_radius(cx,cy,r,x2,y2):
        return False
    return True

# Return a bin number between min and max 
# that is NOT good_die_bin
def failing_bin(min, max, good_die_bin):
    binnum = good_die_bin
    while binnum == good_die_bin:       
        binnum = random.randint(min ,max)
    return binnum
        
def generate_lot(wafer_count = 1):
    
    # Put a practical upper limit on the number of wafers in the lot...
    wafer_count = min(wafer_count,99)
    
    x1 = App.cfg['demo']['min_X']
    x2 = App.cfg['demo']['max_X']
    y1 = App.cfg['demo']['min_Y']
    y2 = App.cfg['demo']['max_Y']  
    
    # Create Lot  
    lot = DemoLot()
    
    # All wafers in a lot will have SAME diecount
    if App.cfg['demo']['random_diecount'] and not App.cfg['demo']['random_diecount_eachwafer']: 
        (x1, x2, y1, y2) = random_diecount("(ALL)") 
    
    # Create wafers
    for wfr in range(0, wafer_count):
        # All wafers in a lot will have RANDOM diecount
        wafer_id = "{:>02d}".format(wfr+1)
        if App.cfg['demo']['random_diecount_eachwafer']: 
            (x1, x2, y1, y2) = random_diecount(wafer_id) 

        lot.wafers.append(generate_wafer(wafer_id,x1,x2,y1,y2))
        
    return lot 
        
#Generate some dummy wafer data           
def generate_wafer(wafer_id, min_X, max_X, min_Y, max_Y):
    
    start_t = random.randint(1,int(time.time()))
    
    wfr=Wafer(1, 255, start_t, wafer_id, demo=True)
    #self.lot.cur_wafer = Wafer(self.data['HEAD_NUM'], self.data['SITE_GRP'], self.data['START_T'], self.data['WAFER_ID'])
    
    # Conveniences...

    minbin = App.cfg['demo']['minbin']
    maxbin = App.cfg['demo']['maxbin']
    good_die_bin = App.cfg['good_die_bin']
    min_yield = float(App.cfg['demo']['minimum_yield'])
    
    if App.cfg['demo']['random_yield'] == False:
        die_yield = App.cfg['demo']['fixed_yield']
    else:
        die_yield = random.uniform(min_yield, 100.0)
    
         
    log.debug("Bin Range = {} - {}".format(minbin,maxbin))
    log.debug("good_die_bin = {}, die_yield = {}".format(good_die_bin, die_yield))
       
    if not (minbin <= good_die_bin <= maxbin):
        raise ValueError("good_die_bin must be between minbin and maxbin inclusive!")
    
    col_count = max_X - min_X
    row_count = max_Y - min_Y 
    Y_pixels = col_count
    X_pixels = row_count
    
    radius= (X_pixels * Y_pixels)//2
    midx = (X_pixels * Y_pixels)//2
    midy = (X_pixels * Y_pixels)//2
    log.info("Demo Test Set Count = {}".format(App.cfg['demo']['testcount']))
    
    for testset in range(1, int(App.cfg['demo']['testcount']) + 1):
        if testset not in wfr.testcounts:
            wfr.testcounts[testset] = 0     #initialize counter
        for row in range(min_Y,max_Y):
            for col in range(min_X,max_X):
                binnum = good_die_bin
                x1= (col - min_X) * X_pixels
                y1= (row - min_Y) * Y_pixels
                x2 = x1 + X_pixels
                y2 = y1 + Y_pixels       
             
                if _box_in_radius(x1,y1,x2,y2,midx,midy,radius):
                    d=WaferDie(col,row,binnum,binnum, testset=testset)                                  
                    wfr.dielist.append(d)                   
                    wfr.testcounts[testset] += 1
     
    # Die at this point all have failing bin numbers.  Turn a bunch of them into    
    # {good_die_bin} according to the value in the config file (or specified by 
    # the -g option)
    die_count = len(wfr.dielist)
    wfr.part_cnt = die_count
    
    log.debug("Demo Die Count = {}".format(die_count))
    
    good_die_count = 0
        
    #Enforce fixed_yield limits
    die_yield = min(die_yield,100.0)
    die_yield = max(die_yield,0.0)
    

    tmpidx=[]    
    die_pct = 100.0  # All die were created as good die
    
    if die_yield == 100.0: # All die were marked good when created, nothing to do...
        pass
 
    elif die_yield == 0.0:  # Mark all die bad
       for d in wfr.dielist:
            d.sbin = d.hbin = failing_bin(minbin, maxbin, good_die_bin)      
               
    elif die_yield > 50.0:  # Mark enough die bad to get to desired yield
        while (die_pct > die_yield):
            random_die = random.randint(0, die_count-1)
            if random_die not in tmpidx:
                binnum = failing_bin(minbin, maxbin, good_die_bin)
                tmpidx.append(random_die)
                wfr.dielist[random_die].sbin=binnum
                wfr.dielist[random_die].hbin=binnum
                good_die_count = die_count - len(tmpidx)
                die_pct = (float(good_die_count) / float(die_count)) * 100.0
    else:  # Mark all die bad, then mark enough good to get to desired yield
        for d in wfr.dielist:
            d.sbin = d.hbin = failing_bin(minbin, maxbin, good_die_bin)
        die_pct = 0.0         
        while (die_pct < die_yield):
            random_die = random.randint(0, die_count-1)
            if random_die not in tmpidx:
                tmpidx.append(random_die)
                wfr.dielist[random_die].sbin=good_die_bin
                wfr.dielist[random_die].hbin=good_die_bin
                good_die_count = len(tmpidx)
                die_pct = (float(good_die_count) / float(die_count)) * 100.0            
            
        
    wfr.good_cnt = good_die_count
    log.info("Good Die Count = {} Yield: {:.2f}%  (Requested Yield = {:.2f})".format(good_die_count, die_pct, die_yield))
        
    
    #Setup the bin dictionary for MULTITEST Flag detection.   
    for eachDie in wfr.dielist:
        xystr="{}|{}".format(eachDie.X, eachDie.Y)
        if xystr not in wfr.diedict:
            wfr.diedict[xystr]={'testset':testset,'sbin':[], 'hbin':[]}
                    
        wfr.diedict[xystr]['sbin'].append(eachDie.sbin)
        wfr.diedict[xystr]['hbin'].append(eachDie.hbin)
        wfr.diedict[xystr]['testset'] = eachDie.testset        
        
    return wfr


def random_diecount(wafer_id):
    
    # Conveniences...
    min_X = App.cfg['demo']['min_X']
    max_X = App.cfg['demo']['max_X']
    min_Y = App.cfg['demo']['min_Y']
    max_Y = App.cfg['demo']['max_Y']  
    
    if App.cfg['demo']['random_diecount']:
  

        rangeX = max_X - min_X
        rangeY = max_Y - min_Y
        
        # Divide the ranges in half, then take a random
        # number from each half.        
        min_X1 = random.randint(min_X, min_X + (rangeX)//2 - 1)
        max_X1 = random.randint(max_X - (rangeX)//2 + 1, max_X)       
        min_Y1 = random.randint(min_Y, min_Y + (rangeY)//2 - 1)
        max_Y1 = random.randint(max_Y - (rangeY)//2 + 1, max_Y)
#         print "minx1: {} - {}".format(min_X, min_X + (rangeX)//2 - 1)
#         print "maxx1: {} - {}".format(max_X - (rangeX)//2 + 1, max_X)
#         print "miny1: {} - {}".format(min_Y, min_Y + (rangeY)//2 - 1)
#         print "maxy1: {} - {}".format(max_Y - (rangeY)//2 + 1, max_Y)
                       
    
        min_X = min_X1
        max_X = max_X1
        min_Y = min_Y1
        max_Y = max_Y1
        
    log.info("Wafer {} Demo Die Range X: {:=d} to {:+d}   Y: {:+d} to {:+d}".format(
        wafer_id, min_X, max_X, min_Y, max_Y))        
  
    
    return(min_X, max_X, min_Y, max_Y)
    
