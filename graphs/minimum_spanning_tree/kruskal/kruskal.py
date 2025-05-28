'''
    Autor: Fernando de Souza Teixeira
    Referência: https://www.techiedelight.com/pt/kruskals-algorithm-for-finding-minimum-spanning-tree/

    Objetivo:
        Implementar um algoritmo para criar uma arvore geradora mínima usando Kruskal
            a. O algoritmo deve receber um grafo não dirigido e valorado, e criar uma arvore geradora mínima.
            b. O algoritmo deve informar ao usuário quantos circuitos foram retirados do grafo original.
            c. Deve mostrar os circuitos retirados
            d. O algoritmo deve informar quando a arvore geradora mínima é o próprio grafo
            e.  O algoritmo deve mostrar ao usuário a formação final da arvore, com os respectivos custos de suas arestas
'''

import tkinter as tk
from typing import List, Tuple, Dict
import math

class ConjuntoDisjunto:
    """
    Classe para gerenciar conjuntos disjuntos (Union-Find).

    Esta estrutura permite agrupar elementos em conjuntos que não se sobrepõem, 
    sendo muito utilizada para detectar ciclos e unir componentes em algoritmos de grafos, 
    como o de Kruskal para árvore geradora mínima.
    """

    def __init__(self, numero_elementos: int):
        """
        Inicializa a estrutura Union-Find com cada elemento sendo seu próprio pai.
        O atributo 'pai' é uma lista onde o índice representa o elemento e o valor é o pai dele.
        O atributo 'rank' é usado para otimizar a união dos conjuntos, representando a "altura" da árvore.

        Args:
            numero_elementos (int): Número total de elementos na estrutura.
        """
        self.pai = list(range(numero_elementos))
        self.rank = [0] * numero_elementos

    def encontrar_raiz(self, elemento: int) -> int:
        """
        Encontra a raiz (representante) do conjunto ao qual o elemento pertence.
        Aplica compressão de caminho para otimizar futuras buscas, fazendo com que todos os
        elementos no caminho apontem diretamente para a raiz.

        Args:
            elemento (int): O elemento para o qual se quer encontrar a raiz.

        Returns:
            int: O representante (raiz) do conjunto.
        """
        if self.pai[elemento] != elemento:
            self.pai[elemento] = self.encontrar_raiz(self.pai[elemento])
        return self.pai[elemento]

    def unir_conjuntos(self, elemento_a: int, elemento_b: int) -> bool:
        """
        Une os conjuntos que contêm os elementos 'elemento_a' e 'elemento_b'.
        Utiliza a heurística de rank para manter as árvores balanceadas, anexando a árvore
        de menor rank à de maior rank.

        Args:
            elemento_a (int): Primeiro elemento.
            elemento_b (int): Segundo elemento.

        Returns:
            bool: True se a união foi realizada (os elementos estavam em conjuntos diferentes),
                  False se já pertenciam ao mesmo conjunto.
        """
        raiz_a = self.encontrar_raiz(elemento_a)
        raiz_b = self.encontrar_raiz(elemento_b)
        if raiz_a == raiz_b:
            return False
        if self.rank[raiz_a] < self.rank[raiz_b]:
            self.pai[raiz_a] = raiz_b
        else:
            self.pai[raiz_b] = raiz_a
            if self.rank[raiz_a] == self.rank[raiz_b]:
                self.rank[raiz_a] += 1
        return True

def algoritmo_kruskal(numero_vertices: int, arestas: List[Tuple[int, int, int]]) -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]], bool]:
    """
    Implementa o algoritmo de Kruskal para encontrar a árvore geradora mínima (MST) de um grafo não dirigido e valorado.

    Args:
        numero_vertices (int): Número de vértices do grafo.
        arestas (list): Lista de tuplas representando as arestas no formato (origem, destino, peso).

    Returns:
        tuple: Uma tupla contendo:
            - arvore_geradora_minima (list): Lista de arestas que compõem a MST.
            - arestas_circuito (list): Lista de arestas que formariam ciclos e foram removidas.
            - grafo_original_era_arvore (bool): Indica se o grafo original já era uma árvore (sem circuitos).
    """
    estrutura_union_find = ConjuntoDisjunto(numero_vertices)
    arvore_geradora_minima: List[Tuple[int, int, int]] = []
    arestas_circuito: List[Tuple[int, int, int]] = []
    arestas_ordenadas = sorted(arestas, key=lambda x: x[2])
    
    for vertice_origem, vertice_destino, peso in arestas_ordenadas:
        if estrutura_union_find.unir_conjuntos(vertice_origem, vertice_destino):
            arvore_geradora_minima.append((vertice_origem, vertice_destino, peso))
        else:
            arestas_circuito.append((vertice_origem, vertice_destino, peso))
    
    grafo_original_era_arvore = len(arvore_geradora_minima) == len(arestas)
    return arvore_geradora_minima, arestas_circuito, grafo_original_era_arvore

class VisualizadorGrafo(tk.Tk): #TODO: Refatorar para herdar de tk.Tk e remover de dentro dessa arquivo
    """
    Classe para visualização gráfica do algoritmo de Kruskal usando Tkinter.

    Exibe o grafo original, a árvore geradora mínima (MST) e destaca as arestas removidas (circuitos).
    Mostra também informações textuais sobre a MST, circuitos e custo total.

    Args:
        numero_vertices (int): Número de vértices do grafo.
        arestas_originais (list): Lista de arestas do grafo original.
        arvore_geradora_minima (list): Lista de arestas da MST.
        arestas_circuito (list): Lista de arestas removidas por formarem ciclos.
        grafo_original_era_arvore (bool): Indica se o grafo original já era uma árvore.
    """

    def __init__(self, numero_vertices: int, arestas_originais: List[Tuple[int, int, int]], 
                 arvore_geradora_minima: List[Tuple[int, int, int]], arestas_circuito: List[Tuple[int, int, int]], 
                 grafo_original_era_arvore: bool):
        super().__init__()
        self.title("Kruskal - Visualização Gráfica")
        self.geometry("900x500")
        self.numero_vertices = numero_vertices
        self.arestas_originais = arestas_originais
        self.arvore_geradora_minima = arvore_geradora_minima
        self.arestas_circuito = arestas_circuito
        self.grafo_original_era_arvore = grafo_original_era_arvore

        self.configurar_interface()
        self.posicoes_vertices = self.calcular_posicoes_vertices(numero_vertices, 180, 200, 200)
        self.desenhar_grafo(self.canvas_original, arestas_originais, destaque=[])
        self.desenhar_grafo(self.canvas_mst, arvore_geradora_minima, destaque=arestas_circuito)
        self.mostrar_informacoes()

    def configurar_interface(self):
        """
        Configura os componentes da interface gráfica, incluindo os painéis de desenho dos grafos
        e a área de informações textuais.
        """
        tk.Label(self, text="Grafo Original").pack()
        self.canvas_original = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas_original.pack(side=tk.LEFT, padx=10, pady=10)
        
        tk.Label(self, text="Árvore Geradora Mínima (MST)").pack()
        self.canvas_mst = tk.Canvas(self, width=400, height=400, bg="white")
        self.canvas_mst.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.area_informacoes = tk.Text(self, width=110, height=8)
        self.area_informacoes.pack(side=tk.BOTTOM, padx=10, pady=10)

    def calcular_posicoes_vertices(self, numero_vertices: int, raio: int, centro_x: int, centro_y: int) -> Dict[int, Tuple[int, int]]:
        """
        Calcula as posições dos vértices distribuindo-os em um círculo para visualização no canvas.

        Args:
            numero_vertices (int): Número de vértices.
            raio (int): Raio do círculo.
            centro_x (int): Coordenada x do centro do círculo.
            centro_y (int): Coordenada y do centro do círculo.

        Returns:
            dict: Dicionário com as posições dos vértices {vertice: (x, y)}.
        """
        posicoes = {}
        angulo_passo = 2 * math.pi / numero_vertices
        for vertice in range(numero_vertices):
            angulo = angulo_passo * vertice
            pos_x = int(centro_x + raio * math.cos(angulo))
            pos_y = int(centro_y + raio * math.sin(angulo))
            posicoes[vertice] = (pos_x, pos_y)
        return posicoes

    def desenhar_grafo(self, canvas: tk.Canvas, arestas: List[Tuple[int, int, int]], destaque: List[Tuple[int, int, int]]):
        """
        Desenha o grafo (arestas e vértices) no canvas especificado.
        Arestas presentes na lista 'destaque' são desenhadas em vermelho.

        Args:
            canvas (tk.Canvas): Canvas onde o grafo será desenhado.
            arestas (list): Lista de arestas a serem desenhadas.
            destaque (list): Lista de arestas a serem destacadas (ex: circuitos).
        """
        for origem, destino, peso in arestas:
            x_origem, y_origem = self.posicoes_vertices[origem]
            x_destino, y_destino = self.posicoes_vertices[destino]
            cor = "red" if (origem, destino, peso) in destaque or (destino, origem, peso) in destaque else "black"
            canvas.create_line(x_origem, y_origem, x_destino, y_destino, fill=cor, width=2 if cor=="red" else 1)
            self.desenhar_peso_aresta(canvas, x_origem, y_origem, x_destino, y_destino, peso)
        for vertice, (x, y) in self.posicoes_vertices.items():
            self.desenhar_vertice(canvas, x, y, vertice)

    def desenhar_vertice(self, canvas: tk.Canvas, x: int, y: int, rotulo: int):
        """
        Desenha um vértice (nó) individual no canvas.

        Args:
            canvas (tk.Canvas): Canvas onde o vértice será desenhado.
            x (int): Coordenada x do vértice.
            y (int): Coordenada y do vértice.
            rotulo (int): Rótulo do vértice.
        """
        canvas.create_oval(x-18, y-18, x+18, y+18, fill="lightgray", outline="black", width=2)
        canvas.create_text(x, y, text=str(rotulo), font=("Arial", 12, "bold"))

    def desenhar_peso_aresta(self, canvas: tk.Canvas, x1: int, y1: int, x2: int, y2: int, peso: int):
        """
        Desenha o peso de uma aresta no ponto médio entre dois vértices.

        Args:
            canvas (tk.Canvas): Canvas onde o peso será desenhado.
            x1, y1 (int): Coordenadas do primeiro vértice.
            x2, y2 (int): Coordenadas do segundo vértice.
            peso (int): Peso da aresta.
        """
        ponto_medio_x = (x1 + x2) // 2
        ponto_medio_y = (y1 + y2) // 2
        canvas.create_text(ponto_medio_x, ponto_medio_y, text=str(peso), fill="blue", font=("Arial", 10, "bold"))

    def mostrar_informacoes(self):
        """
        Exibe informações textuais sobre a árvore geradora mínima, circuitos removidos
        e o custo total da MST na área de informações da interface.
        """
        self.area_informacoes.insert(tk.END, "=== Resultados do Kruskal ===\n")
        if self.grafo_original_era_arvore:
            self.area_informacoes.insert(tk.END, "O grafo original já era uma árvore (não havia circuitos).\n")
        else:
            self.area_informacoes.insert(tk.END, f"Circuitos removidos: {len(self.arestas_circuito)}\n")
            for origem, destino, peso in self.arestas_circuito:
                self.area_informacoes.insert(tk.END, f"  {origem} --{peso}-- {destino}\n")
        self.area_informacoes.insert(tk.END, "\nÁrvore Geradora Mínima:\n")
        custo_total = sum(peso for _, _, peso in self.arvore_geradora_minima)
        for origem, destino, peso in self.arvore_geradora_minima:
            self.area_informacoes.insert(tk.END, f"  {origem} --{peso}-- {destino}\n")
        self.area_informacoes.insert(tk.END, f"\nCusto total: {custo_total}\n")
        self.area_informacoes.config(state=tk.DISABLED)

if __name__ == "__main__":
    # Configuração do grafo de exemplo
    arestas_exemplo = [
        (0, 1, 7), (1, 2, 8), (0, 3, 5), (1, 3, 9), (1, 4, 7), (2, 4, 5),
        (3, 4, 15), (3, 5, 6), (4, 5, 8), (4, 6, 9), (5, 6, 11)
    ]
    numero_vertices = 7

    mst, circuitos, eh_arvore = algoritmo_kruskal(numero_vertices, arestas_exemplo)
    app = VisualizadorGrafo(numero_vertices, arestas_exemplo, mst, circuitos, eh_arvore)
    app.mainloop()
