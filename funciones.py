import numpy as np
from tkinter import messagebox  # Para ventanas emergentes
from tkinter import filedialog  # Para manejar archivos
from scipy import fft


def fft_mag(x, fs):
    """
    ------------------------
    INPUT:
    --------
    x: array de una dimensión conteniendo la señal cuya fft se busca calcular
    fs: frecuncia a la que está muestreada la señal
    ------------------------
    OUTPUT:
    --------
    f: array de una dimension con con los valores correspondientes al eje de
    frecuencias de la fft.
    mag: array de una dimensión conteniendo los valores en magnitud de la fft
    de la señal.
    """
    freq = fft.fftfreq(len(x), d=1 / fs)  # se genera el vector de frecuencias
    senial_fft = fft.fft(x)  # se calcula la transformada rápida de Fourier

    # El espectro es simétrico, nos quedamos solo con el semieje positivo
    f = freq[np.where(freq >= 0)]
    senial_fft = senial_fft[np.where(freq >= 0)]

    # Se calcula la magnitud del espectro
    mag = np.abs(senial_fft) / len(x)  # Respetando la relación de Parceval
    # Al haberse descartado la mitad del espectro, para conservar la energía
    # original de la señal, se debe multiplicar la mitad restante por dos (excepto
    # en 0 y fm/2)
    mag[1:len(mag) - 1] = 2 * mag[1:len(mag) - 1]

    return f, mag


# Función para promediar datos en tiempo real #
def RealTimeAverage(signal, ventana):
    if ventana < len(signal):
        acum = np.average(signal[len(signal)-1-ventana:len(signal)-1])
    else:
        acum = np.average(signal)
    return acum


# Función para filtrar en tiempo real
def RealTimefilter(b, a, signal, filreredSignal, i):
    acum = 0
    if len(signal) >= len(b):
        for j in range(0, len(b), 1):
            acum += b[j]*signal[i-j]
        for j in range(1, len(a), 1):
            acum += a[j]*filreredSignal[i-j]
    else:
        acum = signal[i]/1000
    return acum


def infoAdicional():
    messagebox.showinfo("Software desarrollado por Denis Genero", "Versión del sistema: 1.3")


def avisoLicencia():
    messagebox.showwarning("Licencia", "Por el momento este Software es de licencia gratuita")


def salirAplicacion(root):
    valorSalida = messagebox.askokcancel("Salir", "Desea salir de la aplicacion?")
    if valorSalida:
        root.quit()
        root.destroy()


def cerrarDocumento(root):
    valor = messagebox.askretrycancel("Reintentar", "No es posible cerrar el documento")
    if not valor:
        root.destroy()


def comienzoSoftware():
    messagebox.showinfo("Comenzar a utilizar el Software SDR", "Para utilizar el software debe seguir"
                                                                    " los siguientes pasos:  \n\r"
                                                                    "1- Asegurese de que el dispositivo esté encendido:\n\r"
                                                                    "Verifique que el led del dispositivo esté encendido. \n\r"
                                                                    "2- Encienda el Bluetooth de su computadora:\n\r"
                                                                    "Empareje el dispositivo con nombre SDR-Meter (el "
                                                                    "código de emparejamiento es 1234). Solo debe "
                                                                    "realizar este paso la primera vez. Luego el dispositivo"
                                                                    " se vinculará con su computadora automáticamente, "
                                                                    "siempre y cuando el Bluetooth esté encendido. \n\r"
                                                                    "3- Complete los campos de la izquierda:\n\r"
                                                                    "Debe colocar la información del paciente y la "
                                                                    "duración del estudio. Solo este último parámetro "
                                                                    "es requerido para comenzar el estudio. Los demás "
                                                                    "campos podrá completarlos posteriormente y serán exigidos"
                                                                    " si desea guardar los resultados.\n\r"
                                                                    "4- Pulse el botón comenzar estudio:\n\r"
                                                                    "Si colocó una duración válida y el dispositivo se"
                                                                    " encuentra encendido y emparejado con su computadora"
                                                                    " en unos segundos comenzará a visualizar la información "
                                                                    " proveniente de los sensores del dispositivo en los "
                                                                    "paneles de la derecha.\n\r"
                                                                    "\n\r"
                                                                    "¡Gracias por elegirnos!")


def descCampos():
    messagebox.showinfo("Descripción de campos", "La interfaz del Software presenta dos grandes campos, el de la "
                                                 "izquierda donde se encuentran los datos, y el de la derecha donde "
                                                 "están los paneles para graficar. \n\r"
                                                 "Los datos a completar en el campo de la izquierda son:\n\r"
                                                 "- Duración (en segundos): es la cantidad de tiempo que se desea que "
                                                 "dure el estudio, expresada en segundos.\n\r"
                                                 "- Ingrese el nombre: Aquí se debe colocar el nombre del paciente. \n\r"
                                                 "- Ingrese el apellido: Aquí se debe colocar el apellido del paciente. \n\r"
                                                 "- Fecha de gestación: Se debe colocar la fecha de gestación estimada. \n\r"
                                                 "- Fecha de nacimiento: Se debe colocar la fecha de nacimiento. Note "
                                                 " que en caso de que esta fecha sea anterior a la de gestación el "
                                                 "sistema arrojará un error.\n\r"
                                                 "Los datos mencionados anteriormente serán solicitados en carácter "
                                                 "obligatorio para guardar el estudio. \n\r"
                                                 "- Observaciones: destinado a cualquier anotación o descripción adicional"
                                                 " que se necesite o se destaque en el estudio.\n\r"
                                                 "- Comenzar: Pulse en este botón para comenzar el estudio. El único"
                                                 " dato que se requiere para esto es la duración. El resto puede"
                                                 " completarlos posteriormente. \n\r"
                                                 "- Cancelar: Pulse este botón si desea cancelar el estudio que se está"
                                                 " desarrollando. Solo estará disponible si hay un estudio en curso.\n\r"
                                                 "- Ampliar grafico: Solo se activará luego de haber finalizado con "
                                                 "éxito un estudio. "
                                                 "Al presionar este botón, se abrira una nueva ventana más amplia, donde"
                                                 " podrá analizar con más detalle las señales registradas.\n\r"
                                                 "- Consola: Arroja información sobre el funcionamiento del software y"
                                                 " el dispositivo.\n\r"
                                                 "\n\r"
                                                 "¡Gracias por elegirnos!")


def descPestanias():
    messagebox.showinfo("Descripción de pestañas", "En la cabezera del software podrá encontrar 3 pestañas: \n\r"
                                                   "- Archivo: dentro de esta pestaña encontrará 3 opciones:\n\r"
                                                   "    1- Guardar estudio: una vez realizado el estudio y completada la\n\r"
                                                   "    información solicitada, podrá guardar todos los datos en su \n\r"
                                                   "    computadora con esta opción. \n\r"
                                                   "    2- Cargar estudio: si desea volver a revisar algún estudio previo \n\r"
                                                   "    esta opción le permitirá navegar por sus archivos hasta encontrar \n\r "
                                                   "    el estudio que necesite visualizar.\n\r"
                                                   "    3- Nuevo estudio: en caso de que quiera repetir un estudio, esta \n\r"
                                                   "    opción le permitirá borrar toda la información que observa en la \n\r"
                                                   "    pantalla de manera rápida.\n\r"
                                                   "    4- Salir: esta opción le permitirá salir de la aplicación.\n\r"
                                                   "- Dispositivo: aquí encontrará 2 opciones:\n\r"
                                                   "    1- Información del dispositivo: podrá obtener información sobre \n\r"
                                                   "    el estado del dispositivo, luego de efectuar un estudio.\n\r"
                                                   "    2- Apagar dispositivo: en caso de que se desee el dispositivo puede \n\r"
                                                   "    ser apagado desde el software.\n\r"
                                                   "- Ayuda: aquí se encuentran:\n\r"
                                                   "    1- Comenzar a usar el Software: es una guía rápida para comenzar \n\r"
                                                   "    un estudio.\n\r"
                                                   "    2- Descripción de pestañas: podra visualizar este documento.\n\r"
                                                   "    3- Descripción de campos: brinda información de lo que usted ve \n\r "
                                                   "    en pantalla.\n\r"
                                                   "    4- Licencia: muestra información de la licencia del Software.\n\r"
                                                   "    5- Versión del sistema: muestra la versión actual del Software.\n\r"
                                                   "\n\r"
                                                   "¡Gracias por elegirnos!")


def validarNum(numero):
    try:
        float(numero)
        return True
    except ValueError:
        return False
