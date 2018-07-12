
.. image:: images/pageheader.png

Installation
============

	* Unpack
	* Decide where you want to store configuration files 
	* Edit *config.py* (read the comments near the top of the file) and set **_config_path=**. A default configuration file will be created in the directory you select the first time you run the application. 
	* Copy all of the files from the distribution **conf/** directory to the location used in the above step.
	* run **python setup.py install** (or **sudo python setup.py install** on Linux with privs)   
	* the setup file should install an executable in your python's **script** directory.  If your python path is set up correctly, you should be able to run the application with the command: **stdf2map** 
	* try **stdf2map -a**  and you should get a NOTE about generating a default config file and then a list of command-line options
	* assuming that worked, you should now have a default config file in the directory you chose above, change to that directory and edit the config file (should be **stdf2map.config** (or may be **stdf2map-script.config** on Windows)
	* Set/check the following:
		
		* **map_path**  *(default base directory for maps when -o command line option not used)*
		* **stdf_path** *(default location for stdf file input)* 
		* **logfile** *(full path with filename)*
		* **logfile_size**  *(May leave at default)*
		* **logfile_rotates** *(May leave at default)*

		.. note::
		
			Please ensure you have the proper read/write privileges for the directories you select

		* if you typically use **sbin** instead of **hbin** in your STDF files, set **binmap='sbin'** as the default (many fabs populate both with the same bin number, so it may not make a difference to you), plus you can always select one or the other from the command line with the **-b** option.
        
	* all other options can stay the same until you get a feel for things... **save the file**
	* **Optional** - Copy the stdf sample files from the distribution **stdf** directory to **stdf_path** you set above. (Otherwise, you will need to change to the stdf directory to execute the example commands in this documentation)

Dependancies
------------
  * **PIL (pillow)** - graphical routines / image saving
  * **toml** - reading config files
  * **wxPython** - built-in map viewer

Currently set up to use truetype fonts, specifically **Arial** and **Arialbd**.  I have not tested it with other fonts or types (although they *should* (may?) be supported)



.. note::

	Linux users may need to install **Arial** and **Arialbd** 

	Not all Linux systems have truetype fonts installed by default.  There are several methods to install them, and the easiest method may vary by distro.  Consult your favorite search engine if you are not sure how to get them installed.  For Ubuntu, here's a link that should help: https://www.ostechnix.com/install-microsoft-windows-fonts-ubuntu-16-04/

Setup.py should take care of installing **PIL** and **toml** if you don't already have them installed, but again, depending on your linux distribution, you many need to install **wxPython** manually.  For many distributions, it may be as simple as:: 

	 $ pip install -U wxPython  
	
Please see the wxPython website for more information if you have trouble getting wxPython installed.  https://www.wxpython.org/



