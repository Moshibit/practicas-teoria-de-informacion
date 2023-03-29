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

class LZ:
    """Pass"""
    def __init__(self, path):
        self.path = path
        self.file_name , self.ext = os.path.splitext(self.path)
        self.out_fn = self.file_name + ".lpz"
        self.file_dict = self.file_name + "_huff.lpz"
        self.max_size = 16 #4#16
        self.code_dict = None
        self.decode_dict = None
        self.coded_content = ""

        # self.padding = 2 # TODO poner en cero por cuestiones de debug es ahora 2
        # self.numberof_hex = 3 # DEBUG

    def compress(self):
        """Pass"""
        self.__read_input()
        self.__pickle()

    def __read_input(self):
        symbol = ""
        prefix = None
        least = None
        code_list = []
        content = []
        bitstring = ""
        bitstring_debug = ""
        to_remove = ""
        count_hex = 0 # DEBUG
        #break_centinel = False

        with open(self.path, "rb") as file:
            for byte in file.read():
                count_hex += 1
                bin_byte = bin(byte)[2:]
                if len(bin_byte) < 8:
                    bin_byte = "0" * (8 - len(bin_byte)) + bin_byte
                bitstring += bin_byte
                bitstring_debug += bin_byte

                # if count_hex == self.numberof_hex:
                #     bitstring = bitstring[:-2]
                #     bitstring_debug = bitstring_debug[:-2]

                for char in bitstring:
                    symbol += char
                    if not symbol in content: # and len(content) < 2 ** self.max_size:
                        least = symbol[-1]
                        prefix = symbol[:-1]

                        try:
                            code = bin(content.index(prefix) + 1)[2:]
                            code += least
                        except ValueError:
                            code = least

                        if len(code) <= self.max_size:

                            content.append(symbol)
                            code_list.append(code) # code_list.append(int(prefix + least, 2))
                            self.coded_content += code + " " # TODO quitar esl espacio
                        else:
                            code = symbol[:-1]
                            symbol = symbol[-1]
                            code = content.index(code)
                            self.coded_content += code_list[code]  + "_" # TODO quitar esl guin bajo
                            continue
                        
                        
                        # print(symbol) # DEBUG
                        to_remove += symbol
                        symbol = ""
                    # elif: #len(symbol) == self.max_size:
                    #     # TODO escribe en el archivo de salida - busca el valor en
                    #     code = bin(content.index(symbol) + 1)[2:]
                    #                                                     #X if len(code) < self.max_size:
                    #                                                     #X     code = "0" * (8 - self.max_size) + code     
                    #     #append
                    #     self.coded_content += code + "_" # TODO quitar el guion bajo

                    #     to_remove += symbol
                    #     symbol = ""
                        
                    #     continue
                        
                # if break_centinel:
                #     break

                

                bitstring = bitstring.partition("to_remove")[2]
                to_remove = ""

            # print("ultimo simbolo", symbol)

            code = symbol
            #self.coded_content += bin(content.index(code) + 1)[2:] + "F" # TODO quitar esl "F"
            code = content.index(code)
            self.coded_content += code_list[code]  + "F"
            
        self.code_dict = dict(zip(content, code_list))
        self.decode_dict = dict(zip(code_list, content))
        
        #print(self.code_dict)
        #print(self.decode_dict)
        
        # print(len(self.code_dict))
        # print(bitstring)
        # print(len(bitstring))
        # print(bitstring_debug)
        # print(len(bitstring_debug))
        for k,v in self.code_dict.items():
            print(f"{k:16}",":",v)

    def __pickle(self):
        """Serializa el diccionario [codigo: símbolo] y la extención del 
        archivo original, para que se puedan llevar al script de decodificación
        y esa información se pueda recuperar.
        """
        #[str, int, dict[str: str]
        # 0: la extención original
        # 1: numero de ceros agregados al bytearray
        # 2: el diccionaraio para decodificar
        serial = [self.ext, self.padding, self.decode_dict]
        with open(self.file_dict, 'wb') as file:
            pickle.dump(serial, file)

def arguments_parser():
    """Recive el nombre del archivo a comprimir como argumento desde la línea 
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
    input_file = r"test20.bin"
    # input_file = r"test15.bin"
    #input_file = r"test10.jpg"
    #args = arguments_parser()
    #input_file = str(args.file_name)
    #b = "010110100101"

    # *** Codificación del archivo

    o_lz = LZ(input_file) #(b)
    o_lz.compress()
    print("--->", o_lz.coded_content) # TODO grabar en archivo

    # *** Cálculo de tiempo de ejecución:
    end_time = time.time()
    elapsed_time = (end_time - start_time)# * (10**3)
    print(f"Tiempo de ejecución: {elapsed_time:.4f}s.")

    print("Done.")


if __name__ == "__main__":
    # contenido = "001011101001011101101100"
    # NOMBRE_ARCHIVO = r"test20.bin"
    # byte_output = bytearray()
    # print("Beggin...")
    # with open(NOMBRE_ARCHIVO, "wb") as file:
    #     while len(contenido) >= 8:
    #         byte_output.append(int(contenido[:8], 2))
    #         contenido = contenido[8:]
    #     file.write(byte_output)
    # print("End.")


    main()
