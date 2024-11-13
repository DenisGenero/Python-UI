from tkinter import Entry, Text, Label, Scrollbar
import tkinter.ttk


class parameters_t():
    # Set up parameters
    SetupVoltage = Entry
    SetupTime = Entry
    # Signal parameters
    Signal = tkinter.ttk.Combobox
    Vmax = Entry
    Vmin = Entry
    Slope = Entry
    Repetition = Entry
    Commentaries = Text

    def __init__(self):
        return None

    def showLeftPanel(self, frame):
        init_row = 0
        col_span = 3
        # ------------------------------ Left Panel ------------------------------ #
        titleLabel = Label(frame, text="Señal de excitación", bg="grey", fg="white", font=("Arial", 16))
        titleLabel.grid(row=init_row, column=0, columnspan=col_span, pady=(20, 5), sticky="we")
        init_row += 1

        # ------------------------------ Parámetros de Set Up ------------------------------ #
        SetUpLabel = Label(frame, text="Parámetros iniciales", bg="blue", fg="white", font=("Arial", 14))
        SetUpLabel.grid(row=init_row, column=0, columnspan=col_span, pady=(10, 1), sticky="we")
        init_row += 1

        SetUpLabel = Label(frame, text="Potencial", bg="#eee", font=12)
        SetUpLabel.grid(row=init_row, column=0, columnspan=1, pady=(10, 1), sticky="w", padx=(10, 5))

        self.SetupVoltage = Entry(frame, font=12, bg="white", width=10)
        self.SetupVoltage.insert(0, "50")
        self.SetupVoltage.grid(row=init_row, column=1, padx=(10, 5), sticky="w")

        SetupPotmV = Label(frame, text="mV", bg="#eee", font=12)
        SetupPotmV.grid(row=init_row, column=2, columnspan=1, pady=(10, 5), sticky="w", padx=(10, 5))
        init_row += 1

        SetUpLabeltime = Label(frame, text="Tiempo de inicio", bg="#eee", font=12)
        SetUpLabeltime.grid(row=init_row, column=0, columnspan=1, pady=(10, 1), sticky="w", padx=(10, 5))

        self.SetupTime = Entry(frame, font=12, bg="white", width=10)
        self.SetupTime.insert(0, "500")
        self.SetupTime.grid(row=init_row, column=1, padx=(10, 5), sticky="w")

        SetupTimemSeg = Label(frame, text="mSeg", bg="#eee", font=12)
        SetupTimemSeg.grid(row=init_row, column=2, columnspan=1, pady=(10, 5), sticky="w", padx=(10, 5))
        init_row += 1
        # ------------------------------ Parámetros de Set Up ------------------------------ #

        # ------------------------------ Parámetros de señal ------------------------------ #
        SignalLabel = Label(frame, text="Parámetros de señal", bg="green", fg="white", font=("Arial", 14))
        SignalLabel.grid(row=init_row, column=0, columnspan=col_span, pady=(10, 1), sticky="we")
        init_row += 1

        senialLabel = Label(frame, text="Señal", bg="#eee", font=12)
        senialLabel.grid(row=init_row, column=0, columnspan=1, pady=(10, 1), sticky="w", padx=(10, 5))

        self.Signal = tkinter.ttk.Combobox(frame, state="readonly", width=10)
        self.Signal["values"] = ("Triangular", "Rampa positiva", "Rampa negativa")  # "Cuadrada"
        self.Signal.current(0)
        self.Signal.grid(row=init_row, column=1, columnspan=1, pady=(10, 5), sticky="we", padx=(10, 5))
        init_row += 1

        VmaxLabel = Label(frame, text="Voltaje máximo", bg="#eee", font=12)
        VmaxLabel.grid(row=init_row, column=0, columnspan=1, pady=(10, 5), sticky="w", padx=(10, 5))

        self.Vmax = Entry(frame, font=12, bg="white", width=10)
        self.Vmax.insert(0, "500")
        self.Vmax.grid(row=init_row, column=1, padx=(10, 5), sticky="w")

        SigVmaxLab = Label(frame, text="mV", bg="#eee", font=12)
        SigVmaxLab.grid(row=init_row, column=2, columnspan=1, pady=(10, 5), sticky="w", padx=(10, 5))
        init_row += 1

        VminLabel = Label(frame, text="Voltaje mínimo", bg="#eee", font=12)
        VminLabel.grid(row=init_row, column=0, columnspan=1, pady=(10, 5), sticky="w", padx=(10, 5))

        self.Vmin = Entry(frame, font=12, bg="white", width=10)
        self.Vmin.insert(0, "-500")
        self.Vmin.grid(row=init_row, column=1, padx=(10, 5), sticky="w")

        SigVminLab = Label(frame, text="mV", bg="#eee", font=12)
        SigVminLab.grid(row=init_row, column=2, columnspan=1, pady=(10, 5), sticky="w", padx=(10, 5))
        init_row += 1

        PendienteLabel = Label(frame, text="Pendiente", bg="#eee", font=12)
        PendienteLabel.grid(row=init_row, column=0, columnspan=1, pady=(10, 5), sticky="w", padx=(10, 5))

        self.Slope = Entry(frame, font=12, bg="white", width=5)
        self.Slope.insert(0, "100")
        self.Slope.grid(row=init_row, column=1, padx=(10, 5), sticky="w")

        PendienteLabel = Label(frame, text="mV/seg.", bg="#eee", font=12)
        PendienteLabel.grid(row=init_row, column=2, columnspan=1, pady=(10, 5), sticky="w", padx=(10, 5))
        init_row += 1

        RepeticionesLabel = Label(frame, text="Repeticiones", bg="#eee", font=12)
        RepeticionesLabel.grid(row=init_row, column=0, columnspan=1, pady=(10, 5), sticky="w", padx=(10, 5))

        self.Repetition = Entry(frame, font=12, bg="white", width=5)
        self.Repetition.insert(0, "2")
        self.Repetition.grid(row=init_row, column=1, padx=(10, 5), sticky="w")
        init_row += 1
        # ------------------------------ Parámetros de señal ------------------------------ #

        labelObserv = Label(frame, text="Observaciones", font=12)
        labelObserv.grid(row=init_row, column=0, sticky="w", pady=(20, 5), padx=(10, 20))
        init_row += 1

        self.Commentaries = Text(frame, height=3, font=11)
        self.Commentaries.grid(row=init_row, column=0, columnspan=col_span, sticky="w", padx=(10, 20))
        scrollVert = Scrollbar(frame, command=self.Commentaries.yview)
        scrollVert.grid(row=init_row, column=col_span - 1, sticky="e")
        scrollVert.config(cursor="arrow", width=20)
        self.Commentaries.config(yscrollcommand=scrollVert.set)
        init_row += 1

        return init_row

