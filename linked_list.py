# Create Node

class Node(object):
    """
    Create Node
    """
    def __init__(self, data):
        """
        Initialize the data and next of Node
        """
        self.data = data
        self.next = None


class LinkedList(object):
    """
    Create the Link between two Node
    """
    def __init__(self):
        """
        Initialize the head to None
        """
        self.head = None

    # Adding Node
    def pushatbegining(self, new_data):
        """
        Push the new data at begining
        """
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node

    def afternode(self, p_node, new_data):
        """
        Push new data after p_node
        """
        if p_node is None:
            return
        new_node = Node(new_data)
        new_node.next = p_node.next
        p_node.next = new_node

    def pushatlast(self, new_data):
        """
        Push new data at last of linked list
        """
        new_node = Node(new_data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def printlist(self):
        """
        Printing the linked list
        """
        current = self.head
        while current:
            print(current.data)
            current = current.next
    def getCount(self):
        """
        Get the count of nodes in linked list
        """
        current = self.head
        count = 0
        while current:
            count += 1
            current = current.next
        return count

    def reverse(self):
        """
        Reverse the Linked list
        """
        prev = None
        current = self.head
        while (current is not None):
            next = current.next
            current.next = prev
            prev = current
            current = next
        self.head = prev

    def detectloop(self):
        """
        Detect the loop in Linked list
        """
        p_slow = self.head
        p_fast = self.head

        while p_slow and p_fast and p_fast.next:
            p_slow = p_slow.next
            p_fast = p_fast.next.next

            if p_slow == p_fast:
                print("Loop found")
                return


if __name__ == '__main__':
    ll = LinkedList()
    ll.head = Node(1)
    ll.pushatbegining(2)
    ll.pushatlast(3)
    ll.afternode(ll.head.next, 4)
    ll.printlist()
    ll.reverse()
    ll.printlist()
    print("Count of Node: %d" % ll.getCount())
