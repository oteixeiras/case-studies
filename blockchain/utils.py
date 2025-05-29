"""
    Author: Bruna Carlette e Fernando de Souza Teixeira
"""

from dataclasses import dataclass
import os
from matplotlib import pyplot as plt

@dataclass
class Utils():
    @staticmethod
    def plot_results(threads: list[int], times:list[int])-> None:
        """
            Plota os resultados de tempo de mineração concorrente em um gráfico.
        """
        plt.figure(figsize=(10,6))
        plt.plot(threads, times, 'o-', label='Tempo de Mineração')
        plt.xlabel('Número de Threads')
        plt.ylabel('Tempo (segundos)')
        plt.title('Escalabilidade de Mineração Concorrente')
        plt.xticks(threads)
        plt.legend()
        
        Utils.save_results()

    @staticmethod
    def save_results()-> None:
        """
            Salva o gráfico de resultados em um arquivo PNG na pasta 'graficos'.
        """
        path = f"graficos/mineracao_concorrente.png"

        os.makedirs('graficos', exist_ok=True)
        plt.tight_layout()
        plt.savefig(path)
        print(f"\nResultado salvo em: {path}")
