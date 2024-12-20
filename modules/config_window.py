import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys

class ConfigWindow:
    def __init__(self, manager, refresh_callback):
        """
        Inicializa la ventana de configuración.
        """
        self.window = tk.Toplevel()
        self.window.title("Configuración de Hábitos")
        self.manager = manager
        self.refresh_callback = refresh_callback

        # Encabezado
        tk.Label(self.window, text="Configuración de Hábitos", font=("Arial", 14, "bold")).pack(pady=10)

        # Sección: Eliminar o actualizar hábitos
        tk.Label(self.window, text="Eliminar o actualizar hábitos existentes:", font=("Arial", 12, "underline")).pack(pady=5)
        self.habit_frame = tk.Frame(self.window)
        self.habit_frame.pack(pady=5)

        self.load_habit_list()

        # Separador
        ttk.Separator(self.window, orient="horizontal").pack(fill="x", pady=10)

        # Sección: Crear un nuevo hábito
        tk.Label(self.window, text="Crear un nuevo hábito:", font=("Arial", 12, "underline")).pack(pady=5)

        tk.Label(self.window, text="Nombre del nuevo hábito:").pack(pady=2)
        self.new_habit_name = tk.Entry(self.window, width=30)
        self.new_habit_name.pack(pady=5)

        tk.Label(self.window, text="Letra identificadora (única):").pack(pady=2)
        self.new_habit_letter = tk.Entry(self.window, width=5)
        self.new_habit_letter.pack(pady=5)

        tk.Button(self.window, text="Crear Hábito", command=self.create_habit).pack(pady=10)

        # Separador
        ttk.Separator(self.window, orient="horizontal").pack(fill="x", pady=10)

        # Sección: Ejecución Automática
        tk.Label(self.window, text="Ejecución Automática:", font=("Arial", 12, "underline")).pack(pady=5)

        self.auto_run_var = tk.BooleanVar(value=self.manager.data.get("auto_run", False))
        tk.Checkbutton(
            self.window,
            text="Habilitar ejecución automática",
            variable=self.auto_run_var
        ).pack(pady=5)

        time_frame = tk.Frame(self.window)
        time_frame.pack(pady=5)
        self.hour_var = tk.StringVar(value=self.manager.data.get("auto_run_hour", "23:00").split(":")[0])
        self.minute_var = tk.StringVar(value=self.manager.data.get("auto_run_hour", "23:00").split(":")[1])

        tk.Label(time_frame, text="Hora:").grid(row=0, column=0, padx=5)
        hour_combobox = ttk.Combobox(
            time_frame, textvariable=self.hour_var, values=[f"{h:02}" for h in range(24)], width=5, state="readonly"
        )
        hour_combobox.grid(row=0, column=1, padx=5)
        tk.Label(time_frame, text="Minutos:").grid(row=0, column=2, padx=5)
        minute_combobox = ttk.Combobox(
            time_frame, textvariable=self.minute_var, values=[f"{m:02}" for m in range(0, 60, 5)], width=5, state="readonly"
        )
        minute_combobox.grid(row=0, column=3, padx=5)

        tk.Button(self.window, text="Aplicar", command=self.apply_settings).pack(pady=10)

    def load_habit_list(self):
        """
        Carga la lista de hábitos con botones de eliminar y editar.
        """
        for widget in self.habit_frame.winfo_children():
            widget.destroy()

        for letter, habit in self.manager.data["habits"].items():
            frame = tk.Frame(self.habit_frame)
            frame.pack(anchor="w", pady=2)

            tk.Label(frame, text=f"{habit['name']} (Meta: {habit['goal_days']} días)", width=30, anchor="w").pack(side="left")
            tk.Button(frame, text="🗑️", command=lambda l=letter: self.delete_habit(l), width=3).pack(side="left", padx=5)
            tk.Button(frame, text="✏️", command=lambda l=letter: self.open_edit_window(l), width=3).pack(side="left")

    def delete_habit(self, letter):
        """
        Elimina un hábito seleccionado y actualiza la ventana principal.
        """
        del self.manager.data["habits"][letter]
        self.manager.save()
        self.refresh_callback()  # Refresca la ventana principal
        self.load_habit_list()
        messagebox.showinfo("Éxito", "Hábito eliminado correctamente.")

    def create_habit(self):
        """
        Crea un nuevo hábito y actualiza la ventana principal.
        """
        name = self.new_habit_name.get().strip()
        letter = self.new_habit_letter.get().strip().upper()

        if len(letter) != 1 or letter in self.manager.data["habits"]:
            messagebox.showerror("Error", "Letra inválida o ya existente.")
            return

        self.manager.add_habit(letter, name)
        self.manager.save()
        self.refresh_callback()  # Refresca la ventana principal
        self.load_habit_list()
        messagebox.showinfo("Éxito", f"Hábito '{name}' creado.")

    def apply_settings(self):
        """
        Aplica la configuración de ejecución automática y la hora seleccionada.
        """
        enabled = self.auto_run_var.get()
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        self.manager.data["auto_run"] = enabled
        self.manager.data["auto_run_hour"] = f"{hour}:{minute}"
        self.manager.save()
        if enabled:
            self.schedule_task(hour, minute)
        messagebox.showinfo("Éxito", "Configuración aplicada correctamente.")

    def schedule_task(self, hour, minute):
        """
        Programa el Rastreador de Hábitos en Windows Task Scheduler.
        """
        program_path = os.path.abspath("main.py")
        task_name = "RastreadorHabitos"
        time = f"{hour}:{minute}"
        subprocess.run([
            "schtasks", "/Create", "/F", "/SC", "DAILY",
            "/TN", task_name, "/TR", f"python {program_path}",
            "/ST", time
        ], shell=True)

    def restart_application(self):
        """
        Reinicia la aplicación.
        """
        python = sys.executable
        os.execl(python, python, *sys.argv)
