import hashlib
import time
import threading

class Block:
    """Representa um bloco na blockchain, contendo metadados e mecanismo de encadeamento.
    
    Atributos:
        index (int): Número sequencial do bloco na cadeia.
        previous_hash (str): Hash do bloco anterior, garantindo encadeamento imutável.
        timestamp (float): Data/hora de criação do bloco.
        data (str): Informações armazenadas no bloco.
        nonce (int): Número usado uma única vez para prova de trabalho.
        hash (str): Hash criptográfico do conteúdo atual do bloco.
    """
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Gera o hash SHA-256 do bloco usando todos seus campos.
        
        O hash atua como impressão digital:
        - Liga o bloco ao anterior (previous_hash)
        - Torna alterações detectáveis, uma vez que usa o próprio conteudo(qualquer mudança altera o hash)
        """
        value = str(self.index) + self.previous_hash + str(self.timestamp) + self.data + str(self.nonce)
        return hashlib.sha256(value.encode()).hexdigest()
    
    # Funcao que executa a prova de trabalho (mineracao)
    def mine_block(self, difficulty, stop_event):
        """Executa o algoritmo de prova de trabalho (PoW) para validar o bloco.
        
        O processo consiste em encontrar um nonce que produza um hash com:
        - N zeros iniciais (dificuldade)
        - Custo computacional alto para gerar, mas fácil de verificar
        
        Parâmetros:
            difficulty (int): Número de zeros requeridos no início do hash
            stop_event (threading.Event): Sinal para parar todas as threads quando uma encontrar a solução
        """
        prefix = '0' * difficulty
        while not self.hash.startswith(prefix):
            if stop_event.is_set():
                return
            self.nonce += 1
            self.hash = self.calculate_hash()
        # Avisar que um bloco foi minerado
        stop_event.set()
        print(f"Bloco minerado com nonce {self.nonce}: {self.hash}")

# Blockchain basica com lista de blocos
class Blockchain:
    """Estrutura básica de blockchain com mecanismo de consenso distribuído.
    
    Funcionalidades:
        - Mantém cadeia de blocos imutável
        - Gerencia dificuldade de mineração
        - Valida novos blocos via PoW
    """
     
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty

    def create_genesis_block(self):
        """Bloco inicial especial com valores pre-definidos para iniciar a cadeia de blocos"""
        return Block(0, "0", time.time(), "Genesis Block")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def add_block(self, new_block):
        """Adiciona novo bloco à cadeia após verificação de validade.
        
        Passos:
        1. Vincula ao bloco anterior via hash
        2. Executa PoW para validar o bloco
        3. Adiciona à cadeia somente se válido
        """
        new_block.previous_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty, threading.Event())
        self.chain.append(new_block)

def concurrent_mining(num_threads, difficulty):
    latest_block = Block(1, "0", time.time(), "Concurrent Mining Block")
    stop_event = threading.Event()
    
    def mine():
        block_copy = Block(latest_block.index, latest_block.previous_hash,latest_block.timestamp, latest_block.data)
        block_copy.mine_block(difficulty, stop_event)
    
    threads = []
    start_time = time.time()
    for _ in range(num_threads):
        t = threading.Thread(target=mine)
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    elapsed_time = time.time() - start_time
    print(f"Mineracao com {num_threads} threads concluida em {elapsed_time:.2f} segundos.")
    
# Ponto de entrada principal
if __name__ == "__main__":
# Altere os parametros para testar diferentes numeros de threads
    concurrent_mining(num_threads=4, difficulty=4)