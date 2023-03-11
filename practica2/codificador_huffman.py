#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" Codififador Huffman """
# Implementar el codificador y decodificador Huffman y Shannon-Fano donde cada 
# símbolo a codificar desde un archivo en binario es de 16 bits,
# a
# Implementar codificador y decodificador Lempel-Ziv con símbolos de longitud
# fija de 16 bits.



# from collections.OrderedDict
# TODO: importar arbol binario y lista o diccionario ordenado
# from collections import OrderedDict
#from estructuras import *

import argparse
import heapq
import os
import time

from queue import PriorityQueue
from common import Compression, pickle_dict

class Huffman:

    class Node:
        """clase anidada: Nodo..."""
        def __init__(self, symbol, freq):
            self.symbol = symbol
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other: object) -> bool:
            if not isinstance(other, type(self)):
               raise TypeError(f"El objeto {other} tiene que ser de tipo Node.") # 'other must be proper Position type'
            return self.freq < other.freq
        
        def __eq__(self, other: object) -> bool:
            if not isinstance(other, type(self)):
               raise TypeError(f"El objeto {other} tiene que ser de tipo Node.") # 'other must be proper Position type'
            return self.freq == other.freq
            

    def __init__(self, path: str) -> None:
        self.path = path
        self.fn , self.ext = os.path.splitext(self.path)
        self.freq = {}
        self.total_8 = 0
        self.total_16 = 0
        self.prob = PriorityQueue() # {} # var si alamccenar tuplas (v: k)
        self.heap = []
        self.code = {}
        self.reverse_map = {}
        
    def compress(self):
        """Hace la compresión"""
        self.__read_input()
        self.__heap()

    def __read_input(self):
        """Lee el archivo, cuenta las frecuencias de parejas debytes (2 hex),
        uenta cuantos bytes tiene el archivo, y cuantas parejas de bytes
        """
        holder = None
        symbol = None

        # forma el diccionario de frecuencias
        with open(self.path, "rb") as file:
            for byte_ in file.read():
                self.total_8 += 1
                if self.total_8 % 2 != 0:
                    holder = hex(byte_)
                    continue
                symbol = holder + "\\" + hex(byte_)
                if not symbol in self.freq:
                    self.freq[symbol] = 0
                self.freq[symbol] += 1
                self.total_16 += 1
                # # DEBUG: ----------------------------------------------------
                # if self.total_16 == 1:
                #     print(f"el primer simbolo es: {symbol}")
                # # DEBUG(FIN) ------------------------------------------------

        # verifica que no se omitiera un simbolo
        # le agrega paddin de ser necesario
        if self.total_8 % 2 != 0:
            symbol = holder + "\\" + hex(0)
            if not symbol in self.freq:
                self.freq[symbol] = 0
            self.freq[symbol] += 1
            self.total_16 += 1
        # # DEBUG: ------------------------------------------------------------
        # print(f"el último síbolo es: {symbol}")
        # # DEBUG(FIN) --------------------------------------------------------

    def _print_freq(self):
        """IMprime el diccionario de frecuencias, para uso de debug"""
        print("FREQ DICT:")
        for k, v in self.freq.items():
            print(k, ":", v)

    def __heap(self) -> None:
        """Forma el monticulo (heap)"""
        for key, value in self.freq.items():
            node = self.Node(key, value)
            heapq.heappush(self.heap, node)

    def _print_heap(self):
        for i in self.heap:
            print(i.symbol, ":", i.freq)

    # def __probability(self):
    #     self.prob = {key: value / self.total_16 for key, value in self.freq.items()}

    # para ordenar 
    #input_ = dict(sorted(input_.items(), key=lambda word: word[1], reverse=True))

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

    # *** Codificación del archivo
    o_huffman = Huffman(input_file)
    o_huffman.compress()

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

    # print(vars(o_huffman))
    # o_huffman._print_freq()
    o_huffman._print_heap()
    
    print("Done.")


if __name__ == "__main__":
    main()
    # v = Compression("txt", {1: 'a', 2: 'b'})
    # f = r"dd.dict"
    # pickle_dict(v, f)

    # r = unpickle_dict(f)
    # print(vars(r))
