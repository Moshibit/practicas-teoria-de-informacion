"""
Múdlo que define la clase MainWindow que representa la ventana principal de la
aplicación.
"""
from tkinter import Frame, Button, Label, Entry, StringVar, Tk
from utility.functions import detect_errors

class MainWindow(Frame):
    """
    Clase que represernta la ventana principal de la aplicación.
    """

    def __init__(self, master: Tk) -> None:
        """
        Constructor de la clase MainWindow.

        Args:
            master: La ventana principal de Tkinter.
        """
        super().__init__(master)
        self.master = master
        self.info = StringVar()
        self.polynomial = StringVar()
        self.init_vector = StringVar()
        self.pack()
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Crea y configura los widgets de la ventana principal.
        """
        label_info = Label(self, text="Información en hexadecimal:")
        label_info.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        entry_info = Entry(self, width=30, textvariable=self.info)
        entry_info.grid(row=0, column=1, padx=10, pady=10)

        label_polynomial = Label(self, text="Polinomio:")
        label_polynomial.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        entry_polynomial = Entry(self, width=30, textvariable=self.polynomial)
        entry_polynomial.grid(row=1, column=1, padx=10, pady=10)

        label_init_vector = Label(self, text="Vector de inicialización:")
        label_init_vector.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        entry_init_vector = Entry(self, width=30, textvariable=self.init_vector)
        entry_init_vector.grid(row=2, column=1, padx=10, pady=10)

        button_check = Button(self, text="Verificar", command=self.detect_errors)
        button_check.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.label_result = Label(self, text="Resultado:")
        self.label_result.grid(row=4, column=0, padx=10, pady=10, sticky="w")


    def detect_errors(self) -> None:
        """Realiza la detección de errores y muestra el resultado"""
        info_hex = self.info.get()
        polynomial = self.polynomial.get()
        init_vector = self.init_vector.get()

        # TODO: Aquí se implementa la lógica para calcular el CRC de acuerdo a
        # los parámetros ingresados. Esto debe ser implementado en otro modulo
        # de Python. Una vez completado hay que borrar este bloque TODO: FIN del bloque
        # Invocación de la lógica.
        result = detect_errors(info_hex, polynomial, init_vector)

        # # DEBUG:
        # print(info_hex)
        # print(polynomial)
        # print(init_vector)
        # print(result)
        # # DEBUG: FIN del bloque

        # Mostrar el resultado
        self.label_result.config(text="Resultado: " + result)
