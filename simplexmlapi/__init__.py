r"""
A simple, fast way to create dotted-name APIs for XML data

simplexmlapi exposes an API similar to those of the marshal and pickle modules.

An XML document may be loaded into a L{SimpleXmlApi} object and traversed using
Python-like dotted names. One may also map attributes of the L{SimpleXmlApi}
object to given dotted names.

Each segment of the dotted name will be resolved to the first child element
with that tag name. If no such element exists, it will be resolved to an
attribute on the current element. If no such attribute exists, an exception
will be raised.

Traversing the tree manually -- that is, without using an attribute map -- will
return a L{DotNode} or L{DotNodeAttribute} instance. To get the text value of a node
or attribute, access the '_' property or call the C{getValue()} method. When
accessing an attribute mapping, the text value is returned automatically; no
call to C{getValue()} is necessary.

If multiple matching child elements exist, C{__0} may be appended to the name,
where C{'0'} is the index of the desired element.

In case of tag name/attribute conflicts, attribute resolution may be specified
explicitly by appending C{__a} to the name.

Parsing an XML document and traversing elements with dotted names:

    >>> import simplexmlapi
    >>> s = '''
    ...     <xml> <obj>
    ...         <prop name="value">A Value</prop>
    ...         <prop name="thing">A Thing</prop>
    ...     </obj> </xml>
    ...     '''
    >>> api = simplexmlapi.loads(s)
    >>> api.obj.prop._
    u'A Value'
    >>> api.obj.prop.name._
    'value'
    >>> api.obj.prop__1.name._
    'thing'
    >>> api.obj.prop__1.name__a._
    'thing'
    >>> from StringIO import StringIO
    >>> io = StringIO(s)
    >>> api = simplexmlapi.load(io)
    >>> api.obj.prop._
    u'A Value'

Mapping dotted names to attributes:

    >>> import simplexmlapi
    >>> s = '''
    ...     <xml> <obj>
    ...         <prop name="value">A Value</prop>
    ...         <prop name="thing">A Thing</prop>
    ...     </obj> </xml>
    ...     '''
    >>> api = simplexmlapi.loads(s)
    >>> api.add_mapping('value', 'obj.prop__0')
    >>> api.add_mapping('thing', 'obj.prop__1')
    >>> api.value
    u'A Value'
    >>> api.thing
    u'A Thing'
    >>> attr_map = dict(value="obj.prop__0", thing="obj.prop__1")
    >>> api2 = simplexmlapi.loads(s, map=attr_map)
    >>> api2.value
    u'A Value'
    >>> api2.thing
    u'A Thing'

Extending L{SimpleXmlApi}:
    
    >>> import simplexmlapi
    >>> class SampleApi(simplexmlapi.SimpleXmlApi):
    ...     _map = {
    ...         'value' : 'obj.prop__0',
    ...         'thing' : 'obj.prop__1' }
    ...
    >>> s = '''
    ...     <xml>
    ...         <obj>
    ...             <prop name="value">A Value</prop>
    ...             <prop name="thing">A Thing</prop>
    ...         </obj>
    ...     </xml>
    ...     '''
    >>> api = simplexmlapi.loads(s, cls=SampleApi)
    >>> api.value
    u'A Value'
    >>> api.thing
    u'A Thing'

"""
__version__ = '0.1.1'
__all__ = ['load', 'loads', 'SimpleXmlApi']

from api import SimpleXmlApi, factory as _factory

def load(fp, map=None, cls=None, **kwargs):
    """
    Parse C{fp} (a file-like object containing an XML document) and return a
    dotted-name-walkable L{SimpleXmlApi} instance.

    If C{map} is specified, attributes will be created on the returned
    instance mapping L{map}'s keys to its associated dotted-name values.

    To use a custom L{SimpleXmlApi} subclass, specify it with the C{cls}
    kwarg.
    """
    return _factory(fp.read(), map, cls, **kwargs)


def loads(s, map=None, cls=None, **kwargs):
    """
    Parse C{s} (a C{str} or C{unicode} instance containing an XML document)
    and return a dotted-name-walkable L{SimpleXmlApi} instance.

    If map is specified, attributes will be created on the returned
    instance mapping map's keys to its associated dotted-name values.

    To use a custom L{SimpleXmlApi} subclass, specify it with the L{cls}
    kwarg.
    """
    return _factory(s, map, cls, **kwargs)

