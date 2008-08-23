from xml.dom.minicompat import *
from xml.dom.minidom import Node, parseString, Attr

class NoSuchNode(Exception): 
    "No node is accessible via the dotted name given."

class NoSuchAttribute(Exception): 
    "No attribute is accessible via the dotted name given."

class AttributeParsingError(Exception): 
    "An invalid attribute type was specified."


def _getText(rootnode):
    """
    Get the text value from a C{Node}.

    This is taken nearly verbatim from an example in the Python documentation.
    U{http://docs.python.org/lib/dom-example.html}
    """
    rc = ""
    for node in rootnode.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc.strip()


class DotNodeParent(type):
    """
    Metaclass that makes sure everything in the sequence passed to the 
    constructor is a L{DotNode}.
    """
    def __call__(self, sequence):
        """
        @param sequence: The sequence that should be contained by this
                         instance.
        @type sequence: tuple, list
        @rtype: instance
        """
        mutate = lambda item:item.__class__==DotNode and item or DotNode(item)
        return type.__call__(self, [mutate(item) for item in sequence])


class DotNodeList(NodeList):
    """
    A L{NodeList} that asks its first child for attributes.

    One can also access this like a dictionary to get an L{Attr} on the first child.
    """
    __metaclass__ = DotNodeParent
    
    def __getitem__(self, index):
        """
        If C{index} is an integer, return the C{index}th item in the list.
        Otherwise, attempt to retrieve the attribute named C{index} on the
        first child.
        """
        try:
            return super(DotNodeList, self).__getitem__(int(index))
        except ValueError:
            return self.getAttribute(index)
    
    def __getattribute__(self, attr):
        """
        All attribute access should be passed off to the first item in the
        sequence.
        """
        return getattr(self[0], attr)


class DotNode(object):
    """
    An object whose getattr gets child nodes.
    """     
    def __init__(self, node):
        """
        @param node: The L{Node} to wrap.
        @type node: L{Node}
        """
        self._node = node

    def __getattr__(self, attr):
        """
        Split the attribute and pass it to C{delegate} to be sent on to the
        resolving method.
        """
        def delegate(name, idx=""):
            """
            Treat C{name} as a tagName, an attribute or a list index,
            depending on the value of C{idx}.

            @param name: The name to pass on to the accessor for resolution
            @type name: str
            @param idx: The identifier (empty for a node, "a" for an attribute,
                        an integer for an index)
            @type idx: str
            @return: void
            """
            if not idx:
                # Empty idx, so it's a node
                return self.getChildren(name)
            elif idx=='a':
                # idx is 'a', so it's an attribute
                return self.getAttribute(name)
            else:
                try:
                    # Try casting idx as an integer to see if it's a list index
                    return self.getItem(name, int(idx))
                except ValueError:
                    raise AttributeParsingError(
                        "The locator you've specified is invalid.")
        return delegate(*attr.split('__'))
    
    def getName(self):
        """
        @return: The tag name of the root node.
        @rtype: str
        """
        return self._node.tagName
       
    def getChildren(self, name, *args):
        """
        Attempt to resolve C{name} as the tag name of a L{Node}. If no node
        with that name exists, attempt to resolve it as an L{Attr}.

        @param name: The name to attempt to resolve.
        @type name: str
        @return: The matching nodes or attribute.
        @rtype: L{DotNodeAttribute} or L{DotNodeList}
        """
        children = self._node.getElementsByTagName(name)
        if not children:
            try:
                return self.getAttribute(name, *args)
            except NoSuchAttribute:
                raise NoSuchNode("No %s node found as a child of %s" % (
                    name, self.getName()))
        return DotNodeList(children)
    
    def getItem(self, name, idx):
        """
        Attempt to retrieve the C{idx}th child node that has tagName C{name}.

        @param name: The tag name to resolve into child nodes.
        @type name: str
        @param idx: The list index
        @type idx: int
        @return: A sequence containing the matching node.
        @rtype: L{DotNodeList}
        """
        try:
            return DotNodeList((self.getChildren(name)[idx],))
        except IndexError:
            raise NoSuchNode("There aren't that many %s nodes under %s." %(
                                name, self.getName()))
    
    def getAttribute(self, name, *args):
        """
        Get the C{name} attribute on C{self._node}.

        @param name: The attribute name
        @type name: str
        @return: The matching attribute
        @rtype: L{DotNodeAttribute}
        """
        attrval = self._node.getAttribute(name)
        if not attrval:
            raise NoSuchAttribute('No %s attribute exists on %s node.' % (
                                    name, self.getName()))
        return DotNodeAttribute(attrval)
    
    def getValue(self):
        """
        Get the text value of C{self._node}.

        @return: The text value of C{self._node}
        @rtype: str
        """
        return unicode(_getText(self._node))

    # Property accessor
    _ = property(getValue)


class DotXMLDoc(object):
    """
    Accepts the source of an XML document, parses it, and provides dotted name
    access to the root node.
    """
    def __init__(self, source):
        """
        @param source: A string containing an XML document.
        @type source: str
        """
        self._doc = parseString(source)
        self._root = DotNode(self._doc.documentElement)

    def __getattr__(self, attr):
        """
        Pass off attribute access to the root node.
        """
        return getattr(self._root, attr)
    
    def __del__(self):
        """
        Remove the XML document from memory.
        """
        self._doc.unlink()


class DotNodeAttribute(str):
    """
    A string with a C{getValue} method.

    This allows attribute values to be accessed just like L{DotNode}s.
    """
    def getValue(self): return self
    _ = property(getValue)


