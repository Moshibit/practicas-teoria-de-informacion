#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Título: Práctica 2 - Codififador Huffman.
Descripción: Implementar el codificador Huffman donde cada símbolo a codificar
             desde un archivo en binario es de 16 bits
Autor: Erik Juárez Guerrero
Fecha de creación: 17 de marzo 2023
Última fecha de edición: 1 de abril 2023
Entrada: nombre de un archivo binario introdido por linea de mandos:
Salida: Genera dos archivos:
        * archivo codificado con extención ".huff"
        * archivo que contiene el diccionario para decodificar el archivo 
          con extención ".dict"
Como usar: introducir en la consola o simbolo de sistema la instrucción:
           
           $ python .\codificador_huffman.py .\[nombre_de_archivo]
"""

# Modulos Paquetes Bibliotecas
# ----------------------------
import argparse
import heapq
import os
import pickle
import time

# Clases
# ------
class Huffman:
    """Codifica (comprime) un archivo binario en bloques de 16 bits."""

    class Node:
        """clase anidada: Nodo del árbol binario."""

        def __init__(self, symbol: str, freq) -> None:
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
        self.file_name, self.ext = os.path.splitext(self.path)
        self.out_fn = self.file_name + ".huff"
        self.file_dict = self.file_name + "_huff.dict"
        self.freq = {}
        self.total_8 = 0
        self.total_16 = 0
        self.heap = []
        self.code_dict = {}
        self.decode_dict = {}
        self.padding = 0
        self.padding_16 = None

    def compress(self) -> None:
        """Hace la compresión."""
        self.__read_input()
        self.__heap()
        self.__tree()
        self.__get_code()
        self.__encode()
        self.__pickle()

    def __read_input(self) -> None:
        """Lee el archivo, cuenta las frecuencias de parejas debytes (2 hex),
        uenta cuantos bytes tiene el archivo, y cuantas parejas de bytes
        """
        holder: str  = ""
        symbol: str = ""

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

        # verifica que no se omitiera un simbolo
        # le agrega paddin de ser necesario
        if self.total_8 % 2 != 0:
            symbol = holder + "\\" + hex(0)
            if not symbol in self.freq:
                self.freq[symbol] = 0
            self.freq[symbol] += 1
            self.total_16 += 1
            self.padding_16 = symbol

    def __heap(self) -> None:
        """Forma el monticulo (heap)."""
        for key, value in self.freq.items():
            node = self.Node(key, value)
            heapq.heappush(self.heap, node)

    def __tree(self):
        """Construye el árbol binario."""
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def __get_code(self):
        """Inicia la obtención del código Huffman."""
        root = heapq.heappop(self.heap)
        current_code = ""
        self.__recursive_encode(root, current_code)

    def __recursive_encode(self, root, current_code):
        if root is None:
            return
        if root.symbol is not None:
            self.code_dict[root.symbol] = current_code
            self.decode_dict[current_code] = root.symbol
            return
        self.__recursive_encode(root.left, current_code + "0")
        self.__recursive_encode(root.right, current_code + "1")

    def __encode(self):
        """Codifica el nuevo archivo con el código huffman."""
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
                byte_str += self.code_dict[symbol]
                while len(byte_str) >= 8:
                    byte_output.append(int(byte_str[:8], 2))
                    byte_str = byte_str[8:]
                out_file.write(byte_output)

        # verifica que no falte una pareja por formar
        if self.total_8 % 2 != 0:
            byte_output = bytearray()
            symbol = holder + "\\" + hex(0)
            byte_str += self.code_dict[symbol]
            while len(byte_str) >= 8:
                byte_output.append(int(byte_str[:8], 2))
                byte_str = byte_str[8:]
            with open(self.out_fn, "ab") as out_file:
                out_file.write(byte_output)

        # agrega el padding
        if len(byte_str) < 8:
            byte_output = bytearray()
            self.padding = 8 - len(byte_str)
            byte_str = byte_str + "0" * self.padding
            byte_output.append(int(byte_str, 2))
            with open(self.out_fn, "ab") as out_file:
                out_file.write(byte_output)


    def __pickle(self):
        """Serializa el diccionario [codigo: símbolo] y la extención del 
        archivo original, para que se puedan llevar al script de decodificación
        y esa información se pueda recuperar.

        [str, int, str, dict[str: str]
        0: la extención original
        1: numero de ceros agregados al bytearray
        2: último par de hexadecimales con padding, si no se agrego paddding es None
        3: total de símbolos a decodificar
        4: el diccionaraio para decodificar
        """
        serial = [self.ext, self.padding, self.padding_16, self.total_16, self.decode_dict]
        with open(self.file_dict, 'wb') as file:
            pickle.dump(serial, file)


# Funciones
# ---------
def arguments_parser():
    """Recive el nombre del archivo a comprimir como argumento desde la línea 
    de mandos.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str, default=None, help="Nombre del archivo a comprimir.")
    args = parser.parse_args()
    return args


# Función main
# ------------
def main():
    """ fución main"""
    print("Processing...")

    # Tiempo de inicio
    start_time = time.time()

    # Entrada:
    args = arguments_parser()
    input_file = str(args.file_name)

    # Codificación del archivo
    o_huffman = Huffman(input_file)
    o_huffman.compress()

    # Cálculo de tiempo de ejecución:
    end_time = time.time()
    elapsed_time = (end_time - start_time)
    print(f"Tiempo de ejecución: {elapsed_time:.4f}s.")
    
    print("Done.")


if __name__ == "__main__":
    main()
