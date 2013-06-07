from flask import g, url_for, request
from jinja2 import nodes
from jinja2.ext import Extension
from jinja2.utils import Markup

def setup_jinja_helpers(app):
    # expose constants
    app.jinja_env.globals['config'] = app.config
    
    class OnDomReadyExtension(Extension):
        """provides a ondomready/endondomready block to contain javascript code from anywhere
        which gets printed in 1 go by the printondomready block at the bottom of the page
        """
        
        # a set of names that trigger the extension.
        tags = set(['ondomready', 'printondomready'])
    
        def __init__(self, environment):
            super(OnDomReadyExtension, self).__init__(environment)
    
        def parse(self, parser):
            # grab the name token
            token = parser.stream.next()
            
            # check the value of the name token
            if token.value == 'ondomready':
                
                # check if the name token is followed by a string
                unique = parser.stream.next_if('string')
                # create a constant from the string or None
                args = [nodes.Const(unique.value if unique else None)]
                
                # parse the body up to the end tag
                body = parser.parse_statements(['name:endondomready'], drop_needle=True)
    
                # return a new node (which will be empty)
                return nodes.CallBlock(self.call_method('_store_ondomready', args), [], [], body).set_lineno(token.lineno)
            elif token.value == 'printondomready':
                # return a node with the stashed js code
                return nodes.CallBlock(self.call_method('_print_ondomready'), [], [], []).set_lineno(token.lineno)
    
        def _store_ondomready(self, unique, caller):
            # check if we're to late
            if hasattr(g, 'domreadyprinted') and g.domreadyprinted:
                raise Exception("Atempt to add to ondomready after it has already been output.")
            
            # init the requestglobal var
            if not hasattr(g, 'ondomready'):
                g.ondomready_unique = []
                g.ondomready = []
                
               
            # if we have a unique identifier then make sure we don't add it twice 
            if unique:
                if unique in g.ondomready_unique:
                    return ""
                else:
                    g.ondomready_unique.append(unique)
            
            # add to the requestglobal var
            g.ondomready.append(caller())
    
            # return emptiness
            return ""
    
        def _print_ondomready(self, caller):
            # mark the requestglobal that we can't add more js to it
            g.domreadyprinted = True
            
            # return the stashed js code or emptiness
            return "\n".join(g.ondomready) if hasattr(g, 'ondomready') else ""
        
    # register the OnDomReady extension
    app.jinja_env.add_extension(extension=OnDomReadyExtension)


