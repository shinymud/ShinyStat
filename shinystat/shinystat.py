import re
import socket
from time import strftime, localtime

from genshi.builder import tag

from trac.core import *
from trac.web import IRequestHandler
from trac.web.chrome import INavigationContributor, ITemplateProvider, add_stylesheet

GAME_HOST = 'shiny.game-host.org' # Change this to your game-host!
PORT = 4112 # Change this to your port number!

class ShinyStatPlugin(Component):
    """A plug-in for Trac that will connect to ShinyMUD's StatSender and display
    the status of the game server.
    """
    implements(INavigationContributor, ITemplateProvider, IRequestHandler)
    
    # INavigationContributor methods
    def get_active_navigation_item(self, req):
        return 'shinystat'
    
    def get_navigation_items(self, req):
        yield ('mainnav', 'shinystat',
               tag.a('ShinyMUD Stats', href=req.href.shinystat()))
    
    # IRequestHandler methods
    def match_request(self, req):
        return re.match(r'/shinystat(?:_trac)?(?:/.*)?$', req.path_info)
    
    def process_request(self, req):
        data = {}
        add_stylesheet(req, 'hw/css/shinystat.css')
        result = self.contact_server()
        if result is None:
            data['game_status'] = 'offline'
        else:
            data['game_status'] = 'online'
            players, uptime = result
            if not players:
                data['num_players'] = 'no'
            else:
                data['num_players'] = len(players)
            data['names'] = players
            data['start_date']  = strftime("%a, %d %b %Y %H:%M:%S", 
                                           localtime(float(uptime)))
        # This tuple is for Genshi (template_name, data, content_type)
        # Without data the trac layout will not appear.
        return 'shinystat.html', data, None
    
    # ITemplateProvider methods
    # Used to add the plugin's templates and htdocs 
    def get_templates_dirs(self):
        from pkg_resources import resource_filename
        return [resource_filename(__name__, 'templates')]
    
    def get_htdocs_dirs(self):
        """Return a list of directories with static resources (such as style
        sheets, images, etc.)
        Each item in the list must be a `(prefix, abspath)` tuple. The
        `prefix` part defines the path in the URL that requests to these
        resources are prefixed with.
        The `abspath` is the absolute path to the directory containing the
        resources on the local file system.
        """
        from pkg_resources import resource_filename
        return [('hw', resource_filename(__name__, 'htdocs'))]
    
# ***** ShinyStat specific functions
    def contact_server(self):
        """Contact the ShinyMUD game server."""
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        
        # See if we can connect at all
        try:
            s.connect((GAME_HOST, PORT))
        except:
            # If we can't, then we know the game is offline
            return None
            
        try:
            data = s.recv(1024)
        except socket.timeout:
            # In the future we should probably return an error for when the
            # game times-out.
            result = None
        else:
            data = data.split(':')
            names = [name.capitalize() for name in data[0].split(',') if name]
        return names, data[1]
    
