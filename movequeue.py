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

    def print(self):
        print(self.get_str())

    def get_str(self):
        cur: Node = self.front
        print_str = ""
        while cur is not self.rear:
            print_str += str(cur.data)
            cur = cur.next

        return print_str

    def check_paralysis(self):
        cur: Node = self.front
        queue_dict = dict()
        while cur is not self.rear:
            queue_dict[cur] = queue_dict.get(cur, 0) + 1
            cur = cur.next

        if len(queue_dict) == 2:
            self.print()
            pre_item = None
            for item in queue_dict:
                if pre_item is None:
                    pre_item = item
                else:
                    if pre_item is not item:
                        return False

        return True
