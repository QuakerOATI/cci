from abc import ABC

class SearchTree:

    class _Node:

        def __init__(self, val, left, right):
            self.value = val
            self._weight = 1
            self._left = None
            self._right = None
            self._parent = None
            self.left, self.right = left, right

        @property
        def parent(self):
            return self._parent

        @property
        def weight(self):
            return self._weight

        @property
        def left(self):
            return self._left

        @property
        def right(self):
            return self._left

        @left.setter
        def left(self, child):
            if child is not None:
                self._weight += child.weight
            if self._left is not None:
                self._weight -= self._left.weight
            self._left = child

        @right.setter
        def right(self, child):
            if child is not None:
                self._weight += child.weight
            if self._right is not None:
                self._weight -= self._right.weight
            self._right = child

        def is_left_child(self):
            return self._parent is not None and self._parent.left is self

        def is_right_child(self):
            return self._parent is not None and self._parent.right is self

        @classmethod
        def get_sentinel(cls, val=None, weight=0):
            ret = cls(val, None, None)
            ret._weight = weight
            return ret


    def __init__(self, root_val):
        self._STOP = self._Node.get_sentinel()
        self._root = self._Node(root_val)

    def _walk(self, go_left, go_right):
        curr = self._root
        while True:
            if go_left(curr):
                curr = curr.left
            elif go_right(curr):
                curr = curr.right
            else:
                break
        return curr

    def add(self, val):
        pass
