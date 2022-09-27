#! /usr/bin/env python3
import sys
import argparse
from Class import Tabuleiro
from Functions import bfs, dfs, astar, guloso, hamming, manhattan

def main():
    
    parser = argparse.ArgumentParser(description='Este é um solucionador de 15 quebra-cabeças.')
    parser.add_argument('--dfs', type=int,
                        help='Execute a pesquisa em profundidade (forneça um número inteiro positivo, profundidade máxima para pesquisar)')
    parser.add_argument('--bfs', action='store_true',
                        help='Executar pesquisa em largura')
    parser.add_argument('--astar', '--a', type=int, choices=[1, 2],
                        help='Execute a pesquisa A* (1 - hamming; 2 - manhattan)')
    parser.add_argument('--greedy', '--gulosa', type=int, choices=[1, 2],
                        help='Executar busca gananciosa (1 -hamming; 2 -manhattan)')

    parser.add_argument('--input', '-i', help='Specify an input file for tests')
    args = parser.parse_args()

    # Ler tabuleiros
    if args.input is None:
        inicialState = input("Estado Inicial:\n").split()
        goalState = input("Estado Objetivo:\n").split()
    else:
        try:
            numbers = []
            with open(args.input, "r") as f:
                lines = f.readlines()
                for line in lines:
                    numbers = numbers + line.split()
            inicialState = numbers[:16]
            numbers = numbers[16:]
            goalState = numbers[:16]
        except FileNotFoundError:
            sys.stderr.write("Caminho de arquivo inválido")
            sys.exit(1)

    # iniciar tabuleiros
    inicialState = Tabuleiro(inicialState)
    goalState = Tabuleiro(goalState)
    print('Estado Inicial:')
    print(inicialState)
    print('Estado Objetivo:')
    print(goalState)

    if inicialState == goalState:
        print("Ambos são iguais. Já resolvido!")
        sys.exit(0)

    if inicialState.solvabilidade() ^ goalState.solvabilidade():
        print('Configuração Inválida')
        sys.exit(1)

    if args.astar is None and not args.bfs and args.dfs is None and args.greedy is None:
        sys.stderr.write("Forneça uma entrada válida.")

        #Busca em Largura
        print("Pesquisa em largura:")
        movimento, nodes = bfs(inicialState, goalState)
        print(nodes, "nós usados")
        if movimento:
            print("Caminho para o objetivo:")
            print(" -> ".join(movimento))
        else:
            print("Nenhuma solução encontrada.")
        print("\n")

        #Busca em Profundidade
        print("Pesquisa em profundidade:")
        movimento, nodes= dfs(inicialState, goalState, 12)
        print(nodes, "nós usados")
        if movimento:
            print("Caminho para o objetivo:")
            print(" -> ".join(movimento))
        else:
            print("Nenhuma solução encontrada.")
        print("\n")

        #Busca A*
        print("Busca A*:")
        comp = manhattan
        if args.astar == 1:
            comp = hamming
        movimento, nodes = astar(inicialState, goalState, comp)
        print(nodes, "nós usados.")
        if movimento:
            print("Caminho para o objetivo:")
            print(" -> ".join(movimento))
        else:
            print("Nenhuma solução encontrada.")
        print("\n")

        #Busca Gulosa
        print("Busca Gulosa:")
        comp = manhattan
        print("\nkedia1\n")
        if args.greedy == 1:
            comp = hamming
        print("\nkedia2\n")
        movimento, nodes = guloso(inicialState, goalState, comp)
        print("\nkedia72\n")
        print(nodes, "nós usados.")
        if movimento:
            print("Caminho para o objetivo:")
            print(" -> ".join(movimento))
        else:
            print("Nenhuma solução encontrada.")

        sys.exit(1)

    if inicialState == goalState:
        print("Ambos são iguais. Já resolvido!")
        sys.exit(0)    

if __name__ == '__main__':
    main()
