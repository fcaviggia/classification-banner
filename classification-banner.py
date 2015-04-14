#!/usr/bin/python
# Classification Banner
#
# This script was written by Frank Caviggia, Red Hat Consulting
# Last update was 14 April 2015
# This script is NOT SUPPORTED by Red Hat Global Support Services.
# Please contact Rick Tavares for more information.
#
# Script: classification-banner.py
# Description: Displays a Classification for an Xwindows session
# Copyright: Red Hat Consulting, 2014
# Author: Frank Caviggia <fcaviggi (at) redhat.com>
# Version: 1.6.1
# License: GPLv2

import sys
import os
import optparse
import time

try:
    os.environ['DISPLAY']
    import pygtk
    import gtk
except:
    print("Error: DISPLAY environment variable not set.")
    sys.exit(1)


# Classification Banner Class
class Classification_Banner:
    """Class to create and refresh the actual banner."""

    def __init__(self, message="UNCLASSIFIED", fgcolor="#000000",
                 bgcolor="#00CC00", face="liberation-sans", size="small",
                 weight="bold",x=0,y=0,opacity=0.75):
        """Set up and display the main window

        Keyword arguments:
        message -- The classification level to display
        fgcolor -- Foreground color of the text to display
        bgcolor -- Background color of the banner the text is against
        face    -- Font face to use for the displayed text
        size    -- Size of font to use for text
        weight  -- Bold or normal
        hres    -- Horizontal Screen Resolution (int) [ requires vres ]
        vres    -- Vertical Screen Resolution (int) [ requires hres ]
	opacity -- Opacity of window (float) [0 .. 1, default 0.75]
        """
        # Dynamic Resolution Scaling
        self.monitor = gtk.gdk.Screen()
        self.monitor.connect("size-changed", self.resize)
        # Newer versions of pygtk have this method
        try:
            self.monitor.connect("monitors-changed", self.resize)
        except:
            pass

        # Create Main Window
        self.window = gtk.Window()
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("hide", self.restore)
        self.window.connect("key-press-event", self.keypress)
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(bgcolor))
        self.window.set_property('skip-taskbar-hint', True)
        self.window.set_property('skip-pager-hint', True)
        self.window.set_property('destroy-with-parent', True)
        self.window.stick()
        self.window.set_decorated(False)
        self.window.set_keep_above(True)
        self.window.set_app_paintable(True)
	if self.window.is_composited() == True:
		self.window.set_opacity(opacity)
        if x == 0 or y == 0:
        	# Try Xrandr to determine primary monitor resolution
		try:
			self.screen = os.popen("xrandr | grep primary | awk '{ print $4 }'").readlines()[0]
			self.hres = self.screen.split('x')[0]
			self.vres = self.screen.split('x')[1].split('+')[0]
		except:
			try:
				self.screen = os.popen("xrandr | grep connected | awk '{ print $3 }'").readlines()[0]
				self.hres = self.screen.split('x')[0]
				self.vres = self.screen.split('x')[1].split('+')[0]
			except:
				self.screen = os.popen("xrandr | grep '^\*0' | awk '{ print $2$3$4 }'").readlines()[0]
				self.hres = self.screen.split('x')[0]
				self.vres = self.screen.split('x')[1].split('+')[0]
			else:
				# Fail back to GTK method
				self.display = gtk.gdk.display_get_default()
				self.screen = self.display.get_default_screen()
				self.hres = self.screen.get_width()
				self.vres = self.screen.get_height()
	else:
		# Resoultion Set Staticly
		self.hres = x
		self.vres = y
        self.window.set_default_size(int(self.hres), 5)

        # Create Main Vertical Box to Populate
        self.vbox = gtk.VBox()
	self.hbox = gtk.HBox()

        self.label = gtk.Label(
            "<span font_family='%s' weight='%s' foreground='%s' size='%s'>%s</span>" %
            (face, weight, fgcolor, size, message))
        self.label.set_use_markup(True)
        self.label.set_justify(gtk.JUSTIFY_CENTER)
        self.hbox.pack_start(self.label, True, True, 0)

	self.label = gtk.Label(
            "<span font_family='liberation-sans' weight='normal' foreground='%s' size='x-small'>  (ESC to hide)  </span>" %
            (fgcolor))
        self.label.set_use_markup(True)
        self.label.set_justify(gtk.JUSTIFY_RIGHT)
        self.hbox.pack_start(self.label, False, False, 0)

        self.vbox.pack_start(self.hbox, True, True, 0)

        self.window.add(self.vbox)
        self.window.show_all()
        self.width, self.height = self.window.get_size()

    # Restore Minimized Window
    def restore(self, widget, data=None):
	self.window.deiconify()
	self.window.present()
        return True

    # Destroy Classification Banner Window on Resize (Display Banner Will Relaunch)
    def resize(self, widget, data=None):
        self.window.destroy()
        return True

    # Press ESC to hide window for 15 seconds
    def keypress(self, widget, event=None):
	if event.keyval == 65307:
		if gtk.events_pending() == False:
			self.window.iconify()
			self.window.hide()
			time.sleep(15)
			self.window.show()
			self.window.deiconify()
			self.window.present()
	return True


class Display_Banner:
    """Display Classification Banner Message"""
    def __init__(self):

        # Dynamic Resolution Scaling
        self.monitor = gtk.gdk.Screen()
        self.monitor.connect("size-changed", self.resize)
        # Newer versions of pygtk have this method
        try:
            self.monitor.connect("monitors-changed", self.resize)
        except:
            pass

        # Launch Banner
        self.config, self.args = self.configure()
        self.execute(self.config)

    # Read Global configuration
    def configure(self):
        config = {}
        try:
            execfile("/etc/classification-banner", config)
        except:
            pass
        defaults = {}
        defaults["message"] = config.get("message", "UNCLASSIFIED")
        defaults["fgcolor"] = config.get("fgcolor", "#000000")
        defaults["bgcolor"] = config.get("bgcolor", "#00CC00")
        defaults["face"] = config.get("face", "liberation-sans")
        defaults["size"] = config.get("size", "small")
        defaults["weight"] = config.get("weight", "bold")
        defaults["show_top"] = config.get("show_top", True)
        defaults["show_bottom"] = config.get("show_bottom", True)
        defaults["hres"] = config.get("hres", 0)
        defaults["vres"] = config.get("vres", 0)
	defaults["opacity"] = config.get("opacity", 0.75)
     
        # Use the global config to set defaults for command line options
        parser = optparse.OptionParser()
        parser.add_option("-m", "--message", default=defaults["message"],
                          help="Classification message")
        parser.add_option("-f", "--fgcolor", default=defaults["fgcolor"],
                          help="Foreground (text) color")
        parser.add_option("-b", "--bgcolor", default=defaults["bgcolor"],
                          help="Background color")
        parser.add_option("--face", default=defaults["face"], help="Font face")
        parser.add_option("--size", default=defaults["size"], help="Font size")
        parser.add_option("--weight", default=defaults["weight"],
                          help="Font weight")
        parser.add_option("--hide-top", default=defaults["show_top"],
                          dest="show_top", action="store_false",
                          help="Disable the top banner")
        parser.add_option("--hide-bottom", default=defaults["show_bottom"],
                          dest="show_bottom", action="store_false",
                          help="Disable the bottom banner")
        parser.add_option("-x", "--hres", default=defaults["hres"],
                          help="Horizontal Screen Resolution")
        parser.add_option("-y", "--vres", default=defaults["vres"], 
                          help="Vertical Screen Resolution")
	parser.add_option("-o", "--opacity", default=defaults["opacity"], 
                          help="Window opacity for composted window managers")

        options, args = parser.parse_args()
        return options, args

    # Launch the Classification Banner Window(s)
    def execute(self, options):
        if options.show_top:
            top = Classification_Banner(
                options.message,
                options.fgcolor,
                options.bgcolor,
                options.face,
                options.size,
                options.weight,
                int(options.hres),
                int(options.vres),
		float(options.opacity))
            top.window.move(0, 0)
        if options.show_bottom:
            bottom = Classification_Banner(
                options.message,
                options.fgcolor,
                options.bgcolor,
                options.face,
                options.size,
                options.weight,
                int(options.hres),
                int(options.vres),
		float(options.opacity))
            bottom.window.move(0, int(bottom.vres))

    # Relaunch the Classification Banner on Screen Resize
    def resize(self, widget, data=None):
        self.config, self.args = self.configure()
        self.execute(self.config)
        return True


# Main Program Loop
if __name__ == "__main__":
    run = Display_Banner()
    gtk.main()
