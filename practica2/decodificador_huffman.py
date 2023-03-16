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
        self.file_dict = self.file_name + "_huff.dict"
        # self.freq = {}
        # self.total_8 = 0
        # self.total_16 = 0
        # self.heap = []
        # self.code = {}
        self.symbols_len = None
        self.decode_dict = {}
        self.padding = 0
        self.last_symbol = False

    def decompress(self):
        """Hace la compresión"""
        self.__unpickle()
        self.__read_file()



        # self.__read_input()
        # self.__heap()
        # self.__tree()
        # self.__get_code()
        # self.__encode()

    def __split_hex_pair(self, str_):
        """pass"""
        list_ = str_.split("\\")
        return (list_[0], list_[1])
    
    def __hex_to_bin(self, byte):
        """pass"""
        bin_str = bin(byte)[2:]
        if len(bin_str) < 8:
            zeros = "0" * (8 - len(bin_str))
            bin_str = zeros + bin_str
            # print(bin_str)
        return bin_str



    
    ######################
    # d = "0x6d\\0x70"
    # a, b = split_hex_pair(d)
    # print(a, b)
    # a = int(a, 16)
    # b = int(b, 16)
    #print(a, b)
    #a = chr(a)
    #b = chr(b)
    #print(a, b)
    #print(d)
    ######################

    def __read_file(self):
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
                            #print(chr(a))
                            byte_output = bytearray()
                            byte_output.append(a)
                            out_file.write(byte_output)
                        else:
                            #print(chr(a), chr(b), sep="", end="")
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

        # print(bit_str)
        # print(bit_str_org)


    def __unpickle(self):
        """Recupera el diccionario [codigo: símbolo] y la extención del 
        archivo original desde el archivo .dict.
        """
        #[str, int, str, dict[str: str]
        # 0: la extención original
        # 1: numero de ceros agregados al bytearray
        # 2: último par de hexadecimales con padding, si no se agrego paddding es None
        # 3: total de símbolos a decodificar
        # 4: el diccionaraio para decodificar
        
        with open(self.file_dict, "rb") as file:
            obj = pickle.load(file)

        # print(obj)
        # print(type(obj))

        self.ext = obj[0]
        self.padding = obj[1]
        self.last_symbol = obj[2]
        self.symbols_len = obj[3]
        self.decode_dict = obj[4]

        self.out_fn = self.file_name + "_huff_decompressed" + self.ext




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
    input_file = r"test10.huff"
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
    # print(vars(o_huffman))
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
