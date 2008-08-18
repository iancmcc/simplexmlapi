#!/usr/bin/env python

import unittest

TESTDOC = """
<node1 abc="1" b="2" subnode="subnodeval">
    <subnode>
        Subnode 1 value.
    </subnode>
    <subnode c="3">
        Subnode 2 value.
        <subsubnode>
            <thing>ThingVal</thing>
            <thing x="y"/>
        </subsubnode>
    </subnode>
    <othernode>Other text.</othernode>
</node1>
"""

TESTCFG = dict(
    val1 = "abc",
    val2 = "subnode__0",
    val3 = "othernode",
    val4 = "subnode__a",
    val5 = "subnode.c",
    val6 = "subnode__1.subsubnode.thing",
    val7 = "subnode__1.subsubnode.thing__1.x"
)

from simplexmlapi import *

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.xml = SimpleXmlApi(map=TESTCFG, source=TESTDOC)
        
    def test_traversal(self):
        self.assertEqual(self.xml._traverse('abc'), '1') 
        self.assertEqual(self.xml._traverse(
            'subnode__1.subsubnode.thing__1.x'), 'y')
    
    def test_properties(self):
        self.assertEqual(self.xml.val1, '1')
        self.assertEqual(self.xml.val4, 'subnodeval')

    def test_attrfailover(self):
        self.assertEqual(self.xml.subnode._, 'Subnode 1 value.')
        self.assertEqual(self.xml.subnode__1.c._, '3')

    def test_newProperties(self):
        self.xml.add_mapping('battr', 'b')
        self.assertEqual(self.xml.battr, '2')

    def test_factory(self):
        xml = loads(TESTDOC, map=TESTCFG)
        self.assertEqual(type(xml), SimpleXmlApi)

    def test_subclass(self):
        class SampleApi(SimpleXmlApi):
            _map = TESTCFG
        xml = loads(TESTDOC, cls=SampleApi)
        self.assertEqual(xml.val1, '1')
        self.assertEqual(xml.val4, 'subnodeval')
        
if __name__=="__main__":
    unittest.main()
