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
import pickle
import time


class Huffman:
    """Codifica (comprime) un archivo binario en bloques de 16 bits."""

    class Node:
        """clase anidada: Nodo..."""
        def __init__(self, symbol, freq):
            self.symbol = symbol
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other: object) -> bool:
            if not isinstance(other, Huffman.Node):
                raise TypeError(f"El objeto {other} tiene que ser de tipo Node.")
            return self.freq < other.freq

        def __eq__(self, other: object) -> bool:
            if other is None:
                return False
            if not isinstance(other, Huffman.Node):
                raise TypeError(f"El objeto {other} tiene que ser de tipo Node.")
            return self.freq == other.freq


    def __init__(self, path: str) -> None:
        self.path = path
        self.file_name , self.ext = os.path.splitext(self.path)
        self.out_fn = self.file_name + ".huff"
        self.file_dict = self.file_name + ".dict"
        self.freq = {}
        self.total_8 = 0
        self.total_16 = 0
        self.heap = []
        self.code = {}
        self.reverse_code = {}
        self.padding = 0

    def compress(self):
        """Hace la compresión"""
        self.__read_input()
        self.__heap()
        self.__tree()
        self.__get_code()
        self.__encode()
        self.__pickle()

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
        """Imprime el diccionario de frecuencias, para uso de debug"""
        print("FREQ DICT:")
        for k, v in self.freq.items():
            print(k, ":", v)

    def __heap(self) -> None:
        """Forma el monticulo (heap)"""
        for key, value in self.freq.items():
            node = self.Node(key, value)
            heapq.heappush(self.heap, node)

    def __tree(self):
        while len(self.heap) > 1:
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
        if root is None:
            return
        if root.symbol is not None:
            self.code[root.symbol] = current_code
            self.reverse_code[current_code] = root.symbol
            return
        self.__recursive_encode(root.left, current_code + "0")
        self.__recursive_encode(root.right, current_code + "1")

    def __encode(self):
        holder = None
        symbol = None
        byte_counter = 0 # Cuenta los bytes del archivo de lectura
        byte_str = "" # los bit a ser puesto en le archvio de escritura
        with open(self.path, "rb") as file, open(self.out_fn, "wb") as out_file:
            for byte_ in file.read():
                byte_output = bytearray()
                byte_counter += 1
                if byte_counter % 2 != 0:
                    holder = hex(byte_)
                    continue
                symbol = holder + "\\" + hex(byte_)
                byte_str += self.code[symbol]
                while len(byte_str) >= 8:
                    byte_output.append(int(byte_str[:8], 2))
                    byte_str = byte_str[8:]
                out_file.write(byte_output)

        if len(byte_str) < 8:
            self.padding = 8 - len(byte_str)
            byte_str = byte_str + "0" * self.padding
            byte_output.append(int(byte_str, 2))
            with open(self.out_fn, "ab") as out_file:
                out_file.write(byte_output)

    def _print_code(self):
        """Imprime el diccionario del código, para uso de debug"""
        for k, v in self.code.items():
            print(k, ":", v)

    def __pickle(self):
        """Serializa el diccionario y la extención del archivo original, para 
        que se puedan llevar al script de decodificación y esa información se 
        pueda recuperar.
        """
        serial = [self.ext, self.padding, self.reverse_code]
        with open(self.file_dict, 'wb') as file:
            pickle.dump(serial, file)


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
    # TODO: elimina las siguientes 2 líneas y descomenta la tercera y cuarta.
    # input_file = r"test3.bin"
    # input_file = r"test10.jpg"
    args = arguments_parser()
    input_file = str(args.file_name)

    # *** Codificación del archivo
    o_huffman = Huffman(input_file)
    o_huffman.compress()

    # *** Cálculo de tiempo de ejecución:
    end_time = time.time()
    elapsed_time = (end_time - start_time)# * (10**3)
    print(f"TIempo de ejecución: {elapsed_time:.4f}s.")

    # # DEBUG: ----------------------------------------------------------------
    # print(vars(o_huffman))
    # print("-------------------------")
    # o_huffman._print_freq()
    # print("-------------------------")
    # o_huffman._print_code()
    # # -----------------------------------------------------------------------
    
    print("Done.")


if __name__ == "__main__":
    main()
