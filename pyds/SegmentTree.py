from abc import ABCMeta, abstractmethod

import six


@six.add_metaclass(ABCMeta)
class SegmentTree(object):
    @abstractmethod
    def build(self, iterable):
        pass

    @abstractmethod
    def get(self, idx):
        pass

    @abstractmethod
    def update(self, idx, val):
        pass

    @abstractmethod
    def query(self, low, high):
        pass
