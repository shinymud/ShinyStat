import re
import socket

from genshi.builder import tag

from trac.core import *
from trac.web import IRequestHandler
from trac.web.chrome import INavigationContributor, ITemplateProvider, add_stylesheet

GAME_ROOT = '/home/shiny/shinymud/src/shinymud'
GAME_HOST = 'shiny.game-host.org'
PORT = 4112

class ShinyStatPlugin(Component):
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
        stat = self.contact_server()
        if stat is None:
            data['game_status'] = 'offline'
        else:
            data['game_status'] = 'online'
            if not stat:
                data['num_players'] = 'no'
            else:
                data['num_players'] = len(stat)
            data['names'] = stat
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
            result = s.recv(1024)
        except socket.timeout:
            result = None
        else:
            result = [name for name in result.split() if name]
        return result
    
