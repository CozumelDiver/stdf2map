###########################################################
# $File: wafermap.py $
# $Author: daf $
# $Date: 2018-01-22 12:04:47 -0800 (Mon, 22 Jan 2018) $
# $Revision: 208 $
###########################################################

import logging
import constants
import maputil
# import datetime
from legend import Legend
from title import Title
from config import App
from PIL import Image, ImageDraw, ImageFont

log = logging.getLogger(__name__)

class WaferMap:
 
    def __init__(self):
        self.img = None
        self.legend = Legend()
        self.title = Title()
        self.autosize = App.cfg['image']['autosize']
        self.autosize_minpx = App.cfg['image']['autosize_minpx']
        self.basewidth = App.cfg['image']['basewidth']
        self.baseheight = App.cfg['image']['baseheight']
        self.padding = App.cfg['image']['padding']
        self.showborder = App.cfg['image']['border']
        self.showtitle = App.cfg['title']['show']
        self.showlegend = App.cfg['legend']['show']
        self.showgrid = App.cfg['axis']['grid']
        self.showaxis = App.cfg['axis']['show']
        self.showflat = App.cfg['image']['flatline']
        self.showtimestamp = App.cfg['image']['timestamp']
        self.timestampcolor = App.cfg['image']['timestampcolor']
        self.bordercolor = App.cfg['image']['bordercolor']
        self.streetcolor = App.cfg['image']['streetcolor']
        self.flatcolor = App.cfg['image']['flatcolor']
        self.gridcolor = App.cfg['axis']['gridcolor']
        self.axiscolor = App.cfg['axis']['color']
        self.axisfont = App.cfg['axis']['font']
        self.bgcolor = App.cfg['image']['bgcolor']
      
    def buildmap(self, lot, wfr, testset):
    
        #---------------------------------------------------------------------------
        # Get actual extents... that is number of rows & cols in the wafermap, 
        # If the demodata routine was used, a random number of rows/cols were
        # generated.
        #--------------------------------------------------------------------------- 
        
        min_Y = min(d.Y for d in wfr.dielist)
        max_Y = max(d.Y for d in wfr.dielist)
        min_X = min(d.X for d in wfr.dielist)
        max_X = max(d.X for d in wfr.dielist)
        
        col_count = max_X - min_X+1
        row_count = max_Y - min_Y+1
        
        log.debug('Die Extents: X = {} to {}  Y = {} to {}'.format(min_X, max_X, min_Y, max_Y))
        log.debug('Columns (X) = {}, Rows (Y) = {} (Total Die={})'.format(col_count, row_count, len(wfr.dielist)))
        
         
        if self.basewidth >= self.baseheight:
            sizeRatio = float(self.basewidth) / float(self.baseheight)
        else:
            sizeRatio = float(self.baseheight) / float(self.basewidth)
             
        log.debug('Size Ratio: {:.2f}, width={}, height={}'.format(sizeRatio, self.basewidth, self.baseheight))
        
        
        #---------------------------------------------------------------------------
        # If image autosize is enabled, the canvas size may be increased to ensure
        # die are visible.  This will force a minimum pixel size of "autosize_minpx".
        # The original aspect ratio will be maintained.
        #---------------------------------------------------------------------------
        
        if self.autosize:
            
            autominX = (self.autosize_minpx * col_count) + (2 * self.padding)
            autominY = (self.autosize_minpx * row_count) + (2 * self.padding)
            log.debug('Autosize Minimum Map Size X={} Y={} at Autopx = {}'.format( 
                      autominX, autominY, self.autosize_minpx))
        
            if(autominX > self.basewidth):
                self.basewidth = autominX
                self.baseheight = int (float(self.basewidth) * float(sizeRatio))
                log.debug('Autosize (autominX > bw) Updated sizes - width={}, height={}, sizeRatio={}'.format(
                    self.basewidth, self.baseheight, float(sizeRatio)))
            elif (autominY > self.baseheight):
                self.baseheight = autominY
                self.basewidth = int (float(self.baseheight) * float(sizeRatio))
                log.debug('Autosize (autominY > bh) Updated sizes - width={}, height={}, sizeRatio={}'.format(
                    self.basewidth, self.baseheight, float(sizeRatio)))
            else:
                log.debug('Autosize sizing not required, width={}, height={}, autominX={}, autominY={}'.format(
                    self.basewidth, self.baseheight, autominX, autominY)) 
    
            
            #Store updated values back in cfg 
#             App.cfg['image']['basewidth'] = bw
#             App.cfg['image']['baseheight'] = bh
        
    
        
        # Nominal size of map excluding padding
        mapX = self.basewidth - (self.padding *2)
        mapY = self.baseheight - (self.padding *2)
        log.debug('Map Space (BaseSize - 2*Padding)  (X,Y)=({},{})  Padding = {}'.format(
            mapX, mapY, self.padding))
        
        
        # Calculate the die's pixel size - width (X) and height (Y) based on map size 
        # divided by the number of rows & columns
        X_pixels = mapX / col_count     #X-diesize in pixels
        Y_pixels = mapY / row_count     #Y diesize in pixels
        log.debug('Pixels per die: X={}, Y={}'.format(X_pixels, Y_pixels))
        
        #---------------------------------------------------------------------------
        # Unless the nominal image size (Canvas size minus padding) happens to be an
        # exact multiple of the calculated die size in pixels, we will have some 
        # space left on all sides.
        # Calculate the extra space so we can center the image on the canvas
        #---------------------------------------------------------------------------   
        slackX = (mapX - (X_pixels * col_count)) / 2
        slackY = (mapY - (Y_pixels * row_count)) / 2
        log.debug('Slack: X={}, Y={}'.format(slackX, slackY))
        log.debug('Calculated Map Size (excluding slack) - (X,Y) = ({},{})'.format( 
                  X_pixels * col_count, Y_pixels * row_count))
    #     
        #-------------------------------------------------------------------------
        # Have the legend calculate its size, it will be rendered later, but we
        # need to know the space it will take up so we can adjust the canvas size 
        # Actual Map width is then adjusted to allow for legend.
        #--------------------------------------------------------------------------
        actualWidth = self.basewidth
        if self.showlegend:
            self.legend.getsize(wfr.dielist, testset)
            actualWidth += self.legend.width
            log.debug('Legend Width = {}'.format(self.legend.width))
           
        #--------------------------------------------------------------------------
        # baseheight and fontsize adjusted for title
        #--------------------------------------------------------------------------
        # Start with a reasonable guess for the size of the title font and then
        # autosize it from there.   May not be the most efficient way to do 
        # this, but it works for now...
        #--------------------------------------------------------------------------
        actualHeight = self.baseheight
        titleheight = 0
        if self.showtitle:
            
            #A guess...
            title_fontsize = actualWidth//40    
            titlekeys = self.title.autosize(lot.mir, wfr, title_fontsize, testset)
            upsearch=False
            
            # While title string width at current font size is > canvas width, decrease 
            # font size and re-evaluate 
            if(titlekeys['maxfw'] > actualWidth):
                while titlekeys['maxfw'] > actualWidth:
                    upsearch=False
                    title_fontsize -= 1
                    titlekeys = self.title.autosize(lot.mir, wfr, title_fontsize, testset)
        #             print "D:imageWith = {}, fontsize = {}, maxfw={}, height={}".format(actualWidth, title_fontsize, titlekeys['maxfw'], titlekeys['maxfh'])
            # Otherwise, font is too small, increase it and re-evaluate
            else:
                while titlekeys['maxfw'] < actualWidth:
                    upsearch=True
                    title_fontsize += 1
                    titlekeys = self.title.autosize(lot.mir, wfr, title_fontsize, testset)
        #             print "U:imageWith = {}, fontsize = {}, maxfw={}, height={}".format(actualWidth, title_fontsize, titlekeys['maxfw'], titlekeys['maxfh'])    
        
            # If we were decreasing font size when the while condition became false, all the titlekeys are properly set, 
            # from the last loop cycle.... but if we were increasing font size, the last loop cycle left the titlekeys 
            # in a state for a larger font, so decrease the font size by one and re-evaluate the titlekeys
            if(upsearch):
                title_fontsize -=1
                titlekeys = self.title.autosize(lot.mir, wfr, title_fontsize, testset)
        
            titleheight = titlekeys['maxfh']
            
            # Increase canvas size to allow for title
            actualHeight += titleheight
            log.debug('Title Height = {}, Title Fontsize = {}'.format(titleheight, title_fontsize))
    
        #--------------------------------------------------------------------------
        # Adjust Width and Height for axis space
        #--------------------------------------------------------------------------
#         if self.showaxis:
#             actualWidth += axis_space
#             actualHeight += axis_space
        #--------------------------------------------------------------------------
        # Get axis space, add in 10 pixels for flat spacing.  (the axes are 
        # shifted left or up by 10 pixels when they are drawn to account for the
        # 10 pixels).
        #--------------------------------------------------------------------------
        axis_space = 0
        if self.showaxis:
            axis_space = maputil.do_axis(self, wfr.dielist, X_pixels, Y_pixels) + 10
            log.debug('Axis Space = {}'.format(axis_space))
            
        actualWidth += axis_space
        actualHeight += axis_space           
                      
        log.debug('Axis space = {}'.format(axis_space))    
        log.debug('Actual Image Size (X,Y) = ({},{})'.format(actualWidth, actualHeight))     

                            
        #--------------------------------------------------------------------------
        # Create the canvas and draw the wafermap
        #--------------------------------------------------------------------------
        self.img = Image.new('RGB', (actualWidth,actualHeight), self.bgcolor)
    
        # Get the drawable object...
        dr = ImageDraw.Draw(self.img)
        
        # map_extents are used for tracking the actual pixel extents of the drawn map which makes
        # calculating the location to draw the flat & axis labels a bit easier...
        
        map_extents = {'minx':65535, 'miny':65535, 'maxx':0, 'maxy':0}
        
        # limit flag_size factor to a minimum of 1.0 (or else flag will exceed die boundary)
        App.cfg['flag']['size_factor'] = max(App.cfg['flag']['size_factor'], 1.0)
        
        # if we want the grid, draw it first so it's behind everything else...
        if self.showgrid:   
            maputil.do_grid(self, wfr.dielist, X_pixels, Y_pixels, self.padding, axis_space, slackX, slackY, titleheight)
       
        idx=0       
        imap = []
        #-----------------------------------------------------------
        # Draw All die loop
        #-----------------------------------------------------------
        for eachDie in wfr.dielist:
            mybin=getattr(eachDie,App.cfg['binmap'])
            idx+=1      
            x1 = self.padding + axis_space + ((eachDie.X - min_X) * X_pixels) + slackX
            y1 = self.padding + axis_space + ((eachDie.Y - min_Y) * Y_pixels) + slackY + titleheight
            x2 = x1 + X_pixels
            y2 = y1 + Y_pixels
            
            # Draw the die and file with bincolor
            if eachDie.testset == testset:
                dr.rectangle([x1,y1,x2,y2], fill=App.cfg['bin'][str(mybin)]['color'], outline=self.streetcolor)
                imap.append({'Row':eachDie.Y,'Col':eachDie.X,'x':x1,'y':y1,'width':x2-x1,'height':y2-y1})
                # Draw any specified symbols, if enabled 
                if App.cfg['enable_symbols']:
                    maputil.do_symbol(dr,x1,y1,x2,y2, False, **App.cfg['bin'][str(mybin)])
            
            # Draw flags if appropriate        
            xystr="{}|{}".format(eachDie.X, eachDie.Y)   # Bindict Key 
            if (wfr.diedict[xystr]['flags'] & constants.FLAG_MULTITEST) and App.cfg['flag']['show']:
                if wfr.diedict[xystr]['flags'] & constants.FLAG_DUPLICATE_BIN:
                    flagcolor= App.cfg['flag']['duplicate_color']
                else:
                    flagcolor= App.cfg['flag']['split_color'] 
                flagX = int(float(x2-x1)/float(App.cfg['flag']['size_factor']))
                flagY = int(float(y2-y1)/float(App.cfg['flag']['size_factor'])) 
                dr.polygon([(x1,y1+flagY),(x1,y1),(x1+flagX,y1)], fill=flagcolor, outline=(0,0,0))  
       
        
            # track minimum and maximums of actual drawn wafermap.
            map_extents['minx']= min(map_extents['minx'],x1)
            map_extents['maxx']= max(map_extents['maxx'],x2)
            map_extents['miny']= min(map_extents['miny'],y1)
            map_extents['maxy']= max(map_extents['maxy'],y2)
        
        #-----------------------------------------------------------
           
        log.debug('Drawn Map Extents = {}'.format(map_extents))
    
    #     do_html(imap, actualWidth, actualHeight)
            
        #--------------------------------------------------------------------------
        # Draw title area
        #--------------------------------------------------------------------------
        if self.showtitle:
            dr.rectangle([0,0,actualWidth-1,titleheight], fill=self.title.bgcolor, outline=self.bordercolor)
            self.title.render(self.img, wfr, titlekeys)
        
        #--------------------------------------------------------------------------
        # Draw legend, border, flat indicator, timestamp, axis labels
        #--------------------------------------------------------------------------
        if self.showlegend:
            self.legend.render(self.img, self.basewidth + axis_space , self.padding + titleheight)
        
        if self.showborder:
            dr.rectangle([0,0,actualWidth-1,actualHeight-1], fill=None, outline=self.bordercolor)
        
        if self.showflat:
            maputil.do_flat(self, lot.wcr['WF_FLAT'], map_extents, self.flatcolor)
        
        if self.showtimestamp:
            maputil.do_timestamp(self, color=self.timestampcolor) 
    
        if self.showaxis:
            maputil.do_axis(self, wfr.dielist, X_pixels, Y_pixels, map_extents, True)
       
        return(self.img)
    
       
   
