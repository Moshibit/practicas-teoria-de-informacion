#!/usr/bin/env python3
# -*- coding:utf-8 -*-
""" Codififador Huffman """
# Implementar el codificador y decodificador Huffman y Shannon-Fano donde cada
# símbolo a codificar desde un archivo en binario es de 16 bits,
# a
# Implementar codificador y decodificador Lempel-Ziv con símbolos de longitud
# fija de 16 bits.


import argparse
import os
import pickle
import time

from math import ceil


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
        """Hace la compresión"""
        self.__read_input()
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
            self.padding_16 = symbol
        # # DEBUG: ------------------------------------------------------------
        # print(f"el último síbolo es: {symbol}")
        # # DEBUG(FIN) --------------------------------------------------------
        self.freq = dict(sorted(self.freq.items(), key=lambda item: item[1], reverse=True))

    def _print_freq(self):
        """Imprime el diccionario de frecuencias, para uso de debug"""
        print("FREQ DICT:")
        for k, v in self.freq.items():
            print(k, ":", v)

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
            sum2 = sum(d2.values())
            diff1 = (sum1 - half)
            diff2 = (sum2 - half)
            if sum1 >= half:
                break

        self.__recursive_encode(d1, "0")
        self.__recursive_encode(d2, "1")


    def __recursive_encode(self, dict_, c):
        diff1 = diff2 = 0
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
            sum2 = sum(d2.values())
            diff1 = (sum1 - half)
            diff2 = (sum2 - half)

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
            byte_output = bytearray()  # <-----
            symbol = holder + "\\" + hex(0)
            byte_str += self.code_dict[symbol]
            while len(byte_str) >= 8:
                byte_output.append(int(byte_str[:8], 2))
                byte_str = byte_str[8:]
            with open(self.out_fn, "ab") as out_file:
                out_file.write(byte_output)

        # agrega el padding
        if len(byte_str) < 8:
            byte_output = bytearray()  # <-----
            self.padding = 8 - len(byte_str)
            byte_str = byte_str + "0" * self.padding
            byte_output.append(int(byte_str, 2))
            with open(self.out_fn, "ab") as out_file:
                out_file.write(byte_output)

    def _print_code(self):
        """Imprime el diccionario del código, para uso de debug"""
        for k, v in self.code_dict.items():
            print(k, ":", v)

    def __pickle(self):
        """Serializa el diccionario [codigo: símbolo] y la extención del 
        archivo original, para que se puedan llevar al script de decodificación
        y esa información se pueda recuperar.
        """
        # [str, int, str, dict[str: str]
        # 0: la extención original
        # 1: numero de ceros agregados al bytearray
        # 2: último par de hexadecimales con padding, si no se agrego paddding es None
        # 3: total de símbolos a decodificar
        # 4: el diccionaraio para decodificar
        serial = [self.ext, self.padding, self.padding_16,
                  self.total_16, self.decode_dict]
        with open(self.file_dict, 'wb') as file:
            pickle.dump(serial, file)


def arguments_parser():
    """Recive el nombre del archivo a comprimir como argumento desde la línea 
    de mandos.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("file_name", type=str, default=None,
                        help="Nombre del archivo a comprimir.")
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
    o_shannon = Shannon(input_file)
    o_shannon.compress()

    # *** Cálculo de tiempo de ejecución:
    end_time = time.time()
    elapsed_time = (end_time - start_time)  # * (10**3)
    print(f"Tiempo de ejecución: {elapsed_time:.4f}s.")

    # # DEBUG: ----------------------------------------------------------------
    # print(vars(o_shannon))
    # print("-------------------------")
    # print(o_shannon.freq)
    # print(o_shannon.code_dict)
    # print("-------------------------")
    # o_shannon.
    # # -----------------------------------------------------------------------

    print("Done.")


if __name__ == "__main__":
    main()


# def find_middle(lst):
#   if len(lst) == 1: return None
#   s = k = b = 0
#   for p in lst: s += p
#   s /= 2
#   for p in range(len(lst)):
#     k += lst[p]
#     if k == s: return p
#     elif k > s:
#       j = len(lst) - 1
#       while b < s:
#         b += lst[j]
#         j -= 1
#       return p if abs(s - k) < abs(s - b) else j
#   return

# def shannon(iterable):
#   if len(iterable) == 1: return None
#   half = round(sum(iterable) / 2)
#   print(half)
#   group1=group2=0
#   diff1=diff2=0
#   for index in range(len(iterable)-2):
#     group1 = sum(iterable[:index+1])
#     group2 = sum(iterable[:index+2])
#     diff1 = gru


# print('Hello, world!')

# l = [1/2, 1/4, 1/8, 1/16, 1/32, 1/64, 1/64]
# anita = [6/15, 2/15, 2/15, 2/15, 2/15, 1/15]
# anita2 = [6, 2, 2, 2, 2, 1]

# i=4
# print("grupo1:", sum(anita2[:i+1]))
# print("grupo2:", sum(anita2[:i+2]))

# print(sum(anita2))
# print(shannon(anita2))
