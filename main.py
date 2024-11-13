from datetime import time

import numpy as np

from Study import study_t
from Parameters import parameters_t
from tkinter import *
import scipy as sc
# import json
from tkinter import Tk, Frame, Label
from tkinter import messagebox  # Para ventanas emergentes
import serial
from serial.tools import list_ports
import funciones
import matplotlib.pyplot as plt
# from tkcalendar import Calendar
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)  # , NavigationToolbar2Tk)
from SerialCommands import *

# Global variable for study
paciente0 = study_t()


def ConsoleSendCommand(strVar):
    global raiz
    clear_command = "                                                                                                \r"
    estado.set(clear_command)
    raiz.update_idletasks()
    estado.set(strVar)
    raiz.update_idletasks()


# -------------------------- Global graphic panel --------------------------
# Figure and axis declaration
y_min = -4.5
y_max = 4.5
x_min = -1650  # mV
x_max = 1650  # mV


fig, ax0 = plt.subplots(1, 1, figsize=(10, 10), facecolor='white')
plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.1)

ax0.cla()

# Excitation time evolution
ax0.set_ylabel("Corriente uA")
ax0.set_ylim([y_min, y_max])
ax0.set_ylim(auto=True)
ax0.set_xlabel("Potencial (mV)")
ax0.set_xlim([x_min, x_max])
ax0.xaxis.set_ticks_position('bottom')
ax0.yaxis.set_ticks_position('left')

fig.tight_layout()

fig.canvas.draw()
fig.canvas.flush_events()

background = fig.canvas.copy_from_bbox(fig.bbox)
background1 = fig.canvas.copy_from_bbox(ax0.bbox)

# -------------------------- Global graphic panel --------------------------


# -------------------------- Button Handle functions --------------------------

def cancelEjec():
    global ejecucion
    ejecucion = False


def checkStudioBeg():
    global param

    # check for parameters
    if not paciente0.ingresar_datos(param):
        return False

    # Time calculation
    # First iteration:
    time = paciente0.SetupTime/1000 + (paciente0.Vmax - paciente0.SetupVoltage)/paciente0.Slope \
        + (paciente0.Vmax - paciente0.Vmin)/(paciente0.Slope*1000)
    # The rest of iterations
    if paciente0.Repetition > 1:
        time += 2*(paciente0.Repetition - 1)*(paciente0.Vmax-paciente0.Vmin)/paciente0.Slope

    seconds = int(time % 60)
    showtime = str(seconds)
    showunit = " segundos"
    if time > 60:
        minutes = int(time/60)
        showtime = str(minutes) + ":" + str(seconds)
        showunit = " minutos"

    valorSalida = messagebox.askokcancel("Comenienzo del estudio", "El estudio tendrá una duración total aproximada de "
                                         + showtime + showunit +". ¿Desea continuar?")
    if valorSalida:
        realTimeAdq()
    else:
        return False

# -------------------------- Buttons Handle functions --------------------------


# -------------------------- Real-time adquisition function --------------------------

def realTimeAdq():

    global ejecucion, paciente0

    # ------------ Real-time plot configuration ------------ #
    fig.tight_layout()
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.1, hspace=0.1)

    ax0.cla()
    x_min = (paciente0.Vmin - 1650)*1.25
    x_max = (paciente0.Vmax - 1650)*1.25
    ax0.set_ylabel("Corriente [uA]")
    ax0.set_ylim([y_min, y_max])
    ax0.set_ylim(auto=True)
    ax0.set_xlabel("Potencial [mV]")
    ax0.set_xlim([x_min, x_max])
    fig.tight_layout()
    plt.close('all')

    fig.canvas.draw()
    fig.canvas.flush_events()
    # ------------ Real-time plot configuration ------------ #

    # Value for serial data synchronization: new data line detection
    NewLine = 12337  # must be '0' for msb and '1' for lsb

    # Disable button
    btnComenzar.config(state="disable")

    # Console update: communication beginning indication
    ConsoleSendCommand("Iniciando comunicación con el dispositivo... \n\r")

    # List of available communication ports
    comm_ports = [comport.device for comport in serial.tools.list_ports.comports()]
    # Define com port variable
    ser = 0

    # Define variable to get serial data
    num = 0
    # Execution conditions
    stop_condition = 115  # 's'
    end_condition = 101   # 'e'

    btnCancelar.config(state="normal")

    # ----------------------------------- Connection attempt -----------------------------------
    # Detection of the correct COM port
    for cp in range(len(comm_ports)-1, -1, -1):
        connectionStablished = False
        # Serial port configuration
        # 10 milliseconds timeout: 100Hz sampling rate
        if len(comm_ports) == 0:
            ConsoleSendCommand("ERROR: Reinicie el dispositivo e intente de nuevo...\r")
            btnCancelar.config(state="disable")
            btnComenzar.config(state="normal")
            return False

        else:
            ConsoleSendCommand("Intentando conectar con el puerto: " + comm_ports[cp] + "\r")
            try:
                ser = serial.Serial(port=comm_ports[cp], baudrate=115200, timeout=0.1, writeTimeout=1)
                ser.set_buffer_size(rx_size=(2**16), tx_size=(2**16))  # both buffers with 8.192 Kb (2^16 bits)
                SendStarCommand2uC(ser)
                connectionStablished = True
            except serial.SerialException:
                ConsoleSendCommand("Puerto sin respuesta\r")
                plt.pause(1)

        # Serial port setup pause
        plt.pause(1)
        num = 0

        if connectionStablished:
            # First attempt of data acquisition (2 bytes):
            num = ReadByteFromuC(ser)
            num = num << 8
            num = num + ReadByteFromuC(ser)

        # If port sends the check signal, select it
        if num == NewLine:
            ConsoleSendCommand("Comunicación establecida en el puerto: " + comm_ports[cp] + ". \r")
            ser.inter_byte_timeout = 0.0001
            break

    # If no COM port available indicate an error
    if num != NewLine:
        ConsoleSendCommand("ERROR: La conexión con el dispositivo no fue establecida... \n\r")
        plt.pause(2)
        ConsoleSendCommand("Revise si el Bluetooth está encendido y el dispositivo emparejado.\r")
        messagebox.showerror("Error en la conexión con el dispositivo", "Revise si el Bluetooth está encendido y el dispositivo emparejado.")
        ConsoleSendCommand("El Software nPOC está listo.\r")
        btnCancelar.config(state="disable")
        btnComenzar.config(state="normal")
        return False
    # ----------------------------------- Connection attempt ----------------------------------- #

    # ----------------------------------- Acquisition and processing algorithm ----------------------------------- #
    # Send signal parameters:
    SendParameters2uC(paciente0, ser)
    plt.pause(1)
    # Storage for incoming data
    # Sample ID
    samples = [], [], [], [], []
    # Voltage from reference electrode
    Vre = [], [], [], [], []
    # Voltage from working electrode
    Vwe = [], [], [], [], []
    filt_Vwe = [], [], [], [], []
    # Excitation voltage applied
    Vexc = [], [], [], [], []
    # Estimated current
    Imeasured = [], [], [], [], []

    line_color = 'red'

    repetition = 0
    new_repetition = False

    # Voltage to current conversion factor
    V_Ifactor = 365

    # Index for axis adjustments
    Axisindex = 0
    AxisRefreshRate = 10
    YLimSup = 0
    YlimInf = 0

    # Factors to convert ADC readings
    SourceVoltage = 3300
    virtualReference = int(SourceVoltage/2)
    ADC_bits = 12
    ADC_steps = 2**ADC_bits - 1

    # Index for filtered data
    filt_index = 0
    sample_index = 0
    time_line = 0

    # Real time filter specs
    Window_size = 20

    # Amount of byte to be received
    data_package_size = 11

    while repetition != stop_condition and repetition != end_condition:
        # Ask if new data is available
        if ser.inWaiting() >= data_package_size:
            # See how many packages are available
            bytes_available = ser.inWaiting() - ser.inWaiting() % data_package_size
            package2read = int(bytes_available/data_package_size)

            for h in range(0, package2read, 1):
                # ---------------------- Data reconstruction ---------------------- #
                # Milli seconds passed
                time_line += 10
                #                     Id Vr Vw Ve Rep
                reconstructed_data = [0, 0, 0, 0, 0]
                try:
                    # Read package coming from uC:
                    readPackageFromuC(ser, reconstructed_data)
                except serial.SerialException:
                    ConsoleSendCommand("Ocurrió un problema al leer datos desde el dispositivo.")
                    return False
                if reconstructed_data[4] > repetition:
                    new_repetition = True
                    sample_index = 0
                repetition = reconstructed_data[4]
                # ---------------------- Data reconstruction ---------------------- #

                # ---------------------- End condition detection ---------------------- #
                if repetition == stop_condition:
                    cancelEjec()
                # ---------------------- End condition detection ---------------------- #

                # ---------------------- Data reorganization ---------------------- #
                elif repetition != end_condition and time_line > paciente0.SetupTime:
                    # Sample ID
                    samples[repetition].append(reconstructed_data[0])
                    # Working electrode measure: convert ADC counts into voltage
                    voltage = int(reconstructed_data[1] * SourceVoltage / ADC_steps) - virtualReference
                    Vwe[repetition].append(voltage)
                    # Reference electrode measure: convert ADC counts into voltage
                    voltage = int((reconstructed_data[2] * SourceVoltage / ADC_steps) - virtualReference)
                    Vre[repetition].append(voltage)
                    # Excitation voltage applied: convert ADC counts into voltage
                    Vexc[repetition].append(reconstructed_data[3] - virtualReference)
                    # ---------------------- Data reorganization ---------------------- #

                    # ---------------------- Filtering ---------------------- #
                    # New repetition detection
                    if new_repetition and filt_index >= len(Vwe[0]) - 1:
                        new_repetition = False
                        filt_index = 0
                    # First and end part of current estimation: not applying filtering
                    if filt_index <= Window_size/2 or sample_index < (Window_size / 2 + 1):
                        # Estimated current
                        Imeasured[repetition].append(Vwe[repetition][-1]/V_Ifactor)
                        filt_index += 1
                    # Middle part of current estimation: applying filtering
                    if sample_index > (Window_size / 2 + 1):
                        acum = []
                        for k in range(sample_index - Window_size, sample_index, 1):
                            acum.append(Vwe[repetition][k])
                        acum = np.mean(acum)  # Moving average
                        # acum = np.median(acum) # Median filter
                        filt_Vwe[repetition].append(acum)
                        Imeasured[repetition].append(acum/V_Ifactor)
                        filt_index += 1
                    # ---------------------- Filtering ---------------------- #

                    # ---------------------- Axis adjustment ---------------------- #
                    Axisindex += 1
                    if Axisindex >= AxisRefreshRate:
                        Axisindex = 0
                        # First iteration
                        if AxisRefreshRate == 10:
                            Ymin = min(Imeasured[repetition])
                            Ymax = max(Imeasured[repetition])
                            YlimInf = 1.5 * Ymin
                            YLimSup = 1.5 * Ymax
                            AxisRefreshRate = 100
                        # Rest of iterations
                        if min(Imeasured[repetition]) < Ymin:
                            Ymin = min(Imeasured[repetition])
                            YlimInf = 1.5 * Ymin
                        if max(Imeasured[repetition]) > YLimSup:
                            Ymax = max(Imeasured[repetition])
                            YLimSup = 1.5 * Ymax
                        # Update Y axis
                        ax0.set_ylim(YlimInf, YLimSup)
                        fig.tight_layout()
                        fig.canvas.draw()
                        fig.canvas.flush_events()
                    # ---------------------- Axis adjustment ---------------------- #

                    # Update samples count (for filtering purposes)
                    sample_index += 1

                    # ---------------------- Real-time plot ---------------------- #
                    # Definition: redefine all vector in every loop for
                    # not to overhead the plot process and enhance performance.

                    # Curve color per repetition
                    if repetition == 0:
                        line_color = 'red'
                    elif repetition == 1:
                        line_color = 'blue'
                    elif repetition == 2:
                        line_color = 'green'
                    elif repetition == 3:
                        line_color = 'purple'
                    elif repetition == 4:
                        line_color = 'olive'

                    # Draw every 100 samples
                    if 0 == h % 100 and filt_index > Window_size:
                        # Copy axis information
                        line1 = ax0.plot(Vexc[repetition][0:filt_index], Imeasured[repetition], color=line_color)[0]
                        # Set in line both axis data
                        line1.set_data(Vexc[repetition][0:filt_index], Imeasured[repetition])
                        # Redraw just the points
                        ax0.draw_artist(line1)
                        # Fill in the axes rectangle
                        fig.canvas.blit(ax0.bbox)
                    # ---------------------- Real-time plot ---------------------- #

            # Update canvas draw for tkinter frame
            fig.canvas.flush_events()

        # If abort is require, return to main loop
        if not ejecucion:
            ejecucion = True
            SendStopCommand2uC()
            ser.close()
            btnCancelar.config(state="disable")
            btnComenzar.config(state="normal")
            return False

    # For debug
    #tmin = filt_Vraw[0].index((min(filt_Vraw[0])))
    #tmax = filt_Vraw[0].index((max(filt_Vraw[0])))
    #fig2 = plt.scatter(Vexc[0], Vraw[0], color="red", marker=".")
    #plt.figure()
    #plt.plot(Vexc[0], Vraw[0], color="blue", marker=".", markerfacecolor="red", markersize=10)
    #plt.scatter(Vexc[0][tmin], min(Vraw[0]))
    #plt.scatter(Vexc[0][tmax], max(Vraw[0]))
    #plt.xlabel("Voltaje de excitación")
    #plt.ylabel("Voltaje leído")
    #plt.legend(["Voltaje ADC vs Voltaje de excitación", "Valor máximo: "+str(max(Vraw[0])), "Valor mínimo: "+str(min(Vraw[0]))])
    #plt.figure()
    #plt.scatter(time_vec[0][tmin], min(filt_Vraw[0]), color="green")
    #plt.scatter(time_vec[0][tmax], max(filt_Vraw[0]), color="blue")
    #plt.plot(time_vec[0][0:len(Vraw[0])], Vraw[0], color="red")
    #plt.plot(time_vec[0][0:len(filt_Vraw[0])], filt_Vraw[0], color="red")
    #plt.legend(["Voltaje ADC", "Valor máximo: " + str(max(filt_Vraw[0])),"Valor mínimo: " + str(min(filt_Vraw[0]))], prop={"size": 20})
    #plt.legend("Voltaje ADC vs Voltaje de excitación")
    #plt.xlabel("Tiempo")
    #plt.ylabel("Voltaje leído")
    #plt.title("Voltaje ADC en función del tiempo")
    #freq = sc.fft.fftfreq(len(Vraw[0]), 0.01)
    #FFT = sc.fft.fft(Vraw[0])
    #plt.figure()
    #mifreq = freq[:int(len(freq)/2)]
    #mifft = abs(FFT[:int(len(freq)/2)])
    #plt.semilogy(mifreq, mifft)
    #plt.plot(freq, abs(FFT))
    #plt.xlabel("Frecuencia")
    #plt.ylabel("Módulo")
    #plt.title("FFT del voltaje del ADC")
    #plt.show()
    # ---------------------- Measure finished ---------------------- #
    ConsoleSendCommand("El proceso terminó correctamente. Cerrando el puerto... \r")

    # Close serial port
    ser.close()
    # Change buttons states
    btnCancelar.config(state="disable")
    btnComenzar.config(state="normal")
    # Give some time to ensure port closing
    plt.pause(2)

# -------------------------- Real-time acquisition function --------------------------


# -------------------------- User Interface --------------------------

# Windows root definition
raiz = Tk()

# Start with the window maximized
raiz.state('zoomed')
raiz.wm_title("INTI - FI-UBA - nPoc V1")
raiz.config(bg="grey64")

# Define the screen width
screen_width = raiz.winfo_screenwidth()

graphic = Frame(raiz)
# Set 70% of the screen width for graphics
graphic.config(bg="white", width=screen_width * 0.7)
graphic.pack(
    fill="y",
    side=RIGHT,
    ipadx=10
)

# tkinter draw area
canvas = FigureCanvasTkAgg(fig, master=graphic)
canvas.draw()
canvas.get_tk_widget().pack()

# Frame for data
frame = Frame(raiz)
frame.config(bg="#eee", width=screen_width * 0.3)
frame.columnconfigure(index=0, weight=1)
frame.columnconfigure(index=1, weight=1)

frame.pack(
    fill="y",
    side=LEFT
)

# -------------------------- Left panel --------------------------

param = parameters_t()
init_row = param.showLeftPanel(frame)

col_span = 3

# -------------------------- Buttons --------------------------
btnComenzar = Button(frame, text="Comenzar", font=10, command=lambda: checkStudioBeg())
btnComenzar.grid(row=init_row, column=0, columnspan=1, pady=(50, 5), padx=(40, 10), sticky="w")

btnCancelar = Button(frame, text="Cancelar", font=10, state="disable", command=cancelEjec)
btnCancelar.grid(row=init_row, column=1, columnspan=1, sticky="w", pady=(50, 5), padx=(20, 0))
ejecucion = True
init_row += 1

# -------------------------- Console --------------------------
labelConsola = Label(frame, text="Consola", font=12)
labelConsola.grid(row=init_row, column=0, columnspan=2, sticky="w", pady=(30, 5), padx=(10, 20))
init_row += 1

estado = StringVar()
ConsoleSendCommand("El Software nPOC está listo. \r")
labelState = Label(frame, textvariable=estado, font=("Arial", 12), bg="#eee", fg="grey")
labelState.grid(row=init_row, columnspan=col_span, sticky="w", pady=1, padx=(10, 20))

# ------------------------------- Show load information -------------------------------
infoShow = Frame(raiz)
infoShow.config(bg="grey64", width=screen_width * 0.3)
infoShow.columnconfigure(index=0, weight=1)
infoShow.columnconfigure(index=1, weight=1)

# ------------------------------- Dropdown menu -------------------------------
barraMenu = Menu(raiz)
raiz.config(menu=barraMenu)

# ------------------------------- Interface -------------------------------
# Archivo
ArchivoMenu = Menu(barraMenu, tearoff=0)
ArchivoMenu.add_command(label="Guardar estudio")  # , command=lambda: saveStudy(raiz, estado))
ArchivoMenu.add_command(label="Cargar estudio")  # , command=lambda: abrirArchivo(raiz))
ArchivoMenu.add_command(label="Nuevo estudio")  # , command=lambda: nuevoEstudio())
ArchivoMenu.add_separator()

ArchivoMenu.add_command(label="Salir", command=lambda: funciones.salirAplicacion(raiz))

# Dispositivo
DispositivoMenu = Menu(barraMenu, tearoff=0)
DispositivoMenu.add_command(label="Información del dispositivo")
DispositivoMenu.add_command(label="Apagar dispositivo")

# Ayuda
AyudaMenu = Menu(barraMenu, tearoff=0)                       # Future implementations
AyudaMenu.add_command(label="Comenzar a usar el Software")   # , command=funciones.comienzoSoftware)
AyudaMenu.add_command(label="Descripción de pestañas")  # , command=funciones.descPestanias)
AyudaMenu.add_command(label="Descripción de campos")  # , command=funciones.descCampos)
AyudaMenu.add_separator()

AyudaMenu.add_command(label="Licencia")  # , command=funciones.avisoLicencia)
AyudaMenu.add_command(label="Versión del sistema")  # , command=funciones.infoAdicional)

barraMenu.add_cascade(label="Archivo", menu=ArchivoMenu)
barraMenu.add_cascade(label="Dispositivo", menu=DispositivoMenu)
barraMenu.add_cascade(label="Ayuda", menu=AyudaMenu)

# ----------------------------------------------------------------------
raiz.mainloop()
