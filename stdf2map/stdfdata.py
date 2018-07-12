###########################################################
# $File: stdfdata.py $
# $Author: daf $
# $Date: 2018-01-17 02:31:07 -0800 (Wed, 17 Jan 2018) $
# $Revision: 182 $
###########################################################
#import constants
import logging

from wafer import Lot, Wafer, WaferDie
from stdfparser import parser

log = logging.getLogger(__name__)
#----------------------------------------------------------------------------
# stdf parser from: https://code.google.com/archive/p/stdfparser/
# by Hua Yanghao  GPLv3
#----------------------------------------------------------------------------
class Get_Stdf(parser):
    
    def take(self, typsub):
        

# 
#         if str(self.Cur_Rec) == 'Mir':
#             self.wfr.lotid=self.data['LOT_ID']
#             self.wfr.part=self.data['PART_TYP']
#             
#             if loglevel == logging.DEBUG:
#                 print "======================= {} =======================".format(str(self.Cur_Rec))    
#                 for i,j in self.Cur_Rec.fieldMap:
#                     print "{}:{}".format(i,str(self.data[i]))
#  
#         if str(self.Cur_Rec) == 'Wcr':
#             self.wfr.flat=self.data['WF_FLAT']
#             
#             if loglevel == logging.DEBUG:
#                 print "======================= {} =======================".format(str(self.Cur_Rec))
#                 for i,j in self.Cur_Rec.fieldMap:
#                     print "{}:{}".format(i,str(self.data[i]))
#             
#         if str(self.Cur_Rec) == 'Wir':
#             self.wfr.date=self.data['START_T']
#             
#             if loglevel == logging.DEBUG:
#                 print "======================= {} =======================".format(str(self.Cur_Rec))
#                 for i,j in self.Cur_Rec.fieldMap:
#                     print "{}:{}".format(i,str(self.data[i]))
# 
#                 
#         if str(self.Cur_Rec) == 'Wrr':
#             self.wfr.waferid=self.data['WAFER_ID']
#             self.wfr.goodcount=self.data['GOOD_CNT']
#             self.wfr.partcount=self.data['PART_CNT']
#             self.wfr.retestcount=self.data['RTST_CNT']
#             
#             if loglevel == logging.DEBUG: 
#                 print "======================= {} =======================".format(str(self.Cur_Rec))           
#                 for i,j in self.Cur_Rec.fieldMap:
#                     print "{}:{}".format(i,str(self.data[i]))
#                           
#                 
#         if str(self.Cur_Rec) == 'Prr':
#             
#             # internal flags, not part of STDF Record
#             flags = 0
#             
#             # Conveniences
#             xcoord = self.data['X_COORD']
#             ycoord = self.data['Y_COORD']
#             hbin = self.data['HARD_BIN']
#             sbin = self.data['SOFT_BIN']
#             partflag = self.data['PART_FLG']
#             
#             xystr="{}|{}".format(xcoord, ycoord)
#             xybinstr="{}|{}|{}|{}".format(xcoord, ycoord, hbin, sbin)
#             testset=0
#             if xystr not in self.wfr.diedict:
#                 self.wfr.diedict[xystr]={'testset':testset,'sbin':[], 'hbin':[]}
# 
#             if xystr in self.wfr.diedict:
#                 testset=self.wfr.diedict[xystr]['testset'] + 1
#                                  
#             d=WaferDie(xcoord, ycoord, hbin, sbin , flags=flags, partflag=partflag, testset=testset)
# 
#             self.wfr.diedict[xystr]['sbin'].append(sbin)
#             self.wfr.diedict[xystr]['hbin'].append(hbin)
#             self.wfr.diedict[xystr]['testset'] = testset
#             
#             self.wfr.dielist.append(d)
#             
#             if loglevel == logging.DEBUG:            
#                 print "======================= {} =======================".format(str(self.Cur_Rec))
#                 for i,j in self.Cur_Rec.fieldMap:
#                     print "{}:{}".format(i,str(self.data[i]))


#     def setup(self):
#         pass
# 
#     def cleanup(self):
#         pass
#              
#     def file_setup(self): pass
# 
#     def file_cleanup(self): pass

        loglevel = logging.getLogger().getEffectiveLevel()
                     
        if str(self.Cur_Rec) == 'Mir':
#             tmp ={}
            for i,j in self.Cur_Rec.fieldMap:
                self.lot.mir[i]  = str(self.data[i])
            
#             self.lot.mir = tmp
            
            if loglevel == logging.DEBUG:            
                print "======================= {} =======================".format(str(self.Cur_Rec))
                for i,j in self.Cur_Rec.fieldMap:
                    print "{}:{}".format(i,str(self.data[i]))            
            

        if str(self.Cur_Rec) == 'Mrr':           
            for i,j in self.Cur_Rec.fieldMap:
                self.lot.mrr[i]  = str(self.data[i])
            
#             self.lot.mrr = tmp
            
            if loglevel == logging.DEBUG:            
                print "======================= {} =======================".format(str(self.Cur_Rec))
                for i,j in self.Cur_Rec.fieldMap:
                    print "{}:{}".format(i,str(self.data[i]))                     
 
        if str(self.Cur_Rec) == 'Sbr':          
            tmp ={}
            for i,j in self.Cur_Rec.fieldMap:
                tmp[i]  = str(self.data[i])
                 
            self.lot.sbr.append(tmp)
            
            if loglevel == logging.DEBUG:            
                print "======================= {} =======================".format(str(self.Cur_Rec))
                for i,j in self.Cur_Rec.fieldMap:
                    print "{}:{}".format(i,str(self.data[i]))                 
            
        if str(self.Cur_Rec) == 'Hbr':            
            tmp ={}
            for i,j in self.Cur_Rec.fieldMap:
                tmp[i]  = str(self.data[i])
                 
            self.lot.hbr.append(tmp) 
             
            if loglevel == logging.DEBUG:            
                print "======================= {} =======================".format(str(self.Cur_Rec))
                for i,j in self.Cur_Rec.fieldMap:
                    print "{}:{}".format(i,str(self.data[i]))                       
                           
        if str(self.Cur_Rec) == 'Wcr':                           
            for i,j in self.Cur_Rec.fieldMap:
                self.lot.wcr[i]  = str(self.data[i])
            
#             self.lot.wcr = tmp
            
            if loglevel == logging.DEBUG:            
                print "======================= {} =======================".format(str(self.Cur_Rec))
                for i,j in self.Cur_Rec.fieldMap:
                    print "{}:{}".format(i,str(self.data[i]))                 
        
        if str(self.Cur_Rec) == 'Wir':            
            if self.lot.open_wafer_flag:
                log.warn("WIR encountered before WRR...")
                self.lot.wafers.append(self.lot.cur_wafer)
                self.lot.open_wafer_flag = False
                
            self.lot.cur_wafer = Wafer(self.data['HEAD_NUM'], self.data['SITE_GRP'], self.data['START_T'], self.data['WAFER_ID'])
            log.info('Adding Wafer: WAFER_ID = {}'.format(self.data['WAFER_ID']))
            self.lot.open_wafer_flag = True
            
            if loglevel == logging.DEBUG:            
                print "======================= {} =======================".format(str(self.Cur_Rec))
                for i,j in self.Cur_Rec.fieldMap:
                    print "{}:{}".format(i,str(self.data[i]))     
            
        if str(self.Cur_Rec) == 'Wrr':
            self.lot.cur_wafer.finish_t = self.data['FINISH_T']
            self.lot.cur_wafer.part_cnt = self.data['PART_CNT']
            self.lot.cur_wafer.good_cnt = self.data['GOOD_CNT']
            self.lot.cur_wafer.rtst_cnt = self.data['RTST_CNT']
            
            self.lot.wafers.append(self.lot.cur_wafer)
            self.lot.open_wafer_flag = False
            self.lot.cur_wafer=None
            
            if loglevel == logging.DEBUG:            
                print "======================= {} =======================".format(str(self.Cur_Rec))
                for i,j in self.Cur_Rec.fieldMap:
                    print "{}:{}".format(i,str(self.data[i]))     
                               
        if str(self.Cur_Rec) == 'Prr':
            
            # internal flags, not part of STDF Record
            flags = 0
            
            # Conveniences
            xcoord = self.data['X_COORD']
            ycoord = self.data['Y_COORD']
            hbin = self.data['HARD_BIN']
            sbin = self.data['SOFT_BIN']
            partflag = self.data['PART_FLG']
            
            xystr="{}|{}".format(xcoord, ycoord)
            xybinstr="{}|{}|{}|{}".format(xcoord, ycoord, hbin, sbin)
            testset=0
            if xystr not in self.lot.cur_wafer.diedict:
                self.lot.cur_wafer.diedict[xystr]={'testset':testset,'sbin':[], 'hbin':[]}

            if xystr in self.lot.cur_wafer.diedict:
                testset=self.lot.cur_wafer.diedict[xystr]['testset'] + 1
            
            if testset not in self.lot.cur_wafer.testcounts:
                self.lot.cur_wafer.testcounts[testset] = 0     #initialize counter
                                
            d=WaferDie(xcoord, ycoord, hbin, sbin , flags=flags, partflag=partflag, testset=testset)
            
            self.lot.cur_wafer.testcounts[testset] += 1
            self.lot.cur_wafer.diedict[xystr]['sbin'].append(sbin)
            self.lot.cur_wafer.diedict[xystr]['hbin'].append(hbin)
            self.lot.cur_wafer.diedict[xystr]['testset'] = testset
            
            self.lot.cur_wafer.dielist.append(d)
            
            if loglevel == logging.DEBUG:            
                print "======================= {} =======================".format(str(self.Cur_Rec))
                for i,j in self.Cur_Rec.fieldMap:
                    print "{}:{}".format(i,str(self.data[i]))                 

    def file_cleanup(self):
        
        # if the open wafer flag is true, we had a WIR without a 
        # corresponding WRR... possible truncation or data loss.
        # "close" the current wafer and append it to the lot
        if self.lot.open_wafer_flag:
            self.lot.wafers.append(self.lot.cur_wafer)
            log.warn("Missing WRR, possible data truncation!")

def stdfdata(filename):
    
    stdf = Get_Stdf()
    stdf.lot = Lot()

#     stdf.Rec_Set = ['Mir','Wir','Wrr','Prr','Wcr'] 
    stdf.Rec_Set = ['Mir','Mrr', 'Wcr', 'Wir', 'Wrr', 'Prr','Sbr','Hbr']
    
    #NOTE: stdf.parse is looking for a "list" of filenames...
    stdf.parse( [filename] )
            
    
    return stdf.lot

