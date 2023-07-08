class Router:
    def __init__(self, name, cola_origen, cola_forward):
        self.name = name
        self.received_messages = [] 
        self.is_active = True
        self.messages_forward = None
        self.messages_local = None
        self.next = None



class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def append(self, name):
        new_Router = Router(name)
        if self.is_empty():
            self.head = new_Router
            self.size += 1
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_Router
            self.size += 1

    def prepend(self, name):
        new_Router = Router(name)
        if self.is_empty():
            self.head = new_Router
            self.size += 1
        else:
            new_Router.next = self.head
            self.head = new_Router
            self.size += 1

    def insert_after(self, prev_Router, name):
        if prev_Router is None:
            print("Previous Router must not be None.")
            return
        new_Router = Router(name)
        new_Router.next = prev_Router.next
        prev_Router.next = new_Router
        self.size += 1

    def delete(self, name):
        if self.is_empty():
            print("Linked list is empty. Nothing to delete.")
            return

        if self.head.name == name:
            self.head = self.head.next
            self.size -= 1
            return

        current = self.head
        prev = None
        while current and current.name != name:
            prev = current
            current = current.next

        if current is None:
            print("name not found in the linked list.")
            return

        prev.next = current.next
        self.size -= 1

    def display(self):
        if self.is_empty():
            print("Linked list is empty.")
            return

        current = self.head
        while current:
            print(current.name, end=" ")
            current = current.next
        print()