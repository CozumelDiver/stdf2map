###########################################################
# $File: title.py $
# $Author: daf $
# $Date: 2018-01-19 00:47:33 -0800 (Fri, 19 Jan 2018) $
# $Revision: 185 $
###########################################################

# import logging
# import constants
# import maputil
import datetime
from config import App
from PIL import Image, ImageDraw, ImageFont

class Title:
    
    def __init__(self):
        self.show = App.cfg['title']['show']
        self.padding = App.cfg['title']['padding']
        self.vpadding = App.cfg['title']['vpadding']
        self.bgcolor = App.cfg['title']['bgcolor']
#         self.keyname_part = App.cfg['title']['keyname_part']
#         self.keyname_lotid = App.cfg['title']['keyname_lotid']
#         self.keyname_waferid = App.cfg['title']['keyname_waferid']
#         self.keyname_date = App.cfg['title']['keyname_date']
#         self.keyname_testset = App.cfg['title']['keyname_testset']
#         self.keyname_yieldstr = App.cfg['title']['keyname_yieldstr']
        self.key_color = App.cfg['title']['key_color']
        self.value_color = App.cfg['title']['value_color']
        self.fontname = App.cfg['title']['font']
        self.keys={}
        
        
    # Get the sizes for the various parts of the title.  Wouldn't be so complicated if I didn't want 
    # different colors for the keys and values... (or PIL supported css styles in text :-), 
    # I'm sure there is a more elegant or pythonic way to do this
    # but until I figure it out, I'll have to stick with the brute-force method!

    def autosize(self, mir, wfr, fontsize, testset):
        
        self.keys['fontsize'] = fontsize
        maxfh = 0
        maxfw = 0
        
        titlefont = ImageFont.truetype(App.cfg['title']['font'], fontsize, encoding="unic")
        
        keyname = ['keyname_part', 'keyname_lotid', 'keyname_waferid', 'keyname_date', 'keyname_testset','keyname_yieldstr']
        for key in keyname:
            fw, fh = titlefont.getsize(App.cfg['title'][key])
            maxfh = max(maxfh,fh)
            maxfw += fw
            self.keys[key] = {'kval':App.cfg['title'][key], 'kw':fw, 'kh':fh}
            
        fw, fh = titlefont.getsize(mir['PART_TYP'])
        maxfh = max(maxfh,fh)
        maxfw += fw 
        self.keys['keyname_part']['dval']=mir['PART_TYP']
        self.keys['keyname_part']['dw']=fw
        self.keys['keyname_part']['dh']=fh
        maxfw += fontsize  #add space between keys 
        
        fw, fh = titlefont.getsize(mir['LOT_ID'])
        maxfh = max(maxfh,fh)
        maxfw += fw    
        self.keys['keyname_lotid']['dval']=mir['LOT_ID']
        self.keys['keyname_lotid']['dw']=fw
        self.keys['keyname_lotid']['dh']=fh
        maxfw += fontsize  #add space between keys 
                
        fw, fh = titlefont.getsize(wfr.wafer_id)
        maxfh = max(maxfh,fh)
        maxfw += fw    
        self.keys['keyname_waferid']['dval']=wfr.wafer_id
        self.keys['keyname_waferid']['dw']=fw
        self.keys['keyname_waferid']['dh']=fh
        maxfw += fontsize  #add space between keys 
             
        datestr = "{}".format(datetime.datetime.fromtimestamp(wfr.start_t).strftime('%Y-%m-%d  %H:%M'))
        fw, fh = titlefont.getsize(datestr)
        maxfh = max(maxfh,fh)
        maxfw += fw    
        self.keys['keyname_date']['dval']=datestr
        self.keys['keyname_date']['dw']=fw
        self.keys['keyname_date']['dh']=fh
        maxfw += fontsize  #add space between keys   
         
         
        teststr = "{}{}".format(App.cfg['binmap'][0].upper(), testset)       
        fw, fh = titlefont.getsize(teststr)
        maxfh = max(maxfh,fh)
        maxfw += fw    
        self.keys['keyname_testset']['dval']=str(teststr)
        self.keys['keyname_testset']['dw']=fw
        self.keys['keyname_testset']['dh']=fh
        maxfw += fontsize  #add space between keys 
         
        yieldstr = "{:.1f}%".format(wfr.map_yield)       
        fw, fh = titlefont.getsize(yieldstr)
        maxfh = max(maxfh,fh)
        maxfw += fw    
        self.keys['keyname_yieldstr']['dval']=str(yieldstr)
        self.keys['keyname_yieldstr']['dw']=fw
        self.keys['keyname_yieldstr']['dh']=fh
     
     
        #Add padding into width/height
        maxfw += App.cfg['title']['padding'] * 2
        maxfh += App.cfg['title']['vpadding'] * 2
                    
        self.keys['maxfw'] = maxfw
        self.keys['maxfh'] = maxfh
                                      
        return(self.keys) 
    
    def render(self, img, wfr, keys):
        
        dr=ImageDraw.Draw(img)
        
        titlefont = ImageFont.truetype(App.cfg['title']['font'], keys['fontsize'], encoding="unic")  
        keyspacing = keys['fontsize']
         
        cur_X = App.cfg['title']['padding']
        cur_Y = App.cfg['title']['vpadding']

        dr.text((cur_X, cur_Y), keys['keyname_part']['kval'], App.cfg['title']['key_color'], titlefont) 
        cur_X += keys['keyname_part']['kw']
        dr.text((cur_X, cur_Y), keys['keyname_part']['dval'], App.cfg['title']['value_color'], titlefont)       
        cur_X += keys['keyname_part']['dw'] + keyspacing
        
        dr.text((cur_X, cur_Y), keys['keyname_lotid']['kval'], App.cfg['title']['key_color'], titlefont)
        cur_X += keys['keyname_lotid']['kw']
        dr.text((cur_X, cur_Y), keys['keyname_lotid']['dval'], App.cfg['title']['value_color'], titlefont)       
        cur_X += keys['keyname_lotid']['dw'] + keyspacing
        
        dr.text((cur_X, cur_Y), keys['keyname_waferid']['kval'], App.cfg['title']['key_color'], titlefont)
        cur_X += keys['keyname_waferid']['kw']
        dr.text((cur_X, cur_Y), keys['keyname_waferid']['dval'], App.cfg['title']['value_color'], titlefont)       
        cur_X += keys['keyname_waferid']['dw'] + keyspacing
        
        dr.text((cur_X, cur_Y), keys['keyname_date']['kval'], App.cfg['title']['key_color'], titlefont)
        cur_X += keys['keyname_date']['kw']
        dr.text((cur_X, cur_Y), keys['keyname_date']['dval'], App.cfg['title']['value_color'], titlefont) 
        cur_X += keys['keyname_date']['dw'] + keyspacing
                      
        dr.text((cur_X, cur_Y), keys['keyname_testset']['kval'], App.cfg['title']['key_color'], titlefont)
        cur_X += keys['keyname_testset']['kw']
        dr.text((cur_X, cur_Y), keys['keyname_testset']['dval'], App.cfg['title']['value_color'], titlefont) 
        cur_X += keys['keyname_testset']['dw'] + keyspacing
        
        dr.text((cur_X, cur_Y), keys['keyname_yieldstr']['kval'], App.cfg['title']['key_color'], titlefont)
        cur_X += keys['keyname_yieldstr']['kw']
        dr.text((cur_X, cur_Y), keys['keyname_yieldstr']['dval'], App.cfg['title']['value_color'], titlefont)                                