from datetime import datetime
from Database.database_manager import DatabaseManager

class AlertProcessor:
    """Processor for handling alerts."""

    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def _update_belief(self, prior_belief: float, signal_quality: float) -> float:
        """Updates belief based on signal quality."""
        if signal_quality == 0:
            return 1.0
        likelihood_given_belief = signal_quality
        likelihood_given_not_belief = 1 - signal_quality
        prior_not_belief = 1 - prior_belief

        numerator = likelihood_given_belief * prior_belief
        denominator = numerator + (likelihood_given_not_belief * prior_not_belief)

        return max(0.2, min(0.9, numerator / denominator))

    def _get_strategy(self, p: float, gamma_t: float, gamma_n: float, rel_cost_analyst: float, rel_cost_damage: float):
        """Determines alert strategy based on thresholds."""
        threshold_analyst = rel_cost_analyst / p
        threshold_siem = rel_cost_damage / p

        #Full If Else Block for understanding the matrix of the paper
        #if threshold_siem > gamma_t:
        #    if threshold_analyst > gamma_t:
        #        return False, 1
        #    elif gamma_t >= threshold_analyst >= gamma_n:
        #        return False, 2
        #    else:
        #        return False, 3
        #elif gamma_t >= threshold_siem >= gamma_n:
        #    if threshold_analyst > gamma_t:
        #        return False, 4
        #    else:
        #        return True, 5
        #else:
        #    if threshold_analyst >= gamma_n:
        #        return False, 6
        #    else:
        #        return True, 7
        
        return (gamma_t >= threshold_siem >= gamma_n and threshold_analyst <= gamma_t) or (threshold_siem < gamma_n and threshold_analyst < gamma_n)

    def process_new_incident(self, opened_time: datetime, rule_name: str, incident_id: int) -> bool:
        """Processes an alert based on rule data and threat history."""
        try:
            threat_history = self.db_manager.get_last_threat_history()
            pi = threat_history.threat_level
            rule_data = self.db_manager.get_rule_data(rule_name)

            incident_id = self.db_manager.create_incident(
                incident_id, rule_data.rule_id, opened_time
            )
            
            tau = rule_data.signal_quality
            gamma_t = self._update_belief(pi, tau)
            gamma_n = self._update_belief(pi, 1 - tau)
            p = 0.95

            notify_analyst = self._get_strategy(p, gamma_t, gamma_n, rule_data.rel_cost_analyst, rule_data.rel_cost_damage)

            self.db_manager.update_incident_result(incident_id, "True" if notify_analyst else "False")
            self.db_manager.create_new_threat_history(incident_id, gamma_t if notify_analyst else pi, opened_time)

            return notify_analyst

        except ValueError as e:
            print(f"Error during alert processing: {e}")
            return False

    def process_investigated_incident(self, timestamp: datetime, rule_name: str) -> None:
        # Fetch the last threat history entry
        threat_history = self.db_manager.get_last_threat_history()
        pi = threat_history.threat_level

        # Fetch rule data for the specified rule name
        rule_data = self.db_manager.get_rule_data(rule_name)

        # Calculate the updated belief based on signal quality
        signal_quality = 1 - rule_data.signal_quality
        updated_belief = self._update_belief(pi, signal_quality)

        # Create a new threat history entry with the updated belief
        self.db_manager.create_new_threat_history(None, updated_belief, timestamp)

    def reduce_threat_level(self, timestamp: datetime) -> None:
        """Reduces the threat level over time."""
        threat_history = self.db_manager.get_last_threat_history()
        pi = threat_history.threat_level
        if pi > 0.2:
            new_pi = max(0.2, pi - (0.04 if pi > 0.6 else 0.01))
            self.db_manager.create_new_threat_history(None, new_pi, timestamp)

