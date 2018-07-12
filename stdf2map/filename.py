###########################################################
# $File: filename.py $
# $Author: daf $
# $Date: 2018-01-17 02:26:25 -0800 (Wed, 17 Jan 2018) $
# $Revision: 176 $
###########################################################
import re
import time
import os.path
from config import App


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))
    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)

def make_filename(mir, wfr, path, basefile=None, thumb_mode=False, filetype=None):
    
    if basefile:
        basename = os.path.splitext(basefile)[0]
        filetype = os.path.splitext(basefile)[1]              
    else:
        basename = auto_basename(mir, wfr, thumb_mode)
          
    if not filetype:
        filetype = App.cfg['map_format']
        
    if not filetype.startswith('.'):
        filetype = '.' + filetype
    
    tmpfile = basename + filetype        
    filename = os.path.join(path,tmpfile)
  
    if not App.cfg['file']['clobbermode']:
        idx=0
        while os.path.isfile(filename):
            idx += 1
            tmpfile = '{}-{:d}{}'.format(basename,idx,filetype)
            filename = os.path.join(path, tmpfile)      
    
    head, tail = os.path.split(filename)
#     print "head = {}".format(head)
#     print "tail = {}".format(tail)
    if not os.path.exists(os.path.abspath(head)):
        os.makedirs(os.path.abspath(head))
    
#     print "filename = {}".format(filename)
      
    return filename
    
    
def auto_basename(mir, wfr, thumb_mode):

    now = int(time.time())
    nowhex = '{:x}'.format(now)
    nowdec = '{:d}'.format(now)
    tshex = '{:x}'.format(wfr.start_t)
    tsdec = '{:d}'.format(wfr.start_t)
    
    tshum = time.strftime('%Y%m%d-%H%M%S', time.gmtime(wfr.start_t))
    nowhum = time.strftime('%Y%m%d-%H%M%S', time.gmtime())
    
    prefix=''
    suffix=''
    
    if 'prefix' in App.cfg['file']:
        prefix = App.cfg['file']['prefix']
        
    if 'suffix' in App.cfg['file']:
        suffix = App.cfg['file']['suffix']
    
    thumbstr=""
    if thumb_mode and App.cfg['file']['thumbstr']:
        thumbstr=App.cfg['file']['thumbstr']
    
    testset = str(App.cfg['testset'])
        
    redict=  {'%lotid':mir['LOT_ID'], 
              '%waferid':wfr.wafer_id, 
              '%part':mir['PART_TYP'],
              '%nowhex':nowhex,
              '%nowdec':nowdec,
              '%nowhum':nowhum,
              '%tshex':tshex,
              '%tsdec':tsdec,
              '%tshum':tshum,
              '%prefix':prefix, 
              '%suffix':App.cfg['file']['suffix'],
              '%testset':testset,
              '%thumbstr':thumbstr, 
              '%binmap':App.cfg['binmap'][0]}
    
    # Real work is done by multiple_replace...
    basename = multiple_replace(App.cfg['file']['auto_filename'], redict)
#     print "Format = {}".format(App.cfg['file']['auto_filename'])
#     print "basename = {}".format(basename)
   
    # Translate to upper / lower case if specified
    if 'auto_translate' in App.cfg['file']:
        translate = App.cfg['file']['auto_translate'].lower()
        
        if translate == 'upper':
            basename = basename.upper()
        
        if translate == 'lower':
            basename = basename.lower()
        
        if translate == 'capitalize':
            basename = basename.capitalize()
        

    return(basename)
    



