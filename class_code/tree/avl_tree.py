import unittest
from avltree import AvlTree

class TestAvlTree(unittest.TestCase):
    def setUp(self) -> None:
        self.tree = AvlTree[int, str]()
    
    def test_insert(self):
        self.tree[10] = "dez"
        self.tree[20] = "vinte"
        self.tree[30] = "trinta"

        self.assertEqual(self.tree[10], "dez")
        self.assertEqual(self.tree[20], "vinte")
        self.assertEqual(self.tree[30], "trinta")

        self.assertIsNotNone(self.tree)
    
    def test_delete(self):
        self.tree[10] = "dez"
        self.tree[20] = "vinte"
        self.tree[30] = "trinta"
        
        del self.tree[20]
        self.assertNotIn(20, self.tree)
        self.assertEqual(len(self.tree), 2)
    
    def test_inorder_traversal(self):
        elements = [10, 20, 30]

        for i in elements:
            self.tree[i] = str(i)

        inorder_elements = list(self.tree)

        self.assertEqual(inorder_elements, elements)
    
    def test_update_value(self):
        self.tree[10] = "dez"
        self.tree[20] = "vinte"
        self.tree[30] = "trinta"
        
        self.tree[10] = "ten"
        self.tree[20] = "twenty"

        self.assertEqual(self.tree[10], "ten")
        self.assertEqual(self.tree[20], "twenty")
        self.assertEqual(self.tree[30], "trinta")

    def test_empty_tree(self):
        breakpoint()
        self.assertEqual(len(self.tree), 0)
        
        


if __name__ == "__main__":
    unittest.main()