###########################################################
# $File: legend.py $
# $Author: daf $
# $Date: 2018-07-05 20:50:12 -0700 (Thu, 05 Jul 2018) $
# $Revision: 209 $
###########################################################
from PIL import ImageDraw, ImageFont
from config import App
import maputil

import logging
import constants

log = logging.getLogger(__name__)
        
class Legend:
    
#     legend = {}
#    bincount = {}

    # Crude autosizing method, could probably be improved...   
    def _autosize(self):
        
        # No science behind this... these values were created after a few
        # trial & errors for visual appearance.
        
        self.fontsize = App.cfg['image']['basewidth'] // 35
        self.fontsize = max(self.fontsize, 12)  #set an Absolute minimum
        self.boxsize = self.fontsize - self.fontsize//10
        self.hspace = self.fontsize//2
        self.padding = self.fontsize
        
        log.debug('legend fontsize = {}, boxsize={}'.format(App.cfg['legend']['fontsize'], App.cfg['legend']['boxsize']))
        log.debug('legend hspace = {}, padding = {}'.format(App.cfg['legend']['hspace'], App.cfg['legend']['padding'])) 
        
    def __init__(self):
        
        self.bincount = {}
                  
        # Conveniences to improve readability... 
        self.boxsize = App.cfg['legend']['boxsize']
        self.padding = App.cfg['legend']['padding']
        self.hspace = App.cfg['legend']['hspace']
        self.vspace = App.cfg['legend']['vspace']                
        self.fontname = App.cfg['legend']['font']
        self.fontsize = App.cfg['legend']['fontsize']
        self.fontcolor = App.cfg['legend']['fontcolor']
        self.autosize = App.cfg['legend']['autosize']
        self.showbincounts = App.cfg['legend']['show_bin_counts']
        self.sortbinsbycount = App.cfg['legend']['sort_bins_by_count'] 
        self.overflow_text = App.cfg['legend']['overflow_text']
        self.overflow_textcolor = App.cfg['legend']['overflow_textcolor']
                
        # Actual values set during getsize()
        self.maxfh = 0      # Max fontwidth of Bin label
        self.maxfw = 0      # Max fontheight of Bin label
        self.height = 0     
        self.width = 0      

    def getsize(self, dielist, testset):
                           
        for eachDie in dielist:
           
            #Count the number of Bin occurences
            if eachDie.testset == testset:
#                 print "X={}, Y={} hbin={}, sbin={}, testset={}, bc={}".format(
#                    eachDie.X, eachDie.Y, eachDie.hbin, eachDie.sbin, eachDie.testset,self.bincount)
                mybin = getattr(eachDie,App.cfg['binmap'])
                if not mybin in self.bincount:
                    self.bincount[mybin] = 1
                else:
                    self.bincount[mybin] += 1 
        
        if self.autosize:
            self._autosize()
            
        # Get the maximum length & height of legend text
        self.font = ImageFont.truetype(self.fontname, self.fontsize, encoding="unic")      
        for k, v in self.bincount.items():
            if self.showbincounts:
                string = "Bin {} : {} [{}]".format(k,App.cfg['bin'][str(k)]['label'],v)
            else:
                string = "Bin {} : {}".format(k,App.cfg['bin'][str(k)]['label'])
                
            fw, fh = self.font.getsize(string)
            self.maxfw = max(self.maxfw, fw)
            self.maxfh = max(self.maxfh, fh)
    
        count = len(self.bincount)
        log.debug('Max Legend font string size:  Width = {}, Height = {}'.format(self.maxfw, self.maxfh))
        log.debug("Number of Legend Bins = {}".format(count))
        
        self.width = (self.padding * 2) + self.boxsize + self.hspace + self.maxfw  
        self.height = (self.padding * 2) + (count * self.maxfh) + ((count - 1) * self.vspace)
        self.height = (count * self.maxfh) + ((count - 1) * self.vspace)
        self.boxsize = min(self.boxsize, self.maxfh + 1)
#         print "width={}, pad={}, boxsize={}, hspace={}, maxfw={}".format(self.width, self.padding, self.boxsize, self.hspace, self.maxfw)
#         print "count={}, height={}, vspace={}, maxfh={}".format(count, self.height, self.vspace, self.maxfh)       

    
    def render(self,img,x,y):
                   
        maxheight=img.height
        
        dr=ImageDraw.Draw(img)
#         print "img.width = {}, img.height={}, x={}, y={}, leg.width = {}, leg.height={}".format(
#             img.width, img.height, x, y, self.width, self.height)
        
        boxslack = (self.maxfh - self.boxsize) / 2
        
        box_X = x + self.padding
        box_Y = y + boxslack     
        strx = box_X + self.boxsize + self.hspace  # X location of text
#         dr.rectangle([x, y, x+self.width, y+self.height], fill='#CCCCCC', outline=(0, 0, 0))
        
        # Sort displayed bincounts either by bincount or bin number
        # depending on config value
        
        if self.sortbinsbycount: 
            sortbins = 'lambda kv: kv[1]'
            sortrev = True
        else:
            sortbins = 'lambda kv: kv[0]'
            sortrev = False
        
        for key, value in sorted(self.bincount.items(), key=eval(sortbins), reverse=sortrev):
            if self.showbincounts:
                string = "Bin {} : {} [{}]".format(key, App.cfg['bin'][str(key)]['label'],value)
            else:
                string = "Bin {} : {}".format(key, App.cfg['bin'][str(key)]['label'])   
            dr.rectangle([box_X, box_Y, box_X + self.boxsize, box_Y + self.boxsize+1], fill=(App.cfg['bin'][str(key)]['color']), outline=(0, 0, 0))

            if App.cfg['enable_symbols']:
                maputil.do_symbol(dr,box_X,box_Y,box_X + self.boxsize,box_Y+self.boxsize+1, True, **App.cfg['bin'][str(key)])
            
            dr.text((strx, y), string, self.fontcolor, self.font)
            y += self.maxfh + self.vspace
            box_Y = y + boxslack
            
            # Bin list will overflow the available canvas space...  
            # print overflow text and break loop
            if((y + self.maxfh * 2)  + self.padding > maxheight):
                dr.text((strx, y), self.overflow_text, self.overflow_textcolor, self.font)
                break
            
    
  
            
 
            
 
        


                    

                                       