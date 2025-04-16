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

def factory_node(tree_identify: int = 1) -> Node:

    match tree_identify:
        case 1:
            root = Node(value="1")
            childre2 = Node(value="2")
            childre3 = Node(value="3")
            childre4= Node(value="4")
            childre5 = Node(value="5")
            childre6 = Node(value="6")
            childre7 = Node(value="7")

            root.left = childre2
            root.right = childre3
            childre2.left = childre4
            childre2.right = childre5
            childre3.left = childre6
            childre3.right = childre7
        case 2:
            root = Node(value="1")
            childre2 = Node(value="2")
            childre3 = Node(value="3")
            childre4= Node(value="4")
            childre5 = Node(value="5")
            childre6 = Node(value="6")
            childre7 = Node(value="7")

            root.left = childre2
            root.right = childre3
            childre2.left = childre4
            childre2.right = childre5
            childre3.left = childre6
        case 3:
            root = Node(value="1")
            childre2 = Node(value="2")
            childre3 = Node(value="3")
            childre4= Node(value="4") 
            childre5 = Node(value="5")
            childre6 = Node(value="6")
            childre8 = Node(value="8")

            root.left = childre2
            root.right = childre3
            childre2.left = childre4
            childre2.right = childre5
            childre3.left = childre6
            childre3.right = childre8

        case _:
            raise ValueError("Invalid tree identifier")

    return root

def compare_trees(tree_1: Node | None, tree_2: Node | None) -> dict[str, str]:
    if tree_1 is None and tree_2 is None:
        return {'Output': 'True', 'Explanation': 'Ambas as árvores são iguais'}
    if tree_1 is None or tree_2 is None:
        return {'Output': 'False', 'Explanation': 'As árvores têm estruturas diferentes'}
    if tree_1.value != tree_2.value:
        return {'Output': 'False', 'Explanation': 'As árvores têm a mesma estrutura, porém, com valores de nós diferentes'}

    for child_a, child_b in [(tree_1.left, tree_2.left), (tree_1.right, tree_2.right)]:
        result = compare_trees(child_a, child_b)
        if result['Output'] == 'False':
            return result
   
    return {'Output': 'True', 'Explanation': 'Ambas as árvores são iguais'}


def menu(root_identify_1: int = 1, root_identify_2: int = 1) -> None:
    print('#' * 25, f'Compare Trees {root_identify_1} and {root_identify_2}', '#' * 25)
    root_1 = factory_node(tree_identify=root_identify_1)
    root_2 = factory_node(tree_identify=root_identify_2)

    root_1.print_tree()
    print('\n')
    root_2.print_tree()
    print(compare_trees(root_1, root_2))

if __name__ == "__main__":
    menu(root_identify_1=1, root_identify_2=1)
    print('\n')
    menu(root_identify_1=1, root_identify_2=1)
    print('\n')
    menu(root_identify_1=1, root_identify_2=3)
    