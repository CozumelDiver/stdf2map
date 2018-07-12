###########################################################
# $File: maputil.py $
# $Author: daf $
# $Date: 2018-01-20 00:35:55 -0800 (Sat, 20 Jan 2018) $
# $Revision: 192 $
###########################################################

import time
import datetime
import logging
from PIL import Image, ImageDraw, ImageFont


log = logging.getLogger(__name__)
    
def do_axis(wmap, dielist, X_pixels, Y_pixels, extents=None, render=False):
    
    xlist=[]
    ylist=[]
    
    minpx = min(X_pixels, Y_pixels)
   
    fontsize = max (minpx-2, 8)
    fontsize = min (fontsize, 30)
    
#     print "axis fontsize = {}".format(fontsize)
    maxfw = maxfh = 0

    font = ImageFont.truetype(wmap.axisfont, fontsize, encoding="unic")
    
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
    
    dr=ImageDraw.Draw(wmap.img)        
    
    idx = 0
    for row in xrange(min_Y, max_Y+1):
        idx += 1
        #-10 because we add 10 in the main routine, 
        # allows space for flat indicator...
        x1 = extents['minx'] - maxfw - 10 
        y1 = extents['miny'] + (Y_pixels * (idx -1)) + (Y_pixels //2) - maxfh // 2 
        label="{:>3d}".format(row)
        dr.text((x1, y1), label, wmap.axiscolor, font)
    
    # For columns, create a small temporary image so we can rotate the text 
    # then paste into the main image
    idx = 0
    for col in xrange(min_X, max_X+1):
        idx += 1
        x1 = extents['minx'] + (X_pixels * (idx -1)) + (X_pixels //2) - maxfh // 2 - 1
        # maxfw because text is rotated, -10 because we add 10 in the main routine, 
        # to allow space for flat indicator...
        y1 = extents['miny'] - maxfw - 10  
        label="{:>3d}".format(col)
        newimg = Image.new('RGB', (maxfw,maxfh), wmap.bgcolor)
        dr1 = ImageDraw.Draw(newimg)
        dr1.text((0, 0), label, wmap.axiscolor, font)
        myimg = newimg.transpose(Image.ROTATE_90)
#         print "myimg height={}, width={}".format(myimg.height,myimg.width)
        wmap.img.paste(myimg,(x1,y1))
        del newimg
        
def do_grid(wmap, dielist, X_pixels, Y_pixels, padding, axis_space, slackX, slackY, titleheight):

    min_Y = min(d.Y for d in dielist)
    max_Y = max(d.Y for d in dielist)
    min_X = min(d.X for d in dielist)
    max_X = max(d.X for d in dielist)
    
    dr=ImageDraw.Draw(wmap.img)
    
    idx = 0
    for row in xrange(min_Y, max_Y+1):
        idx += 1
        x1 = padding + axis_space + slackX
        y1 = padding + axis_space + titleheight + (Y_pixels * (idx -1)) + (Y_pixels //2) + slackY
        x2 = x1 + X_pixels * (max_X - min_X + 1) 
        y2 = y1
#         print "drawing line ({},{})({},{})".format(x1,y1,x2,y2)
        dr.line([x1, y1, x2, y2], wmap.gridcolor, 1)
    
    idx = 0
    for col in xrange(min_X, max_X+1):
        idx += 1
        x1 = padding + axis_space + (X_pixels * (idx -1)) + (X_pixels //2) + slackX
        y1 = padding + axis_space + titleheight + slackY
        x2 = x1
        y2 = y1 + Y_pixels * (max_Y-min_Y + 1)
#         print "drawing line ({},{})({},{})".format(x1,y1,x2,y2)
        dr.line([x1, y1, x2, y2], wmap.gridcolor, 1) 
        
# Draw die symbols
def do_symbol(dr,x1,y1,x2,y2,legbox,**kw):
        
        length = x2-x1
        width = y2-y1
        minsz = min(length,width)
        
        # Nothing to do if no symbol specified
        if 'symbol' not in kw:
            return
        
        # special default for 'dot3' in case 
        # scale is not specified
        if kw['symbol'] == 'dot3':
            if 'scale' not in kw:
                kw['scale'] = 0.2

        # Give the legend box 'dot' a 
        # consistent size   
        if legbox:
            if kw['symbol'] == 'dot':
                kw['scale'] = 0.40
    
        DEF_KW = {
            'shade': '#000000',
            'size': 1,
            'width':1,
            'fill': None,
            'scale': 0.40,
            'limit': None,
            'outline': None
        }
        
        for key in DEF_KW:
            if key not in kw:
                kw[key] = DEF_KW[key]
    
        pixels = int(kw['size']) #Default
        
        if kw['scale']:
            pixels = int(minsz * float(kw['scale']))
#             print "scale, pixels = {}".format(pixels)
              
        if kw['limit']:
            pixels = min(pixels, int(kw['limit']))
        
        cx = x1 + (x2-x1)//2
        cy = y1 + (y2-y1)//2
        
        if kw['symbol'] == 'dot':
            p = pixels // 2  #Since everything is based as offsets from center        
            dr.ellipse([cx-p, cy-p, cx+p, cy+p], fill=kw['shade'], outline=kw['outline'] )
            
        if kw['symbol'] == 'dot3':
            p = pixels // 2  #Since everything is based as offsets from center

            #offset center down & left by "pixels*2"
            cx1 = cx-(p*2)
            cy1 = cy+(p*2)         
            dr.ellipse([cx1-p, cy1-p, cx1+p, cy1+p], fill=kw['shade'], outline=kw['outline'] )

            #offset center down & right by "pixels*2"
            cx1 = cx+(p*2)
            cy1 = cy+(p*2)         
            dr.ellipse([cx1-p, cy1-p, cx1+p, cy1+p], fill=kw['shade'], outline=kw['outline'] )
            
            #offset center up by "pixels*2"
            cy1 = cy-(p*2)         
            dr.ellipse([cx-p, cy1-p, cx+p, cy1+p], fill=kw['shade'], outline=kw['outline'] )
                        
                     
        if kw['symbol'] == 'cross':
            p = pixels        
            dr.line([x1+p, y1+p, x2-p, y2-p], fill=kw['shade'], width=kw['width'] )
            dr.line([x2-p, y1+p, x1+p, y2-p], fill=kw['shade'], width=kw['width'] ) 
            
        if kw['symbol'] == 'diamond':
            p = pixels // 2  #Since everything is based as offsets from center           
            dr.polygon([(cx-p, cy), (cx,cy-p), (cx+p,cy), (cx,cy+p),(cx-p,cy)], fill=kw['shade'], outline=kw['outline'])
            
        if kw['symbol'] == 'triangle':
            p = pixels // 2  #Since everything is based as offsets from center         
            dr.polygon([(cx-p, cy+p), (cx,cy-p), (cx+p,cy+p), (cx-p,cy+p)], fill=kw['shade'], outline=kw['outline'])
            
        if kw['symbol'] == 'square':
            p = pixels // 2  #Since everything is based as offsets from center            
            dr.polygon([(cx-p, cy-p), (cx+p,cy-p), (cx+p,cy+p), (cx-p,cy+p),(cx-p,cy-p)], fill=kw['shade'], outline=kw['outline'])                        
            
        if kw['symbol'] == 'dash':
            p = pixels // 2  #Since everything is based as offsets from center      
            dr.line([cx-p, cy, cx+p, cy], fill=kw['shade'], width=kw['width'] )
            
        if kw['symbol'] == 'plus':
            p = pixels // 2  #Since everything is based as offsets from center          
            dr.line([cx-p, cy, cx+p, cy], fill=kw['shade'], width=kw['width'] )          
            dr.line([cx, cy-p, cx, cy+p], fill=kw['shade'], width=kw['width'] )
            
def do_timestamp(wmap, font='arial.ttf', fontsize=10, color=(66,66,66)):
        
        ts=time.time()
        str_ts = "Created: " + datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')
        fontsize = max(10, wmap.basewidth // 50)   
        ih = wmap.img.height
        iw = wmap.img.width
        
        dr=ImageDraw.Draw(wmap.img)
        font = ImageFont.truetype(font, fontsize, encoding="unic")
        fw, fh = font.getsize(str_ts)

        if(iw > fw + 10):
            dr.text((iw-fw-10, ih-fh-10), str_ts, color, font)
            
def do_flat(wmap, flatpos, map_extents, color=(127,0,0)):
              
        if (flatpos not in ['U','D','L','R']):
            log.warn("No Valid Flat location found!")
            return
        
        log.debug('Flat Location = {}'.format(flatpos))
        
        linewidth = 3
        
        # conveniences
        minx = map_extents['minx']
        maxx = map_extents['maxx']
        miny = map_extents['miny']
        maxy = map_extents['maxy']
        
        xcenter = minx + ((maxx - minx) / 2)
        ycenter = miny + ((maxy - miny) / 2)
 
        dr = ImageDraw.Draw(wmap.img)
                   
        if(flatpos =='U'):
            y1 = y2 = miny - 6
            x1 = xcenter - int(float(xcenter) / 4)
            x2 = xcenter + int(float(xcenter) / 4)
            dr.line([x1,y1,x2,y2], color, linewidth)
                                    
        if(flatpos =='D'):
            y1 = y2 = maxy + 6
            x1 = xcenter - int(float(xcenter) / 4)
            x2 = xcenter + int(float(xcenter) / 4)
            dr.line([x1,y1,x2,y2], color, linewidth)
            
        if(flatpos =='L'):
            x1 = x2 = minx - 6
            y1 = ycenter - int(float(ycenter) / 4)
            y2 = ycenter + int(float(ycenter) / 4)
            dr.line([x1,y1,x2,y2], color, linewidth)
            
        if(flatpos =='R'):
            x1 = x2 = maxx + 6
            y1 = ycenter - int(float(ycenter) / 4)
            y2 = ycenter + int(float(ycenter) / 4)
            dr.line([x1,y1,x2,y2], color, linewidth)

        