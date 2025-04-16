class Node:
    def __init__(self, value: str):
        self.value: str = value
        self.right: Node | None = None
        self.left: Node | None = None
    
    def in_order(self) -> list[str]:
        result = []
        if self.left:
            result = self.left.in_order()
        result = result + [self.value]
        if self.right:
            result = result + self.right.in_order()
        return result

    def pre_order(self) -> list[str]:
        result = [self.value]
        if self.left:
            result = result + self.left.pre_order()
        if self.right:
            result = result + self.right.pre_order()
        return result

    def post_order(self) -> list[str]:
        result = []
        if self.left:
            result = self.left.post_order()
        if self.right:
            result = result + self.right.post_order()
        result = result + [self.value]
        return result

def factory_node() -> Node:
    root = Node(value="1")
    childre2 = Node(value="2")
    childre3 = Node(value="3")
    childre4= Node(value="4")
    childre5 = Node(value="5")
    childre6 = Node(value="6")
    childre7 = Node(value="7")
    childre8 = Node(value="8")


    root.left = childre2
    root.right = childre3
    childre2.left = childre4
    childre3.left = childre5
    childre3.right = childre6
    childre5.left = childre7
    childre5.right = childre8

    return root

if __name__ == "__main__":

    root = factory_node()
    
    print("In-order:", root.in_order())
    print("Pre-order:", root.pre_order())
    print("Post-order:", root.post_order())
