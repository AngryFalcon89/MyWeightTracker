from controllers.data_controller import DataController
from controllers.stats_controller import StatsController
from views.main_view import MainView
from config import DATA_FILE

def main():
    # Initialize controllers
    data_controller = DataController(DATA_FILE)
    stats_controller = StatsController(data_controller)
    
    # Create and run the application
    app = MainView(data_controller, stats_controller)
    app.mainloop()

if __name__ == "__main__":
    main()