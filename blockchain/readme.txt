
Author: Bruna Carlette e Fernando de Souza Teixeira

Guia de Execução do Projeto

1. Criar e ativar o ambiente virtual
    ➜ python -m venv venv 
    ➜ source venv/bin/activate

    Obs: Se estiver usando Windows:
        ➜ venv\Scripts\activate no CMD

2. Instalar as dependências
    ➜ pip install matplotlib

3. Rodar o projeto
    ➜ python main.py

4. Exemplo de saida
    ➜  python main.py
    Nonce encontrado: 67572, Hash: 0000d20d7d8bea17f1d9c721c3789cfa30af8c63ef0bd71174a23ea87d8717e7
    Threads: 1 | Tempo: 0.15s

    Nonce encontrado: 11614, Hash: 0000113cfe344f53b168b2606d9fef8468ab45ab0fc1cd9b4c5e714c7f78cd8b
    Threads: 2 | Tempo: 0.03s

    Nonce encontrado: 54564, Hash: 0000cd5d85fcfe4769b2cd247c3f5e0428a6869d3a2f31a7288278d431f2bbff
    Threads: 4 | Tempo: 0.05s

    Nonce encontrado: 230886, Hash: 00006aec667d71771430b4831c2c02bdae5bf72638d73541661f50824ac024e5
    Threads: 8 | Tempo: 0.26s

    Resultado salvo em: resultados/mineracao_concorrente.png

