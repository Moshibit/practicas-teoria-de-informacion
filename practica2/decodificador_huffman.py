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

# TODO: OJO con los ceros a la izquierda qeu no pone el bin(byte_)[2:]

class Huffman:
    """Decodifica (descomprime) un archivo binario."""

    def __init__(self, path: str) -> None:
        self.path = path
        self.file_name , self.ext = os.path.splitext(self.path)
        self.out_fn = None
        self.file_dict = self.file_name + ".dict"
        # self.freq = {}
        # self.total_8 = 0
        # self.total_16 = 0
        # self.heap = []
        # self.code = {}
        self.reverse_code = {}
        self.padding = 0
        self.padding_16 = False

    def decompress(self):
        """Hace la compresión"""
        self.__unpickle()

        with open(self.path, "rb") as file, open(self.out_fn, "wb") as out_file:
            for byte_ in file.read():
                print(bin(byte_)[2:])


        # self.__read_input()
        # self.__heap()
        # self.__tree()
        # self.__get_code()
        # self.__encode()

    def __unpickle(self):
        """Recupera el diccionario [codigo: símbolo] y la extención del 
        archivo original desde el archivo .dict.
        """
        # [str, int, bool, dict[str: str]]
        # serial = [self.ext, self.padding, self.padding_16, self.reverse_code]
        with open(self.file_dict, "rb") as file:
            obj = pickle.load(file)

        # print(obj)
        print(type(obj))

        self.ext = obj[0]
        self.padding = obj[1]
        self.padding_16 = obj[2]
        self.reverse_code = obj[3]

        self.out_fn = self.file_name + "_decompressed" + self.ext




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
    input_file = r"test3.huff"
    # input_file = r"test10.jpg"
    # args = arguments_parser()
    # input_file = str(args.file_name)

    # *** decodificación del archivo
    o_huffman = Huffman(input_file)
    o_huffman.decompress()


    # *** Cálculo de tiempo de ejecución:
    end_time = time.time()
    elapsed_time = (end_time - start_time)# * (10**3)
    print(f"Tiempo de ejecución: {elapsed_time:.4f}s.")

    # # DEBUG: ----------------------------------------------------------------
    print(vars(o_huffman))
    # print("-------------------------")
    # o_huffman._print_freq()
    # print("-------------------------")
    # o_huffman._print_code()
    # # -----------------------------------------------------------------------



    print("Done.")





# def remove_padding(self, padded_encoded_text):
# 		padded_info = padded_encoded_text[:8]
# 		extra_padding = int(padded_info, 2)

# 		padded_encoded_text = padded_encoded_text[8:] 
# 		encoded_text = padded_encoded_text[:-1*extra_padding]

# 		return encoded_text

# 	def decode_text(self, encoded_text):
# 		current_code = ""
# 		decoded_text = ""

# 		for bit in encoded_text:
# 			current_code += bit
# 			if(current_code in self.reverse_mapping):
# 				character = self.reverse_mapping[current_code]
# 				decoded_text += character
# 				current_code = ""

# 		return decoded_text


# 	def decompress(self, input_path):
# 		filename, file_extension = os.path.splitext(self.path)
# 		output_path = filename + "_decompressed" + ".txt"

# 		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
# 			bit_string = ""

# 			byte = file.read(1)
# 			while(len(byte) > 0):
# 				byte = ord(byte)
# 				bits = bin(byte)[2:].rjust(8, '0')
# 				bit_string += bits
# 				byte = file.read(1)

# 			encoded_text = self.remove_padding(bit_string)

# 			decompressed_text = self.decode_text(encoded_text)
			
# 			output.write(decompressed_text)

# 		print("Decompressed")
# 		return output_path



if __name__ == "__main__":
    main()
