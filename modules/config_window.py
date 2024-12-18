import tkinter as tk
from tkinter import messagebox

class ConfigWindow:
    def __init__(self, manager, refresh_callback):
        """
        Inicializa la ventana de configuración.
        """
        self.window = tk.Toplevel()
        self.window.title("Configuración de Hábitos")
        self.manager = manager
        self.refresh_callback = refresh_callback

        tk.Label(self.window, text="Configuración de Hábitos", font=("Arial", 14)).pack(pady=10)

        # Botón para eliminar un hábito
        tk.Label(self.window, text="Eliminar un hábito:").pack()
        self.habit_to_delete = tk.StringVar()

        if self.manager.data["habits"]:
            # Si hay hábitos, selecciona el primero por defecto
            self.habit_to_delete.set(list(self.manager.data["habits"].keys())[0])
            tk.OptionMenu(self.window, self.habit_to_delete, *self.manager.data["habits"].keys()).pack(pady=5)
            tk.Button(self.window, text="Eliminar Hábito", command=self.delete_habit).pack(pady=5)
        else:
            # Si no hay hábitos, muestra un mensaje
            tk.Label(self.window, text="No hay hábitos para eliminar.").pack(pady=5)

        # Botón para crear un nuevo hábito
        tk.Label(self.window, text="Crear un nuevo hábito:").pack()
        self.new_habit_name = tk.Entry(self.window, width=20)
        self.new_habit_name.pack(pady=5)
        self.new_habit_letter = tk.Entry(self.window, width=5)
        self.new_habit_letter.pack(pady=5)
        tk.Button(self.window, text="Crear Hábito", command=self.create_habit).pack(pady=5)

        # Opción de ejecución automática
        self.auto_run_var = tk.BooleanVar(value=self.manager.data.get("auto_run", False))
        tk.Checkbutton(
            self.window,
            text="Ejecutar automáticamente después de las 23:00 hrs o al iniciar el PC",
            variable=self.auto_run_var,
            command=self.setup_auto_run
        ).pack(pady=10)


    def delete_habit(self):
        """
        Elimina un hábito seleccionado.
        """
        habit_letter = self.habit_to_delete.get()
        self.manager.delete_habit(habit_letter)
        self.refresh_callback()
        messagebox.showinfo("Éxito", f"Hábito '{habit_letter}' eliminado.")
        self.window.destroy()

    def create_habit(self):
        """
        Crea un nuevo hábito.
        """
        name = self.new_habit_name.get().strip()
        letter = self.new_habit_letter.get().strip().upper()

        if len(letter) != 1 or letter in self.manager.data["habits"]:
            messagebox.showerror("Error", "Letra inválida o ya existente.")
            return

        self.manager.add_habit(letter, name)
        self.refresh_callback()
        messagebox.showinfo("Éxito", f"Hábito '{name}' creado.")
        self.window.destroy()

    def setup_auto_run(self):
        """
        Configura la ejecución automática del programa.
        """
        enabled = self.auto_run_var.get()
        self.manager.save_auto_run(enabled)

        if enabled:
            messagebox.showinfo("Configuración", "Se ha habilitado la ejecución automática.")
        else:
            messagebox.showinfo("Configuración", "Se ha deshabilitado la ejecución automática.")
