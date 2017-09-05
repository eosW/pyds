from abc import abstractmethod, ABCMeta

import six

from OrderedBinaryTree import OrderedBinaryTree


class BinarySearchTree(OrderedBinaryTree):

    @abstractmethod
    def insert(self, node, key, val):
        pass
