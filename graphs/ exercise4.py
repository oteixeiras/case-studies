class Node:
    def __init__(self, value: str):
        self.value: str = value
        self.right: Node | None = None
        self.left: Node | None = None

    
    def print_tree(self, prefix: str = '', is_left: bool = True):
        if self.right:
            self.right.print_tree(prefix + ('│   ' if is_left else '    '), False)
        print(prefix + ('└── ' if is_left else '┌── ') + str(self.value))
        if self.left:
            self.left.print_tree(prefix + ('    ' if is_left else '│   '), True)

def factory_node() -> Node:
    root = Node(value="1")
    childre2 = Node(value="2")
    childre3 = Node(value="3")
    childre4= Node(value="4")
    childre5 = Node(value="5")
    childre6 = Node(value="6")
    childre7 = Node(value="7")
    childre8 = Node(value="8")
    childre9 = Node(value="9")


    root.left = childre2
    root.right = childre3
    childre2.left = childre4
    childre2.right = childre5
    childre3.left = childre6
    childre3.right = childre7
    childre6.left = childre8
    childre6.right = childre9

    return root

def map_leaf_to_root_path(root: Node) -> str:
    if not root:
        return 
    
    stack = [(root, [root.value])]
    
    while stack:
        node, path = stack.pop()
        if not node.left and not node.right:
            print("->".join(map(str, reversed(path))))
        
        if node.right:
            stack.append((node.right, path + [node.right.value]))
        if node.left:
            stack.append((node.left, path + [node.left.value]))

    return 'No elements in the tree'

if __name__ == "__main__":

    root = factory_node()
    root.print_tree()
    print('\n')
    map_leaf_to_root_path(root)