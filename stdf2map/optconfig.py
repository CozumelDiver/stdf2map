###########################################################
# $File: optconfig.py $
# $Author: daf $
# $Date: 2018-01-13 19:00:23 -0800 (Sat, 13 Jan 2018) $
# $Revision: 166 $
###########################################################
import os.path
import logging

from config import App

log = logging.getLogger(__name__)

def democonfig():
    
    democfgfile = os.path.join(App.cfg['_config_path'], 'demomap.toml')
    
    if os.path.isfile(democfgfile):
        log.info("Loading demo config file - '{}'".format(democfgfile))
        App.loadcfg(filename=democfgfile)            

def partconfig(part):
    
    # Check for part-based configuration file.  
    # Merge with default configuration if found 

    partcfgfile = os.path.join(App.cfg['_config_path'], part + '.toml')

    if os.path.isfile(partcfgfile):
        if not App.cfg['_enable_part_config']:
            log.warn('{}: configuration file found, but merging disabled in config.py'.format(partcfgfile))
        
        log.info("Loading part config file - '{}'".format(partcfgfile))
        App.loadcfg(filename=partcfgfile)

        
def userconfig(filename):
    
    head, tail = os.path.split(filename)
    if not head:
        usercfgfile = os.path.join(App.cfg['_config_path'], filename)
    else:
        usercfgfile = filename
     
    if not usercfgfile.lower().endswith('.toml'):
        usercfgfile += ".toml" 
           
    
    if os.path.isfile(usercfgfile):
        if not App.cfg['_enable_user_config']:
            log.warn('{}: user configuration file found, but merging disabled in config.py'.format(usercfgfile))
        
        log.info("Loading user specified config file - '{}'".format(usercfgfile))
        App.loadcfg(filename=usercfgfile)
    else:
        log.warn("Unable to load user specified config file - '{}'".format(usercfgfile))
 
    