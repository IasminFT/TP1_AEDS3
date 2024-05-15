import random
import string
import time

class NoArvoreBinaria: #cada nó possui uma chave e dois dados associados
    def __init__(self, chave, dado1, dado2):
        self.chave = chave
        self.dado1 = dado1
        self.dado2 = dado2
        self.esquerda = None
        self.direita = None

class ArvoreBinariaBusca:
    def __init__(self):
        self.raiz = None

    #inserir novo nó na árvore
    def inserir(self, chave, dado1, dado2):
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
    
    #procurar opor uma chave
    def buscar(self, chave):
        tempo_inicio = time.time()
        atual = self.raiz
        interacoes = 0
        while atual is not None:
            interacoes += 1
            if chave == atual.chave:
                tempo_fim = time.time()
                return atual, tempo_fim - tempo_inicio, interacoes
            elif chave < atual.chave:
                atual = atual.esquerda
            else:
                atual = atual.direita
        tempo_fim = time.time()
        return None, tempo_fim - tempo_inicio, interacoes

#Busca números que existem na árvore
class BuscaNumerosQueExistem:
    #recebe como entrada a árvore, os dados da árvore, o número de buscas a serem realizadas e o número total de entradas na árvore
    def __init__(self, arvore, num_buscas, num_entradas):
        self.arvore = arvore
        self.num_buscas = num_buscas
        self.num_entradas = num_entradas

    #gerador de chaves aleatórias, busca cada uma delas na árvore
    def buscar_numeros_que_existem(self):
        resultados = []
        for _ in range(self.num_buscas):
            chave = random.choice(range(1, self.num_entradas + 1))
            resultado, tempo, interacoes = self.arvore.buscar(chave)
            resultados.append((chave, resultado, tempo, interacoes))
        return resultados

#Busca números que não existem na árvore
class BuscaNumerosQueNaoExistem:
    #recebe como entrada a árvore, os dados da árvore, o número de buscas a serem realizadas e o número total de entradas na árvore
    def __init__(self, arvore, dados, num_buscas, num_entradas):
        self.arvore = arvore
        self.dados = dados
        self.num_buscas = num_buscas
        self.num_entradas = num_entradas

    #gerador de chaves aleatórias que não existem na árvore, busca cada uma delas
    def buscar_numeros_que_nao_existem(self):
        numeros_unicos = set(entry[0] for entry in self.dados)
        numeros_nao_encontrados = []

        while len(numeros_nao_encontrados) < self.num_buscas:
            num_aleatorio = random.randint(1, self.num_entradas * 2)
            if num_aleatorio not in numeros_unicos:
                resultado, tempo, interacoes = self.arvore.buscar(num_aleatorio)
                if not resultado:
                    numeros_nao_encontrados.append((num_aleatorio, tempo, interacoes))
        return numeros_nao_encontrados

#gerar dados aleatórios para preencher a árvore
def gerar_dados(num_entradas, ordenado=False):
    dados = []
    chaves = list(range(1, num_entradas + 1))
    if not ordenado:
        random.shuffle(chaves)

    for chave in chaves:
        dado1 = random.randint(1, 100)
        dado2 = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        dados.append((chave, dado1, dado2))
    return dados

#cria arquivo de dados
def criar_arquivo_de_dados(dados, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        for entrada in dados:
            arquivo.write(f"{entrada[0]} {entrada[1]} {entrada[2]}\n")

def main():
    #solicitar informações do usuário
    num_entradas = int(input("Número de chaves no arquivo: "))
    quantidade_buscas = int(input("Quantidade de chaves aleatórias a buscar: "))
    opcao_ordenado = input("Chaves ordenadas? (S/N): ").strip().lower()
    dados_ordenados = opcao_ordenado == 's'
    #gera dados aleatórios
    dados = gerar_dados(num_entradas, ordenado=dados_ordenados)
    criar_arquivo_de_dados(dados, 'dados.txt')

    #cria árvore
    arvore = ArvoreBinariaBusca()
    for entrada in dados:
        arvore.inserir(*entrada)

    #realiza busca por números que existem
    busca_existente = BuscaNumerosQueExistem(arvore, quantidade_buscas, num_entradas)
    resultados_existente = busca_existente.buscar_numeros_que_existem()

    #imprime os resultados das buscas por números que existem
    print("Busca pelos números que existem:")
    for chave, resultado, tempo, interacoes in resultados_existente:
        if resultado:
            print(f"Chave: {chave}, encontrada, Tempo médio de pesquisa: {tempo:.6f} segundos, Interacoes: {interacoes}")
        else:
            print(f"Chave: {chave}, não encontrada, Tempo médio de pesquisa: {tempo:.6f} segundos, Interacoes: {interacoes}")

    input("Pressione Enter para continuar e buscar números que não existem...")
    print()

     #realiza busca por números que não existem
    busca_nao_existente = BuscaNumerosQueNaoExistem(arvore, dados, quantidade_buscas, num_entradas)
    resultados_nao_existente = busca_nao_existente.buscar_numeros_que_nao_existem()

    #imprime os resultados das buscas por números que não existem na árvore
    print("\nBusca pelos números que não existem:")
    for chave, tempo, interacoes in resultados_nao_existente:
        print(f"Chave: {chave}, não encontrada, Tempo médio de pesquisa: {tempo:.6f} segundos, Interacoes: {interacoes}")

    #calcula e imprime o tempo total das buscas e o número total de interações realizadas
    tempo_total_existente = sum(tempo for _, _, tempo, _ in resultados_existente)
    tempo_total_nao_existente = sum(tempo for _, tempo, _ in resultados_nao_existente)

    interacoes_total_existente = sum(interacoes for _, _, _, interacoes in resultados_existente)
    interacoes_total_nao_existente = sum(interacoes for _, _, interacoes in resultados_nao_existente)

    print()
    print(f"Tempo total das buscas pelos números que existem: {tempo_total_existente:.6f} segundos")
    print(f"Tempo total das buscas pelos números que não existem: {tempo_total_nao_existente:.6f} segundos")
    print(f"Número total de interações nas buscas pelos números que existem: {interacoes_total_existente}")
    print(f"Número total de interações nas buscas pelos números que não existem: {interacoes_total_nao_existente}")

if __name__ == "__main__":
    main()