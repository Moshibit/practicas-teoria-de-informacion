""" pass """
#
#
#

#from collections.OrderedDict
# TODO: importar arbol binario y lista o diccionario ordenado
from collections import OrderedDict
# TODO importar parser


def snf():
    """ pass """
    pass

def huff():
    """ pass """
    pass

def lpz():
    """ pass """
    pass

def encode():
    """ pass """
    pass

def decode():
    """ pass """
    pass

# def sum_dict(dict_: dict) -> int | float:
#     """ Suma los valores del diccionario. """
#     return sum(dict_.values())

# def probability(frec: dict) -> dict:
#     """ Obtiene las probabilidades INDEPENDIENTE de la fuente 
#     (diccionario). """
#     total = sum_dict(frec)
#     return {k: v / total for k, v in frec.items()}

def read_input(file_name: str, level=2) -> bytes:
    """ pass """

    counter = {}
    total = 0
    keeper = None
    symbol = None
    with open(file_name, "rb") as file:
        for item in file.read():
            if total == 156089: # con esto fuerzo a que sea impar par probar
                break 
            total += 1
            if total % level != 0:
                keeper = hex(item)
                continue
            symbol = keeper + "\\" + hex(item)
            try:
                counter[symbol] += 1
            except KeyError:
                counter[symbol] = 0
                counter[symbol] += 1
            if total <= 2: # <- el primero
                print("el primer simbolo es: ", symbol)
            # if total >= 156090: # 156090 <- el último
            #     print(symbol)
    if total % level != 0: # TODO esto es solo para dos ajustar para level 2, ajustar para level n 
        symbol = keeper + "\\" + hex(0)
        try:
            counter[symbol] += 1
        except KeyError:
            counter[symbol] = 0
            counter[symbol] += 1
    print("el último síbolo es: ", symbol) # <- el último
    
    print("DICT:")
    for k, v in counter.items():
        print(k,":", v)
    prob = {key: value / total for key, value in counter.items()}
    # print("total: ", total)
    # prob = probability(counter)
    return prob

    # counter = [0 for x in range(256)]
    # with open(file_name, "rb") as file:
    #     for item in file.read():
    #         counter[item] += 1
    # return counter

    # with open(file_name, "rb") as file:
    #     print(file.read(1))
    #     print(file.read(1))
    #     print(file.read(1))
    #     print(file.read(1))
    #     print(file.read(1))

    # # with open(file_name, "rb") as file:
    #     data = file.read()
    # return data

    # with open(file_name, "rb") as file:
    #     for item in file:
    #         print(item)
    #     return 0

def main():
    """ fucnón main"""
    #i = read_input(r"practica2_input.jpg")
    i = read_input(r"test2.bin")
    i = dict(sorted(i.items(), key=lambda word: word[1], reverse=True ))
    print("PROBA:")
    for k, v in i.items():
        print(k,":", v)
    # print(len(i))

if __name__ == "__main__":
    print("Processing...")
    main()
    print("Done.")
    # print( hex(ord("a")) + "\\" + hex(ord("A")) )
    # print( type(hex(ord("a"))) )
