"""
    Autor: Fernando de Souza Teixeira
"""

import unittest

from kruskal import algoritmo_kruskal

class TestKruskal(unittest.TestCase):
    def test_grafo_ja_e_arvore(self):
        """
        Testa o caso em que o grafo já é uma árvore (n-1 arestas e conexo).
        A MST deve ser igual ao grafo, sem circuitos removidos.
        """
        arestas = [
            (0, 1, 1),
            (1, 2, 2),
            (2, 3, 3)
        ]
        numero_vertices = 4
        mst, circuitos, eh_arvore = algoritmo_kruskal(numero_vertices, arestas)
        # A MST deve ser igual às arestas originais
        self.assertEqual(set(mst), set(arestas))
        # Não deve haver circuitos
        self.assertEqual(circuitos, [])
        # O grafo já era uma árvore
        self.assertTrue(eh_arvore)

    def test_grafo_com_circuitos(self):
        """
        Testa um grafo com circuitos, onde o algoritmo deve remover algumas arestas.
        """
        arestas = [
            (0, 1, 1),
            (1, 2, 2),
            (2, 0, 3),  # Esta aresta forma um ciclo
            (1, 3, 4)
        ]
        numero_vertices = 4
        mst, circuitos, eh_arvore = algoritmo_kruskal(numero_vertices, arestas)
        # A MST deve ter n-1 arestas
        self.assertEqual(len(mst), numero_vertices - 1)
        # Deve haver uma aresta removida (a que forma o ciclo)
        self.assertEqual(len(circuitos), 1)
        self.assertIn((2, 0, 3), circuitos)
        # O grafo não era uma árvore
        self.assertFalse(eh_arvore)
    
    def test_grafo_vazio(self):
        """
        Testa o caso de um grafo vazio.
        A MST deve ser vazia e não deve haver circuitos.
        """
        arestas = []
        numero_vertices = 0
        mst, circuitos, eh_arvore = algoritmo_kruskal(numero_vertices, arestas)
        self.assertEqual(mst, [])
        self.assertEqual(circuitos, [])
        self.assertTrue(eh_arvore)
    def test_grafo_com_uma_aresta(self):
        """
        Testa o caso de um grafo com uma única aresta.
        A MST deve ser igual à aresta e não deve haver circuitos.
        """
        arestas = [
            (0, 1, 5)
        ]
        numero_vertices = 2
        mst, circuitos, eh_arvore = algoritmo_kruskal(numero_vertices, arestas)
        self.assertEqual(mst, arestas)
        self.assertEqual(circuitos, [])
        self.assertTrue(eh_arvore)

if __name__ == "__main__":
    unittest.main()
