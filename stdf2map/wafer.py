###########################################################
# $File: wafer.py $
# $Author: daf $
# $Date: 2018-01-20 00:33:05 -0800 (Sat, 20 Jan 2018) $
# $Revision: 189 $
###########################################################
import random
import time
#from config import App

# Some random name to use as demo Part types
OldTimers = ['Aphrodite','Apollo','Athena','Dionysus','Hephaestus','Proteus','Telchines','Lycos',
             'Hyperion','Phorcys','Acheron','Cerberus','Cronus','Pontus','Iacchus','Charon','Furia',
             'Heracles','Echo','Zeus','Thor','Poseidon','Dionysus','Prometheus','Concordia', 
             'Artemis','Vulcan','Mercury','Venus','Earth','Mars','Jupiter','Saturn','Uranus',
             'Neptune','Pluto','Perses','Atlas','Helios']

# For selection of random Lot Id's
AlphaStr='ABCDEFGHJKLMNPRSTUVWXYZ'

# Major flat locations
Flats = 'UDLR'

class WaferDie(object):
 
    def __init__(self,X,Y,hbin,sbin,partid=None,flags=0, partflag=0, testset=0):
        self.X=X
        self.Y=Y
        self.hbin=hbin
        self.sbin=sbin
#         self.partid=partid
        self.flags=flags
        self.partflag = partflag
        self.testset=testset
        


class Wafer(object):
    
    def __init__(self, head_num, site_grp, start_t, wafer_id, demo=False):
            
        self.head_num = head_num
        self.site_grp = site_grp
        self.start_t = start_t
        self.finish_t = None
        self.part_cnt = 4294967295
        self.good_cnt = 4294967295
        self.rtst_cnt = 4294967295
        self.abrt_cnt = 4294967295
        self.func_cnt = 4294967295
        self.map_yield = 0
        self.wafer_id = wafer_id
        self.sbr=[]
        self.hbr=[]
        self.testcounts={}
        self.dielist=[]
        self.diedict={}
        self.legend={} 
            
        
class Lot(object):
    
    def __init__(self):
    
        self.mir={}
        self.mrr={}
        self.wcr = {
            'WAFR_SIZ': 0,  
            'WF_FLAT' : ' ',
            'WF_UNITS': 0,
            'DIE_HT': 0,
            'DIE_WID': 0,
            'CENTER_X': -32768,
            'CENTER_Y': -32768,
            'POS_X': ' ',
            'POS_Y': ' '
            } 
               
        self.wafers=[]
        self.sbr=[]
        self.hbr=[]
        self.cur_wafer=None
        self.open_wafer_flag = False
        
class DemoLot(Lot):
    
    # For Demo, just fill MIR, MRR and WCR with some random data... 
    def __init__(self):
        super(DemoLot, self).__init__()
        random_date = random.randint(1,int(time.time()))
        self.mir = {
            'LOT_ID': random.choice(AlphaStr) + random.choice(AlphaStr) + random.choice(AlphaStr) + str(random.randint(10000,99999)),
            'PART_TYP': random.choice(OldTimers),
            'SETUP_T': random_date,
            'START_T': random_date + random.randint(30,300),
            'TSTR_TYP': 'DEMO',
            'MODE_COD': 'E'
            }
        
        # MRR, Don't actually use any of this, just for --info command line option
        self.mrr = {
            'FINISH_T': random_date + random.randint(500,50000),
            'DISP_COD': None,
            'USR_DESC': "Demo Data generated with STDF2MAP"
            }
        
        # For Demo, set a random flat
        self.wcr['WF_FLAT'] = random.choice(Flats)

        
