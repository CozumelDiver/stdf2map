.. image:: images/pageheader.png


Optional Config Files
=====================

In addition to the main config file, **stdf2map.config**, There are three other types of config files, all optional.  These config files may contain any entries that are found in **stdf2map.config** (exclusive of the entries noted at the very top of **stdf2map.config**).  All config files should be created in your **conf/** directory.  

.. note::
	When using config files, be aware that settings are applied in this order: 
	
	* **stdf2map_config**
	* **THEME config file**
	* **PART config file**
	* **USER config file specified with -c option**
	* **other command line arguments (-b, -x, -w, -t, etc..)**

Any options applied later in the chain will supersede previous values, thus you should put the **bare minimum** in any config file that will get the desired results.

.. warning::

	Keep backups of your config files! It's ***very easy*** to crash the program with an obscure **typo** in a config file. You **WILL** run into this!  It is highly recommended you **keep backups** until you've tested them! 

.. _userconf-label:

USER Config Files
-----------------

User config files are specified on the command line with the **-c** option and can be very useful for temporarily changing various options without having to edit **stdf2map.config**.  You can give user config files any legal name, but it must have a **.toml** extension.  There are a few sample user config files supplied in the distribution **conf/** directory.

For example::

	$ stdf2map -c thumb a595 -v 
	
.. note:: 

	The file extension **".toml"** is optional when using the **-c** option
	
.. image:: images/a595-thumb.png

*thumb.toml* file::

	# thumb.toml
	# Generate a small thumbnail, set image to a small size with
	# minimal padding and disable symbols, title, legend, axes, 
	# flagging, grid, timestamp, flat

	# NOTE: Autosizing will still be enabled by default.
	# If you "really want" the image to be "basewidth x baseheight"
	# in size, uncomment the autosize entry

	enable_symbols=false

	[image]
	padding=3
	basewidth=100
	baseheight=100
	border=true
	flatline=false
	timestamp=false

	#autosize=false

	[flag]
	show = false

	[axis]
	show = false
	grid = false

	[title]
	show=false

	[legend]
	show=false

	[file]
	thumb_mode=true

|
	
Or a slightly different version that makes the thumbnail a little bigger, removes the border, includes the flat and sets the background to white::

	$ stdf2map -c thumb1 a595 -v 
	
.. image:: images/a595-thumb1.png

We will see the user config file in action again when we discuss :ref:`symbol-label`

PART Config Files
-----------------

Unlike user config files, part config files are **automatically** applied when a file with a matching **MIR** field **PART_TYP** is processed.  These can be used to control options that will be applied to specific groups of maps based on the part type.

.. warning:: 
	
	**Linux Note:** - Part config file naming must have the **same casing** as your actual part name.  

Some typical uses might be:

	* Set different Bin labels for different parts
	* Use the **map_path** and **auto_filename** options to group maps into specific directories by part
	* Alter Bin Colors or set Symbols on specific parts so critical bins are more visible
	* Alter the base map size to make parts with **many** die bigger and easier to see
	
As an example, **lot2** and **lot3** in the distribution **stdf** directories both have and MIR **PART_TYP** of GOLD8BAR,  Since a GOLD8BAR.toml file exists, the settings in there will be automatically applied, and we've used them to change the map base size, several of the maps colors, and to give the Bin labels generic values::

	$ stdf2map lot2 -vf 
	
.. image::  images/lot2.png

*GOLD8BAR.toml* file::

	# GOLD8BAR.toml
	# Sample part config file for lot2 and lot3 in the 
	# distribution stdf directory

	[image]
	bgcolor='#DAFEE7'
	autosize_minpx=6
	basewidth=800
	baseheight=800

	[axis]
	color = '#366523'
	grid = true
	gridcolor='#999999'

	[title]
	bgcolor='#C7E6FF'
	key_color = "#8A0404"
	value_color ="#113AAD"

	[legend]
	sort_bins_by_count=true

	[flag]
	# size of flag as a ratio of diesize 
	# flagsize = diesize/size_factor.
	# i.e. smaller numbers = bigger flag
	# use a minimum of 1.0 
	size_factor = 1.4

	#Change Some Bin Labels
	[bin]
	0 = {color="#FFFFFF", label='-'}
	1 = {color="#00FF00", label="Good Die"}
	2 = {color="#FF0000", label="Bin 2"}
	3 = {color="#009999", label="Bin 3"}
	4 = {color="#FEF102", label="Bin 4"}
	5 = {color="#7120A8", label="Bin 5"}
	6 = {color="#880000", label="Bin 6"}
	7 = {color="#FFFFFF", label="Bin 7"}
	8 = {color="#FF9933", label="Bin 8"}
	9 = {color="#BF6E11", label="Bin 9"}
	10 = {color="#0000FF", label="Bin 10"}
	
.. _themeconf-label:
	
THEME Config Files
------------------
Theme config files can be used for any purpose but would typically be used to change the visual appearance of the maps *(background color, font colors, borders, etc.)*.  A desired default theme can be specified in the **_theme=** variable near the top of **stdf2map.config** or you can supply a theme file using the command-line **-e** option 

Two examples are provided in **conf/** directory::  

	$ stdf2map -etheme_light a595 -v  
	
.. note:: 

	The file extension **".toml"** is optional when using the **-e** option
	
.. image:: images/a595-theme_light.png

*theme_light.toml* file::	

	# theme_light.toml
	# A light wafermap theme

	[image]
	bgcolor='#FFFFFF'
	streetcolor='#000000'
	border=false
	bordercolor='#FFFFFF'
	timestampcolor='#999999'

	[axis]
	color = '#7F7F7F'
	grid = true
	gridcolor='#CCCCCC'

	[title]
	bgcolor='#FFFFFF'
	key_color = "#007F00"
	value_color ="#00007F"

	[legend]
	sort_bins_by_count=true
	fontcolor='#000000'
	
...and another example::

	$ stdf2map -etheme_dark a595 -v  
	
.. image:: images/a595-theme_dark.png

*theme_dark.toml* file::

	# theme_dark.toml
	# A dark wafermap theme

	[image]
	bgcolor='#000000'
	streetcolor='#000000'
	bordercolor='#666666'
	timestampcolor='#D2D2D2'

	[axis]
	color = '#999999'
	grid = true
	gridcolor='#333333'

	[title]
	bgcolor='#000000'
	key_color = "#FFFFAA"
	value_color ="#D4FFFF"

	[legend]
	sort_bins_by_count=true
	fontcolor='#FFFFFF'
	overflow_textcolor='#FC9090'	