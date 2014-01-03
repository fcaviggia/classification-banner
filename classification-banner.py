#!/usr/bin/python
# Classification Banner
# Author: Frank Caviggia (fcaviggia@gmail.com)
# Copyright: Frank Caviggia, 2013
# Version: 1.2
# License: GPLv2

import getopt
import sys
import os
try:
    os.environ['DISPLAY']
    import pygtk
    import gtk
except:
    print "Error: DISPLAY environment varible not set."
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
        options, remainder = getopt.gnu_getopt(sys.argv[1:], 'm:f:b:h', [
                                               'message=', 'fgcolor=', 'bgcolor=', 'font=', 'size=', 'weight=', 'top=', 'bottom=', 'help'])
        for opt, arg in options:
            if opt in ('-h', '--help'):
                print ""
                print "Classification Banner Usage"
                print "===================================="
                print ""
                print "  Options:"
                print "     -m, --message: Classification Message (Defualt: 'UNCLASSIFIED')"
                print "     -f, --fgcolor: Foreground Color (Default: '#000000')"
                print "     -b, --bgcolor: Background Color (Defualt: '#00CC00') "
                print "     --font: Font Face (Defualt: 'liberation-sans')"
                print "     --size: Font Size (Defualt: 'small')"
                print "     --weight: Font Weight (Defualt: 'bold')"
                print "     --top: Display Top Banner (Defualt: 'Y')"
                print "     --bottom: Display Bottom Banner (Defualt: 'Y')"
                print "     -h, --help: This Message"
                print ""
                print "  Examples:"
                print ""
                print "    Default (UNCLASSIFIED)"
                print "    ./classification-banner.py &"
                print ""
                print "    CONFIDENTIAL"
                print "    ./classification-banner.py --message='CONFIDENTIAL' --bgcolor='#33FFFF' &"
                print ""
                print "    SECRET"
                print "    ./classification-banner.py --message='SECRET' --fgcolor='#FFFFFF' --bgcolor='#FF0000' &"
                print ""
                print "    TOP SECRET"
                print "    ./classification-banner.py --message='TOP SECRET' --fgcolor='#FFFFFF' --bgcolor='#FF9900' &"
                print ""
                print "    TOP SECRET//SCI"
                print "    ./classification-banner.py --message='TOP SECRET//SCI' --bgcolor='#FFFF00' &"
                print ""
                sys.exit()
            elif opt in ('-m', '--message'):
                message = arg
            elif opt in ('-f', '--fgcolor'):
                fgcolor = arg
            elif opt in ('-b', '--bgcolor'):
                bgcolor = arg
            elif opt == '--font':
                face = arg
            elif opt == '--size':
                size = arg
            elif opt == '--weight':
                weight = arg
            elif opt == '--top':
                top = arg
            elif opt == '--bottom':
                bottom = arg

        # Use Global Configuration
        try:
            config = {}
            execfile("/etc/classification-banner", config)
            message = config['message']
            bgcolor = config['bgcolor']
            fgcolor = config['fgcolor']
        except:
            pass

        try:
            message
        except:
            message = "UNCLASSIFIED"
        try:
            fgcolor
        except:
            fgcolor = "#000000"
        try:
            bgcolor
        except:
            bgcolor = "#00CC00"
        try:
            face
        except:
            face = "liberation-sans"
        try:
            size
        except:
            size = "small"
        try:
            weight
        except:
            weight = "bold"
        try:
            top
        except:
            top = 'Y'
        try:
            bottom
        except:
            bottom = 'Y'

        if top == 'Y':
            self.top = Classification_Banner(
                message,
                fgcolor,
                bgcolor,
                face,
                size,
                weight)
            self.top.window.move(0, 0)
        if bottom == 'Y':
            self.bottom = Classification_Banner(
                message,
                fgcolor,
                bgcolor,
                face,
                size,
                weight)
            self.bottom.window.move(0, self.bottom.vres)

# Main Program Loop
if __name__ == "__main__":
    run = Display_Banner()
    gtk.main()
