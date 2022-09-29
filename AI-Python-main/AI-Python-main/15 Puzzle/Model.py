import copy


class Tabuleiro:
    def __init__(no, arg, pai=None, profundidade=0):
        no.estado = arg
        no._findx()
        no.filhos = []
        no.retroceder = pai
        no.profundidade = profundidade


    def __hash__(no):
        return hash(''.join(no.estado))

    def __copy__(no):
        return Tabuleiro(no.estado)

    def __str__(no):
        text = """┌──┬──┬──┬──┐
│{}│{}│{}│{}│
├──┼──┼──┼──┤
│{}│{}│{}│{}│
├──┼──┼──┼──┤
│{}│{}│{}│{}│
├──┼──┼──┼──┤
│{}│{}│{}│{}│
└──┴──┴──┴──┘""" \
            .format(no.estado[0].rjust(2, '0'), no.estado[1].rjust(2, '0'), no.estado[2].rjust(2, '0'),
                    no.estado[3].rjust(2, '0'),
                    no.estado[4].rjust(2, '0'), no.estado[5].rjust(2, '0'), no.estado[6].rjust(2, '0'),
                    no.estado[7].rjust(2, '0'),
                    no.estado[8].rjust(2, '0'), no.estado[9].rjust(2, '0'), no.estado[10].rjust(2, '0'),
                    no.estado[11].rjust(2, '0'),
                    no.estado[12].rjust(2, '0'), no.estado[13].rjust(2, '0'), no.estado[14].rjust(2, '0'),
                    no.estado[15].rjust(2, '0')).replace("00", "  ")
        return text

    def __repr__(no):
        return str(no.estado)

    def __eq__(no, other):
        return no.estado == other

    def _findx(no):
        i = 0
        while no.estado[i] != '0':
            i += 1
        no.x, no.y = (int(i / 4), i % 4)

    def solvabilidade(no):
        # Par:1 ; Impar:0
        soma = 0
        for i in range(0, 16):
            for j in range(i + 1, 16):
                if no.estado[i] > no.estado[j] and no.estado[i] != '0' and no.estado[j] != '0':
                    soma += 1
        for i in range(0, 16):
            if no.estado[i] == '0':
                a = int(i / 4) % 2 == 0
                b = not (soma % 2 == 0)
                no.solvable = (a == b)
                return no.solvable

    def getX(no):
        return no.x, no.y

    # Definicao dos movimentos
    def _left(no):
        movimento = copy.deepcopy(no.estado)
        caminho = copy.deepcopy(no.retroceder)
        if caminho is None:
            caminho = ['Esquerda']
        else:
            caminho.append('Esquerda')
        if no.y != 0:
            movimento[no.x * 4 + no.y] = movimento[no.x * 4 + no.y - 1]
            movimento[no.x * 4 + no.y - 1] = '0'
            tleft = Tabuleiro(movimento, pai=caminho, profundidade=no.profundidade + 1)
            no.filhos.append(tleft)

    def _right(no):
        movimento = copy.deepcopy(no.estado)
        caminho = copy.deepcopy(no.retroceder)
        if caminho is None:
            caminho = ['Direita']
        else:
            caminho.append('Direita')
        if no.y != 3:
            movimento[no.x * 4 + no.y] = movimento[no.x * 4 + no.y + 1]
            movimento[no.x * 4 + no.y + 1] = '0'
            tright = Tabuleiro(movimento, pai=caminho, profundidade=no.profundidade + 1)
            no.filhos.append(tright)

    def _up(no):
        movimento = copy.deepcopy(no.estado)
        caminho = copy.deepcopy(no.retroceder)
        if caminho is None:
            caminho = ['Acima']
        else:
            caminho.append('Acima')
        if no.x != 0:
            movimento[no.x * 4 + no.y] = movimento[(no.x - 1) * 4 + no.y]
            movimento[(no.x - 1) * 4 + no.y] = '0'
            tup = Tabuleiro(movimento, pai=caminho, profundidade=no.profundidade + 1)
            no.filhos.append(tup)

    def _down(no):
        movimento = copy.deepcopy(no.estado)
        caminho = copy.deepcopy(no.retroceder)
        if caminho is None:
            caminho = ['Baixo']
        else:
            caminho.append('Baixo')
        if no.x != 3:
            movimento[no.x * 4 + no.y] = movimento[(no.x + 1) * 4 + no.y]
            movimento[(no.x + 1) * 4 + no.y] = '0'
            tdown = Tabuleiro(movimento, pai=caminho, profundidade=no.profundidade + 1)
            no.filhos.append(tdown)

    def movimentos(no):
        if no.profundidade > 1:
            last = no.retroceder[no.profundidade-1]
        else:
            last = "0"
        if last != "Direita":
            no._left()
        if last != "Esquerda":
            no._right()
        if last != "Baixo":
            no._up()
        if last != "Acima":
            no._down()
        return no.filhos
