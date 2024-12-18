from modules.config_manager import ConfigManager
from modules.gui import HabitTrackerGUI

def main():
    config_manager = ConfigManager()
    config = config_manager.load_config()

    if not config:
        config_manager.setup_initial_config_gui()
        config = config_manager.load_config()

    HabitTrackerGUI(config)

if __name__ == "__main__":
    main()
