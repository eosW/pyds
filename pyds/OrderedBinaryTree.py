from abc import ABCMeta, abstractmethod

import six


@six.add_metaclass(ABCMeta)
class OrderedBinaryTree(object):
    @property
    @abstractmethod
    def root(self):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    def update(self, key, val):
        node = self.search(key)
        if node is not None:
            node.val = val
        return node

    def search(self, key):
        return self._search(self._root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if self._key_eq(node.key, key):
            return node
        if self._key_gt(node.key, key):
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

    def _right_rotate(self, node):
        l = node.left
        node.left = l.right
        if l.right is not None:
            l.right.parent = node
        l.right = node
        if not node.parent:
            self._root = l
        elif node is node.parent.left:
            node.parent.left = l
        else:
            node.parent.right = l
        l.parent = node.parent
        node.parent = l

    def _left_rotate(self, node):
        r = node.right
        node.right = r.left
        if r.left is not None:
            r.left.parent = node
        r.left = node
        if not node.parent:
            self._root = r
        elif node is node.parent.left:
            node.parent.left = r
        else:
            node.parent.right = r
        r.parent = node.parent
        node.parent = r
