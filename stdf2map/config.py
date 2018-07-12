###########################################################
# $File: config.py $
# $Author: daf $
# $Date: 2018-07-11 23:05:53 -0700 (Wed, 11 Jul 2018) $
# $Revision: 215 $
###########################################################

import toml
import copy
import os
import __main__ as main

# ------- USER Configuration -----------------------------------------------------
# Important - You must set _config_path!  If the directory doesn't' exist it will 
# be created.  Windows users, DO NOT use backslashes. i.e:
# _config_path = os.path.normpath('C:\MyApps\Python\stdf2map')  <---NO, NO, NO
# _config_path = os.path.normpath('C:/MyApps/Python/stdf2map')  <---YES
# I know... it's weird, just do it anyway!

_config_path = os.path.normpath('E:/WMapDemo/conf/')

# For normal use, I suggest leaving this at INFO
_loglevel='INFO'

#-------- End of USER Configuration ---------------------------------------------- 

class App(object):
    
    @classmethod
    def loadcfg(self,filename):
 #       self.cfg = merge(self.cfg,toml.load(filename, _dict=dict),update=True)
        self.cfg = merge_dicts(self.cfg,toml.load(filename, _dict=dict))

    
    @classmethod    
    def autocfg(self,options):
        
        cfgfile = _find_config()
        if(cfgfile):
#             if(options.verbose):
#             print "NOTE: Loading config from - '{}".format(cfgfile)
            self.cfg = toml.load(cfgfile, _dict=dict)
            self.cfg['_config_file'] = cfgfile
        else:
#             if(options.verbose):
#             print "NOTE: Using built-in config defaults..."
            self.cfg = toml.loads(builtin_config, _dict=dict)
            self.cfg['_config_file'] = 'built-in defaults'
            
        # default_cfg used for "reset" between wafers since entries may be changed
        # at runtime by part or user config files.
        
        self.cfg['_loglevel'] = _loglevel
        self.cfg['_config_path'] = _config_path            
        self.default_cfg = copy.deepcopy(self.cfg)  
        
        if self.cfg['binmap'] not in ['sbin','hbin']:
            raise ValueError("binmap must be either 'sbin' or 'hbin' (see config.py)") 
        if self.cfg['map_format'].upper() not in ['PNG','JPG','GIF','BMP','EPS','PCX','PPM','TIFF','WEBP']:
            raise ValueError("invalid map_format - {} (see config.py)".format(self.cfg['map_format']))
                     
#         self.cfg['_enable_user_config'] = _enable_user_config
#         self.cfg['_enable_part_config'] = _enable_part_config
         

def _find_config():
    # Name of the main routine (without .py) + "config" i.e 'stdf2map.config' 
    cfg_file = main.__file__.rsplit('.',1)[0] + ".config"
    
    # Check for config file in same dir as main file - Note: this is primarily a debugging aid 
    # that allows you to create a "debugging config file" that you can muck about the settings 
    # with and when done, you simply delete it and the app will revert to using the untouched 
    # "proper" config file. 
    maindir = os.path.abspath(os.path.dirname(main.__file__))   
    cfg_filepath = os.path.join(maindir, os.path.basename(cfg_file))
    if os.path.isfile(cfg_filepath):
        return cfg_filepath
    
    # Not found?  Look in the '_config_path' location
    cfg_filepath = os.path.join(_config_path, os.path.basename(cfg_file))
    if os.path.isfile(cfg_filepath):
        return cfg_filepath
    
    # Still not found, create one using built in defaults...
    if not os.path.exists(os.path.abspath(_config_path)):
        os.makedirs(os.path.abspath(_config_path))
        
#     if(options.verbose):
    print "===================================================================="
    print "NOTE: Generating default config file: {}".format(cfg_filepath)
    print "===================================================================="
    with open(cfg_filepath, "w") as text_file:
        text_file.write(builtin_config)
    return cfg_filepath
 
    
                   
# Blatantly borrowed from:
#"http://stackoverflow.com/questions/7204805/python-dictionaries-of-dictionaries-merge"
#
# def merge(a, b, path=None, update=True):
# 
#     if path is None: path = []
#     for key in b:
#         if key in a:
#             if isinstance(a[key], dict) and isinstance(b[key], dict):
#                 merge(a[key], b[key], path + [str(key)])
#             elif a[key] == b[key]:
#                 pass # same leaf value
#             elif isinstance(a[key], list) and isinstance(b[key], list):
#                 for idx, val in enumerate(b[key]):
#                     a[key][idx] = merge(a[key][idx], b[key][idx], path + [str(key), str(idx)], update=update)
#             elif update:
#                 a[key] = b[key]
#             else:
#                 raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
#         else:
#             a[key] = b[key]
#     return a

# Ditto...
def merge_dicts(dict1, dict2):
    """ Recursively merges dict2 into dict1 """
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return dict2
    for k in dict2:
        if k in dict1:
            dict1[k] = merge_dicts(dict1[k], dict2[k])
        else:
            dict1[k] = dict2[k]
    return dict1

#===========================================================================    
# Builtin_config file
# Only used for writing a default config file when one doesn't exist in 
# the specified _config_path location
#--------------------------------------------------------------------------- 
 
builtin_config = """
#====================================================
# IMPORTANT - README!!! 
#  1. true/false values MUST be specified in ALL
#     LOWER CASE (toml rule, not mine...)
#  2. Floating point number values < 1 MUST have a 
#     leading zero.  i.e. "setting = 0.5"
#----------------------------------------------------
# Caution -- Hazard Section!
#----------------------------------------------------
# NOT advisable to use anything in this section in  
# a user or part config file! (Either won't be applied
# or may cause unpredictable results...) 
#----------------------------------------------------
 
_enable_user_config = true
_enable_part_config = true
_theme = 'theme_default'

#----------- End of Hazard Section ------------------
 
 
# Set to your "Good Die" Bin Number
good_die_bin=1
 
# create map for either sbin or hbin
binmap = 'hbin'  
 
# If duplicate die warnings is true, entries
# will be logged for retested die 
# indicating same or different bin failures
 
duplicate_die_warnings = false
 
# Following output types are supported:
# BMP, EPS, GIF, JPG, PCX, PNG, PPM, TIFF, WEBP
# NOTE: Case is unimportant, but WILL be carried
# through to automatically generated filenames!
# which may be significant on Linux
map_format = 'png'
 
# Default to symbols enabled, setting to false would
# have the same effect as always using the -s option
# (which may be useful in user config files)
enable_symbols=true
 
# Default to map die that have not be retested
 
testset=1
 
# --------------- File Section Group ---------------------
[file]
# File Paths, enter in either normal Windows or Linux 
# format depending on your system.  You **DO NOT ** need 
# to escape backslashes on Windows
# Examples:
# map_path = 'C:\Mydata\Binmaps\"
# map_path = "/home/user/mydata/binmaps/"

map_path = 'E:\WMapDemo\Maps\'
stdf_path = 'E:\WMapDemo\stdf\'
logfile = 'E:\WMapDemo\Wmap.log'
logfile_size = 2000000
logfile_rotates = 5
 
# Auto-generated filename format (i.e no -o option on command line)
#---------------------
# Valid Keywords are:
#---------------------
# %part - Part ID
# %lotid - Wafer lotid 
# %waferid - Wafer ID 
# %nowhex - Current unix time in hex
# %nowdec - Current unix time in decimal
# %nowhum - Current human readable gmtime (Ymd-HMS)
# %tshex - Test datetime unix time in hex
# %tsdec - Test datetime unix time in decimal
# %tshum - Test datetime - Human readable gmtime (Ymd-HMS)
# %testset - Test number as specified with -t command line option
# %binmap - "Will be either H for HBIN or S for SBIN"
# %prefix - User specified string (see below)
# %suffix - User specified string (see below)
# %thumbstr - ONLY inserted if thumb_mode = True (see below)
#---------------------
# Note that string literals remain unchanged, thus if you wanted  
# a fab number for example, at the beginning of all your files you could use
# something like: "FAB1_%part_waferid_...etc" 
# You can also use path separators appropriate to your system
# (use \\ on Windows) to create a directory structure.
# For example, the following would put maps in sub-directories by part and lotid
# ( sub-directories are automatically created if they don't exist )
# auto_filename = '%prefix%part\%lotid\%waferid_%binmap%testset%suffix%thumbstr'
 
auto_filename = "%prefix%part_%waferid_%tshum-%binmap%testset%suffix%thumbstr"

# If "clobbermode" = True, output files of the same name will be overwritten,
# if False, a "dash-number" will be appended just preceding the file type until
# a unique file name is obtained (i.e file-1, file-2, file-3 .... file-n)

clobbermode = false
  
# Prefix and suffix are arbitrary user-defined strings that are provided
# primarily as a means of customizing the filename from within config files
# They can be placed anywhere in the format string, they don't necessarily 
# need to go at the beginning or end.
 
prefix = ""
suffix = ""
 
# Thumb_mode should ALWAYS be false in the main configuration file.
# It is provided as a means of enabling thumbnail mode from a user 
# configuration file.  The ONLY effect thumb_mode has is the automatic
# insertion of "thumbstr" in the output filename (assuming 'auto_filename'
# contains the %thumbstr keyword)  
 
thumb_mode = false
thumbstr = "_thumb"
 
# Automatically translate case in the output filename. Valid values are:
# 'upper','lower','capitalize' (Only capitalizes the first letter)
# If it is commented out, no case changing will be performed 
auto_translate = 'lower'
 
# --------------- Fiag Section Group ---------------------
[flag]
show = true
 
# Flag color if Bin results the SAME for all test sets
duplicate_color = '#FFFFFF'
 
# Flag color if Bin results DIFFERENT across test sets
split_color = '#FF0000'
 
# size of flag as a ratio of diesize 
# flagsize = diesize/size_factor.
# (i.e. smaller numbers = bigger flag)
# Typically you would want a slightly smaller number
# for smaller die to increase the apparent flag size.
# A number of 1.0 would divide the die in half 
# corner to corner (Use a minimum of 1.0) 
 
size_factor = 2.5
 
# --------------- Image Section Group ---------------------
 
[image]
padding=15  # Spacer around map image
bgcolor='#FFFFCE' # Map background color
streetcolor='#000000'     #Border around die
 
# Base Map size (not including legend)
# If autosize is enabled, the base size
# may be increased during rendering if
# the calculated die size is too small
# (See Autosize below)
basewidth=500    
baseheight=500
 
border=true  # Border around entire image
bordercolor = '#990000'
flatline=true  # line indicating flat location
flatcolor='#990000'
timestamp=true # Map creation timestamp
timestampcolor = '#000099'
 
# Autosize and Autosize_minpx work together
# if autosize is enabled, the map basesize
# will be increased so that each die has a
# minimum shorter side of "minpx" Pixels
# This can be useful for autosizing wafers with 
# thousands of die, like discrete devices. 
autosize=true
autosize_minpx=6
 
# ------------- Axis / Grid Section Group -----------------
[axis]
show = true
font = 'arialbd.ttf'
color = '#000000'
 
grid = true
gridcolor='#CCCCCC'
 
# --------------- Title Section Group ---------------------
[title]
show=true
padding = 10
vpadding = 6
bgcolor='#DCFEDA'
keyname_part = 'Part: '
keyname_lotid = 'Lot ID: '
keyname_waferid = 'Wafer ID: '
keyname_date = 'Date: '
keyname_testset = 'T:'
keyname_yieldstr = 'Y:'
key_color = "#868686"
value_color ="#000099"
font = 'arialbd.ttf'
 
# --------------- Legend Section Group ---------------------
[legend]
show=true           #Legend drawn
autosize=true        #Autosize font / boxsize
sort_bins_by_count=false
show_bin_counts=true      #Show bincounts in [] after Bin labels
padding = 10        #Padding around entire legend
vspace = 4          #Vertical space between Bin text
hspace = 5          #Horizonal space between colored square and Bin text
font = 'arial.ttf'  #Legend Font
fontcolor = '#000000' 
overflow_text='...More...'
overflow_textcolor='#00007F'

# Following 2 entries ignored if autosize=true
 
boxsize = 12        #Size of colored square
fontsize = 14
 
# --------------- Demo Section Group ---------------------
[demo]
# random_diecount = true will create maps with a random
# number of rows & columns. (within min/max limits)  
# ALL WAFERS in lot will have the same counts
 
random_diecount=true

# Same as above EXCEPT ALL WAFERS within a lot will have
# random diecounts. 

random_diecount_eachwafer = true

# If BOTH the above are false, Demo map will always have 
# row & col counts specified by the min/max values.

min_X=-30
max_X=30
min_Y=-30
max_Y=30
 
# Minimum and Maximum Bin numbers to use.  ONLY valid for Demo
minbin=1
maxbin=30
 
# Default number of test sets in the demo map, this would 
# typically be changed by using the -t option with -d 
# (In demo mode -t SETS the number of testcounts) 
 
testcount=1

# If "random_yield" = true, then "fixed_yield" is 
# ignored and die yield will be random.  If it is false, then
# wafer will yield at (or close to) the "fixed_yield" number
# "fixed_yield"  can be a floating point or integer number 
# and is internally limited between  0.0 and 100.0 
# (numbers outside that range will be set to the nearest limit)
# The -g option can be used to temporarily override the 
# random yield and set yield for that demo run
# For more realistic demo yields, you can also set 
# "minimum_yield"

random_yield = true
fixed_yield = 78.6
minimum_yield = 60.0
 
 
# --------------- BIN Section Group ---------------------
# Specify Bin Label / Color combos.  If Bins NOT in this 
# list are encountered at runtime, they will be given 
# random colors and labels according to:
#--------------------------
#  1 - Demo mode - Both colors and Labels randomly assigned
#  2 - STDF mode - Color randomly assigned, Bin Label set to "-"
#--------------------------
# The following bins are provided as a sample... bins are 
# best specified in part config files where you can 
# customize the bin labels for each part (unless of course you
# always use the same bin labels for ALL parts.)
# For each bin listed, color and label MUST be specified
# although label can be blank (as in label='').  
# Symbol is optional and valid symbols are:
#   dot
#   dot3
#   dash
#   plus
#   square
#   diamond
#   triangle
#   cross
#
# Symbol modifiers are also optional as defaults are used, but 
# in most cases the defaults won't look very well as it's impossible 
# to have a "one-size fits all" default that works for all calculated
# die sizes.  Valid modifiers are:
#   shade - synonymous with "color", but applies to the symbol
#   scale - the size of the symbol, in general, you can think of this as:
#         "if you draw a square around the symbol, it's the percentage of
#         die space it will take up"
#   width - line width in pixels - applies only to symbols drawn with lines 
#         (cross, dash, plus). Because the image routines do not support 
#         anti-aliasing, "width" often looks best with odd numbers (1, 3, 5, etc.)
#   outline - 1-pixel outline color, applies only to symbols that get a
#         color fill (dot, dot3, square, diamond, triangle).  Not for small die...
#
# Symbols in general will not work very with small die, experimentation is the 
# best way to get a look you are after for any specific die size. (However, you 
# can always increase the apparent die size by making the image bigger :-) 
  
 
# Some sample Bins with symbol definitions.  These are also provided in a 
# sample config file (symbols.toml)  so you can just do:
#     stdf2map -c symbols lot3
# to see the results of using them
 
[bin]
#1 = {color='#00FF00', label='Good Die'}
#2 = {color='#FF0000', label='Setup/Continuity', symbol='cross', shade='#FFFFFF', scale=0.75, width=3}
#3 = {color='#009999', label='Leakage', symbol='dot', shade='#FFFFFF', scale=0.5}
#4 = {color='#FEF102', label='Threshhold', symbol='dot3', shade='#FF0000', scale=0.25}
#5 = {color='#CC6699', label='Resistance', symbol='plus', shade='#ffff00', scale=0.6}
#7 = {color='#FFFFFF', label='Breakdown', symbol='plus', shade='#FF0000', scale=0.5, width=3 }
#8 = {color='#00FF00', label='Statistical Failure', symbol='cross', shade='#ff0000', scale=1.0, width=2}
#10 = {color='#0000FF', label='Capacitance', symbol='dash', shade='#FFFFFF', scale=0.65, width=3}
#16 = {color='#BF6030', label='V/I Ramp Sense', symbol='square', shade='#000000', scale=0.5 }
#17 = {color='#FF5500', label='Strobe Failure', symbol='dot', shade='#ffffff', scale=0.5, outline='#000000'}
#20 = {color='#009999', label='RAM CRC', symbol='diamond', shade='#ffff00', scale=0.6, outline='#000000' }
 
#Samples with no symbol definitions.
0 = {color="#FFFFFF", label='-'}
1 = {color="#00FF00", label="Good Die -"}
2 = {color="#FF0000", label="Setup/Continuity"}
3 = {color="#009999", label="Leakage"}
4 = {color="#FEF102", label="Threshhold"}
5 = {color="#3333CC", label="Resistance"}
6 = {color="#880000", label="Timing"}
7 = {color="#FFFFFF", label="Breakdown"}
8 = {color="#990000", label="Active Fail"}
9 = {color="#BF6E11", label="Passive Fail"}
10 = {color="#0000FF", label="Capacitance"}
11 = {color="#666666", label="Self-Test"}
12 = {color="#32CC99", label="Conductance"}
13 = {color="#8F3C2F", label="Unlucky"}
 
## EOF
"""