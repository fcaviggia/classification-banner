#!/usr/bin/python
# Classification Banner
# Author: Frank Caviggia (fcaviggia@gmail.com)
# Copyright: Frank Caviggia, 2013
# Version: 1.2
# License: GPLv2

import sys
import os
import optparse

try:
    os.environ['DISPLAY']
    import pygtk
    import gtk
except:
    print("Error: DISPLAY environment varible not set.")
    sys.exit(1)

# Classifion Banner Class
class Classification_Banner:
    """Class to create and refresh the actual banner."""

    def __init__(self, message="UNCLASSIFIED", fgcolor="#000000",
        bgcolor="#00CC00", face="liberation-sans", size="small",
        weight="bold"):
        """Set up and display the main window

        Keyword arguments:
        message -- The classification level to display
        fgcolor -- Foreground color of the text to display
        bgcolor -- Background color of the banner the text is against
        face    -- Font face to use for the displayed text
        size    -- Size of font to use for text
        weight  -- Bold or normal
        """

        # Create Main Window
        self.window = gtk.Window()
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.connect("delete_event", self.refresh)
        self.window.connect("destroy", self.refresh)
        self.window.connect("hide", self.restore)
        self.window.connect("window-state-event", self.restore)
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(bgcolor))
        self.window.set_property('skip-taskbar-hint', True)
        self.window.set_property('skip-pager-hint', True)
        self.window.set_property('destroy-with-parent', True)
        self.window.stick()
        self.window.set_decorated(False)
        self.window.set_keep_above(True)
        self.window.set_app_paintable(True)
        self.display = gtk.gdk.display_get_default()
        self.screen = self.display.get_default_screen()
        self.hres = self.screen.get_width()
        self.vres = self.screen.get_height()
        self.window.set_default_size(self.hres, 5)

        # Create Main Vertical Box to Populate
        self.vbox = gtk.VBox()

        self.label = gtk.Label(
            "<span font_family='%s' weight='%s' foreground='%s' size='%s'>%s</span>" %
            (face, weight, fgcolor, size, message))
        self.label.set_use_markup(True)
        self.label.set_justify(gtk.JUSTIFY_CENTER)
        self.vbox.pack_start(self.label, True, True, 0)

        self.window.add(self.vbox)
        self.window.show_all()
        self.width, self.height = self.window.get_size()

    def refresh(self, widget, data=None):
        run = Display_Banner()
        return True

    def restore(self, widget, data=None):
        self.window.present()
        return True

class Display_Banner:
    """Display Classification Banner Message"""

    def __init__(self):

        # First read the global configuration
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

        options, args = parser.parse_args()

        if options.show_top:
            self.top = Classification_Banner(
                options.message,
                options.fgcolor,
                options.bgcolor,
                options.face,
                options.size,
                options.weight)
            self.top.window.move(0, 0)
        if options.show_bottom:
            self.bottom = Classification_Banner(
                options.message,
                options.fgcolor,
                options.bgcolor,
                options.face,
                options.size,
                options.weight)
            self.bottom.window.move(0, self.bottom.vres)

# Main Program Loop
if __name__ == "__main__":
    run = Display_Banner()
    gtk.main()
