#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Título: Práctica 2 - Codififador Shannon Fano.
Descripción: Implementar el codificador Shannon Fano donde cada símbolo a codificar
             desde un archivo en binario es de 16 bits
Autor: Erik Juárez Guerrero
Fecha de creación: 17 de marzo 2023
Última fecha de edición: 1 de abril 2023
Entrada: nombre de un archivo binario introducido por línea de mandos:
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
import os
import pickle
import time

from math import ceil

# Clases
# ------
class Shannon:
    """Codifica (comprime) un archivo binario en bloques de 16 bits."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.file_name, self.ext = os.path.splitext(self.path)
        self.out_fn = self.file_name + ".sha"
        self.file_dict = self.file_name + "_sha.dict"
        self.freq = {}
        self.total_8 = 0
        self.total_16 = 0
        self.heap = []
        self.code_dict = {}
        self.decode_dict = {}
        self.padding = 0
        self.padding_16 = None

    def compress(self):
        """Hace la compresión."""
        self.__read_input()
        self.__get_code()
        self.__encode()
        self.__pickle()

    def __read_input(self):
        """Lee el archivo, cuenta las frecuencias de parejas debytes (2 hex),
        cuenta cuantos bytes tiene el archivo, y cuantas parejas de bytes.
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

        # verifica que no se omitiera un simbolo
        # le agrega padding de ser necesario
        if self.total_8 % 2 != 0:
            symbol = holder + "\\" + hex(0)
            if not symbol in self.freq:
                self.freq[symbol] = 0
            self.freq[symbol] += 1
            self.total_16 += 1
            self.padding_16 = symbol

        self.freq = dict(sorted(self.freq.items(), key=lambda item: item[1], reverse=True))

    def __get_code(self):
        d = self.freq
        if len(d) == 1:
            k = list(d.keys())[0]
            self.code_dict[k] = "1"
            self.decode_dict["1"] = k
            return
        if len(d) == 2:
            k = list(d.keys())
            k1 = k[0]
            k2 = k[1]
            self.code_dict[k1] = "0"
            self.code_dict[k2] = "1"
            self.decode_dict["0"] = k1
            self.decode_dict["1"] = k2
            return
        half = ceil(sum(d.values()) / 2)
        for index in range(len(d)-1):
            d1 = dict(list(d.items())[:index+1])
            d2 = dict(list(d.items())[index+1:])
            sum1 = sum(d1.values())
            if sum1 >= half:
                break

        self.__recursive_encode(d1, "0")
        self.__recursive_encode(d2, "1")


    def __recursive_encode(self, dict_, c):
        if len(dict_) == 1:
            k = list(dict_.keys())[0]
            self.code_dict[k] = c
            self.decode_dict[c] = k
            return
        if len(dict_) == 2:
            self.__recursive_encode(dict(list(dict_.items())[:1]), c+"0")
            self.__recursive_encode(dict(list(dict_.items())[1:]), c+"1")
            return

        half = ceil(sum(dict_.values()) / 2)
        for index in range(len(dict_)-1):
            d1 = dict(list(dict_.items())[:index+1])
            d2 = dict(list(dict_.items())[index+1:])
            sum1 = sum(d1.values())

            if sum1 >= half:
                break

        self.__recursive_encode(d1, c+"0")
        self.__recursive_encode(d2, c+"1")


    def __encode(self):
        holder = None
        symbol = None
        byte_counter = 0  # Cuenta los bytes del archivo de lectura
        byte_str = ""  # los bit a ser puesto en le archvio de escritura
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

        # verifica que no falte por formar una pareja
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

        serial = [self.ext, self.padding, self.padding_16,
                  self.total_16, self.decode_dict]
        with open(self.file_dict, 'wb') as file:
            pickle.dump(serial, file)

            
# Funciones
# ---------
def arguments_parser():
    """Recive el nombre del archivo a comprimir como argumento desde la línea 
    de mandos.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str, default=None,
                        help="Nombre del archivo a comprimir.")
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
    o_shannon = Shannon(input_file)
    o_shannon.compress()

    # Cálculo de tiempo de ejecución:
    end_time = time.time()
    elapsed_time = (end_time - start_time)  # * (10**3)
    print(f"Tiempo de ejecución: {elapsed_time:.4f}s.")

    print("Done.")


if __name__ == "__main__":
    main()
