"""
Múdlo que define la clase MainWindow que representa la ventana principal de la
aplicación.
"""

from tkinter import Frame, Button
from utility.functions import do_something

class MainWindow(Frame):
    """
    Clase que represernta la ventana principal de la aplicación.
    """

    def __init__(self, master):
        """
        Constructor de la clase MainWindow.

        Args:
            master: La ventana principal de Tkinter.
        """
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        """
        Crea los widgets de la ventana principal.
        """
        self.button1 = Button(self, text="Haz algo", command=self.do_something)
        self.button1.pack() # o button1.place

    def do_something(self):
        """
        Método invocado al hacer clic en el botón.
        Realiza alguna acción utilizando la función hacer_algo() del módulo utilidades.funciones.
        """
        do_something()
