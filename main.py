from datetime import datetime
from Simulator.simulator import Simulator
from Database.database_manager import DatabaseManager
from AlertProcessor.alert_processor import AlertProcessor


DB_URL = "sqlite:///incident_evaluation_results.db"
RULE_DATA_PATH = "C:/Users/sever/OneDrive/Schule/OST/Module/MSE-Thesis/Scripts/Data/Filled_Incident_Classification_Dataset.csv"
INCIDENT_HISTORY_PATH = "C:/Users/sever/OneDrive/Schule/OST/Module/MSE-Thesis/Scripts/Data/Incident_Data.csv"

if __name__ == "__main__":
    DB_MANAGER = DatabaseManager(DB_URL)
    PROCESSOR = AlertProcessor(DB_MANAGER)

    #Example regular usage
    #notify_analyst = PROCESSOR.process_new_incident(current_time, rule_name, incident_id)
    #PROCESSOR.reduce_threat_level(datetime.now())
    #PROCESSOR.process_investigated_incident(datetime.now(), rule_name)

    # Example Simulation
    SIMULATOR = Simulator(PROCESSOR, DB_MANAGER)
    SIMULATOR.add_rules_bulk(RULE_DATA_PATH)
    SIMULATOR.run_simulation(INCIDENT_HISTORY_PATH)