###########################################################
# $File: buildmap.py $
# $Author: daf $
# $Date: 2018-01-17 02:25:41 -0800 (Wed, 17 Jan 2018) $
# $Revision: 175 $
###########################################################

import logging
import constants
from config import App
from legend import Legend
from PIL import Image, ImageDraw, ImageFont
from util import do_symbol
from html import do_html
    
log = logging.getLogger(__name__)


def buildmap(lot, wfr, testset):
          
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
    
    
    baseWidth=App.cfg['image']['basewidth']
    baseHeight=App.cfg['image']['baseheight']
     
    if baseWidth >= baseHeight:
        sizeRatio = float(baseWidth) / float(baseHeight)
    else:
        sizeRatio = float(baseHeight) / float(baseWidth)
         
    log.debug('Size Ratio: {:.2f}, width={}, height={}'.format(sizeRatio, baseWidth, baseHeight))
    
    
    #---------------------------------------------------------------------------
    # If image autosize is enabled, the canvas size may be increased to ensure
    # die are visible.  This will force a minimum pixel size of "autosize_minpx".
    # The original aspect ratio will be maintained.
    #---------------------------------------------------------------------------
    padding=App.cfg['image']['padding']
    autosize_minpx = App.cfg['image']['autosize_minpx']
    
    if App.cfg['image']['autosize']:
        # conveniences for calculations...
        bw = App.cfg['image']['basewidth']
        bh = App.cfg['image']['baseheight']
        
        autominX = (autosize_minpx * col_count) + (2 * padding)
        autominY = (autosize_minpx * row_count) + (2 * padding)
        log.debug('Autosize Minimum Map Size X={} Y={} at Autopx = {}'.format( 
                  autominX, autominY, autosize_minpx))
    
        if(autominX > bw):
            bw = autominX
            bh = int (float(bw) * float(sizeRatio))
            log.debug('Autosize (autominX > bw) Updated sizes - width={}, height={}, sizeRatio={}'.format(bw, bh, float(sizeRatio)))
        elif (autominY > bh):
            bh = autominY
            bw = int (float(bh) * float(sizeRatio))
            log.debug('Autosize (autominY > bh) Updated sizes - width={}, height={}, sizeRatio={}'.format(bw, bh, float(sizeRatio)))
        else:
            log.debug('Autosize sizing not required, width={}, height={}, autominX={}, autominY={}'.format(bw, bh, autominX, autominY)) 

        
        #Store updated values back in cfg 
        App.cfg['image']['basewidth'] = bw
        App.cfg['image']['baseheight'] = bh
    

    
    # Nominal size of map excluding padding
    mapX = App.cfg['image']['basewidth'] - (padding *2)
    mapY = App.cfg['image']['baseheight'] - (padding *2)
    log.debug('Map Space (BaseSize - 2*Padding)  (X,Y)=({},{})'.format(mapX,mapY))
    
    
    #Calculate the die's pixel size  width (X) and height (Y)
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
    # Generate the legend data, it will be rendered later, but we require
    # knowing the space it will take up so we can adjust the canvas size 
    #-------------------------------------------------------------------------
    wfr.legend = Legend(wfr.dielist, testset)
    
    #--------------------------------------------------------------------------
    # baseWidth adjusted to allow for legend.
    #--------------------------------------------------------------------------
    actualWidth = App.cfg['image']['basewidth']
    if App.cfg['legend']['show']:
        actualWidth += wfr.legend.legend['legendwidth']
        log.debug('Legend Width = {}'.format(wfr.legend.legend['legendwidth']))
           
    #--------------------------------------------------------------------------
    # Get axis space, add in 10 pixels for flat spacing.  (the axes are 
    # shifted left or up by 10 pixels when they are drawn to account for these
    # 10 pixels).
    #--------------------------------------------------------------------------
    axis_space = 0
    if App.cfg['axis']['show']:
        axis_space = _do_axis(wfr.dielist,X_pixels,Y_pixels) + 10
        log.debug('Axis Space = {}'.format(axis_space))
        
       
    #--------------------------------------------------------------------------
    # baseheight and fontsize adjusted for title
    #--------------------------------------------------------------------------
    # Start with a reasonable guess for the size of the title font and then
    # autosize it from there.   May not be the most efficient way to do 
    # this, but it works for now...
    #--------------------------------------------------------------------------
    actualHeight = App.cfg['image']['baseheight']
    titleheight = 0
    if App.cfg['title']['show']:
        
        #A guess...
        title_fontsize = actualWidth//40    
        titlekeys = wfr.legend.titlesize(lot.mir, wfr, title_fontsize, testset)
        upsearch=False
        
        if(titlekeys['maxfw'] > actualWidth):
            while titlekeys['maxfw'] > actualWidth:
                upsearch=False
                title_fontsize -= 1
                titlekeys = wfr.legend.titlesize(lot.mir, wfr, title_fontsize, testset)
    #             print "D:imageWith = {}, fontsize = {}, maxfw={}, height={}".format(actualWidth, title_fontsize, titlekeys['maxfw'], titlekeys['maxfh'])
    
        else:
            while titlekeys['maxfw'] < actualWidth:
                upsearch=True
                title_fontsize += 1
                titlekeys = wfr.legend.titlesize(lot.mir, wfr, title_fontsize, testset)
    #             print "U:imageWith = {}, fontsize = {}, maxfw={}, height={}".format(actualWidth, title_fontsize, titlekeys['maxfw'], titlekeys['maxfh'])    
    
        # If we were decreasing font size when the while condition became false, all the titlekeys are properly set, 
        # from the last loop cycle.... but if we were increasing font size, the last loop cycle left the titlekeys 
        # in a state for a larger font, so decrease the font size by one and re-evaluate the titlekeys
        if(upsearch):
            title_fontsize -=1
            titlekeys = wfr.legend.titlesize(lot.mir, wfr, title_fontsize, testset)
    
        titleheight = titlekeys['maxfh']
        actualHeight += titleheight
        log.debug('Title Height = {}, Title Fontsize = {}'.format(titleheight, title_fontsize))

    #--------------------------------------------------------------------------
    # Adjust Width and Height for axis space
    #--------------------------------------------------------------------------
    if(App.cfg['axis']['show']):
        actualWidth += axis_space
        actualHeight += axis_space
        
    log.debug('Actual Image Size (X,Y) = ({},{})'.format(actualWidth, actualHeight))
 
    log.debug('Padding = {}'.format(padding))
                        
    #--------------------------------------------------------------------------
    # Create the canvas and draw the wafermap
    #--------------------------------------------------------------------------
    img = Image.new('RGB', (actualWidth,actualHeight), App.cfg['image']['bgcolor'])

    # Get the drawable object...
    dr = ImageDraw.Draw(img)
    
    # map_extents are used for tracking the actual pixel extents of the drawn map which makes
    # calculating the location to draw the flat & axis labels a bit easier...
    
    map_extents = {'minx':65535, 'miny':65535, 'maxx':0, 'maxy':0}
    
    # limit flag_size factor to a minimum of 1.0 (or else flag will exceed die boundary)
    App.cfg['flag']['size_factor'] = max(App.cfg['flag']['size_factor'], 1.0)
    
    # if we want the grid, draw it first so it's behind everything else...
    if App.cfg['axis']['grid']:   
        _do_grid(wfr.dielist, img, X_pixels, Y_pixels, padding, axis_space, slackX, slackY, titleheight)
    idx=0
    
    imap = []
    
    for eachDie in wfr.dielist:
        mybin=getattr(eachDie,App.cfg['binmap'])
        idx+=1      
        x1 = padding + axis_space + ((eachDie.X - min_X) * X_pixels) + slackX
        y1 = padding + axis_space + ((eachDie.Y - min_Y) * Y_pixels) + slackY + titleheight
        x2 = x1 + X_pixels
        y2 = y1 + Y_pixels
        
        # Draw the die and file with bincolor
        if eachDie.testset == testset:
            dr.rectangle([x1,y1,x2,y2], fill=App.cfg['bin'][str(mybin)]['color'], outline=(0,0,0))
            imap.append({'Row':eachDie.Y,'Col':eachDie.X,'x':x1,'y':y1,'width':x2-x1,'height':y2-y1})
            # Draw any specified symbols, if enabled 
            if App.cfg['enable_symbols']:
                do_symbol(dr,x1,y1,x2,y2, False, **App.cfg['bin'][str(mybin)])
        
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
       
    log.debug('Drawn Map Extents = {}'.format(map_extents))

#     do_html(imap, actualWidth, actualHeight)
        
    #--------------------------------------------------------------------------
    # Draw title area
    #--------------------------------------------------------------------------
    if App.cfg['title']['show']:
        dr.rectangle([0,0,actualWidth,titleheight], fill=App.cfg['title']['bgcolor'], outline=(0,0,0))
        wfr.legend.render_title(img, wfr, titlekeys)
    
    #--------------------------------------------------------------------------
    # Draw legend, border, flat indicator, timestamp, axis labels
    #--------------------------------------------------------------------------
    if App.cfg['legend']['show']:
        wfr.legend.render(App.cfg['image']['basewidth'] + axis_space , padding + titleheight, img)
    
    if App.cfg['image']['border']:
        dr.rectangle([0,0,actualWidth-1,actualHeight-1], fill=None, outline=(0,0,0))
    
    if App.cfg['image']['flatline']:
        wfr.legend.render_flat(img, lot.wcr['WF_FLAT'], map_extents, (127,0,0))
#        wfr.legend.render_flat(img, 'L', map_extents, (127,0,0))
    
    if App.cfg['image']['timestamp']:
        wfr.legend.timestamp(img, color=(0,0,127)) 

    if App.cfg['axis']['show']:
        _do_axis(wfr.dielist, X_pixels, Y_pixels, map_extents, img, True)
        
# # Add some debug entries to the configuration for examination during a dump
# # (-z command option) 
#     App.cfg['debug']={}
#     
#     App.cfg['debug']['Map'] = {'mapX':mapX, 'mapY':mapY, 'X_pixels':X_pixels, 'Y_pixels':Y_pixels,
#                            'Actual Width':actualWidth, 'Actual Height':actualHeight,
#                            'Title Height':titleheight, 'Axis Space':axis_space,
#                            'Slack X':slackX, 'Slack Y':slackY,
#                            'Drawn Map Extents':map_extents}  
# 
# #   print "Map X,Y............... {},{}".format(mapX,mapY)
# #   print "Die Pixels X,Y........ {},{}".format(X_pixels,Y_pixels)
# #   print "Actual Image Size..... {},{}".format(actualWidth,actualHeight)
# #   print "Title Height.......... {}".format(titleheight)
# #   print "Axis Space............ {}".format(axis_space) 
# #   print "Padding............... {}".format(padding) 
# #   print "Drawn Map Extents..... {}".format(map_extents) 
   
    return(img)

def _do_axis(dielist, X_pixels, Y_pixels, extents=None, img=None, render=False):
    
    xlist=[]
    ylist=[]
    
    minpx = min(X_pixels, Y_pixels)
   
    fontsize = max (minpx-2, 8)
    fontsize = min (fontsize, 30)
    
#     print "axis fontsize = {}".format(fontsize)
    maxfw = maxfh = 0

    font = ImageFont.truetype(App.cfg['axis']['font'], fontsize, encoding="unic")
    
    min_Y = min(d.Y for d in dielist)
    max_Y = max(d.Y for d in dielist)
    min_X = min(d.X for d in dielist)
    max_X = max(d.X for d in dielist)
    
    for w in dielist:
        labelx="{:>3d}".format(w.X)        
        labely="{:>3d}".format(w.Y)    
        fwx, fhx = font.getsize(labelx)
        fwy, fhy = font.getsize(labely)        
        maxfw = max(maxfw,fwx,fwy)
        maxfh = max(maxfh,fhx,fhy) 
        
    # If we are just in "size-checking" mode, return
    if not render:
        return maxfw
    
    dr=ImageDraw.Draw(img)        
    
    idx = 0
    for row in xrange(min_Y, max_Y+1):
        idx += 1
        #-10 because we add 10 in the main routine, 
        # allows space for flat indicator...
        x1 = extents['minx'] - maxfw - 10 
        y1 = extents['miny'] + (Y_pixels * (idx -1)) + (Y_pixels //2) - maxfh // 2 
        label="{:>3d}".format(row)
        dr.text((x1, y1), label, App.cfg['axis']['color'], font)
    
    # For columns, create a small temporary image so we can rotate the text 
    # then paste into the main image
    idx = 0
    for col in xrange(min_X, max_X+1):
        idx += 1
        x1 = extents['minx'] + (X_pixels * (idx -1)) + (X_pixels //2) - maxfh // 2 - 1
        # maxfw because text is rotated, -10 because we add 10 in the main routine, 
        # allows space for flat indicator...
        y1 = extents['miny'] - maxfw - 10  
        label="{:>3d}".format(col)
        newimg = Image.new('RGB', (maxfw,maxfh), App.cfg['image']['bgcolor'])
        dr1 = ImageDraw.Draw(newimg)
        dr1.text((0, 0), label, App.cfg['axis']['color'], font)
        myimg = newimg.transpose(Image.ROTATE_90)
#         print "myimg height={}, width={}".format(myimg.height,myimg.width)
        img.paste(myimg,(x1,y1))
        del newimg
        
def _do_grid(dielist, img, X_pixels, Y_pixels, padding, axis_space, slackX, slackY, titleheight):

    min_Y = min(d.Y for d in dielist)
    max_Y = max(d.Y for d in dielist)
    min_X = min(d.X for d in dielist)
    max_X = max(d.X for d in dielist)
    
    dr=ImageDraw.Draw(img)
    
    idx = 0
    for row in xrange(min_Y, max_Y+1):
        idx += 1
        x1 = padding + axis_space + slackX
        y1 = padding + axis_space + titleheight + (Y_pixels * (idx -1)) + (Y_pixels //2) + slackY
        x2 = x1 + X_pixels * (max_X - min_X + 1) 
        y2 = y1
#         print "drawing line ({},{})({},{})".format(x1,y1,x2,y2)
        dr.line([x1, y1, x2, y2], App.cfg['axis']['gridcolor'], 1)
    
    idx = 0
    for col in xrange(min_X, max_X+1):
        idx += 1
        x1 = padding + axis_space + (X_pixels * (idx -1)) + (X_pixels //2) + slackX
        y1 = padding + axis_space + titleheight + slackY
        x2 = x1
        y2 = y1 + Y_pixels * (max_Y-min_Y + 1)
#         print "drawing line ({},{})({},{})".format(x1,y1,x2,y2)
        dr.line([x1, y1, x2, y2], App.cfg['axis']['gridcolor'], 1) 
        
     
            
            
 
    
