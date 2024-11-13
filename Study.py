import json
from tkinter import messagebox, Scale


# Signal object:
class study_t:
    MaxVoltage = 3300
    RefVoltage = 1650
    MinVoltage = 0
    # Set up parameters
    SetupVoltage = 0
    SetupTime = 0
    # Signal parameters
    Signal = ""
    Vmax = ""
    Vmin = ""
    Slope = " "
    Repetition = ""
    Commentaries = ""
    # Readings
    FirstRep = [[]]
    SecondRep = [[]]
    ThirdRep = [[]]
    FourthRep = [[]]
    FifthRep = [[]]

    def __init__(self):
        self.Signal = "Triangular"

    def ingresar_datos(self, parametros):
        try:
            self.SetupVoltage = int(parametros.SetupVoltage.get()) + self.RefVoltage
        except Exception:
            messagebox.showerror("Error", "Campo 'Potencial' inválido.")
            return False
        if self.SetupVoltage < self.MinVoltage:
            messagebox.showerror("Error", "El voltaje mínimo admitido es: " + str(self.MinVoltage - self.RefVoltage) + " mV.")
            return False
        if self.SetupVoltage > self.MaxVoltage:
            messagebox.showerror("Error", "El voltaje máximo admitido es: " + str(self.MaxVoltage - self.RefVoltage) + " mV.")
            return False
        try:
            self.SetupTime = int(parametros.SetupTime.get())
        except Exception:
            messagebox.showerror("Error", "Campo 'Tiempo de inicio' inválido.")
            return False
        try:
            Senial = str(parametros.Signal.get())
            if Senial == "Triangular":
                self.Signal = 1
            elif Senial == "Rampa positiva":
                self.Signal = 2
            elif Senial == "Rampa negativa":
                self.Signal = 3
        except Exception:
            messagebox.showerror("Error", "Campo 'Señal' inválido.")
            return False
        try:
            self.Vmax = int(parametros.Vmax.get()) + self.RefVoltage
        except Exception:
            messagebox.showerror("Error", "Campo 'Voltaje máximo' inválido.")
            return False
        if self.Vmax > self.MaxVoltage:
            messagebox.showerror("Error", "El voltaje máximo admitido es: " + str(self.MaxVoltage - self.RefVoltage) + " mV.")
            return False
        try:
            self.Vmin = int(parametros.Vmin.get()) + self.RefVoltage
        except Exception:
            messagebox.showerror("Error", "Campo 'Voltaje mínimo' inválido.")
            return False
        if self.Vmin < self.MinVoltage:
            messagebox.showerror("Error", "El voltaje mínimo admitido es: " + str(self.MinVoltage - self.RefVoltage) + " mV.")
            return False
        try:
            self.Slope = int(parametros.Slope.get())
        except Exception:
            messagebox.showerror("Error", "Campo 'Pendiente' inválido.")
            return False
        try:
            self.Repetition = int(parametros.Repetition.get())
        except Exception:
            messagebox.showerror("Error", "Campo 'Repeticiones' inválido.")
            return False
        try:
            self.Commentaries = str(parametros.Commentaries.get("1.0", "end -1c"))
        except Exception:
            messagebox.showerror("Error", "Campo 'Comentarios' inválido.")
            return False
        if self.Vmin > self.Vmax:
            messagebox.showerror("Error", "Voltaje máximo menor que Voltaje mínimo.")
            return False
        if self.Repetition > 5 or self.Repetition <= 0:
            messagebox.showwarning("Advertencia", "El número mínimo de repeticiones es 1 y el máximo es 5.")
            return False
        return True

    def cargar_seniales(self, tiempo, presion, resp, deglucion):
        self.t = tiempo
        self.pressure_signal = presion
        self.breath_signal = resp
        self.swallow_signal = deglucion
        return True

    def save(self, filename):
        data = {
                "duration": self.duracion,
                "name": self.nombre,
                "lastname": self.apellido,
                "gestation": self.gestacion,
                "birth": self.nacimiento,
                "actual_date": self.fecha_estudio,
                "comment": self.comentarios,
                "temp": self.t,
                "pressure": self.pressure_signal,
                "breath": self.breath_signal,
                "swallow": self.swallow_signal
                }
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load(self, filename):
        with open(filename) as f:
            data = json.load(f)
            self.duracion = data["duration"]
            self.nombre = data["name"]
            self.apellido = data["lastname"]
            self.gestacion = data["gestation"]
            self.nacimiento = data["birth"]
            self.fecha_estudio = data["actual_date"]
            self.comentarios = data["comment"]
            self.t = data["temp"]
            self.pressure_signal = data["pressure"]
            self.breath_signal = data["breath"]
            self.swallow_signal = data["swallow"]
