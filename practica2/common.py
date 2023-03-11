#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""pass"""

import pickle

class Compression:
    """Clase para alamacenar el diccionario de codificación del archivo 
    y su extención.

    Esta clase se serializa para poder pasarse al decodificador.
    """
    def __init__(self, ext: str, encoding: dict) -> None:
        self.ext = ext
        self.encoding = encoding

def pickle_dict(c: Compression, fn: str) -> None:
    """Serializa el diccionario de codificación."""
    with open(fn, 'wb') as file:
        pickle.dump(c, file)


# TODO: este metodo debe ir en el .py de decodifiacación
def unpickle_dict(fn: str) -> None:
    """Desserializa el diccionario de codificación."""
    with open(fn, "rb") as file:
        obj = pickle.load(file)
    return obj
