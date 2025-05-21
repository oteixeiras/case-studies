
Author: Fernando de Souza Teixeira

Guia de Execução do Projeto

1. Criar e ativar o ambiente virtual
    ➜ python -m venv venv 
    ➜ source venv/bin/activate

    Obs: Se estiver usando Windows:
        ➜ venv\Scripts\activate no CMD

2. Instalar as dependências
    ➜ pip install pandas scikit-learn matplotlib numpy

3. Rodar o projeto
    ➜ python main.py

4. Saída esperada
    ** Model Evaluation Results **

    ╔══════════════════════════════╗
    ║        Decision Tree         ║
    ╠══════════════════╦═══════════╣
    ║ R²               ║    0.3417 ║
    ║ RMSE             ║    0.4931 ║
    ╚══════════════════╩═══════════╝

    ╔══════════════════════════════╗
    ║      Linear Regression       ║
    ╠══════════════════╦═══════════╣
    ║ R²               ║    0.9447 ║
    ║ RMSE             ║    0.1429 ║
    ╚══════════════════╩═══════════╝

    Chart saved to: 'result-genered/model_comparison.png'

