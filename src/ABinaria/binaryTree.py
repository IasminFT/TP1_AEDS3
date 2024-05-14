import random
import string
import time

class NoArvoreBinaria:
    """Nó para uma Árvore Binária."""
    def __init__(self, chave, dado1, dado2):
        """
        Inicializa um nó da árvore binária.

        Parâmetros:
            chave (int): Chave do nó.
            dado1: Primeiro dado associado à chave.
            dado2: Segundo dado associado à chave.
        """
        self.chave = chave
        self.dado1 = dado1
        self.dado2 = dado2
        self.esquerda = None
        self.direita = None

class ArvoreBinariaBusca:
    """Árvore Binária de Busca."""
    def __init__(self):
        """Inicializa uma árvore binária de busca."""
        self.raiz = None

    def inserir(self, chave, dado1, dado2):
        """
        Insere um nó na árvore binária de busca.

        Parâmetros:
            chave (int): Chave do nó.
            dado1: Primeiro dado associado à chave.
            dado2: Segundo dado associado à chave.
        """
        novo_no = NoArvoreBinaria(chave, dado1, dado2)
        if self.raiz is None:
            self.raiz = novo_no
        else:
            atual = self.raiz
            while True:
                if chave < atual.chave:
                    if atual.esquerda is None:
                        atual.esquerda = novo_no
                        break
                    atual = atual.esquerda
                elif chave > atual.chave:
                    if atual.direita is None:
                        atual.direita = novo_no
                        break
                    atual = atual.direita

    def buscar(self, chave):
        """
        Busca por uma chave na árvore binária de busca.

        Parâmetros:
            chave (int): Chave a ser buscada.

        Retorna:
            (tuple): Tupla contendo o nó encontrado (ou None), o tempo de busca e o número de iterações.
        """
        tempo_inicio = time.time()
        atual = self.raiz
        iteracoes = 0
        while atual is not None:
            iteracoes += 1
            if chave == atual.chave:
                tempo_fim = time.time()
                return atual, tempo_fim - tempo_inicio, iteracoes
            elif chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
        tempo_fim = time.time()
        return None, tempo_fim - tempo_inicio, iteracoes

class BuscaNumerosQueExistem:
    """Classe para buscar números que existem na árvore."""
    def __init__(self, arvore, num_buscas, num_entradas):
        """
        Inicializa a busca por números que existem.

        Parâmetros:
            arvore (ArvoreBinariaBusca): Árvore binária de busca.
            num_buscas (int): Número de buscas a serem realizadas.
            num_entradas (int): Número total de chaves na árvore.
        """
        self.arvore = arvore
        self.num_buscas = num_buscas
        self.num_entradas = num_entradas

    def buscar_numeros_que_existem(self):
        """Realiza buscas por números que existem na árvore."""
        resultados = []
        for _ in range(self.num_buscas):
            chave = random.choice(range(1, self.num_entradas + 1))
            resultado, tempo, iteracoes = self.arvore.buscar(chave)
            resultados.append((chave, resultado, tempo, iteracoes))
        return resultados

class BuscaNumerosQueNaoExistem:
    """Classe para buscar números que não existem na árvore."""
    def __init__(self, arvore, num_buscas, num_entradas, tempo_limite=1):
        """
        Inicializa a busca por números que não existem.

        Parâmetros:
            arvore (ArvoreBinariaBusca): Árvore binária de busca.
            num_buscas (int): Número de buscas a serem realizadas.
            num_entradas (int): Número total de chaves na árvore.
            tempo_limite (float): Tempo máximo permitido para busca por cada chave.
        """
        self.arvore = arvore
        self.num_buscas = num_buscas
        self.num_entradas = num_entradas
        self.tempo_limite = tempo_limite

    def buscar_numeros_que_nao_existem(self):
        """Realiza buscas por números que não existem na árvore."""
        numeros_unicos = set(range(1, self.num_entradas + 1))
        numeros_nao_encontrados = []

        for _ in range(self.num_buscas):
            tempo_inicio = time.time()
            while True:
                num_aleatorio = random.randint(1, self.num_entradas * 2)
                if num_aleatorio not in numeros_unicos:
                    resultado, tempo, iteracoes = self.arvore.buscar(num_aleatorio)
                    if tempo > self.tempo_limite:
                        numeros_nao_encontrados.append((num_aleatorio, tempo, iteracoes))
                        break
            tempo_fim = time.time()
            if tempo_fim - tempo_inicio > self.tempo_limite:
                break

        return numeros_nao_encontrados

def gerar_dados(num_entradas, ordenado=False, intervalo_dado1=(1, 100)):
    """
    Gera dados para preencher a árvore binária de busca.

    Parâmetros:
        num_entradas (int): Número de chaves a serem geradas.
        ordenado (bool): Indica se as chaves devem ser geradas ordenadamente.
        intervalo_dado1 (tuple): Intervalo de valores para o primeiro dado.

    Retorna:
        list: Lista de tuplas contendo as chaves e os dados gerados.
    """
    dados = []
    chaves = list(range(1, num_entradas + 1))
    if not ordenado:
        random.shuffle(chaves)

    for chave in chaves:
        dado1 = random.randint(intervalo_dado1[0], intervalo_dado1[1])
        dado2 = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        dados.append((chave, dado1, dado2))
    return dados

def criar_arquivo_de_dados(dados, nome_arquivo):
    """
    Cria um arquivo de dados com os dados fornecidos.

    Parâmetros:
        dados (list): Lista de tuplas contendo os dados a serem escritos no arquivo.
        nome_arquivo (str): Nome do arquivo a ser criado.
    """
    with open(nome_arquivo, 'w') as arquivo:
        for entrada in dados:
            arquivo.write(f"{entrada[0]} {entrada[1]} {entrada[2]}\n")

def main():
    print("#########################################################")
    num_entradas = int(input("Número de chaves: "))
    quantidade_buscas = int(input("Quantidade chaves aleatórias a buscar: "))
    opcao_ordenado = input("Com ordenação(S) Sem ordenação(N): ").strip().lower()
    print("#########################################################")
    dados_ordenados = opcao_ordenado == 's'
    dados = gerar_dados(num_entradas, ordenado=dados_ordenados)
    criar_arquivo_de_dados(dados, 'dados.txt')

    arvore = ArvoreBinariaBusca()
    for entrada in dados:
        arvore.inserir(*entrada)

    busca_existente = BuscaNumerosQueExistem(arvore, quantidade_buscas, num_entradas)
    resultados_existente = busca_existente.buscar_numeros_que_existem()

    print("Busca pelos números que existem:")
    for chave, resultado, tempo, iteracoes in resultados_existente:
        if resultado:
            print(f"Chave: {chave}, encontrada, Tempo médio de pesquisa: {tempo:.6f} segundos, Iterações: {iteracoes}")
        else:
            print(f"Chave: {chave}, não encontrada, Tempo médio de pesquisa: {tempo:.6f} segundos, Iterações: {iteracoes}")

    input("Pressione Enter para continuar e buscar números que não existem...")
    print()
    
    busca_nao_existente = BuscaNumerosQueNaoExistem(arvore, quantidade_buscas, num_entradas)
    resultados_nao_existente = busca_nao_existente.buscar_numeros_que_nao_existem()

    print("\nBusca pelos números que não existem:")
    for chave, tempo, iteracoes in resultados_nao_existente:
        print(f"Chave: {chave}, não encontrada, Tempo médio de pesquisa: {tempo:.6f} segundos, Iterações: {iteracoes}")

    tempo_total_existente = sum(tempo for _, _, tempo, _ in resultados_existente)
    tempo_total_nao_existente = sum(tempo for _, tempo, _ in resultados_nao_existente)

    print()
    print(f"Tempo de busca números existentes: {tempo_total_existente:.6f} segundos")
    print(f"Tempo de busca números não existentes: {tempo_total_nao_existente:.6f} segundos")

if __name__ == "__main__":
    main()
    