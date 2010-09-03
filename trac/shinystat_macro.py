"""ShinyStatMacro
author: Jess "Surrey" Coulter
A Trac Macro written for the ShinyMUD project.
"""
from trac.wiki.macros import WikiMacroBase
from trac.util.html import Markup

import socket
from time import strftime, localtime

GAME_HOST = '' # Change this to your game-host (or leave it blank for localhost)
IMAGE_SRC = 'http://www.incendiarysoftware.com/shinystat/' # The source url for the online/offline images
PORT = 4112 # This is the default ShinyStat port number

class ShinyStatMacro(WikiMacroBase):
    """The ShinyStat macro.
     
    The ShinyStat macro embeds the ShinyStat plugin in a wiki page.
    For now, the plugin will be floated to the right of the page (sorry).
    """
    
    revision = "$Rev$"
    url = "$URL$"
    
    def expand_macro(self, formatter, name, args):
        """Return some output that will be displayed in the Wiki content.
        
        `name` is the actual name of the macro,
        `args` is the text enclosed in parenthesis at the call of the macro.
          Note that if there are ''no'' parenthesis (like in, e.g.
          [[HelloWorld]]), then `args` is `None`.
        """
        result = self.contact_server()
        if result is None:
            content = """
<div style="font-size: medium;">Our ShinyMUD server is: <b>Offline</b></div>
<div style="margin: 2px 0;">Down for maintenance. It will be back up soon!</div>
"""
            status = "offline"
        else:
            players, uptime = result
            status = "online"
            time_stamp = strftime("%B %d, %Y", localtime(float(uptime)))
            if len(players) == 0:
                playing = "There are <b>no players</b> online right now."
            elif len(players) == 1:
                playing = "There is <b>1 player</b> online right now:"
            else:
                playing = "There are <b>%s players</b> online right now:" % str(len(players))
            player_str = ''
            for player in players:
                player_str += '<li>%s</li>' % player
            content = """
<div style"padding: 0 0 0 10px;">
<div style="font-size: 15px;">Our ShinyMUD server is: <b>Online</b></div>
<div style="margin: 2px 0; font-size: 13px;">Last restarted: <b>%s</b></div>
<div style="font-size: 13px;">%s</div>
<div><ul style="margin: 5px 0px 0px 60px; padding: 0px;">%s</ul></div>
</div>
""" % (time_stamp, playing, player_str)
        
        s = """<div style="float: right; width: 350px; border: 1px solid #D7D7D7; padding: 20px; margin: 10px; background-color: #F7F7F7;">
<img src="%s%s.png"
style="height: 32px; width: 32px; float: left; margin: 0 10px 20px 0;"/>
<div style="margin: 10px 0 0 0;">%s</div>
</div>""" % (IMAGE_SRC, status, content)
        return Markup(s)
    
    # Note that there's no need to HTML escape the returned data,
    # as the template engine (Genshi) will do it for us.
    
    def contact_server(self):
        """Contact the ShinyMUD game server."""
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        
        # See if we can connect at all
        try:
            s.connect((GAME_HOST, PORT))
        except:
            # If we can't, then we know the game is offline or the host/port
            # are wrong
            return None
        try:
            # Receive some data...
            data = s.recv(1024)
        except socket.timeout:
            # In the future we should probably return an error for when the
            # game times-out -- for now we'll just say the game is offline
            return None
        else:
            data = data.split(':')
            names = [name.capitalize() for name in data[1].split(',') if name]
        return names, data[0] # data[0] is the uptime
    

