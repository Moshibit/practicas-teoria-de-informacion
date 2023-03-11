""" Codififador Huffman """
# Implementar el codificador y decodificador Huffman y Shannon-Fano donde cada 
# símbolo a codificar desde un archivo en binario es de 16 bits,

# Implementar codificador y decodificador Lempel-Ziv con símbolos de longitud
# fija de 16 bits.

# from collections.OrderedDict
# TODO: importar arbol binario y lista o diccionario ordenado
# from collections import OrderedDict
# TODO importar parser
# TODO medir mis tiempos
import heapq
import argparse
import time

from queue import PriorityQueue


#from estructuras import *


# TODO: pasar a clase con metodos estaticos

def snf():
    """ pass """
    pass


def huff():
    """ pass """
    pass


def lpz():
    """ pass """
    pass


def encode():
    """ pass """
    pass


def decode():
    """ pass """
    pass


def read_input(file_name: str) -> dict:
    """ Lee el archivo, cada 8 bits """

    counter = {}
    total = 0
    keeper = None
    symbol = None
    with open(file_name, "rb") as file:
        for item in file.read():
            total += 1
            if total % 2 != 0:
                keeper = hex(item)
                continue
            symbol = keeper + "\\" + hex(item)
            try:
                counter[symbol] += 1
            except KeyError:
                counter[symbol] = 0
                counter[symbol] += 1

            # # DEBUG: --------------------------------------------------------
            # if total <= 2:  # <- el primero
            #     print("el primer simbolo es: ", symbol)
            # # ---------------------------------------------------------------

    if total % 2 != 0:
        symbol = keeper + "\\" + hex(0)
        try:
            counter[symbol] += 1
        except KeyError:
            counter[symbol] = 0
            counter[symbol] += 1

    # # DEBUG: ----------------------------------------------------------------
    # print("el último síbolo es: ", symbol)  # <- el último
    # print("DICT:")
    # for k, v in counter.items():
    #     print(k, ":", v)
    # # -----------------------------------------------------------------------

    prob = {key: value / total for key, value in counter.items()}
    return prob

def arguments_parser():
    """Resive el nombre del archivo a comprimir como argumento desde la línea 
    de mandos.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str, default=None, help="Nombre del archivo a comprimir.")
    args = parser.parse_args()
    return args


def main():
    """ fucnón main"""
    print("Processing...")

    # *** Tiempo de inicio
    start_time = time.time()

    # *** Entrada:
    # TODO: este es un archivo fijo, elimina la primera línea y descomenta la segunda y tercera.
    input_file = r"test3.bin" # input_file = r"practica2_input.jpg"
    # args = arguments_parser()
    # input_file = str(args.file_name)

    input_ = read_input(input_file)
    input_ = dict(sorted(input_.items(), key=lambda word: word[1], reverse=True))


    # # DEBUG: ----------------------------------------------------------------
    # print("PROBABILIDAD:")
    # for key, value in input_.items():
    #     print(key, ":", value)
    # print(len(input_))
    # # -----------------------------------------------------------------------

    # first = True
    # pq = PriorityQueue(len(input_))
    # for k, v in input_.items():
    #     if first:
    #         #pq.put( LinkedBinaryTree.root() )
    #         first = False
    #     else:


    # while not pq.empty():
    #     print(pq.get())

    # *** Cálculo de tiempo de ejecución:
    end_time = time.time()
    elapsed_time = (end_time - start_time)# * (10**3)
    print(f"TIempo de ejecución: {elapsed_time:.4f}s.")
    
    print("Done.")


if __name__ == "__main__":
    main()
