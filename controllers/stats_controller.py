from typing import Dict, Any, List, Tuple
from datetime import datetime, timedelta
import numpy as np
from models.weight_entry import WeightEntry

class StatsController:
    def __init__(self, data_controller):
        self.data_controller = data_controller

    def calculate_stats(self) -> Dict[str, Any]:
        entries = [e for e in self.data_controller.entries if not e.skipped and e.pre_gym]
        if len(entries) < 2:
            return {"status": "insufficient_data"}

        dates = [e.date_obj for e in entries]
        weights = [e.pre_gym for e in entries]
        
        first_date = min(dates)
        last_date = max(dates)
        first_weight = weights[0]
        last_weight = weights[-1]
        
        weeks = max((last_date - first_date).days / 7, 1)
        total_loss = first_weight - last_weight
        weekly_loss = total_loss / weeks
        
        # Calculate average calories
        calorie_entries = [e for e in self.data_controller.entries if e.calories_burned]
        avg_calories = (sum(e.calories_burned for e in calorie_entries) / len(calorie_entries)) if calorie_entries else 0
        
        # Calculate projection
        projection = None
        if weekly_loss > 0:
            projection_date = last_date + timedelta(weeks=(last_weight / weekly_loss))
            projection = projection_date.strftime("%b %d, %Y")
        
        return {
            "first_date": first_date.strftime("%b %d, %Y"),
            "last_date": last_date.strftime("%b %d, %Y"),
            "total_loss": round(total_loss, 2),
            "weekly_loss": round(weekly_loss, 2),
            "avg_calories": round(avg_calories),
            "projection": projection,
            "status": "success"
        }

    def prepare_graph_data(self) -> Tuple:
        dates = []
        pre_weights = []
        post_weights = []
        skipped_dates = []
        
        for entry in self.data_controller.entries:
            if entry.skipped:
                skipped_dates.append(entry.date_obj)
            else:
                if entry.pre_gym:
                    dates.append(entry.date_obj)
                    pre_weights.append(entry.pre_gym)
                if entry.post_gym:
                    post_weights.append(entry.post_gym)
        
        return dates, pre_weights, post_weights, skipped_dates