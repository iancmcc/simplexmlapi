#!/usr/bin/env python

import unittest

TESTDOC = """
<node1 abc="1" b="2" subnode="subnodeval">
    <subnode>
        Subnode 1 value.
    </subnode>
    <subnode c="3">
        Subnode 2 value.
    </subnode>
    <othernode>Other text.</othernode>
</node1>
"""

from simplexmlapi.node import *

class TestDotNodes(unittest.TestCase):
    
    def setUp(self):
        self.doc = DotXMLDoc(TESTDOC)

    def test_DotNodeParent(self):
        l = self.doc.subnode
        for i in range(len(l)):
            self.assert_(type(l[i])==DotNode)

    def test_DotNodeList_getattr(self):
        l = self.doc.subnode
        self.assertEqual(l.getValue, l[0].getValue)
        self.assertEqual(len(l), 2)
    
    def test_DotNodeList_getItem(self):
        l = self.doc.subnode
        self.assertEqual(l[1].getValue(), "Subnode 2 value.")
    
    def test_DotNode_getValue(self):
        l = self.doc.othernode
        self.assertEqual(l.getValue(), "Other text.")
    
    def test_DotNode_getAttribute(self):
        l = self.doc.abc__a
        self.assertEqual(l.getValue(), '1')
    
    def test_DotNode_locatorParsing(self):
        self.assertEqual(self.doc.abc.getValue(), '1')
        self.assertEqual(self.doc.subnode__0.getValue(), 'Subnode 1 value.')
        self.assertEqual(self.doc.subnode__1.getValue(), 'Subnode 2 value.')
        self.assertEqual(self.doc.subnode__a.getValue(), 'subnodeval')
        
    def test_DotNode_errorhandling(self):
        self.assertRaises(NoSuchNode, lambda:self.doc.notanode)
        self.assertRaises(NoSuchAttribute, lambda:self.doc.badattr__a)
        self.assertRaises(NoSuchNode, lambda:self.doc.subnode__3)
        self.assertRaises(AttributeParsingError, lambda:self.doc.subnode__x)
    
    def test_DotNode_attributeFailover(self):
        self.assertEqual(self.doc.abc.getValue(), '1')
    
    def test_DotNode_attributeGet(self):
        self.assertEqual(self.doc.subnode__1['c'], '3')
        self.assertRaises(NoSuchAttribute, lambda:self.doc.subnode['c'])


if __name__=="__main__":
    unittest.main()
