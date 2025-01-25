import csv
from datetime import datetime, timedelta

class Simulator:
    def __init__(self, processor, db_manager):
        self.processor = processor
        self.db_manager = db_manager

    def run_simulation(self, path):
        self.db_manager.create_new_threat_history(None, 0.5, datetime(2024, 8, 1, 0, 0))
        previous_time = None
        pending_closed_times = []  # Array to store pending ClosedTime and associated incident data

        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            rows.sort(key=lambda row: datetime.strptime(row['CreatedTime [UTC]'], '%m/%d/%Y, %I:%M:%S.%f %p'))  # Adjust format as needed

            for index, row in enumerate(rows):
                print(f"Processing row {index} of {len(rows)}")
                current_time = datetime.strptime(row['CreatedTime [UTC]'], '%m/%d/%Y, %I:%M:%S.%f %p')
                closed_time = datetime.strptime(row['ClosedTime [UTC]'], '%m/%d/%Y, %I:%M:%S.%f %p')

                rule_name = row['Title']
                incident_id = row['IncidentID']

                # Process pending closed times up to the current_time
                pending_closed_times = self._process_pending_closed_times(pending_closed_times, current_time)

                if previous_time:
                    # Run quality checks every hour between previous_time and current_time
                    next_check_time = previous_time + timedelta(hours=4)
                    while next_check_time < current_time:
                        # Process pending closed times within the interval
                        pending_closed_times = self._process_pending_closed_times(pending_closed_times, next_check_time)

                        # Process hourly checks
                        self.processor.reduce_threat_level(next_check_time)
                        next_check_time += timedelta(hours=4)

                # Run the alert
                notify_analyst = self.processor.process_new_incident(current_time, rule_name, incident_id)

                if notify_analyst:
                    pending_closed_times.append((closed_time, rule_name))

                previous_time = current_time

    def _process_pending_closed_times(self, pending_closed_times, up_to_time):
        remaining_closed_times = []
        for closed_time, rule_name in pending_closed_times:
            if closed_time <= up_to_time:
                # Process the false positive
                self.processor.process_investigated_incident(closed_time, rule_name)
            else:
                # Keep it in the pending list if it's not yet time to process
                remaining_closed_times.append((closed_time, rule_name))
        return remaining_closed_times

    def add_rules_bulk(self, path):
        with open(path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                tau = float(row['tau'])
                title = row['Title']
                rel_cost_analyst = float(row['rel_cost_analyst'])
                rel_cost_damage = float(row['rel_cost_damage'])

                # Call the method with extracted values
                self.db_manager.create_rule_data(
                    rule_name=title,
                    signal_quality=tau,
                    rel_cost_analyst=rel_cost_analyst,
                    rel_cost_damage=rel_cost_damage
                )
