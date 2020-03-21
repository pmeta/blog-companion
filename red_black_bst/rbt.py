"""
Demo code for 
https://www.songfengting.com/2020/03/20/implementing-red-black-trees-with-property-based-testing/
"""

from enum import Enum


class Color(Enum):
    RED = 0
    BLACK = 1

    def __str__(self):
        #: R | B
        return str(self.name)[0]


RED = Color.RED
BLACK = Color.BLACK


class Node:
    def __init__(self, key):
        self.key = key
        #: default to RED as insertion, because when we insert new nodes,
        #: property of black height remain unchanged
        self.color = RED
        self.left = None
        self.right = None
        self.parent = None

    def __str__(self):
        return "<%s key=%s>" % (self.color, self.key)


class RBTree:
    def __init__(self):
        self.root = None

    def get_color(self, node):
        #: nils are black
        if node is None:
            return BLACK
        else:
            return node.color

    def in_order_walk(self, f):
        t = self.root

        def aux(t):
            if t is not None:
                aux(t.left)
                f(t)
                aux(t.right)

        aux(t)

    def __str__(self):
        """
        Adapted from 
        MIT 6.006 reading section, binary search tree example
        """

        if self.root is None:
            return "<B:empty>"

        def aux(node):
            if node is None:
                return [], 0, 0

            label = "<%s:%s>" % (node.color, node.key)

            left_lines, left_pos, left_width = aux(node.left)
            right_lines, right_pos, right_width = aux(node.right)

            middle = max(right_pos + left_width - left_pos + 1, len(label), 2)

            pos = left_pos + middle // 2
            width = left_pos + middle + right_width - right_pos

            while len(left_lines) < len(right_lines):
                left_lines.append(" " * left_width)

            while len(left_lines) > len(right_lines):
                right_lines.append(" " * right_width)

            if (
                (middle - len(label)) % 2 == 1
                and node.parent is not None
                and node is node.parent.left
                and len(label) < middle
            ):

                label += "."

            label = label.center(middle, ".")
            if label[0] == ".":
                label = " " + label[1:]

            if label[-1] == ".":
                label = label[:-1] + " "

            lines = [
                " " * left_pos + label + " " * (right_width - right_pos),
                " " * left_pos
                + "/"
                + " " * (middle - 2)
                + "\\"
                + " " * (right_width - right_pos),
            ]

            for left_line, right_line in zip(left_lines, right_lines):

                lines.append(
                    left_line + " " * (width - left_width - right_width) + right_line
                )

            return lines, pos, width

        lines = aux(self.root)[0]

        return "\n".join(lines)

    def search(self, key):
        current = self.root
        while current is not None and key != current.key:
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return current

    def left_rotate(self, node: Node):
        sibling = node.right

        #: move sibling's left subtree into node's right subtree
        node.right = sibling.left
        if sibling.left is not None:
            sibling.left.parent = node

        #: link sibling's parent to node's parent
        sibling.parent = node.parent

        if node.parent is None:
            self.root = sibling
        else:
            if node.parent.left is node:
                node.parent.left = sibling
            else:
                node.parent.right = sibling

        sibling.left = node
        node.parent = sibling

    def right_rotate(self, node: Node):
        sibling = node.left

        #: move sibling's right subtree into nodes' left subtree
        node.left = sibling.right
        if sibling.right is not None:
            sibling.right.parent = node

        #: link sibling's parent to node's parent
        sibling.parent = node.parent

        if node.parent is None:
            self.root = sibling
        else:
            if node.parent.left is node:
                node.parent.left = sibling
            else:
                node.parent.right = sibling

        sibling.right = node
        node.parent = sibling

    def insert_fix(self, node: Node):
        #: ref: Introduction to Algorithms(CLRS) - Chapter 13
        #: we only need to care about red parents and cases that the tree is not empty.
        while self.get_color(node.parent) == RED and node != self.root:

            if node.parent == node.parent.parent.right:
                uncle = node.parent.parent.left

                if self.get_color(uncle) == BLACK:
                    if node == node.parent.left:
                        #: Case II
                        node = node.parent
                        self.right_rotate(node)

                    #: Case I
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self.left_rotate(node.parent.parent)

                else:
                    #: uncle is red, case III
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent

            else:
                uncle = node.parent.parent.right
                if self.get_color(uncle) == BLACK:
                    if node == node.parent.right:
                        #: Case II
                        node = node.parent
                        self.left_rotate(node)
                    #: case I
                    node.parent.color = BLACK
                    node.parent.parent.color = RED
                    self.right_rotate(node.parent.parent)

                else:
                    #: uncle is red, case III
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    node.parent.parent.color = RED
                    node = node.parent.parent

        self.root.color = BLACK  # final fix

    def insert(self, key):

        new_node = Node(key)

        current = self.root

        if current is None:
            new_node.color = BLACK
            self.root = new_node
            return

        else:
            while True:
                if key == current.key:
                    return current

                if key > current.key:
                    if current.right is None:
                        current.right = new_node
                        new_node.parent = current
                        break
                    current = current.right
                else:
                    if current.left is None:
                        current.left = new_node
                        new_node.parent = current
                        break
                    current = current.left

        self.insert_fix(new_node)
        return new_node


if __name__ == "__main__":
    tree = RBTree()
    for i in range(30):
        tree.insert(i)
    print(tree)
