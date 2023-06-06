<!-- Documentación del proyecto -->
# Práctica 3 - Códigos de redundancia cíclica

<!--
## Descripción
Placeholder

## Objetivos

* Placeholder
* Placeholder
-->

## Programa 1:

1. Diseñar un programa que permita la implementación de los siguientes CRC:

* CRC-8  para Bluetooth:
  * x^{8}+x^{7}+x^{5}+x^{2}+x+1

* CRC-32 para 802.3
--* x^{{32}}+x^{{26}}+x^{{23}}+x^{{22}}+x^{{16}}+x^{{12}}+x^{{11}}+x^{{10}}+x^{8}+x^{7}+x^{5}+x^{4}+x^{2}+x+1

Además, se le debe proporcionar un vector de inicialización para cada elemento del registro de corrimiento.

2. El programa deberá permitir seleccionar el tipo de código a implementar.  
3. El programa gráfica deberá permitir escribir una cadena de texto de no más de 32 caracteres (ASCII).
4. El programa deberá desplegar el código CRC de la información proporcionada (cadena ASCII).
5. El programa deberá desplegar la información códificada en hexadecimal mensaje+CRC (en hexadecimal)


## Programa 2:

El programa debe efectuar la detección de errores, al programa se le debe de proporcionar una cadena en hexadecimal con la información a decodificar, se le debe proporcionar el polinomio a utilizar (en forma de una cadena de bits o hexadecimal) y un vector de inicialización.

Dada la información proporcionada, el programa debe determinar si la cadena posee errores o no.

<!--
## Requerimentos

* Requiere instalar la biblioteca Pyserial
```console
pip install pyserial
```

## Dispositivos conectados el puerto serial

Para identificar los dispositivos conectados se ejecuta en consola:
```console
python -m serial.tools.list_ports
```

## Como usar
1. Placeholder 1
2. Placeholder 2
3. Placeholder 3
-- >
