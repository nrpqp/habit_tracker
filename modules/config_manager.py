import os
import json
import tkinter as tk
from tkinter import messagebox

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", config_file)

    def load_config(self):
        """
        Carga la configuración del archivo JSON si existe.
        """
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as file:
                return json.load(file)
        return None

    def save_config(self, habits):
        """
        Guarda la configuración inicial con los hábitos y metas.
        """
        with open(self.config_file, "w") as file:
            json.dump(habits, file, indent=4)

    def setup_initial_config_gui(self):
        """
        Interfaz gráfica para configurar los hábitos iniciales.
        """
        self.window = tk.Tk()
        self.window.title("Configuración Inicial - Rastreador de Hábitos")
        tk.Label(self.window, text="✨ Configura tus hábitos ✨", font=("Arial", 14)).pack(pady=10)

        self.entries = []
        for i in range(3):
            frame = tk.Frame(self.window)
            frame.pack(pady=5)
            tk.Label(frame, text=f"Hábito {i+1}: ").grid(row=0, column=0)
            name_entry = tk.Entry(frame, width=20)
            name_entry.grid(row=0, column=1)
            tk.Label(frame, text="Letra: ").grid(row=0, column=2)
            letter_entry = tk.Entry(frame, width=5)
            letter_entry.grid(row=0, column=3)
            tk.Label(frame, text="Meta días (21-31): ").grid(row=0, column=4)
            goal_entry = tk.Entry(frame, width=5)
            goal_entry.grid(row=0, column=5)
            self.entries.append((name_entry, letter_entry, goal_entry))

        tk.Button(self.window, text="Guardar Configuración", command=self.save_config_gui).pack(pady=10)
        self.window.mainloop()

    def save_config_gui(self):
        """
        Guarda los hábitos ingresados por el usuario desde la interfaz.
        """
        habits = {}
        for i, (name_entry, letter_entry, goal_entry) in enumerate(self.entries):
            name = name_entry.get().strip()
            letter = letter_entry.get().strip().upper()
            goal = goal_entry.get().strip()

            if not name:
                continue
            if len(letter) != 1 or not letter.isalpha():
                messagebox.showerror("Error", f"Letra para el hábito {i+1} no válida.")
                return
            if not goal.isdigit() or not (21 <= int(goal) <= 31):
                messagebox.showerror("Error", f"Meta de días para el hábito {i+1} no válida (21-31).")
                return

            habits[letter] = {"name": name, "goal_days": int(goal), "completed_days": 0}

        if not habits:
            messagebox.showerror("Error", "Debes ingresar al menos un hábito.")
            return

        self.save_config(habits)
        messagebox.showinfo("Éxito", "Configuración guardada correctamente. Reinicia el programa.")
        self.window.destroy()
