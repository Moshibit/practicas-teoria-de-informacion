#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Título: Práctica 2 - Codififador Lemoel.
Descripción: Implementar el codificador Huffman donde cada símbolo tieneuna 
             longitud de 16 bits
Autor: Erik Juárez Guerrero
Fecha de creación: 17 de marzo 2023
Última fecha de edición: 1 de abril 2023
Entrada: nombre de un archivo binario introdido por linea de mandos:
Salida: Genera dos archivos:
        * archivo codificado con extención ".lpz"
        * archivo que contiene el diccionario para decodificar el archivo 
          con extención ".dict"
Como usar: introducir en la consola o simbolo de sistema la instrucción:
           
           $ python .\codificador_lempel_ziv.py .\[nombre_de_archivo]
"""

# Modulos Paquetes Bibliotecas
# ----------------------------
import argparse
import os
import pickle
import time

class LZ:
    """Codifica (comprime) un archivo binario"""
    def __init__(self, path):
        self.path = path
        self.file_name , self.ext = os.path.splitext(self.path)
        self.out_fn = self.file_name + ".lpz"
        self.file_dict = self.file_name + "_lpz.dict"
        self.max_size = 16
        self.code_dict = None
        self.decode_dict = None
        self.coded_content = ""
        self.padding = 0

    def compress(self):
        """Hace la compresión."""
        self.__read_input()
        self.__pickle()

    def __read_input(self):
        symbol = ""
        prefix = None
        least = None
        code_list = []
        content = []
        bitstring = ""
        to_remove = ""
        count_hex = 0
        byte_output = bytearray()
        
        with open(self.path, "rb") as file, open(self.out_fn, "wb") as out_file:
            for byte in file.read():
                count_hex += 1
                bin_byte = bin(byte)[2:]
                if len(bin_byte) < 8:
                    bin_byte = "0" * (8 - len(bin_byte)) + bin_byte
                bitstring += bin_byte

                if count_hex == 3:
                    bitstring = bitstring[:-2]

                for char in bitstring:
                    symbol += char
                    if not symbol in content:
                        least = symbol[-1]
                        prefix = symbol[:-1]

                        try:
                            code = bin(content.index(prefix) + 1)[2:]
                            code += least
                        except ValueError:
                            code = least

                        if len(code) <= self.max_size:
                            content.append(symbol)
                            code = ((self.max_size - len(code)) * "0") + code
                            code_list.append(code)
                            self.coded_content += code
                        else:
                            code = symbol[:-1]
                            symbol = symbol[-1]
                            code = content.index(code)
                            self.coded_content += code_list[code]
                            continue
                                                   
                        while len(self.coded_content) >= 8:
                            byte_output.append(int(self.coded_content[:8], 2))
                            self.coded_content = self.coded_content[8:]
                        to_remove += symbol
                        symbol = ""

                bitstring = bitstring.partition("to_remove")[2]
                to_remove = ""

            if len(symbol) > 0:
                code = symbol
                code = content.index(code)
                self.coded_content += code_list[code]

            # agrega padding al final para completar 8 bits
            if len(self.coded_content) % 8 != 0:
                self.padding = 8 - len(self.coded_content)
                self.coded_content = self.coded_content + (self.padding * "0")
                byte_output.append(int(self.coded_content[:8], 2))
            
            out_file.write(byte_output)

        self.code_dict = dict(zip(content, code_list))
        self.decode_dict = dict(zip(code_list, content))

    def __pickle(self):
        """Serializa el diccionario [codigo: símbolo] y la extención del 
        archivo original, para que se puedan llevar al script de decodificación
        y esa información se pueda recuperar.

        [str, int, dict[str: str]
        0: la extención original
        1: numero de ceros agregados al bytearray
        2: el diccionaraio para decodificar
        """
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
    o_lz = LZ(input_file) #(b)
    o_lz.compress()

    # Cálculo de tiempo de ejecución:
    end_time = time.time()
    elapsed_time = (end_time - start_time)# * (10**3)
    print(f"Tiempo de ejecución: {elapsed_time:.4f}s.")

    print("Done.")

if __name__ == "__main__":
    main()
