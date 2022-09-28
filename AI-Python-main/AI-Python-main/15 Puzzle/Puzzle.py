#! /usr/bin/env python3
import sys
import argparse
from Class import Tabuleiro
from Functions import bfs, dfs, astar, guloso, hamming, manhattan

def main():
    
    #Argumentos não estão funcionais ainda
    parser = argparse.ArgumentParser(description='Este é um solucionador de 15 quebra-cabeças.')
    parser.add_argument('--dfs', type=int,
                        help='Execute a pesquisa em profundidade (forneça um número inteiro positivo, profundidade máxima para pesquisar)')
    parser.add_argument('--bfs', action='store_true',
                        help='Executar pesquisa em largura')
    parser.add_argument('--astar', '--a', type=int, choices=[1, 2],
                        help='Execute a pesquisa A* (1 - hamming; 2 - manhattan)')
    parser.add_argument('--greedy', '--gulosa', type=int, choices=[1, 2],
                        help='Executar busca gananciosa (1 -hamming; 2 -manhattan)')
    
    parser.add_argument('--input', '-i', help='Especificar um arquivo de entrada para testes')
    args = parser.parse_args()

    # Ler tabuleiros
    if args.input is None:
        estadoInicial = input("Estado Inicial:\n").split()
        estadoObjetivo = input("Estado Objetivo:\n").split()
    else:
        try:
            numeros = []
            with open(args.input, "r") as f:
                linhas = f.readlines()
                for linha in linhas:
                    numeros = numeros + linha.split()
            estadoInicial = numeros[:16]
            numeros = numeros[16:]
            estadoObjetivo = numeros[:16]
        except FileNotFoundError:
            sys.stderr.write("Caminho de arquivo inválido")
            sys.exit(1)

    # iniciar tabuleiros
    estadoInicial = Tabuleiro(estadoInicial)
    estadoObjetivo = Tabuleiro(estadoObjetivo)
    print('Estado Inicial:')
    print(estadoInicial)
    print('Estado Objetivo:')
    print(estadoObjetivo)

    if estadoInicial == estadoObjetivo:
        print("Ambos são iguais. Já resolvido!")
        sys.exit(0)

    if estadoInicial.solvabilidade() ^ estadoObjetivo.solvabilidade():
        print('Configuração Inválida')
        sys.exit(1)

    if args.astar is None and not args.bfs and args.dfs is None and args.greedy is None:
        
        #Busca em Largura
        print("Pesquisa em largura:")
        movimento, nodes = bfs(estadoInicial, estadoObjetivo)
        print(nodes, "nós usados")
        if movimento:
            print("Caminho para o objetivo:")
            print(" -> ".join(movimento))
        else:
            print("Nenhuma solução encontrada.")
        print("\n")

        #Busca em Profundidade
        print("Pesquisa em profundidade:")
        movimento, nodes= dfs(estadoInicial, estadoObjetivo, 12)
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
        movimento, nodes = astar(estadoInicial, estadoObjetivo, comp)
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
        
        if args.greedy == 1:
            comp = hamming
        
        movimento, nodes = guloso(estadoInicial, estadoObjetivo, comp)
        
        print(nodes, "nós usados.")
        
        if movimento:
            print("Caminho para o objetivo:")
            print(" -> ".join(movimento))
        else:
            print("Nenhuma solução encontrada.")

        sys.exit(1)
    else:
        sys.stderr.write("Forneça uma entrada válida.") 
        #sys.exit(0)

    if estadoInicial == estadoObjetivo:
        print("Ambos são iguais. Já resolvido!")
        sys.exit(0)    

if __name__ == '__main__':
    main()
