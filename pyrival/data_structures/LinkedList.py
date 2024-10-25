class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

    def __repr__(self):
        return self.__class__.__name__ + ("({})".format(self.value) if self else "()")


class LinkedList:
    def __init__(self, iterable=None):
        self.sentinel = Node(None)
        # at the top next left
        self.sentinel.next = self.sentinel
        # at the top previous right
        self.sentinel.prev = self.sentinel
        self.__len = 0
        if iterable is not None:
            self += iterable

    def get_node(self, index):
        node = self.sentinel
        i = 0
        while i <= index:
            node = node.next
            if node == self.sentinel:
                break
            i += 1
        if node == self.sentinel:
            node = None
        return node

    def __getitem__(self, index):
        node = self.get_node(index)
        return node.value

    def __len__(self):
        return self.__len

    def __setitem__(self, index, value):
        node = self.get_node(index)
        node.value = value

    def __delitem__(self, index):
        node = self.get_node(index)
        self.del_node(node)

    def del_node(self, node):
        if node:
            node.prev.next = node.next
            if node.next:
                node.next.prev = node.prev
            node.prev = None
            node.next = None
            node.value = None
            self.__len -= 1

    def __repr__(self):
        return str(self.to_list())

    def to_list(self):
        elts = []
        curr = self.sentinel.next
        while curr != self.sentinel:
            elts.append(curr.value)
            curr = curr.next
        return elts

    def append(self, value):
        node = Node(value)
        self.insert_between(node, self.sentinel.prev, self.sentinel)

    def appendleft(self, value):
        node = Node(value)
        self.insert_between(node, self.sentinel, self.sentinel.next)
        return node

    def insert(self, index, value):
        new_node = Node(value)
        len_ = len(self)
        if len_ == 0:
            self.insert_between(new_node, self.sentinel, self.sentinel)
        elif index >= 0 and index < len_:
            node = self.get_node(index)
            self.insert_between(new_node, node.prev, node)
        elif index == len_:
            self.insert_between(new_node, self.sentinel.prev, self.sentinel)
        else:
            raise IndexError

    def insert_between(self, node, left_node, right_node):
        if node and left_node and right_node:
            node.prev = left_node
            node.next = right_node
            left_node.next = node
            right_node.prev = node
            self.__len += 1
        else:
            raise IndexError

    def insert_after(self, node, value):
        new_node = Node(value)
        node.next.prev = new_node
        new_node.next = node.next
        node.next = new_node
        new_node.prev = node
        self.__len += 1

    def merge_left(self, other):
        self.sentinel.next.prev = other.sentinel.prev
        other.sentinel.prev.next = self.sentinel.next
        self.sentinel.next = other.sentinel.next
        self.sentinel.next.prev = self.sentinel
        self.__len += other.__len

    def merge_right(self, other):
        self.sentinel.prev.next = other.sentinel.next
        other.sentinel.next.prev = self.sentinel.prev
        self.sentinel.prev = other.sentinel.prev
        self.sentinel.prev.next = self.sentinel
        self.__len += other.__len

    def pop(self, node = None):
        if node is None:
            node = self.sentinel.prev
        if self.__len < 1:
            raise IndexError
        node.prev.next = node.next
        node.next.prev = node.prev
        self.__len -= 1
        return node.value

    def before(self, node):
        return node.prev.prev if node.prev == self.sentinel else node.prev

    def after(self, node):
        return node.next.next if node.next == self.sentinel else node.next
