import os
import json

class HabitManager:
    def __init__(self, data_file="progress.json"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        """
        Carga los datos desde el archivo JSON. Si no existe, inicializa la estructura.
        """
        if not os.path.exists(self.data_file):
            return {"habits": {}, "progress": [], "auto_run": False}
        with open(self.data_file, "r") as file:
            return json.load(file)

    def save(self):
        """
        Guarda los datos actuales en el archivo JSON.
        """
        with open(self.data_file, "w") as file:
            json.dump(self.data, file, indent=4)

    def save_habits_config(self, new_habits_config):
        """
        Actualiza la configuración de hábitos y guarda los cambios.
        """
        self.data["habits"] = new_habits_config
        self.save()

    def save_auto_run(self, enabled):
        """
        Guarda el estado de ejecución automática.
        """
        self.data["auto_run"] = enabled
        self.save()

    def add_habit(self, letter, name, goal_days=30):
        """
        Agrega un nuevo hábito a la configuración.
        """
        self.data["habits"][letter] = {"name": name, "goal_days": goal_days, "completed_days": 0}
        self.save()

    def delete_habit(self, letter):
        """
        Elimina un hábito de la configuración.
        """
        if letter in self.data["habits"]:
            del self.data["habits"][letter]
            self.save()
