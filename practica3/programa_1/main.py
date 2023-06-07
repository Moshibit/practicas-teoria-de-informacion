#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Archivo principal del proyecto.
Inicia la aplicación y crea la ventana principal

Entrada: 
Salida: 
Fecha de creación: 06/06/2023
Última fecha de edición: 06/06/2023

"""

# Bibliotecas
# -----------
from tkinter import Tk
from gui.main_window import MainWindow


# Funcion main
# ------------
def main():
    """
    Crea la ventana princial.
    """
    root = Tk()
    root.title("Calculadora CRC")
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    print("Start.")
    # Invoca la función main
    main()
    print("End.")
