import random
import string
import time

class No:
    def __init__(self, chave, dado1, dado2):
        self.chave = chave
        self.dado1 = dado1
        self.dado2 = dado2
        self.proximo = None

class ArvoreSequencial:
    def __init__(self):
        self.raiz = None

    def inserir(self, chave, dado1, dado2):
        novo_no = No(chave, dado1, dado2)
        if not self.raiz:
            self.raiz = novo_no
        else:
            atual = self.raiz
            while atual.proximo:
                atual = atual.proximo
            atual.proximo = novo_no

    def buscar(self, chave):
        atual = self.raiz
        tempo_inicial = time.time()
        while atual:
            if atual.chave == chave:
                tempo_final = time.time()
                return atual, tempo_final - tempo_inicial
            atual = atual.proximo
        tempo_final = time.time()
        return None, tempo_final - tempo_inicial

class BuscaNumerosQueExistemSequencial:
    def __init__(self, arvore, num_buscas, num_registros):
        self.arvore = arvore
        self.num_buscas = num_buscas
        self.num_registros = num_registros

    def buscar_numeros_que_existem(self):
        resultados = []
        for _ in range(self.num_buscas):
            chave = random.choice(range(1, self.num_registros + 1))
            resultado, tempo = self.arvore.buscar(chave)
            resultados.append((chave, resultado, tempo))
        return resultados

class BuscaNumerosQueNaoExistemSequencial:
    def __init__(self, arvore, dados, num_buscas, num_registros):
        self.arvore = arvore
        self.dados = dados
        self.num_buscas = num_buscas
        self.num_registros = num_registros

    def buscar_numeros_que_nao_existem(self):
        numeros_unicos = set(entry[0] for entry in self.dados)
        numeros_nao_encontrados = []

        while len(numeros_nao_encontrados) < self.num_buscas:
            num_aleatorio = random.randint(1, self.num_registros * 2)  # Use um limite maior
            if num_aleatorio not in numeros_unicos:
                resultado, tempo = self.arvore.buscar(num_aleatorio)
                if not resultado:
                    numeros_nao_encontrados.append((num_aleatorio, tempo))
        return numeros_nao_encontrados

def gerar_dados_sequencial(num_registros, ordenados=False):
    dados = []
    for i in range(num_registros):
        chave = i + 1 if ordenados else random.randint(1, num_registros)
        dado1 = random.randint(1, 100)
        dado2 = ''.join(random.choice(string.ascii_letters) for _ in range(100))  # Usando 100 letras em vez de 10000
        dados.append((chave, dado1, dado2))
    return dados

def criar_arquivo_de_dados_sequencial(dados, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for entrada in dados:
            arquivo.write(f"{entrada[0]} {entrada[1]} {entrada[2]}\n")

def main_sequencial():
    print("#########################################################")
    num_registros = int(input("Número de chaves: "))
    num_buscas = int(input("Quantidade de chaves aleatórias a buscar: "))
    ordenados_opcao = input("Com ordenação(S) Sem ordenação(N): ").strip().lower()
    print("#########################################################")
    dados_ordenados = ordenados_opcao == 's'
    dados = gerar_dados_sequencial(num_registros, ordenados=dados_ordenados)
    criar_arquivo_de_dados_sequencial(dados, 'dados_sequencial.txt')

    arvore = ArvoreSequencial()
    for entrada in dados:
        arvore.inserir(*entrada)

    busca_existente = BuscaNumerosQueExistemSequencial(arvore, num_buscas, num_registros)
    resultados_existente = busca_existente.buscar_numeros_que_existem()

    print("Busca pelos números que existem:")
    for chave, resultado, tempo in resultados_existente:
        if resultado:
            print(f"Chave: {chave}, encontrada, Tempo de pesquisa: {tempo:.6f} segundos")
        else:
            print(f"Chave: {chave}, não encontrada, Tempo de pesquisa: {tempo:.6f} segundos")

    input("Pressione Enter para continuar e buscar números que não existem...")
    print()

    busca_nao_existente = BuscaNumerosQueNaoExistemSequencial(arvore, dados, num_buscas, num_registros)
    resultados_nao_existente = busca_nao_existente.buscar_numeros_que_nao_existem()

    print("\nBusca pelos números que não existem:")
    for chave, tempo in resultados_nao_existente:
        print(f"Chave: {chave}, não encontrada, Tempo de pesquisa: {tempo:.6f} segundos")

    tempo_total_existente = sum(tempo for _, _, tempo in resultados_existente)
    tempo_total_nao_existente = sum(tempo for _, tempo in resultados_nao_existente)

    print()
    print(f"Tempo de busca números existentes: {tempo_total_existente:.6f} segundos")
    print(f"Tempo de busca números não existentes: {tempo_total_nao_existente:.6f} segundos")

if __name__ == "__main__":
    main_sequencial()
