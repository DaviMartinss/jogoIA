from collections import deque

class MinHeap:
    def __init__(no, estadoObjetivo, compare):
        no.informacao = [None]
        no.size = 0
        no.comparator = compare
        no.estadoObjetivo = estadoObjetivo

    def __len__(no):
        return no.size

    def __contains__(no, item):
        return item in no.informacao

    def __str__(no):
        return str(no.informacao)

    def _compare(no, x, y):
        x = no.comparator(no.informacao[x], no.estadoObjetivo)
        y = no.comparator(no.informacao[y], no.estadoObjetivo)

        if x < y:
            return True
        else:
            return False

    def getpos(no, x):
        for i in range(no.size+1):
            if x == no.informacao[i]:
                return i
        return None

    def _upHeap(no, i):
        while i > 1 and no._compare(i, int(i/2)):
            no._swap(i, int(i/2))
            i = int(i/2)

    def _downHeap(no, i):
        size = no.size
        while 2*i <= size:
            j = 2*i
            if j < size and no._compare(j+1, j):
                j += 1
            if no._compare(i, j):
                break
            no._swap(i, j)
            i = j

    def _swap(no, i, j):
        t = no.informacao[i]
        no.informacao[i] = no.informacao[j]
        no.informacao[j] = t

    def push(no, x):
        no.size += 1
        no.informacao.append(x)
        no._upHeap(no.size)

    def pop(no):
        if no.size < 1:
            return None
        t = no.informacao[1]
        no.informacao[1] = no.informacao[no.size]
        no.informacao[no.size] = t
        no.size -= 1
        no._downHeap(1)
        no.informacao.pop()
        return t

    def peek(no):
        if no.size < 1:
            return None
        return no.informacao[1]


# comparadores
def hamming(estadoInicial, estadoObjetivo):
    inicial = estadoInicial.estado
    objetivo = estadoObjetivo.estado
    profundidade = estadoInicial.profundidade
    soma = 0
    for x, y in zip(objetivo, inicial):
        if x != y and x != '0':
            soma += 1
    return soma + profundidade

def manhattan(estadoInicial, estadoObjetivo):
    inicial = estadoInicial.estado
    objetivo = estadoObjetivo.estado
    profundidade = estadoInicial.profundidade
    soma = 0
    for i in range(16):
        if objetivo[i] == '0':
            continue
        x1, y1 = (int(i / 4), i % 4)
        for j in range(16):
            if objetivo[i] == inicial[j]:
                x2, y2 = (int(j / 4), j % 4)
                soma += abs(x1 - x2) + abs(y1 - y2)
                break
    return soma + profundidade

#Algoritmos de Pesquisa

# Busca em Largura
def bfs(estadoInicial, estadoObjetivo):
    total_nos = 1
    fronteira = deque()
    fronteira.append(estadoInicial)

    while len(fronteira) > 0:
        estado = fronteira.popleft()

        if estadoObjetivo == estado:
            return estado.retroceder, total_nos
        for filho in estado.movimentos():
            total_nos += 1
            fronteira.append(filho)
        del(estado);
    return False, total_nos

# Busca em Profundidade
def dfs(estadoInicial, estadoObjetivo, profundidade):
    total_nos = 1
    fronteira = list()
    visitados = set()
    fronteira.append(estadoInicial)

    while len(fronteira) > 0:
        estado = fronteira.pop()
        visitados.add(estado)

        if estado == estadoObjetivo:
            return estado.retroceder, total_nos

        for filho in estado.movimentos():
            total_nos += 1
            if filho.profundidade <= profundidade:
                if filho not in visitados or filho not in fronteira:
                    fronteira.append(filho)
        del(estado)
    return False, total_nos

# Busca Gulosa
def guloso(estadoInicial, estadoObjetivo, comparador):
    total_nos = 1
    estado = estadoInicial
    contador = 0
    while estado != estadoObjetivo:
        filhos = estado.movimentos()
        estado = filhos.pop()
        for x in filhos:
            total_nos += 1
            if comparador(x, estadoObjetivo) < comparador(estado, estadoObjetivo):
                estado = x
        contador = contador + 1
    return estado.retroceder, total_nos

# Busca A*
def astar(estadoInicial, estadoObjetivo, comparador):
    total_nos = 1
    fronteira = MinHeap(estadoObjetivo, comparador)
    fronteira.push(estadoInicial)
    visitados = set()

    while len(fronteira) > 0:
        estado = fronteira.pop()
        visitados.add(estado)

        if estadoObjetivo == estado:
            return estado.retroceder, total_nos

        for filho in estado.movimentos():
            total_nos += 1
            if filho not in fronteira and filho not in visitados:
                fronteira.push(filho)
            elif filho in fronteira:
                i = fronteira.getpos(filho)
                if fronteira.informacao[i].profundidade > filho.profundidade:
                    fronteira.informacao[i] = filho
                    fronteira._upHeap(i)

    return False, total_nos
