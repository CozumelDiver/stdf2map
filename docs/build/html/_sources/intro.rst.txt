
	
.. image:: images/pageheader.png
	
Intro
=====

**stdf2map** is a lightweight python-based command line application for generating 
reasonably good looking Bin wafermaps from industry standard STDF data files  
created by Automated Test Equipment (ATE) used in the semiconductor industry.

Features
--------

 * Supports multiple wafers within an STDF file
 * Handles multiple testing *(retesting)* of die on the same wafer
 * Supports mapping either software or hardware BIN (*sbin* or *hbin*)
 * Flagging of die that did not **result in the same bin number** when multiply tested
 * Bin assignable symbols improves visual feedback for critical bins.
 * Part-based configuration files allow assignment of bin labels, colors, options, etc on a part-by-part basis
 * Highly configurable, nearly every aspect can be changed via configuration file
 * Create tiny thumbnails or huge images that can be made into posters
 * Auto-sizing feature allows wafers with thousands of die to have legible maps automatically created.
 * Command-line based, should be easy to integrate into user-written scripts for automatic/batch wafermap creation.
 * File globbing supported, Create entire directories of maps with a single command.
 * Demo mode creates realistic wafermaps and provides a path for testing modifications / enhancements that may fall outside the realm of available STDF files
 * STDF v4 Compatible *(possibly v3 - untested)*
 * Supported Output Formats: BMP, EPS, GIF, JPG, PCX, PNG, PPM, TIFF, WEBP
 * Built-in map viewer (BMP, GIF, JPG, PNG, PPM, TIFF Only)
 * **Free!!** - Peek under the hood, modify it, make it better, share it!

Potential Drawbacks
-------------------
 
 * Still young in the development cycle, may contain bugs!
 * Has not been rigorously tested with a wide variety of STDF files from different fabs/testers.  (I have a very limited supply and they are -*understandably-* quite rare on the web).  I'm retired now... testing is your job!
 * Has only been tested on Windows 7 x64 and Linux Ubuntu v16.04 (x64, VM-based)
 * Not a lot of config file error/syntax checking.  Very easy to crash the program via typo's in config files (although the error typically provides a pretty good clue to the nature of the issue)
 
	.. warning:: **Disclaimer**
	
		This software is provided **AS-IS** without any expressed or implied warranty for fitness or usage.  The end user is responsible for any and all liability that may arise from usage of this software.  *(In other words, if you make process decisions based on this software that end up costing millions of dollars in lost product, don't blame me!)*
	

Inspiration
-----------

I wrote this because I had done something similar many years ago in perl & libgd while working in the semiconductor industry.  Although I have a fairly long programming history (Fortran, C, C++, Perl, PHP, some Java, Javascript and C#, I was interested in learning Python, so it started as a teaching aid...  This is my second python program (*HelloWorld* was the first).  

It's very easy to carry programming habits from an older language to a newer one, and the results may be less than optimal for efficiency or style in the new language. If you wonder why I did something the way I did, or if it's not very *pythonic*, it's out of ignorance and inexperience to the language...  educate me by providing feedback or suggestions, or better yet, fork and improve the application for others.

Implementation
--------------

Built on an stdf parser subclassed from one written in python by Hua Yanghao (available on GitHub at https://github.com/yanghao ) The application uses **PIL** *(pillow)* to generate the wafermap, and **toml** to read configuration files.  The stdf parser appears to be lightweight, yet quite solid, stable, complete and last, but certainly not least, easy for a *pythonic newbie* like myself to grok!

Unlike some wafer mapping tools I've used in the past, **stdf2map** does not know or care about the actual wafer size, or even the die size.  It does not draw a circle with a flat and try to fit the data inside of it.  Instead, it lets the data define the shape, which to no surprise is *usually* circular... I say *usually* because in some situations, such as probing half a wafer, the resulting map will be "cone-shaped" instead of circular.  This was a deliberate design decision to add flexibility and simplicity.  


Sample Maps
-----------
Since images are worth more than a few dozen words, below are some sample wafer maps created by this application.  If these look promising, feel free to explore the rest of the documentation and test out the application on your own data.  

|
 
.. image:: images/a595-thumb.png
	:align: center
	
|
	
.. image:: images/a595-thumb1.png
	:align: center
	
|
	
.. image:: images/a595-09.png
	:align: center
	
|
	
.. image:: images/demo2.png
	:align: center
	
|
	
.. image:: images/demo3.png
	:align: center

|

.. image:: images/a595-theme_light.png
	:align: center

|

.. image:: images/a595-theme_dark.png
	:align: center

|
		
.. image:: images/lot2-t1_flags.png
	:align: center

|
	
.. image:: images/lot2-t2_noflags.png
	:align: center

|
	
.. image:: images/lot3-symbols.png
	:align: center
	






  
 
