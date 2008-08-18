from xml.dom.minicompat import *
from xml.dom.minidom import Node, parseString

class NoSuchNode(Exception): 
    "No node is accessible via the dotted name given."

class NoSuchAttribute(Exception): 
    "No attribute is accessible via the dotted name given."

class AttributeParsingError(Exception): 
    "An invalid attribute type was specified."


def _getText(rootnode):
    """
    Get the text value from a Node.

    This is taken nearly verbatim from an example in the Python documentation.
    L{http://docs.python.org/lib/dom-example.html}
    """
    rc = ""
    for node in rootnode.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data
    return rc.strip()


class DotNodeParent(type):
    """
    Metaclass that makes sure everything in the sequence passed to the 
    constructor is a DotNode.
    """
    def __call__(self, sequence):
        mutate = lambda item:item.__class__==DotNode and item or DotNode(item)
        return type.__call__(self, [mutate(item) for item in sequence])


class DotNodeList(NodeList):
    """
    A NodeList that asks its first child for attributes.
    """
    __metaclass__ = DotNodeParent
    
    def __getitem__(self, index):
        try:
            return super(DotNodeList, self).__getitem__(int(index))
        except ValueError:
            return self.getAttribute(index)
    
    def __getattribute__(self, attr):
        return getattr(self[0], attr)


class DotNode(object):
    """
    An object whose getattr gets child nodes.
    """     
    def __init__(self, node):
        self._node = node

    def __getattr__(self, attr):
        """
        Get the next object specified.
        """
        def delegate(name, idx=None):
            if idx is None:
                return self.getChildren(name)
            elif idx=='a':
                return self.getAttribute(name)
            else:
                try:
                    return self.getItem(name, int(idx))
                except ValueError:
                    raise AttributeParsingError(
                        "The locator you've specified is invalid.")
        return delegate(*attr.split('__'))
    
    def getName(self):
        return self._node.tagName
       
    def getChildren(self, name, *args):
        children = self._node.getElementsByTagName(name)
        if not children:
            try:
                return self.getAttribute(name, *args)
            except NoSuchAttribute:
                raise NoSuchNode("No %s node found as a child of %s" % (
                    name, self.getName()))
        return DotNodeList(children)
    
    def getItem(self, name, idx):
        try:
            return DotNodeList((self.getChildren(name)[idx],))
        except IndexError:
            raise NoSuchNode("There aren't that many %s nodes under %s." %(
                                name, self.getName()))
    
    def getAttribute(self, name, *args):
        attrval = self._node.getAttribute(name)
        if not attrval:
            raise NoSuchAttribute('No %s attribute exists on %s node.' % (
                                    name, self.getName()))
        return DotNodeAttribute(attrval)
    
    def getValue(self):
        return unicode(_getText(self._node))
    _ = property(getValue)

        
class DotXMLDoc(object):
    def __init__(self, source):
        self._doc = parseString(source)
        self._root = DotNode(self._doc.documentElement)

    def __getattr__(self, attr):
        return getattr(self._root, attr)
    
    def __del__(self):
        self._doc.unlink()


class DotNodeAttribute(str):
    """
    A string with a getValue method.

    This allows attribute values to be accessed just like DotNodes.
    """
    def getValue(self): return self
    _ = property(getValue)


