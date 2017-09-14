import operator

from BinarySearchTree import BinarySearchTree
from treenode.RedBlackTreeNode import RedBlackTreeNode


class RedBlackTreeImpl(BinarySearchTree):
    def __init__(self, nodeclass=RedBlackTreeNode, eq=operator.eq, gt=operator.gt):
        """
        :param nodeclass: the class of tree node, should be derived from :class:`RedBlackTreeNode`
        :param eq: function used to evaluate equality of `nodeclass`.key
        :param gt: function used to evaluate priority of `nodeclass`.key
        """
        self._root = None
        self._nodeclass = nodeclass
        self._key_eq = eq
        self._key_gt = gt

    @property
    def root(self):
        return self._root

    def insert(self, node=None, key=None, val=None):
        """
        insert a shallow copy of `node` if it is provided, else insert a new node of given `key` adn `value`
        :param node:
        :param key:
        :param val:
        """
        if node is None:
            if key is None:
                raise ValueError("one of node and key must be passed")
            node = self._nodeclass()
            node.key = key
            if val is not None:
                node.val = val
        node.red = True
        if self._root is None:
            self._root = node
            self._insert_fix(node)
            return
        self._insert(self._root, node)

    def _insert(self, node, new):
        if self._key_gt(node.key, new.key):
            if node.left is None:
                node.left = new
                new.parent = node
                self._insert_fix(new)
            else:
                self._insert(node.left, new)
        else:
            if node.right is None:
                node.right = new
                new.parent = node
                self._insert_fix(new)
            else:
                self._insert(node.right, new)

    def _insert_fix(self, node):
        p = node.parent
        if p is None:
            node.red = False
            return
        if not p.red:
            return
        gp = p.parent
        # left case
        if p is gp.left:
            # red uncle
            if gp.right and gp.right.red:
                gp.right.red = False
                p.red = False
                gp.red = True
                self._insert_fix(gp)
                return
            # left-right
            if node is p.right:
                self._left_rotate(p)
                p = node
            # left-left
            p.red = False
            gp.red = True
            self._right_rotate(gp)
        else:
            # red uncle
            if gp.left and gp.left.red:
                gp.left.red = False
                p.red = False
                gp.red = True
                self._insert_fix(gp)
                return
            # right-left
            if node is p.left:
                self._right_rotate(p)
                p = node
            # right-right
            p.red = False
            gp.red = True
            self._left_rotate(gp)

    def delete(self, key):
        return self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if self._key_eq(node.key, key):
            p = node.parent
            l = p and p.left is node
            if node.left is None:
                if p is None:
                    self._root = node.right
                elif l:
                    p.left = node.right
                else:
                    p.right = node.right
                if node.right:
                    node.right.parent = p
                # delete red is fine
                if not node.red:
                    # black + red = black
                    if node.right and node.right.red:
                        node.right.red = False
                    # black + black = double black
                    else:
                        self._delete_fixup(p, l)

            elif node.right is None:
                if p is None:
                    self._root = node.left
                elif l:
                    p.left = node.left
                else:
                    p.right = node.left
                node.left.parent = p
                # delete red is fine
                if not node.red:
                    # black + red = black
                    if node.left.red:
                        node.left.red = False
                    # black + black = double black
                    # impossible case?
                    else:
                        self._delete_fixup(p, l)

            else:
                curr = node.left
                while curr.right is not None:
                    curr = curr.right
                if p is None:
                    self._root = curr
                elif p.left is node:
                    p.left = curr
                else:
                    p.right = curr
                curr.right = node.right
                curr.right.parent = curr
                cp = curr.parent
                if cp is not node:
                    cp.right = curr.left
                    if cp.right is not None:
                        cp.right.parent = cp
                    curr.left = node.left
                    curr.left.parent = curr
                curr.parent = node.parent
                temp = curr.red
                curr.red = node.red
                # delete red is fine
                if not temp:
                    if cp is not node:
                        # black + red = black
                        if cp.right is not None and cp.right.red:
                            cp.right.red = False
                        # black + black = double black
                        else:
                            self._delete_fixup(cp, False)
                    else:
                        # black + red = black
                        if curr.left is not None and curr.left.red:
                            curr.left.red = False
                        # black + black = double black
                        else:
                            self._delete_fixup(curr, True)

            return node
        if self._key_gt(node.key, key):
            return self._delete(node.left, key)
        else:
            return self._delete(node.right, key)

    def _delete_fixup(self, p, left):
        # root case
        if not p:
            return
        # left case
        if left:
            sibling = p.right
            # red sibling: change to black
            if sibling.red:
                p.red = True
                sibling.red = False
                self._left_rotate(p)
                sibling = p.right
            leftniece = sibling.left
            rightniece = sibling.right
            lnr = leftniece is not None and leftniece.red
            rnr = rightniece is not None and rightniece.red
            # black parent and black niece: recolor
            if not p.red and not lnr and not rnr:
                sibling.red = True
                l = p.parent and p.praent.left is p
                self._delete_fixup(p.parent, l)
                return
            # red parent and black niece: recolor
            if p.red and not lnr and not rnr:
                p.red = False
                sibling.red = True
                return
            # black right niece: change to red
            if not rnr:
                sibling.red = True
                leftniece.red = False
                self._right_rotate(sibling)
                rightniece = sibling
                sibling = leftniece
            # red right niece: rotate
            sibling.red = p.red
            p.red = False
            rightniece.red = False
            self._left_rotate(p)
            return
        # right case
        else:
            sibling = p.left
            # red sibling: change to black
            if sibling.red:
                p.red = True
                sibling.red = False
                self._right_rotate(p)
                sibling = p.left
            leftniece = sibling.left
            rightniece = sibling.right
            lnr = leftniece is not None and leftniece.red
            rnr = rightniece is not None and rightniece.red
            # black parent and black niece: recolor
            if not p.red and not lnr and not rnr:
                sibling.red = True
                l = p.parent and p.praent.left is p
                self._delete_fixup(p.parent, l)
                return
            # red parent and black niece: recolor
            if p.red and not lnr and not rnr:
                p.red = False
                sibling.red = True
                return
            # black left niece: change to red
            if not lnr:
                sibling.red = True
                rightniece.red = False
                self._left_rotate(sibling)
                leftniece = sibling
                sibling = rightniece
            # red left niece: rotate
            sibling.red = p.red
            p.red = False
            leftniece.red = False
            self._right_rotate(p)
            return
