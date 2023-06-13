"""
Múdlo que define la clase MainWindow que representa la ventana principal de la
aplicación.
"""
import re

from tkinter import Frame, Button, Label, Entry, StringVar, Tk
from tkinter import Radiobutton, Event
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
        self.radio_var_format = StringVar()
        self.radio_var_format.set("binary")  # Valor por defecto
        self.pack()
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Crea y configura los widgets de la ventana principal.
        """
        label_info = Label(self, text="Información en hexadecimal:")
        label_info.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        label_polynomial_format = Label(self, text="Formato del polinomio:")
        label_polynomial_format.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        entry_info = Entry(self,
            width=30,
            textvariable=self.info,
            validate="key",
            validatecommand=(self.register(self.validate_hex_text), "%P"),
            )
        entry_info.grid(row=0, column=1, padx=10, pady=10)

        radio_binary = Radiobutton(self,
            text="Binary",
            variable=self.radio_var_format,
            value="binary",
            command=self.delete_entry_polynomial,
            )
        radio_hexadecimal = Radiobutton(self,
            text="Hexadecimal",
            variable=self.radio_var_format,
            value="hexadecimal",
            command=self.delete_entry_polynomial,
            )

        radio_binary.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        radio_hexadecimal.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        label_polynomial = Label(self, text="Polinomio:")
        label_polynomial.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.entry_polynomial = Entry(self, width=30,
            textvariable=self.polynomial,
            validate="key",
            validatecommand=(self.register(self.validate_polinomial), "%P"),
            )
        self.entry_polynomial.bind("<FocusIn>", self.update_polynomial)
        self.entry_polynomial.grid(row=2, column=1, padx=10, pady=10)

        label_init_vector = Label(self, text="Vector de inicialización:")
        label_init_vector.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.entry_init_vector = Entry(self,
            width=30,
            textvariable=self.init_vector,
            validate="key",
            validatecommand=(self.register(self.validate_init_vector), "%P"),
            )
        self.entry_init_vector.grid(row=3, column=1, padx=10, pady=10)

        button_check = Button(self, text="Verificar", command=self.detect_errors)
        button_check.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.label_result = Label(self, text="Resultado:")
        self.label_result.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    def validate_hex_text(self, new_value: str) -> bool:
        """Valida la entrada de información en formato hexadecimal"""
        # Verifica que la cadena esté en formato hexadecimal
        if re.match(r"^[0-9a-fA-F]*$", new_value):
            return True

        return False
        
    def delete_entry_polynomial(self):
        """Limpia el campo del polinomio"""
        self.entry_polynomial.delete(0, 'end')
        self.entry_init_vector.delete(0, 'end')

    def validate_polinomial(self, new_value: str) -> bool:
        """Valida el polinomio CRC"""
        if self.radio_var_format.get() == "binary":
            # Validación en formato binario
            if re.match(r"^[01]*$", new_value):
                return True
        elif self.radio_var_format.get() == "hexadecimal":
            # Validación en formato hexadecimal
            if re.match(r"^[0-9a-fA-F]*$", new_value):
                return True

        return False
    
    def update_polynomial(self, event=None) -> None:
        """Actualiza el campo del polinomio y borra el campo del vector de inicialización"""
        self.entry_init_vector.delete(0, "end")

    # NOTE: causa problemas si el campo de del polinomio está vacio.
    def validate_init_vector(self, new_value: str) -> bool:
        """Valida el vector de inicialización"""
        radio_var_format = self.radio_var_format.get()
        
        if re.match(r"^[01]*$", new_value):
            crc_polynomial = self.polynomial.get()
            
            if radio_var_format == "hexadecimal":
                # Bloquear escritura si el campo del polinomio está vacío
                if not crc_polynomial:
                    return False
                crc_binary = bin(int(crc_polynomial, 16))[2:]
                if len(new_value) <= len(crc_binary) - 1:
                    return True
            elif radio_var_format == "binary":
                # Bloquear escritura si el campo del polinomio está vacío
                if not crc_polynomial:
                    return False
                crc_binary = crc_polynomial
                if len(new_value) <= len(crc_binary) - 1:
                    return True

        return False



    def get_max_init_vector_length(self) -> int:
        """
        Obtiene la longitud máxima del vector de inicialización según el 
        tipo de CRC seleccionado
        """
        crc_polynomial = self.polynomial.get()
        if len(crc_polynomial) <= 8:
            return 8
        else:
            return 32

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
