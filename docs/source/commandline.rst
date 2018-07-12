
.. include:: <isoamsa.txt>
 
.. image:: images/pageheader.png

.. role::  raw-html(raw)
    :format: html

Command Line Options
====================

The following command line options are available:

    * **--version** |rAarr| *self explanatory*
    
    * **-h, --help** |rAarr| *self explanatory*
        
    * **-a, --autosize** |rAarr| *Disable autosize mode*  
        Autosize is enabled by default, and forces each die to have a minimum pixel size so that all die are visible.  You normally won't notice any effect from autosize unless you are making a small map with a large number of die.  There are two entries in **stdf2map.config** that control autosizing::

            # Autosize and Autosize_minpx work together
            # if autosize is enabled, the map basesize
            # will be increased so that each die has a
            # minimum shorter side of "minpx" Pixels
            # This can be useful for autosizing wafers with 
            # thousands of die, like discrete devices. 
            autosize=true
            autosize_minpx=6
            
    * **-b BINMAP, --binmap=BINMAP**
        An STDF Part Result Record (PRR) has two different variables to record Die Binning information: *HARD_BIN* and *SOFT_BIN*, (or sometimes referred to as *HBIN* and *SBIN*).  *HARD_BIN* is most commonly used, but some implementations will use *SOFT_BIN* as well, or they may both be populated with the same number.  **stdf2map** can map either variable and the default is set in **stdf2map.config**  To map the non-default variable use **-bsbin** (or **--binmap=sbin**) 
        
    * **-c USER_CONF, --conf=USER_CONF** 
        Load a user configuration file, see :ref:`userconf-label`
        
    * **-d DEMO, --demo=DEMO**  
        Generate a Demo WaferMap, integer argument is number of wafers (1-99), see :ref:`demo-label`
        
    * **-e THEME, --theme=THEME**  
        Load a theme configuration file, see :ref:`themeconf-label`
        
    * **-f,--flag** |rAarr| *Disable flagging multiple die results*
        Flagging of multiply tested die is enabled by default in **stdf2map.config**, use this flag to temporarily disable it, see :ref:`flags-label`
    
    * **-g GOOD_DIE, --good=GOOD_DIE**
        Specify Good Die Percentage - Applies to Demo ONLY, see :ref:`demo-label`

    * **-i, --info**  |rAarr| *Print Data Summary Info - Does not create map*   
        This command is useful if you want to determine the wafer id's, number of wafers, or number of test sets in an STDF file
    
    * **-l LOGLEVEL, --loglevel=LOGLEVEL**  |rAarr| *Override default Log Level*
        The default loglevel is set in **stdf2map.config** and is typically INFO.  This command allows you to temporarily override the default, i.e.::
            
                --loglevel=DEBUG
                
        Valid values in order of increasing severity are NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
        
    * **-o OUTFILE, --output=OUTFILE** |rAarr| *Specify output image file*
        Use this option to override the default file naming routine to give your map a specific filename.  File will be saved in the format given by the file extension (.bmp, .jpg, .png, etc...).  If you do not supply a file extension the default is **.png** (or that specified by the **map_format** option in **stdf2map.config**)
        
    * **-q, --quiet**  |rAarr|  *Suppress messages*
        By default, **stdf2map** will output messages to the screen at the currently active loglevel.  Use this mode to suppress these messages
        
        .. note::
        
            **--quiet** only suppresses messages to the screen.  Messages are still sent to the logfile.
        
    * **-s, --symbols** |rAarr|  *Disable Symbols*
        Use this option to temporarily disable symbols on an output map.  It only has an effect if symbols have actually been assigned to specific Bins, see :ref:`symbol-label`
        
    * **-t TESTSET, --testset=TESTSET**
        Select a specific testset to be mapped, requires integer argument > 0.  If the requested testset does not exist in the data, an error will be logged. See also: :ref:`flags-label`
        
    * **-v, --viewer** |rAarr| *Launch MapViewer*, See :ref:`viewer-label`
    
    * **-w WAFERID, --wafer=WAFERID**
        Select a specific wafer to be mapped.  Argument is the string waferid as stored in the STDF **WIR** *WAFER_ID* field.  For the purposes of extraction, the string is NOT case sensitive.  If you are not sure what WAFER_ID's a lot contains, you can use the **-i** command.  
        
        .. note::
        
            **If** the internal WAFER_ID is stored as a string that can be converted to an integer (i.e. "01", "10", "24", etc), you can specify a integer value as the argument.  For example if the internal WAFER_ID is "03", then the following are all equivalent:
            
                * stdf2map -w03  *-(or)-* stdf2map --wafer=03
                * stdf2map -w3   *-(or)-* stdf2map --wafer=3
    
    * **-x BASEWIDTH, --width=BASEWIDTH**  |rAarr|  *Base Width of map*
    * **-y BASEHEIGHT, --height=BASEHEIGHT** |rAarr| *Base Height of map* 
        The base width and height of an image are set by two options in **stdf2map.config** appropriately named **basewidth** and **baseheight**.  The **-x** and **-y** options allow you to temporarily override these defaults to create a different size image.  Please note that **basewidth** and **baseheight** do not define the **actual** size of the output image, but rather a starting point for the size of the actual diemap itself.  Adding a title, legend and axes will all increase the actual size of the rendered image.  In addition, the actual size of the output map may be increased by the autosizing methods. 

    * **-z, --dump**  |rAarr|  Dumps some internal data structures to the screen that may be useful for debugging.
        
            
Output from stdf2map --help::

    Usage: stdf2map [options] filename

     Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -a, --autosize        Disable autosize mode
      -b BINMAP, --binmap=BINMAP
                            Binmap should be either 'sbin' or 'hbin'
      -c USER_CONF, --conf=USER_CONF
                            Load a user configuration file
      -d DEMO, --demo=DEMO  Generate a Demo WaferMap, integer argument is number
                            of wafers (1-99)
      -e THEME, --theme=THEME
                            Specify a theme configuration file
      -f, --flag            Disable flagging multiple die results
      -g GOOD_DIE, --good=GOOD_DIE
                            Specify Good Die Percentage - Applies to Demo ONLY
      -i, --info            Print Data Summary Info - Does not create map
      -l LOGLEVEL, --loglevel=LOGLEVEL
                            Override default Log Level
      -o OUTFILE, --output=OUTFILE
                            Specify output image file
      -q, --quiet           Suppress messages
      -s, --symbols         Disable Symbols
      -t TESTSET, --testset=TESTSET
                            Select testset number - First test is 1, retests are
                            2,3 ...etc.
      -v, --viewer          Launch MapViewer
      -w WAFERID, --wafer=WAFERID
                            Specify a single wafer ID within file
      -x BASEWIDTH, --width=BASEWIDTH
                            Base Width of map (overrides default)
      -y BASEHEIGHT, --height=BASEHEIGHT
                            Base Height of map (overrides default)
      -z, --dump            Dump lot data to screen   