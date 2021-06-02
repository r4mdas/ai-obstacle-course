class Node:

    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:

    def __init__(self):
        self.front = self.rear = None
        self.len = 0

    def isEmpty(self):
        return self.front is None

    def add(self, item):
        temp = Node(item)

        if self.rear is None:
            self.front = self.rear = temp
            return
        self.rear.next = temp
        self.rear = temp
        self.len += 1

    def poll(self):

        if self.isEmpty():
            return
        temp = self.front
        self.front = temp.next
        self.len -= 1

        if self.front is None:
            self.rear = None
