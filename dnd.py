#!/usr/bin/env python
#
# Copyright 2013 Ramkumar Shankar
#
# Author: Ramkumar Shankar <ram.i.am@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
 
import sys
import os
import gobject
import gtk
import appindicator

# Main class - Do not disturb indicator

class Dnd:
  
  def __init__(self):
    self.ind = appindicator.Indicator ("dnd-indicator",
                                       self.set_idle_icon(),
                                       appindicator.CATEGORY_APPLICATION_STATUS)
    self.ind.set_status (appindicator.STATUS_ACTIVE)
    self.ind.set_attention_icon (self.set_attention_icon())
    
    self.menu_setup()
    self.ind.set_menu(self.menu)

  def set_idle_icon(self):
    return os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "icons" + os.path.sep + "do-not-disturb-sign.png"
    
  def set_attention_icon(self):
    return os.path.dirname(os.path.realpath(__file__)) + os.path.sep + "icons" + os.path.sep + "do-not-disturb-sign-busy.png"
    
  def menu_setup(self):
    self.menu = gtk.Menu()
    self.dnd_item = gtk.CheckMenuItem("Do not disturb")
    self.dnd_item.connect("toggled", self.set_dnd)
    self.dnd_item.show()
    self.quit_item = gtk.MenuItem("Quit")
    self.quit_item.connect("activate", self.quit)
    self.quit_item.show()
    self.menu.append(self.dnd_item)
    self.menu.append(self.quit_item)
      
  def main(self):
    gtk.main()

  def set_dnd(self, widget):
    if widget.active:
      bashCommand = "sudo mv /usr/share/dbus-1/services/org.freedesktop.Notifications.service /usr/share/dbus-1/services/org.freedesktop.Notifications.service.disabled"
      os.system(bashCommand)
      self.ind.set_status (appindicator.STATUS_ATTENTION)
    else:
      bashCommand = "sudo mv /usr/share/dbus-1/services/org.freedesktop.Notifications.service.disabled /usr/share/dbus-1/services/org.freedesktop.Notifications.service"
      os.system(bashCommand)
      self.ind.set_status (appindicator.STATUS_ACTIVE)
    bashCommand = "killall notify-osd"
    os.system(bashCommand)

  def quit(self, widget):
    # Enable notifications if they are not, before exit
    if self.dnd_item.get_active() == True:
      bashCommand = "sudo mv /usr/share/dbus-1/services/org.freedesktop.Notifications.service.disabled /usr/share/dbus-1/services/org.freedesktop.Notifications.service"
      os.system(bashCommand)
      bashCommand = "killall notify-osd"
      os.system(bashCommand)
    sys.exit(0)

if __name__ == "__main__":
  indicator = Dnd()
  indicator.main()
