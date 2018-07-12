
import os.path
import sys
import wx
import wx.adv
import wx.lib.dialogs
import re
import toml     #loading/saving config info
import imghdr   #for determining image type

import embedded_images as emb   #toolbar images
import wx.lib.scrolledpanel as scrolled
from _version import __version__
from config import App

try:
    from agw import hyperlink as hl
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.hyperlink as hl

try:
    import agw.infobar as IB
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.infobar as IB

 
class Mapviewer(wx.App):
    
    def __init__(self, redirect=False, filename=None, size=(800,600)):
        
        sidepanel_width = 200
        
        self.saveImage = wx.Image(1,1)
                
        wx.App.__init__(self, redirect, filename)
        
        # Default configuration if the config file cannot be read
        self.config={'width':800, 
                     'height':600, 
                     'xpos':10, 
                     'ypos':10,
                     'splitter': -200,
                     'lastdir':App.cfg['file']['map_path']}
        
        self.cfg_file = os.path.basename(__file__).rsplit('.',1)[0] + ".config"
        self.cfg_path = os.path.join(App.cfg['_config_path'], self.cfg_file)
        
        try:
            self.config = toml.load(self.cfg_path, _dict=dict)
        except:
            pass
        
        self.frame = wx.Frame(None, title='Map Viewer', size = (self.config['width'], self.config['height']))  
        self.frame.SetPosition((self.config['xpos'],self.config['ypos']))
            
        self.frame.Bind(wx.EVT_CLOSE, self.onClose)
        
        # Frame icon...
        icon=wx.Icon()
        icon.CopyFromBitmap(wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE, wx.ART_TOOLBAR, (16,16)))
        self.frame.SetIcon(icon)
        
        # Create a status bar
        self.sb = self.frame.CreateStatusBar(style=wx.SB_SUNKEN)
      
        # Create a splitter and instantiate the two classes 
        # they will hold, ImagePanel on the left and SidePanel 
        # on the right
        self.splitter=wx.SplitterWindow(self.frame, -1, )
        self.imgPanel = ImagePanel(self.splitter)
        self.sidePanel = SidePanel(self.splitter, sidepanel_width)
        
        
        self.splitter.SplitVertically(self.imgPanel, self.sidePanel, self.config['splitter'])
        # This seems to cause issues with restoring a saved splitter sash location.
#         self.splitter.SetMinimumPaneSize(sidepanel_width)

        #Anchor the splitter to the Side Panel
        self.splitter.SetSashGravity(1.0)  
                       
        self.frame.Show()
        
        
    def loadFile(self, filepath):
        
        if not filepath:
            return
        if os.path.isdir(filepath):
            return
        if imghdr.what(filepath) is None:
            self.imgPanel.info.ShowMessage("Not an Image or supported image type!", wx.ICON_WARNING)
            return
        
        img = wx.Image(filepath, wx.BITMAP_TYPE_ANY)
        if img.IsOk():
            self.imgPanel.info.Dismiss()
            self.show(img)
            
               
    # The only reason this is in a separate function is so we can 
    # directly feed it an image from stdf2map        
    def show(self,img=None):
        
        if not img:
            return 
        
        self.saveImage = img        
        self.imgPanel.setImage(img)        

    
    
    def onClose(self, event):
       
        # Try to save some settings, but we don't
        # want anything mucking up the close event...
        try: 

            xpos, ypos = wx.GetApp().frame.Position
            width, height = wx.GetApp().frame.GetSize()
            
            self.config['width'] = width
            self.config['height'] = height
            self.config['xpos'] = xpos
            self.config['ypos'] = ypos
            self.config['splitter'] = self.splitter.GetSashPosition()
                   
            f = open(self.cfg_path, 'w')
            toml.dump(self.config,f)
            f.close()
                       
        except:
            pass
        
        finally:
            # Let default handler do the destroying...
            event.Skip()
             
            
            
    def fitImage(self):
        
        #Get the currently displayed
        bitmap = self.imgPanel.getImage()          
        
        wxImg = bitmap.ConvertToImage()
        
        #Scale the image, preserving the aspect ratio
        W = wxImg.GetWidth()
        H = wxImg.GetHeight()
        
        client_width, client_height = self.imgPanel.GetClientSize()
        
        if W > H:
            NewW = client_width
            NewH = client_width * H / W
        else:
            NewH = client_height
            NewW = client_height * W / H
            
        wxImg = wxImg.Scale(NewW,NewH,wx.IMAGE_QUALITY_HIGH)
        self.imgPanel.setImage(wxImg)
 
    # Convert PIL image to wxImage        
    def PilImageToWxImage(self, myPilImage, copyAlpha=True ) :

        hasAlpha = myPilImage.mode[ -1 ] == 'A'
        if copyAlpha and hasAlpha :  # Make sure there is an alpha layer copy.

            myWxImage = wx.EmptyImage( *myPilImage.size )
            myPilImageCopyRGBA = myPilImage.copy()
            myPilImageCopyRGB = myPilImageCopyRGBA.convert( 'RGB' )    # RGBA --> RGB
            myPilImageRgbData =myPilImageCopyRGB.tobytes()
            myWxImage.SetData( myPilImageRgbData )
            myWxImage.SetAlphaData( myPilImageCopyRGBA.tostring()[3::4] )  # Create layer and insert alpha values.

        else :    # The resulting image will not have alpha.

            myWxImage = wx.Image( *myPilImage.size )
            myPilImageCopy = myPilImage.copy()
            myPilImageCopyRGB = myPilImageCopy.convert( 'RGB' )    # Discard any alpha from the PIL image.
            myPilImageRgbData =myPilImageCopyRGB.tobytes()
            myWxImage.SetData( myPilImageRgbData )

            return myWxImage
        
        
#==============================================================================
# ImagePanel class, displays the map image
#------------------------------------------------------------------------------
class ImagePanel(scrolled.ScrolledPanel):
    def __init__(self, parent, id = -1, size = wx.DefaultSize):
        
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        
        #Placeholder for the imageCtrl creation
        self.mapImage = wx.Image(1,1)
        self.imageCtrl = wx.StaticBitmap(self, wx.ID_ANY,wx.Bitmap(self.mapImage))
                    
#        self.maxWidth  = 1000
#        self.maxHeight = 1000

        self.SetBackgroundColour("WHITE")

#        self.SetVirtualSize((self.maxWidth, self.maxHeight))
                         
        self.Bind(wx.EVT_SIZE, self.OnResize, self)

        font = wx.Font(16, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        
        self.info = IB.InfoBar(self)
        self.info.SetFont(font) 
        self.info.SetBackgroundColour("#FFFF00")
        
        # Yeah, I know... _variable's are supposed to be private... but I wanted a color
        # with a little more contrast than the default...  will wrap this in a try, just 
        # in case it ever changes.
        
        try:
            self.info._text.SetBackgroundColour("#FFFF00")
            self.info._text.SetOwnForegroundColour("#000000")
        except:
            pass
 
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.info, 0, wx.EXPAND)
        vbox.Add(self.imageCtrl,0,wx.ALL)     
        self.SetSizer(vbox) 

        self.SetupScrolling()
        
    def OnResize(self,event):
        self.updateStatusBar()
       
    def getImage(self):
        return(self.imageCtrl.GetBitmap())
    
    def setImage(self, newimg):
        self.SetVirtualSize(newimg.GetSize())
        self.imageCtrl.SetBitmap(wx.Bitmap(newimg))       
        self.updateStatusBar()
        self.Refresh()
        self.SetupScrolling()
    
    def updateStatusBar(self):
        clientsize=self.GetClientSize()
        imagesize = self.imageCtrl.GetBitmap().GetSize()
        wx.GetApp().sb.SetStatusText("Image Size: {}  Client Size: {}".format(imagesize, clientsize))
         

        
        
#==============================================================================
# SidePanel class, contains the toolbar & directory lists
#------------------------------------------------------------------------------        
class SidePanel(wx.Panel):
    def __init__(self, parent, splitwidth):
        wx.Panel.__init__(self, parent=parent)
      
        #--------------------------------------------------------------------------       
        # Build the toolbar
        #--------------------------------------------------------------------------
        self.tb = wx.ToolBar(self,-1, style=wx.TB_NODIVIDER)
        self.tb.SetToolBitmapSize((16,16))  # sets icon size
        
        fitTool = self.tb.AddTool(wx.ID_ANY, "Fit", emb.GetBitmap_resize_fit_png(), "Fit Image To Frame")
        self.Bind(wx.EVT_MENU, self.onFitImage, fitTool)
        
        actualTool = self.tb.AddTool(wx.ID_ANY, "Fit", emb.GetBitmap_resize_actual_png(), "Retore image to Original Size")
        self.Bind(wx.EVT_MENU, self.onRestoreImage, actualTool)
        
        # Adds some visual separation, but no actual divider since we 
        # created the toolbar with the NO_DIVIDER style
        self.tb.AddSeparator()
        
        homeTool = self.tb.AddTool(wx.ID_ANY, 'Home', emb.GetBitmap_home_png(), 'Go to Home Directory')
        self.Bind(wx.EVT_MENU, self.onHomeDir, homeTool)
        
        folderTool = self.tb.AddTool(wx.ID_ANY, 'Folder', emb.GetBitmap_directory_png(), 'Select Map Directory')
        self.Bind(wx.EVT_MENU, self.onSetMapDir, folderTool)
        
        refreshTool = self.tb.AddTool(wx.ID_ANY, "Refresh", emb.GetBitmap_refresh_png(), "Refresh Directory List")
        self.Bind(wx.EVT_MENU, self.onFileRefresh, refreshTool)
        
        self.tb.AddSeparator()
                        
        logTool =  self.tb.AddTool(wx.ID_ANY, 'Logfile', emb.GetBitmap_filelog_png(), 'Show Log File')
        self.Bind(wx.EVT_MENU, self.onShowLog, logTool)
        
        infoTool =  self.tb.AddTool(wx.ID_ANY, 'Info',  emb.GetBitmap_info_png(), 'Application Information')
        self.Bind(wx.EVT_MENU, self.onAboutDlg, infoTool)
        
        self.tb.Realize()
        
        #----------------------------------------------------------------------
        # File Control for map/directory selection
        #----------------------------------------------------------------------
        map_path = App.cfg['file']['map_path']
        self.fc = FileCtrl(self, pos=(5,10), defaultDirectory=map_path)
        self.fc.SetSize((splitwidth,400))
        lastdir = wx.GetApp().config['lastdir']
        
        self.fc.SetDirectory(lastdir)  
             
        wcstr = "All Files (*.*)|*.*|PNG Files (*.png)|*.png|BMP Files (*.bmp)|*.bmp|GIF Files (*.gif)|*.gif|"
        wcstr += "JPG Files (*.jpg)|*.jpg|TIFF Files (*.tiff)|.tiff|PPM files (*.ppm)|.ppm"
        
        self.fc.SetWildcard(wcstr)

        #----------------------------------------------------------------------
        # User defined directory listbox
        #----------------------------------------------------------------------
        text1 = wx.StaticText(self, -1, "User Defined Map Directories", (20, 10))

        self.lb_config = wx.ListBox(self, id=wx.ID_ANY, pos=(100, 250), size=(splitwidth, 120), style=wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.onLB_Config, self.lb_config)
        self.get_conf_mapdirs() 
               
        #----------------------------------------------------------------------
        # Sizers to glue everything together...
        #----------------------------------------------------------------------                
        tbSizer = wx.BoxSizer(wx.HORIZONTAL)
        tbSizer.AddStretchSpacer(prop=3)
        tbSizer.Add(self.tb,1,wx.ALL,5)
        
        topSizer = wx.BoxSizer(wx.VERTICAL)                
        topSizer.Add(tbSizer,0,wx.ALL,5)       
        topSizer.Add(self.fc,6,wx.EXPAND)
        topSizer.Add(text1,0,wx.ALL,5)
        topSizer.Add(self.lb_config,2,wx.ALL|wx.EXPAND,5)
        
        self.SetSizer(topSizer)
        topSizer.Fit(self)
              
    
    #--------------------------------------------------------------------------
    # Toolbar Callbacks
    #--------------------------------------------------------------------------
    # Callback when the toolbar "Fit Image" icon is selected 
    def onFitImage(self,event):
        wx.GetApp().fitImage()
        
    def onRestoreImage(self,event):
        img = wx.GetApp().saveImage
        wx.GetApp().imgPanel.setImage(img)
    
    # Callback when the toolbar "Home" icon is selected 
    def onHomeDir(self,event):
        self.fc.SetDirectory(App.cfg['file']['map_path'])    
        
       
     # Callback when the toolbar "Folder" icon is selected.       
    def onSetMapDir(self, event):
         # In this case we include a "New directory" button.
        dlg = wx.DirDialog(self, "Select Directory:",
                          style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )

        if dlg.ShowModal() == wx.ID_OK:
            self.fc.SetDirectory(dlg.GetPath())
            wx.GetApp().config['lastdir'] = dlg.GetPath()

        dlg.Destroy()
        
    # Callback when the toolbar "Refresh" icon is selected 
    def onFileRefresh(self, event):
        self.fc.SetDirectory(wx.GetApp().config['lastdir'])
        
    # Callback when the toolbar "Sho Log" icon is selected   
    def onShowLog(self,event):
        
        logfile = App.cfg['file']['logfile']
        f = open(logfile, "r")
        msg = f.read()
        f.close()

        dlg = wx.lib.dialogs.ScrolledMessageDialog(self, msg, "Log file", size=(700,500))
#         dlg.ShowModal()
        dlg.Show(show=1)
    
        
    # Callback when the toolbar "Info" icon is selected.
    def onAboutDlg(self, event):
        
        # Size of the about dialog
        about_width = 400
        about_height = 300
        
        # Center the dialog in the middle of the App Frame
        app_x, app_y = wx.GetApp().frame.Position
        frw, frh = wx.GetApp().frame.GetSize()

        x = frw // 2 - about_width // 2 + app_x 
        y = frh // 2 - about_height // 2 + app_y
                
        aboutDlg = AboutDlg(None, x=x, y=y)
        aboutDlg.ShowModal()
        aboutDlg.Destroy()
        

    # Callback when selecting a directory in the user 
    # specified directories ListBox        
    def onLB_Config(self,event):
        self.fc.SetDirectory(event.GetString())
        wx.GetApp().config['lastdir'] = event.GetString()

    # Populate the "User Specified Directories" (bottom listbox) with a 
    # list of all "map_path" entries found in config files.          
    def get_conf_mapdirs(self):
        
        self.config_dirs=[]
        
        confdir = App.cfg['_config_path']
        os.chdir(confdir)
        # List of files in "config_path"
        conf_files = os.listdir(confdir)

        # Search each file for a "map_path" entry 
        # Typically none or one, but search for any number...
        # This allows a user to create a special file just for 
        # populating this list.
        for fn in conf_files:
            if os.path.isfile(fn):
                for entry in self._getmapdir(fn):
                    if(entry):
                        if entry not in self.config_dirs:
                            self.config_dirs.append(entry)


        # Sort the list and add it to the listbox.
        # if it's a valid dir (and NOT the Home dir)
        for d in sorted(self.config_dirs):
            if os.path.isdir(d) and d != App.cfg['file']['map_path']:
                self.lb_config.Append(d) 

 
    # Generator to search a given file for one or more 
    # "map_path" entries.       
    def _getmapdir(self,filename):
        
        with open(filename,"r") as conf_file:
            for line in conf_file:
                line = line.strip()
                match = re.match("^map_path\s*=\s*[\'\"](.*)[\'\"]",line)
#                 print "line={}, match={}".format(line,match)
                if(match):
                    yield(match.group(1))

           
class FileCtrl(wx.FileCtrl):
    def __init__(self, parent, id=wx.ID_ANY, defaultDirectory="",
                 defaultFilename="",
                 wildCard=wx.FileSelectorDefaultWildcardStr,
                 style=wx.FC_DEFAULT_STYLE|wx.FC_NOSHOWHIDDEN,
                 # | wx.FC_OPEN
                 # | wx.FC_SAVE
                 # | wx.FC_MULTIPLE
                 # | wx.FC_NOSHOWHIDDEN
                 pos=wx.DefaultPosition, size=wx.DefaultSize, name="filectrl", log=None):
        wx.FileCtrl.__init__(self, parent, id, defaultDirectory, defaultFilename,
                             wildCard, style, pos, size, name)

        self.Bind(wx.EVT_FILECTRL_FILEACTIVATED, self.OnFileActivated)
        self.Bind(wx.EVT_FILECTRL_SELECTIONCHANGED, self.OnSelectionChanged)
        self.Bind(wx.EVT_FILECTRL_FOLDERCHANGED, self.OnFolderChanged)
        
# Not currently used
#         self.Bind(wx.EVT_FILECTRL_FILTERCHANGED, self.OnFilterChanged)

    # Callback when a file (map) in the File Control list is
    # single-clicked 
    def OnFileActivated(self, event): 
#         print "...onFileActivated"             
        wx.GetApp().loadFile(self.GetPath())

    # Callback when a file (map) in the File Control list is
    # double-clicked 
    def OnSelectionChanged(self, event):
#         print "...onSelectionChanged"      
        wx.GetApp().loadFile(self.GetPath())
        
    # Callback when a the directory in the File Control list is
    # changed 
    def OnFolderChanged(self, event):
#         print "...onFolderChanged"
        wx.GetApp().config['lastdir']=self.GetDirectory()

# Not currently used 
#     def OnFilterChanged(self, event):
#         self.log.write('Filter Changed: %s\n' % self.GetFilterIndex())

class AboutDlg(wx.Dialog):
 
    def __init__(self, parent, x=100, y=100):
        
        wx.Dialog.__init__(self, None, title="About", pos=(x,y), size=(400,350))
        
        bmp = emb.GetBitmap_wafermap_png()
        img = wx.StaticBitmap(self, -1, bmp, (20, 20), (bmp.GetWidth(), bmp.GetHeight()))
        
        str = "This is a different font."
        hdgtext = wx.StaticText(self, -1, "Map Viewer", (20, 120))
        font = wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
        hdgtext.SetFont(font)
        
        vertext = wx.StaticText(self, -1, __version__, (20, 130))
        font = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        vertext.SetFont(font)
        
        copytext = wx.StaticText(self, -1, "Copyright (c) 2017 - D. Fish\nReleased under GPLv3", (20, 140))
        font = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        copytext.SetFont(font)
        
        str = "This program was developed using wxPython and is part of the stdf2map package available at:"
        abouttext = wx.StaticText(self, -1, str , (40, 200))
        abouttext.Wrap(300)
        
        font = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_NORMAL)
        abouttext.SetFont(font)
        
                
        lblsizer = wx.BoxSizer(wx.VERTICAL)
        lblsizer.Add(hdgtext,0,wx.ALL|wx.CENTER,5)
        lblsizer.Add(vertext,0,wx.ALL|wx.CENTER,5)
        lblsizer.Add(copytext,0,wx.ALL|wx.CENTER,5)
        
        hdgsizer = wx.BoxSizer(wx.HORIZONTAL)
        hdgsizer.Add(img,0,wx.ALL,5)
        hdgsizer.Add(lblsizer,0,wx.ALL,5)
        
        link = hl.HyperLinkCtrl(self, wx.ID_ANY, "http://www.github.com/CozumelDiver/stdf2map",
                                        URL="http://www.github.com/CozumelDiver/stdf2map")
        
        midsizer = wx.BoxSizer(wx.VERTICAL)
        midsizer.Add(abouttext,0,wx.ALL,5) 
        midsizer.Add(link,0,wx.ALL,10)                      
        
        okBtn = wx.Button(self, wx.ID_OK)
              
        topsizer = wx.BoxSizer(wx.VERTICAL)
        topsizer.Add(hdgsizer,0,wx.ALL,5)
        topsizer.Add(midsizer,1,wx.ALL,5)
                        
        topsizer.Add(okBtn, 0, wx.ALL|wx.CENTER,5)
        
        self.SetSizer(topsizer)
        

        
