"""
Demo code for 
https://www.songfengting.com/2020/03/20/implementing-red-black-trees-with-property-based-testing/
"""

import unittest

import hypothesis.strategies as st
from hypothesis.database import DirectoryBasedExampleDatabase
from hypothesis.stateful import RuleBasedStateMachine, rule, precondition, invariant

from rbt import RBTree, Color, Node


class RBTreeMachine(RuleBasedStateMachine):
    """
    Invariants:
        0. The nodes are either black or red.
        1. The root of the red-black tree is black, and leaves(nil) are black.
        2. The children of a red node are black.
        3. Every path from a given node to any of its
           descendant NIL nodes goes through the same number of black nodes.
    """

    def __init__(self):
        super().__init__()
        self.tree = RBTree()

    @rule(key=st.integers())
    def insert(self, key):
        self.tree.insert(key)
        assert self.tree.search(key) is not None

    @precondition(lambda self: self.tree.root is not None)
    @invariant()
    def node_is_either_red_or_black(self):
        #: Invariant 0
        def f(node):
            assert node.color in Color, (
                "nodes should either be red or black \n %s" % self.tree
            )

        self.tree.in_order_walk(f)

    @precondition(lambda self: self.tree.root is not None)
    @invariant()
    def root_is_black(self):
        #: Invariant 1
        assert self.tree.root.color == Color.BLACK, (
            "root has to be black\n %s" % self.tree
        )

    @precondition(lambda self: self.tree.root is not None)
    @invariant()
    def red_nodes_have_black_children(self):
        #: Invariant 2
        def f(node):
            if node.color is Color.RED:
                if node.left is not None:
                    assert node.left.color is Color.BLACK, (
                        "red nodes can only have black children(left)\n %s" % self.tree
                    )
                if node.right is not None:
                    assert node.right.color is Color.BLACK, (
                        "red nodes can only have black children(right)\n %s" % self.tree
                    )

        self.tree.in_order_walk(f)

    @precondition(lambda self: self.tree.root is not None)
    @invariant()
    def black_heights_are_the_same(self):
        #: Invariant 3
        def aux(t):
            if t is None:
                return 1
            left, right = aux(t.left), aux(t.right)
            assert left == right, (
                "left's black height should equal to right's \n %s" % self.tree
            )
            return left + (1 if t.color is Color.BLACK else 0)

        bh = aux(self.tree.root)
        assert bh > 0


TestTrees = RBTreeMachine.TestCase

if __name__ == "__main__":
    unittest.main()
