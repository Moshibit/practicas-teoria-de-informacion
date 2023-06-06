#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Autores: 
Fecha de creación: 05/06/2023
Última fecha de edición: 

"""
# Este archivo contiene la interface gráfica.
# No hay lógica de negocio aquí.

# Bibliotecas
# -----------

import tkinter


# Constantes
# ----------

WIDTH = 720
HEIGHT = 480


# Contenedores de la GUI
# ----------------------

# Raiz
root = tkinter.Tk()
root.title("placeholder del título") # TODO: poner título.
#root.geometry("720x480")
root.resizable(False, False)
#root.iconbitmap("app.ico") # TODO: agregar un icono.

# Contenedor principal
frm = tkinter.Frame(root, width=WIDTH, height=HEIGHT)
frm.pack(pady=10, padx=10)
#frm.config(bg="red")


# Contenido de la GUI
# -------------------

# Título # TODO cambiar texto. centrar
#tkinter.Label(frm, text="Título.", fg="red", font=18).place(top)

# Instrucciones # TODO cambiar texto.
tkinter.Label(frm, text="Instrucciones:").grid(row=0, column=0, sticky="w")
tkinter.Label(frm, text="1. Presiona el botón \"Generar\".").grid(row=1, column=0, sticky="w")
tkinter.Label(frm, text="2. Selecciona cuantos erroes quieres enviar.").grid(row=2, column=0, sticky="w")
tkinter.Label(frm, text="3. Selecciona la forma de los errores.").grid(row=3, column=0, sticky="w")
tkinter.Label(frm, text="4. Presiona el botón \"Enviar\".").grid(row=4, column=0, sticky="w")

# Botón Generar
# TODO: hacer botón

# Botones rádio para numero de errores
# TODO: hacer 5 botones rádio, etiquetados del 1 al 5

# Botones radio para el tipo de errores
# TODO: hacer 2 botones rádio, etiquetados como 'rafaga' y '___'

# Botón Enviar
# TODO: hacer botón


# Ejecución
# ---------

root.mainloop()
