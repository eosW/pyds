import operator

from BinarySearchTree import BinarySearchTree
from treenode.BinaryIndexTreeNode import BinaryIndexTreeNode


class BasicBSTImpl(BinarySearchTree):
    def __init__(self, nodeclass=BinaryIndexTreeNode, eq=operator.eq, gt=operator.gt):
        """
        :param nodeclass: class of the node to be used when create new nodes, must have attribute `key`, `left`, and
        `right`, and a __init__ requires no parameter. default to BinaryIndexTreeNode. Used when call `insert`
        without parameter `node`
        :param eq: binary function used to assert equality of key, default to operator.eq
        :param gt: binary function used to compare keys, default to operator.gt
        """
        self._root = None
        self._nodeclass = nodeclass
        self._key_eq = eq
        self._key_gt = gt

    @property
    def root(self):
        """
        :return: root node of the tree
        """
        return self._root

    def insert(self, node=None, key=None, val=None):
        """
        Insert the node if `node` is provided
        Else a new node will be created by calling nodeclass(key=key), and `val` will be then inserted with name val
        if provided
        One of `node` or `key` must be provided.
        :return:
        """
        if node is None:
            if key is None:
                raise ValueError("one of node and key must be passed")
            node = self._nodeclass()
            node.key = key
            if val is not None:
                node.val = val
        if self._root is None:
            self._root = node
            return
        self._insert(self._root, node)

    def _insert(self, node, new):
        if self._key_gt(node.key, new.key):
            if node.left is None:
                node.left = new
            else:
                self._insert(node.left, new)
        else:
            if node.right is None:
                node.right = new
            else:
                self._insert(node.right, new)

    def delete(self, key):
        return self._delete(self.root, key, self, "_root")

    def _delete(self, node, key, parent, side):
        if node is None:
            return None
        if self._key_eq(node.key, key):
            if node.left is None:
                parent.__setattr__(side, node.right)
            elif node.right is None:
                parent.__setattr__(side, node.left)
            else:
                old = None
                curr = node.left
                while curr.right is not None:
                    old = curr
                    curr = curr.right
                parent.__setattr__(side, curr)
                curr.right = node.right
                if old is not None:
                    old.right = curr.left
                    curr.left = node.left
            return node
        if self._key_gt(node.key, key):
            return self._delete(node.left, key, node, "left")
        else:
            return self._delete(node.right, key, node, "right")
