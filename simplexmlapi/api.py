from node import DotXMLDoc, AttributeParsingError

class SimpleXmlApi(object):

    _map = {}
    _doc = None

    def __init__(self, source="", map=None):
        if map is not None:
            self.load_map(map)
        self.load_source(source)
    
    def add_mapping(self, name, path):
        self._map[name] = path

    def load_source(self, source):
        self._doc = DotXMLDoc(source)

    def load_map(self, map):
        self._map.update(map)

    def __getattr__(self, attr):
        try:
            return self._traverse(self._map[attr])
        except KeyError:
            return getattr(self._doc, attr)
        
    def _traverse(self, path):
        try:
            return eval("self._doc.%s" % path).getValue()
        except SyntaxError:
            raise AttributeParsingError

def factory(source, map=None, cls=None):
    if cls is None:
        cls = SimpleXmlApi
    return cls(source, map)
