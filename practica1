#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Título: Práctica 1 - Introducción a la teoría de la información.
Descripción: Conceptos básicos de teoría de información y codificación
Autor: Erik Juárez Guerrero
Fecha de creación: 17 de febrero 2023
Última fecha de edición: 25 de febrero 2023
Entrada: Un libro en tres diferentes idiomas con extención 'txt':
        'romeo y julieta.txt', 'romeo and juliet.txt' y 'romeo et juliette.txt'
Salida: Impresión en pantalla, por cada archivos se imprime:
        * Una tabla con los símbolos (letras) encontrados en el documento,
          las occurencias encontradas, su probabilidad y la información.
        * La entropía calculada de la información.
        * Valores de las entropías de fuentes extendidas de 2° y 3° orden.
"""
# Práctica 1 - Introducción a la teoría de la información.
# Objetivo: comprender los conceptos básicos de la teoría de la información.
# Desarrollo :
#   1) Desarrollar un programa que permita obtener todos los símbolos ASCII.
#   2) Realizar el conteo de frecuencias de los símbolos imprimibles.
#   3) Obtener las probabilidades para un sólo dígito.
#   4) Calcular:
#       * La información para cada uno de los símbolos en unidades, parejas y
#         tercias.
#       * La entropía, utilizando la información calculada.
#       * La entropía de 2° y 3° orden para la fuente (corroborar).

# MÓDULOS PAQUETES BIBLIOTECAS
# ----------------------------
from math import log2

# CONSTANTES
# ----------
ACCENTS = 'ÁÂÀÄÉÊÈËÍÎÌÏÓÔÒÖÚÛÙÜŸÝáéíóúâêîôûàèìòùäëïöüÿý'
ES_ALPHABET = 'abcdefghijklmnñopqrstuvwxyz '
EN_ALPHABET = 'abcdefghijklmnopqrstuvwxyz '
FR_ALPHABET = 'abcdefghijklmnopqrstuvwxyzçæœ '

# FUNCIONES
# ---------
def sum_dict(dict_: dict) -> int | float:
    """ Suma los valores del diccionario. """
    return sum(dict_.values())


def probability(frec: dict) -> dict:
    """ Obtiene las probabilidades INDEPENDIENTE de la fuente 
    (diccionario). """
    total = sum_dict(frec)
    return {k: v / total for k, v in frec.items()}


def src_ord_prob(prob: dict, order: int) -> dict:
    """ Genera fuentes extendidas, calcula probabilidades dependientes. """
    ext_src = prob.copy()
    for i in range(order - 1):
        ext_src = {k1 + k2: v1 * v2 for k1, v1 in ext_src.items()
                    for k2, v2 in prob.items()}
    return ext_src


def information(prob: dict) -> dict:
    """ Calcula la información. """
    info = {}
    for key, value in prob.items():
        try:
            info[key] = log2(1 / value)
        except ZeroDivisionError:
            info[key] = float("inf")
    return info


def entropy(prob: dict) -> float:
    """ Calcula la entropía usando la información. """
    ent = {}
    info = information(prob)
    for key in prob.keys():
        if info[key] == float("inf"):
            ent[key] = 0.0
        else:
            ent[key] = info[key] * prob[key]
    return sum_dict(ent)


def print_ascii() -> str:
    """ Imprime los caracteres ascii 128. """
    printable_chars = ""
    for character in range(32, 127):
        printable_chars = printable_chars + chr(character)
    return printable_chars


def strip_accents(char: str) -> str:
    """ Retira los acentos de las letras. """
    if char in 'áâàä':
        char = 'a'
    elif char in 'éêèë':
        char = 'e'
    elif char in 'íîìï':
        char = 'i'
    elif char in 'óôòö':
        char = 'o'
    elif char in 'úûùü':
        char = 'u'
    elif char in 'ÿý':
        char = 'y'
    return char


def normalize(text: str) -> str:
    """ Normaliza una cadena, la cambia a minúsculas y quita acentos. """
    text = list(text)
    len_text = len(text)
    for index in range(len_text):
        text[index] = text[index].lower()
        if text[index] in ACCENTS:
            text[index] = strip_accents(text[index])
    text = "".join(text)
    return text


def get_dict_1(alphabet: str) -> dict:
    """ Regresa un dicionario con las letras como
    claves y con valores cero. """
    return {i: 0 for i in alphabet}


def get_dict_2(alphabet: str) -> dict:
    """ Regresa un dicionario con las parejas 
    de letras como claves y con valores cero. """
    return {i + j: 0 for i in alphabet for j in alphabet}


def get_dict_3(alphabet: str, dict_2: dict) -> dict:
    """ Regresa un dicionario con las tercias 
    de letras como claves y con valores cero. """
    return {i + j: 0 for i in alphabet for j in dict_2}


def count(text: str, dict_1: dict, dict_2: dict, dict_3: dict) -> dict:
    """ Cuenta las frecuencias de los símbolos. """
    text = normalize(text)
    len_text = len(text)
    for index in range(len_text):
        # conteo de unidades
        try:
            char_1 = text[index]
            dict_1[char_1] += 1
        except KeyError:
            pass
        # conteo de parejas
        try:
            char_2 = text[index] + text[index + 1]
            dict_2[char_2] += 1
        except IndexError:
            pass
        except KeyError:
            pass
        # conteo de tercias
        try:
            char_3 = text[index] + text[index + 1] + text[index + 2]
            dict_3[char_3] += 1
        except IndexError:
            pass
        except KeyError:
            pass
    return dict_1, dict_2, dict_3


def print_output(msg: str, src: dict, pro: dict,
    inf: dict, ent: float, table=False) -> None:
    """ Imprime en pantallas los datos obtenidos. """
    msg = f"Fuente {msg}° orden."
    separator(msg, "=")
    if table:
        print_table(src, pro, inf)
    print(f"Entropía de la fuente: {ent:.4f} [bits / símbolo].")
    # print("-" * 80)


def data_source(source: dict) -> tuple:
    """ Obtiene todos los datos de una fuente de primer orden. """
    prob = probability(source)
    info = information(prob)
    ent = entropy(prob)
    print_output("1", source, prob, info, ent, table=True)
    print("-" * 80)
    print(f"Fuente de primer orden * 2 = {ent*2:.4f} [bits / símbolo].")
    print(f"Fuente de primer orden * 3 = {ent*3:.4f} [bits / símbolo].")
    return (prob, info, ent)


def print_table(simb: dict, prob: dict, info: dict) -> None:
    """ Imprime una tabla con la frecuencia, probabilidad e 
    información de cada símbolo. """
    print("Símbolo Frecuencia Probabilidad Información[bits]")
    for key, value in simb.items():
        print(
            f"{key:^7} {value:10} {prob[key]:12.4f} {info[key]:17.4f}")


def data_source_ext(source_ext: dict, prob_1, orden: int) -> tuple:
    """ Obtiene todos los datos de una fuente extendida, a partir de las 
    probabilidades de la fuente de primer orden. """
    prob = src_ord_prob(prob_1, orden)
    info = information(prob)
    ent = entropy(prob)
    print_output(str(orden), source_ext, prob, info, ent)
    return (source_ext, prob, info, ent)


def practice(file_name: str, alphabet: str) -> None:
    """ Presenta los conceptos de Teoría de Información. """
    # crea las fuentes, aún no tienen probabilidades
    d1 = get_dict_1(alphabet)
    d2 = get_dict_2(alphabet)
    d3 = get_dict_3(alphabet, d2)
    # recorre el documento y cuenta la frecuencia de cada letra
    with open(file_name, 'rt', encoding='utf-8') as file:
        for line in file:
            d1, d2, d3 = count(line, d1, d2, d3)
    p1, i1, e1 = data_source(d1)
    del i1, e1
    data_source_ext(d2, p1, 2)
    data_source_ext(d3, p1, 3)
    print("=" * 80)


def separator(text: str, symbol: str) -> None:
    """ Imprime una línea para delimitar en la salida por pantalla
    symbol debe un sólo caracter. """
    num = 80 - (len(text) + 4)
    print(symbol * 2, text, symbol * num)


def main() -> None:
    """ Función main. """
    print('Processing...')
    # print(print_ascii())
    separator("ESPAÑOL", "*")
    practice('romeo y julieta.txt', ES_ALPHABET)
    separator("INGLÉS", "*")
    practice('romeo and juliet.txt', EN_ALPHABET)
    separator("FRANCÉS", "*")
    practice('romeo et juliette.txt', FR_ALPHABET)
    print('Done.')


if __name__ == '__main__':
    main()
