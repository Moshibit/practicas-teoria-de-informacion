#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Título: Práctica 2 - Decodififador Shannon Fano.
Descripción: Implementar el decodificador Huffman donde cada símbolo a codificar
             desde un archivo en binario es de 16 bits
Autor: Erik Juárez Guerrero
Fecha de creación: 17 de marzo 2023
Última fecha de edición: 1 de abril 2023
Entrada: nombre de un archivo binario introducido por línea de mandos:
Salida: Genera dos archivos:
        * archivo codificado con extención ".sha"
        * archivo que contiene el diccionario para decodificar el archivo 
          con extención ".dict"
Como usar: introducir en la consola o simbolo de sistema la instrucción:
           
           $ python .\decodificador_shannon_fano.py .\[nombre_de_archivo]
"""

# Modulos Paquetes Bibliotecas
# ----------------------------
import argparse
import os
import pickle
import time


# Clases
# ------
class Shannon:
    """Decodifica (descomprime) un archivo binario."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.file_name , self.ext = os.path.splitext(self.path)
        self.out_fn = None
        self.file_dict = self.file_name + "_sha.dict"
        self.symbols_len = None
        self.decode_dict = {}
        self.padding = 0
        self.last_symbol = False

    def decompress(self):
        """Hace la compresión"""
        self.__unpickle()
        self.__read_file()

    def __split_hex_pair(self, str_):
        """divide una pareja de simbolos hexadecimales."""
        list_ = str_.split("\\")
        return (list_[0], list_[1])
    
    def __hex_to_bin(self, byte):
        """pasa un numero hexadecimal a binario."""
        bin_str = bin(byte)[2:]
        if len(bin_str) < 8:
            zeros = "0" * (8 - len(bin_str))
            bin_str = zeros + bin_str
        return bin_str

    def __read_file(self):
        """Lectura de archivo."""
        bit_str = ""
        bit_str_org = ""
        with open(self.path, "rb") as file, open(self.out_fn, "wb") as out_file:
            bin_code = ""
            symbol_counter = 0
            for byte_ in file.read():
                # print(hex(byte_))
                bit_str += self.__hex_to_bin(byte_)
                bit_str_org += self.__hex_to_bin(byte_)

                bit_counter = 0
                for char in bit_str:
                    bin_code += char
                    bit_counter += 1
                    if bin_code in self.decode_dict:
                        symbol_counter += 1
                        symbol = self.decode_dict[bin_code]
                        a, b = self.__split_hex_pair(symbol)
                        a = int(a, 16)
                        b = int(b, 16)
                        if symbol_counter == self.symbols_len:
                            byte_output = bytearray()
                            byte_output.append(a)
                            out_file.write(byte_output)
                        else:
                            byte_output = bytearray()
                            byte_output.append(a)
                            out_file.write(byte_output)
                            byte_output = bytearray()
                            byte_output.append(b)
                            out_file.write(byte_output)
                        bin_code = ""
                        if symbol_counter == self.symbols_len:
                            break
                    bit_str = bit_str[bit_counter + 1:]

    def __unpickle(self):
        """Recupera el diccionario [codigo: símbolo] y la extención del 
        archivo original desde el archivo .dict.

        str, int, str, dict[str: str]
        0: la extención original
        1: numero de ceros agregados al bytearray
        2: último par de hexadecimales con padding, si no se agrego paddding es None
        3: total de símbolos a decodificar
        4: el diccionaraio para decodificar
        """
        with open(self.file_dict, "rb") as file:
            obj = pickle.load(file)

        self.ext = obj[0]
        self.padding = obj[1]
        self.last_symbol = obj[2]
        self.symbols_len = obj[3]
        self.decode_dict = obj[4]

        self.out_fn = self.file_name + "_sha_decompressed" + self.ext


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
    """ fucnón main"""
    print("Processing...")

    start_time = time.time()

    # Entrada:
    args = arguments_parser()
    input_file = str(args.file_name)

    # Decodificación del archivo
    o_huffman = Shannon(input_file)
    o_huffman.decompress()


    # Cálculo de tiempo de ejecución:
    end_time = time.time()
    elapsed_time = (end_time - start_time)# * (10**3)
    print(f"Tiempo de ejecución: {elapsed_time:.4f}s.")

    print("Done.")


if __name__ == "__main__":
    main()
