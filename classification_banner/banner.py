#
# Copyright (C) 2018 classification-banner Contributors. See LICENSE for license
#

import sys
import os
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from tempfile import TemporaryFile
import time
from socket import gethostname

# Python version check
# Check the version by e.g., `if python.major is 3:`.  Available keys
# are .major, .minor, .micro, .releaselevel, and .serial.  All are
# integers except for .releaselevel (which are strings e.g., beta).
python = sys.version_info

if python.major is 3:
    from ConfigParser import ConfigParser, MissingSectionHeaderError, DEFAULTSECTs
else:
    from ConfigParser import ConfigParser, MissingSectionHeaderError, DEFAULTSECT

# Global Configuration File
CONF_FILE = "/etc/classification-banner"

# Check if DISPLAY variable is set
try:
    os.environ["DISPLAY"]
    import pygtk
    import gtk
except:
    try:
        import Gtk
    except:
        print("Error: DISPLAY environment variable not set.")
        sys.exit(1)


# Returns Username
def get_user():
    try:
        user = os.getlogin()
    except:
        user = ''
        pass
    return user


# Returns Hostname
def get_host():
    host = gethostname()
    host = host.split('.')[0]
    return host


# Classification Banner Class
class ClassificationBanner:
    """Class to create and refresh the actual banner."""

    def __init__(self, message="UNCLASSIFIED", fgcolor="#000000",
                 bgcolor="#00CC00", face="liberation-sans", size="small",
                 weight="bold", x=0, y=0, esc=True, opacity=0.75,
                 sys_info=False):

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
        self.hres = x
        self.vres = y

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

        try:
            self.window.set_opacity(opacity)
        except:
            pass

        # Set the default window size
        self.window.set_default_size(int(self.hres), 5)

        # Create Main Horizontal Box to Populate
        self.hbox = gtk.HBox()

        # Create the Center Vertical Box
        self.vbox_center = gtk.VBox()
        self.center_label = gtk.Label(
            "<span font_family='%s' weight='%s' foreground='%s' size='%s'>%s</span>" %
            (face, weight, fgcolor, size, message))
        self.center_label.set_use_markup(True)
        self.center_label.set_justify(gtk.JUSTIFY_CENTER)
        self.vbox_center.pack_start(self.center_label, True, True, 0)

        # Create the Right-Justified Vertical Box to Populate for hostname
        self.vbox_right = gtk.VBox()
        self.host_label = gtk.Label(
            "<span font_family='%s' weight='%s' foreground='%s' size='%s'>%s</span>" %
            (face, weight, fgcolor, size, get_host()))
        self.host_label.set_use_markup(True)
        self.host_label.set_justify(gtk.JUSTIFY_RIGHT)
        self.host_label.set_width_chars(20)

        # Create the Left-Justified Vertical Box to Populate for user
        self.vbox_left = gtk.VBox()
        self.user_label = gtk.Label(
            "<span font_family='%s' weight='%s' foreground='%s' size='%s'>%s</span>" %
            (face, weight, fgcolor, size, get_user()))
        self.user_label.set_use_markup(True)
        self.user_label.set_justify(gtk.JUSTIFY_LEFT)
        self.user_label.set_width_chars(20)

        # Create the Right-Justified Vertical Box to Populate for ESC message
        self.vbox_esc_right = gtk.VBox()
        self.esc_label = gtk.Label(
            "<span font_family='liberation-sans' weight='normal' foreground='%s' size='xx-small'>  (ESC to hide temporarily)  </span>" %
            (fgcolor))
        self.esc_label.set_use_markup(True)
        self.esc_label.set_justify(gtk.JUSTIFY_RIGHT)
        self.esc_label.set_width_chars(20)

        # Empty Label for formatting purposes
        self.vbox_empty = gtk.VBox()
        self.empty_label = gtk.Label(
            "<span font_family='liberation-sans' weight='normal'>                 </span>")
        self.empty_label.set_use_markup(True)
        self.empty_label.set_width_chars(20)

        if not esc:
            if not sys_info:
                self.hbox.pack_start(self.vbox_center, True, True, 0)
            else:
                self.vbox_right.pack_start(self.host_label, True, True, 0)
                self.vbox_left.pack_start(self.user_label, True, True, 0)
                self.hbox.pack_start(self.vbox_right, False, True, 20)
                self.hbox.pack_start(self.vbox_center, True, True, 0)
                self.hbox.pack_start(self.vbox_left, False, True, 20)

        else:
            if esc and not sys_info:
                self.empty_label.set_justify(gtk.JUSTIFY_LEFT)
                self.vbox_empty.pack_start(self.empty_label, True, True, 0)
                self.vbox_esc_right.pack_start(self.esc_label, True, True, 0)
                self.hbox.pack_start(self.vbox_esc_right, False, True, 0)
                self.hbox.pack_start(self.vbox_center, True, True, 0)
                self.hbox.pack_start(self.vbox_empty, False, True, 0)

        if sys_info:
                self.vbox_right.pack_start(self.host_label, True, True, 0)
                self.vbox_left.pack_start(self.user_label, True, True, 0)
                self.hbox.pack_start(self.vbox_right, False, True, 20)
                self.hbox.pack_start(self.vbox_center, True, True, 0)
                self.hbox.pack_start(self.vbox_left, False, True, 20)

        self.window.add(self.hbox)
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
            if not gtk.events_pending():
                self.window.iconify()
                self.window.hide()
                time.sleep(15)
                self.window.show()
                self.window.deiconify()
                self.window.present()

        return True


class DislayBanner:

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
        self.config = self.configure()
        self.execute(self.config)

    # Read configuration(s)
    def configure(self):
        defaults = {}
        defaults["message"] = "UNCLASSIFIED"
        defaults["fgcolor"] = "#FFFFFF"
        defaults["bgcolor"] = "#007A33"
        defaults["face"] = "liberation-sans"
        defaults["size"] = "small"
        defaults["weight"] = "bold"
        defaults["show_top"] = True
        defaults["show_bottom"] = True
        defaults["hres"] = 0
        defaults["vres"] = 0
        defaults["sys_info"] = False
        defaults["opacity"] = 0.75
        defaults["esc"] = True
        defaults["spanning"] = False

        # Check if a configuration file was passed in from the command line
        default_heading = DEFAULTSECT
        conf_parser = ArgumentParser(
            formatter_class=RawDescriptionHelpFormatter,
            add_help=False)
        conf_parser.add_argument("-c", "--config",
                                help="Specify the configuration file",
                                metavar="FILE")
        conf_parser.add_argument("--heading",
                                help="Specify the config. section to use.",
                                default=default_heading)
        options, args = conf_parser.parse_known_args()

        config_file = None
        if options.config:
            config_file = os.path.abspath(options.config)
            if not os.path.isfile(config_file):
                print("ERROR: Specified configuration file does not exist.")
                sys.exit(1)
        else:
            config_file = os.path.abspath(CONF_FILE)
            if not os.path.isfile(config_file):
                config_file = None

        # In order to maintain backwards compatibility with the way the
        # previous configuration file format, a dummy section may need
        # to be added to the configuration file.  If this is the case,
        # a temporary file is used in order to avoid overwriting the
        # user's configuration.
        config = ConfigParser()

        if config_file is not None:
            fp = open(config_file, "r")
            while True:
                try:
                    if python.major is 3:
                        config.read_file(fp, source=config_file)
                    else:
                        config.readfp(fp, config_file)
                    break
                except MissingSectionHeaderError:
                    # Recreate the file, adding a default section.
                    fp.close()
                    fp = TemporaryFile()
                    with open(config_file) as original:
                        fp.write("[%s]\n" % default_heading + original.read())
                    fp.seek(0)
            fp.close()  # If this was a temporary file it will now be deleted.

        # ConfigParser treats everything as strings and any quotation
        # marks in a setting are explicitly added to the string.
        # One way to fix this is to add everything to the defaults and
        # then strip the quotation marks off of everything.
        defaults.update(dict(config.items(options.heading)))
        for key, val in defaults.items():
            if config.has_option(options.heading, key):
                defaults[key] = val.strip("\"'")
        # TODO: This coercion section is hacky and should be fixed.
        for key in ["show_top", "show_bottom", "sys_info", "esc", "spanning"]:
            if config.has_option(options.heading, key):
                defaults[key] = config.getboolean(options.heading, key)
        for key in ["hres", "vres"]:
            if config.has_option(options.heading, key):
                defaults[key] = config.getint(options.heading, key)
        for key in ["opacity"]:
            if config.has_option(options.heading, key):
                defaults[key] = config.getfloat(options.heading, key)

        # Use the global config to set defaults for command line options
        parser = ArgumentParser(parents=[conf_parser])
        parser.add_argument("-m", "--message", default=defaults["message"],
                          help="Set the Classification message")
        parser.add_argument("-f", "--fgcolor", default=defaults["fgcolor"],
                          help="Set the Foreground (text) color")
        parser.add_argument("-b", "--bgcolor", default=defaults["bgcolor"],
                          help="Set the Background color")
        parser.add_argument("-x", "--hres", default=defaults["hres"], type=int,
                          help="Set the Horizontal Screen Resolution")
        parser.add_argument("-y", "--vres", default=defaults["vres"], type=int,
                          help="Set the Vertical Screen Resolution")
        parser.add_argument("-o", "--opacity", default=defaults["opacity"],
                          type=float, dest="opacity",
                          help="Set the window opacity for composted window managers")
        parser.add_argument("--face", default=defaults["face"], help="Font face")
        parser.add_argument("--size", default=defaults["size"], help="Font size")
        parser.add_argument("--weight", default=defaults["weight"],
                          help="Set the Font weight")
        parser.add_argument("--disable-esc-msg", default=defaults["esc"],
                          dest="esc", action="store_false",
                          help="Disable the 'ESC to hide' message")
        parser.add_argument("--hide-top", default=defaults["show_top"],
                          dest="show_top", action="store_false",
                          help="Disable the top banner")
        parser.add_argument("--hide-bottom", default=defaults["show_bottom"],
                          dest="show_bottom", action="store_false",
                          help="Disable the bottom banner")
        parser.add_argument("--system-info", default=defaults["sys_info"],
                          dest="sys_info", action="store_true",
                          help="Show user and hostname in the top banner")
        parser.add_argument("--enable-spanning", default=defaults["spanning"],
                          dest="spanning", action="store_true",
                          help="Enable banner(s) to span across screens as a single banner")

        options = parser.parse_args()
        return options

    # Launch the Classification Banner Window(s)
    def execute(self, options):
        self.num_monitor = 0

        if options.hres == 0 or options.vres == 0:
            # Try Xrandr to determine primary monitor resolution
            try:
                self.screen = os.popen("xrandr | grep ' connected ' | awk '{ print $3 }'").readlines()[0]
                self.x = self.screen.split('x')[0]
                self.y = self.screen.split('x')[1].split('+')[0]

            except:
                try:
                    self.screen = os.popen("xrandr | grep ' current ' | awk '{ print $8$9$10+0 }'").readlines()[0]
                    self.x = self.screen.split('x')[0]
                    self.y = self.screen.split('x')[1].split('+')[0]

                except:
                    self.screen = os.popen("xrandr | grep '^\*0' | awk '{ print $2$3$4 }'").readlines()[0]
                    self.x = self.screen.split('x')[0]
                    self.y = self.screen.split('x')[1].split('+')[0]

                else:
                    # Fail back to GTK method
                    self.display = gtk.gdk.display_get_default()
                    self.screen = self.display.get_default_screen()
                    self.x = self.screen.get_width()
                    self.y = self.screen.get_height()
        else:
            # Resoultion Set Staticly
            self.x = options.hres
            self.y = options.vres

        if not options.spanning and self.num_monitor > 1:
            for monitor in range(self.num_monitor):
                mon_geo = self.screen.get_monitor_geometry(monitor)
                self.x_location, self.y_location, self.x, self.y = mon_geo
                self.banners(options)
        else:
            self.x_location = 0
            self.y_location = 0
            self.banners(options)

    def banners(self, options):
            if options.show_top:
                top = ClassificationBanner(
                    options.message,
                    options.fgcolor,
                    options.bgcolor,
                    options.face,
                    options.size,
                    options.weight,
                    self.x,
                    self.y,
                    options.esc,
                    options.opacity,
                    options.sys_info)
                top.window.move(self.x_location, self.y_location)

            if options.show_bottom:
                bottom = ClassificationBanner(
                    options.message,
                    options.fgcolor,
                    options.bgcolor,
                    options.face,
                    options.size,
                    options.weight,
                    self.x,
                    self.y,
                    options.esc,
                    options.opacity)
                bottom.window.move(self.x_location, int(bottom.vres))

    # Relaunch the Classification Banner on Screen Resize
    def resize(self, widget, data=None):
        self.config, self.args = self.configure()
        self.execute(self.config)
        return True


def main():
    run = DislayBanner()
    gtk.main()
