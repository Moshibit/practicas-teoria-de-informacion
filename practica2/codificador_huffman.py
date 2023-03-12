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
            if not isinstance(other, Huffman.Node):
               raise TypeError(f"El objeto other tiene que ser de tipo Node.") # 'other must be proper Position type'
            return self.freq < other.freq
        
        def __eq__(self, other: object) -> bool:
            if other == None:
                return False
            if not isinstance(other, Huffman.Node):
               raise TypeError(f"El objeto other tiene que ser de tipo Node.") # 'other must be proper Position type'
            return self.freq == other.freq
            

    def __init__(self, path: str) -> None:
        self.path = path
        self.file_name , self.ext = os.path.splitext(self.path)
        self.out_fn = self.file_name + ".huff"
        self.freq = {}
        self.total_8 = 0
        self.total_16 = 0
        self.prob = PriorityQueue() # {} # var si alamccenar tuplas (v: k)
        self.heap = []
        self.code = {}
        self.reverse_map = {}
        self.encoded_str = ""
        
    def compress(self):
        """Hace la compresión"""
        self.__read_input()
        self.__heap()
        self.__tree()
        self.__get_code()
        self.__encode()
        # self.__add_padding()
        # bytearray
        # self.__write_output()

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

    def __tree(self):
        while(len(self.heap) > 1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def __get_code(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.__recursive_encode(root, current_code)

    def __recursive_encode(self, root, current_code):
        if root == None:
            return
        if root.symbol != None:
            self.code[root.symbol] = current_code
            self.reverse_map[current_code] = root.symbol
            return
        self.__recursive_encode(root.left, current_code + "0")
        self.__recursive_encode(root.right, current_code + "1")

    def __encode(self):
        holder = None
        symbol = None
        counter = 0
        with open(self.path, "rb") as file, open(self.out_fn, "wb") as out_file:
            for byte_ in file.read():
                counter += 1
                if counter % 2 != 0:
                    holder = hex(byte_)
                    continue
                symbol = holder + "\\" + hex(byte_)
                self.encoded_str = self.code[symbol]
                byte_ = bytearray


    def _print_code(self):
        for k, v in self.code.items():
            print(k, ":", v)
            

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
    # input_file = r"test10.jpg"
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
    # print("-------------------------")
    # o_huffman._print_freq()
    # print("-------------------------")
    # o_huffman._print_heap()
    # print("-------------------------")
    # o_huffman._print_code()
    print(o_huffman.encoded_str)
    
    print("Done.")


if __name__ == "__main__":
    main()
    # v = Compression("txt", {1: 'a', 2: 'b'})
    # f = r"dd.dict"
    # pickle_dict(v, f)

    # r = unpickle_dict(f)
    # print(vars(r))
