from node import DotXMLDoc, AttributeParsingError

class SimpleXmlApi(object):
    """
    The main API class, comprising a map of attributes to dotted path names.

    Accessing an attribute that has been mapped to a dotted name will return
    the text value of that node/attribute. If an attribute is passed that 
    isn't in the map, it's passed off to the L{DotXMLDoc} instance, so that 
    the document can be walked manually.

    May be subclassed, overriding C{_map}, to provide custom APIs for known XML
    structures.
    """
    _map = {}
    _doc = None

    def __init__(self, source="", map=None):
        """
        @param source: A string containing an XML document
        @type source: str
        @param map:
        @type map: dict
        @return: void
        """
        if map is not None:
            self.load_map(map)
        self.load_source(source)
    
    def add_mapping(self, name, path):
        """
        Add a new attribute - dotted name mapping to the instance's map
        registry.

        @param name: The name of the attribute.
        @type name: str
        @param path: A dotted name that can be traversed.
        @type path: str
        @return: void
        """
        self._map[name] = path

    def load_source(self, source):
        """
        Parse an XML document and set it as this API's target.

        @param source: A string containing an XML document.
        @type source: str
        @return: void
        """
        self._doc = DotXMLDoc(source)

    def load_map(self, map):
        """
        Update the attribute registry with one or more mappings. Will not
        remove attributes that currently exist.

        @param map: A dictionary of the form C{\{'attribute':'dotted.name'\}}
        @type map: dict
        @return: void
        """
        self._map.update(map)

    def del_mapping(self, name):
        """
        Remove an attribute mapping from the registry.

        @param name: The name of the attribute to remove from the registry.
        @type name: str
        @return: void
        """
        try: del self._map[name]
        except KeyError: pass

    def __getattr__(self, attr):
        try:
            return self._traverse(self._map[attr])
        except KeyError:
            return getattr(self._doc, attr)
        
    def _traverse(self, path):
        """
        Traverse a dotted path against the XML document in memory and return
        its text value.

        @param path: A dotted path that will resolve to a node or attribute.
        @type path: str
        @return: The text value of the node.
        @rtype: str
        """
        try:
            return eval("self._doc.%s" % path).getValue()
        except SyntaxError:
            raise AttributeParsingError


def factory(source, map=None, cls=None):
    """
    Create a new L{SimpleXmlApi} instance using the given source and optional
    attribute map.

    To create an instance of a subclass, pass in the C{cls} attribute.
    """
    if cls is None:
        cls = SimpleXmlApi
    return cls(source, map)
