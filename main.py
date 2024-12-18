from modules.habit_manager import HabitManager
from modules.gui import HabitTrackerGUI

def main():
    """
    Función principal para inicializar el programa.
    """
    manager = HabitManager(data_file="progress.json")
    habits_config = manager.data["habits"]
    HabitTrackerGUI(manager, habits_config)

if __name__ == "__main__":
    main()
