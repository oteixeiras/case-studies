"""
    Author: Bruna Carlette e Fernando de Souza Teixeira
    reference: class_base_code.py
"""
import hashlib
import time
import threading

from utils import Utils

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self, nonce:int | None =None )-> str:
        nonce = self.nonce if nonce is None else nonce
        value = f"{self.index}{self.previous_hash}{self.timestamp}{self.data}{nonce}"
        return hashlib.sha256(value.encode()).hexdigest()

def concurrent_mining(num_threads: int, difficulty: int)-> float:
    """Executa mineração concorrente com múltiplas threads competindo para encontrar um nonce válido.
    
    Parâmetros:
        num_threads (int): Número de threads para paralelizar a mineração
        difficulty (int): Dificuldade do algoritmo Proof-of-Work (número de zeros iniciais requeridos)
    
    Funcionamento:
        1. Cria uma instância de bloco inicial para minerar
        2. Usa um Event para coordenar a parada imediata de todas as threads quando uma encontrar a solução
        3. Cada thread opera em uma cópia independente do bloco para evitar condições de corrida
    """

    bloco = Block(1, "0", time.time(), "Bloco de Mineração Concorrente")
    stop_event = threading.Event()
    nonce_encontrado = {'valor': None}
    lock = threading.Lock()

    def minerar(thread_id: int)-> None:
        """
        Função executada por cada thread para encontrar um nonce válido para o bloco.

        Cada thread começa a busca pelo nonce a partir de um valor inicial único (thread_id),
        incrementando de acordo com o número total de threads para evitar sobreposição.
        Quando encontrar um hash que começa com o prefixo requerido (dificuldade), atualiza
        o nonce encontrado e sinaliza para todas as outras threads pararem.
        Apenas a primeira thread que encontra o nonce válido registra o resultado.

        Parâmetros:
            thread_id (int): Identificador da thread, usado como valor inicial do nonce.

        Notas:
            - Utiliza um mecanismo de lock para evitar condições de corrida ao atualizar o nonce.
            - Usa um evento (stop_event) para coordenar a parada imediata de todas as threads.
        """
        nonce = thread_id
        prefixo = '0' * difficulty
        while not stop_event.is_set():
            hash_candidato = bloco.calculate_hash(nonce)
            if hash_candidato.startswith(prefixo):
                with lock:
                    if nonce_encontrado['valor'] is None:
                        nonce_encontrado['valor'] = nonce
                        stop_event.set()
                return
            nonce += num_threads

    threads = []
    inicio = time.time()
    
    for identifier in range(num_threads):
        thread = threading.Thread(target=minerar, args=(identifier,))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()
    
    if nonce_encontrado['valor'] is not None:
        bloco.nonce = nonce_encontrado['valor']
        bloco.hash = bloco.calculate_hash()
        print(f"Nonce encontrado: {bloco.nonce}, Hash: {bloco.hash}")
    
    duracao = time.time() - inicio
    print(f"Threads: {num_threads} | Tempo: {duracao:.2f}s\n")
    return duracao


# Coleta de dados para gráfico
if __name__ == "__main__":
    count_threads_list = [1, 2, 4, 8] # Número de threads para testar
    tempos = [] # Lista para armazenar os tempos de mineração
    
    for threads in count_threads_list:
        tempo = concurrent_mining(num_threads=threads, difficulty=4)
        tempos.append(tempo)
    
    Utils.plot_results(threads=count_threads_list, times=tempos)