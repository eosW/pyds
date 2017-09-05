from abc import abstractmethod

from OrderedBinaryTree import OrderedBinaryTree


class Treap(OrderedBinaryTree):
    @abstractmethod
    def insert(self, node, key, priority, val):
        pass

    @abstractmethod
    def update_priority(self, key, priority):
        pass

    @abstractmethod
    def split(self, key, keep_pivot):
        pass

    @classmethod
    @abstractmethod
    def join(cls, left, right):
        pass

    @classmethod
    @abstractmethod
    def union(cls, t1, t2):
        pass

    @classmethod
    @abstractmethod
    def intersect(cls, t1, t2):
        pass

    @classmethod
    @abstractmethod
    def difference(cls, left, right):
        pass
