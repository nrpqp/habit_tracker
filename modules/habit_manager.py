import os
import json

class HabitManager:
    def __init__(self, data_file="progress.json", habits_config=None):
        """
        Inicializa el gestor de hábitos.
        """
        self.data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", data_file)
        self.habits_config = habits_config or {}
        self.data = self.load_data()


    def load_data(self):
        """
        Carga los datos desde el archivo JSON. Si está corrupto, inicializa de nuevo.
        """
        if not os.path.exists(self.data_file) or os.path.getsize(self.data_file) == 0:
            return {"habits": self.habits_config, "progress": []}

        with open(self.data_file, "r") as file:
            try:
                data = json.load(file)
                if "progress" not in data or not isinstance(data["progress"], list):
                    data["progress"] = []
                return data
            except json.JSONDecodeError:
                # Reescribir si el JSON está corrupto
                return {"habits": self.habits_config, "progress": []}

    def save_data(self, new_record=None):
        """
        Guarda el progreso y actualiza el archivo JSON.
        """
        if new_record:
            # Asegúrate de que el nuevo registro sea un diccionario
            if isinstance(new_record, dict):
                self.data["progress"].append(new_record)

        with open(self.data_file, "w") as file:
            json.dump(self.data, file, indent=4)


    def delete_last_record(self):
        if self.data["progress"]:
            self.data["progress"].pop()
            self.save_data()

    def register_habits(self):
        """
        Registra los hábitos seleccionados por el usuario.
        """
        current_day = len(self.manager.data["progress"]) + 1
        daily_data = {"Día": current_day}
        for letter in self.habits_config.keys():
            daily_data[letter] = self.habit_vars[letter].get()
        self.manager.save_data(daily_data)
        self.update_progress_table()
        messagebox.showinfo("Éxito", "Hábitos registrados correctamente.")
        self.register_button.config(state="disabled")

    def update_progress_table(self):
        """
        Actualiza la tabla de progreso y la leyenda.
        """
        for row in self.tree.get_children():
            self.tree.delete(row)

        for day in self.manager.data["progress"]:
            row = [day["Día"]] + [day.get(letter, "") for letter in self.habits_config.keys()]
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
            percentage = (completed_days / total_goal) * 100
            legend_text += f"{letter}: {habit['name']} - {completed_days}/{total_goal} días ({percentage:.0f}%)\n"

            if completed_days >= total_goal:
                legend_text += f"🎉 ¡Felicidades! Completaste '{habit['name']}' 🎉\n"

        self.legend_label.config(text=legend_text)

    def ensure_data_folder(self):
        """
        Verifica si la carpeta 'data' existe y la crea si no existe.
        """
        folder = os.path.dirname(self.data_file)
        if not os.path.exists(folder):
            os.makedirs(folder)

    def calculate_streaks(self):
        """
        Calcula las rachas consecutivas y totales por hábito.
        """
        streaks = {key: {"racha": 0, "total": 0, "temp_racha": 0} for key in self.habits.keys()}
        
        for day in self.data:
            for key in self.habits.keys():
                if day.get(key) == "X":
                    streaks[key]["total"] += 1
                    streaks[key]["temp_racha"] += 1
                else:
                    streaks[key]["temp_racha"] = 0
                streaks[key]["racha"] = max(streaks[key]["racha"], streaks[key]["temp_racha"])

        return streaks

    def ask_habit_status(self, habit_name):
        """
        Pregunta al usuario por el estado de un hábito: vacío o "X".
        """
        value = input(f"¿Completaste '{habit_name}' hoy? (Enter = No, X = Sí): ").strip().upper()
        if value == "X":
            detail = input("¿Deseas agregar un comentario o detalle? (Enter = No): ").strip()
            return "X", detail
        return "", ""

    def get_daily_habits(self):
        """
        Solicita al usuario completar el progreso diario de los hábitos.
        """
        print("\n📋 Registro diario de hábitos:")
        today = len(self.data) + 1  # Cuenta como racha actual (Día consecutivo)
        daily_data = {"Día": today, "Racha": today}

        for key, habit_name in self.habits.items():
            status, detail = self.ask_habit_status(habit_name)
            daily_data[key] = status
            daily_data[f"{key}_Detalle"] = detail

        self.data.append(daily_data)
        self.save_data(daily_data)
        self.streaks = self.calculate_streaks()
        print("✅ Hábitos registrados correctamente.\n")
        return daily_data

    def show_progress(self):
        """
        Muestra las rachas y totales de cada hábito.
        """
        print("\n📊 Progreso de Hábitos:")
        for key, habit_name in self.habits.items():
            racha = self.streaks[key]["racha"]
            total = self.streaks[key]["total"]
            print(f"- {habit_name}: {total} días en total | Racha más larga: {racha} días consecutivos.")