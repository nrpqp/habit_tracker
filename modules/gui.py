import tkinter as tk
from tkinter import ttk, messagebox
from modules.config_window import ConfigWindow

class HabitTrackerGUI:
    def __init__(self, manager, habits_config):
        """
        Inicializa la interfaz principal.
        """
        self.manager = manager
        self.habits_config = habits_config
        self.window = tk.Tk()
        self.window.title("Rastreador de Hábitos")

        self.create_widgets()
        self.update_progress_table()
        self.window.mainloop()

    def create_widgets(self):
        """
        Crea los elementos de la interfaz gráfica.
        """
        # Título principal
        tk.Label(self.window, text="Rastreador de Hábitos", font=("Arial", 16)).pack(pady=10)

        # Botón de Configuración
        tk.Button(self.window, text="⚙️ Configuración", command=self.open_config_window).pack(pady=5)

        # Sección de hábitos
        habit_frame = tk.Frame(self.window)
        habit_frame.pack(pady=10)
        tk.Label(self.window, text="Selecciona los hábitos completados y agrega comentarios:", font=("Arial", 12)).pack()

        self.habit_vars = {}
        self.comment_entries = {}

        for idx, (letter, habit) in enumerate(self.habits_config.items()):
            var = tk.StringVar(value="")
            tk.Checkbutton(habit_frame, text=f"{habit['name']} ({letter})", variable=var, onvalue="X", offvalue="").grid(row=idx, column=0, sticky="w")
            self.habit_vars[letter] = var

            comment_entry = tk.Entry(habit_frame, width=40)
            comment_entry.grid(row=idx, column=1, padx=5)
            self.comment_entries[letter] = comment_entry

        # Botones de acción
        button_frame = tk.Frame(self.window)
        button_frame.pack(pady=5)
        self.register_button = tk.Button(button_frame, text="Registrar Hábitos", command=self.register_habits)
        self.register_button.grid(row=0, column=0, padx=10)

        self.delete_button = tk.Button(button_frame, text="Eliminar Último Registro", command=self.delete_last_record)
        self.delete_button.grid(row=0, column=1, padx=10)

        # Tabla de progreso
        tk.Label(self.window, text="📊 Progreso de Hábitos:", font=("Arial", 12)).pack()
        self.tree = ttk.Treeview(self.window, columns=("Dia", *self.habits_config.keys()), show="headings", height=10)
        self.tree.pack(pady=10)

        self.tree.heading("Dia", text="Día")
        for letter in self.habits_config.keys():
            self.tree.heading(letter, text=letter)

        for col in ("Dia", *self.habits_config.keys()):
            self.tree.column(col, width=100, anchor="center")

        # Leyenda
        self.legend_label = tk.Label(self.window, text="", font=("Arial", 10), justify="left")
        self.legend_label.pack(pady=10)

    def open_config_window(self):
        """
        Abre la ventana de configuración para administrar hábitos.
        """
        ConfigWindow(self.manager, self.refresh_ui)

    def register_habits(self):
        """
        Registra los hábitos seleccionados por el usuario y sus comentarios.
        """
        current_day = len(self.manager.data["progress"]) + 1

        if any(int(day["Día"]) == current_day for day in self.manager.data["progress"]):
            messagebox.showwarning("Advertencia", "Ya registraste hábitos para hoy.")
            return

        daily_data = {"Día": current_day}
        for letter in self.habits_config.keys():
            if self.habit_vars[letter].get() == "X":
                daily_data[letter] = "X"
                comment = self.comment_entries[letter].get().strip()
                if comment:
                    daily_data[f"{letter}_Comentario"] = comment
            else:
                daily_data[letter] = ""

        self.manager.data["progress"].append(daily_data)
        self.manager.save()
        self.update_progress_table()
        messagebox.showinfo("Éxito", "Hábitos registrados correctamente.")
        self.register_button.config(state="disabled")

        for entry in self.comment_entries.values():
            entry.delete(0, tk.END)

    def delete_last_record(self):
        """
        Elimina el último registro de progreso.
        """
        if not self.manager.data["progress"]:
            messagebox.showwarning("Advertencia", "No hay registros para eliminar.")
            return

        self.manager.data["progress"].pop()
        self.manager.save()
        self.update_progress_table()
        messagebox.showinfo("Éxito", "Último registro eliminado.")

    def update_progress_table(self):
        """
        Actualiza la tabla de progreso.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        for day in self.manager.data["progress"]:
            row = [day.get("Día", "")] + [
                day.get(letter, "") + (f" ({day.get(f'{letter}_Comentario', '')})" if day.get(letter) == "X" and day.get(f"{letter}_Comentario") else "")
                for letter in self.habits_config.keys()
            ]
            self.tree.insert("", "end", values=row)

        self.update_legend()

    def update_legend(self):
        """
        Actualiza la leyenda con el progreso de cada hábito.
        """
        legend_text = ""
        for letter, habit in self.habits_config.items():
            completed_days = sum(1 for day in self.manager.data["progress"] if day.get(letter) == "X")
            total_goal = habit["goal_days"]
            percentage = (completed_days / total_goal) * 100 if total_goal > 0 else 0
            legend_text += f"{letter}: {habit['name']} - {completed_days}/{total_goal} días ({percentage:.0f}%)\n"

        self.legend_label.config(text=legend_text)

    def refresh_ui(self):
        """
        Refresca la interfaz gráfica.
        """
        self.update_progress_table()
