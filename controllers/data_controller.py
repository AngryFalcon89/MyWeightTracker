import csv
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from models.weight_entry import WeightEntry

class DataController:
    def __init__(self, data_file: str):
        self.data_file = Path.home() / data_file
        self.entries: List[WeightEntry] = []
        self.load_data()

    def load_data(self) -> None:
        if not self.data_file.exists():
            return

        with open(self.data_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.entries.append(self._create_entry_from_row(row))

    def _create_entry_from_row(self, row: dict) -> WeightEntry:
        return WeightEntry(
            date=row['date'],
            pre_gym=float(row['pre_gym']) if row['pre_gym'] else None,
            post_gym=float(row['post_gym']) if row['post_gym'] else None,
            preworkout=row.get('preworkout', 'Normal'),
            note=row.get('note', ''),
            skipped=row.get('skipped', 'False') == 'True',
            calories_burned=int(row['calories_burned']) if row.get('calories_burned') else None,
            breakfast=row.get('breakfast', ''),
            lunch=row.get('lunch', ''),
            snacks=row.get('snacks', ''),
            dinner=row.get('dinner', '')
        )

    def save_data(self) -> None:
        with open(self.data_file, mode='w', newline='') as file:
            fieldnames = [
                'date', 'pre_gym', 'post_gym', 'preworkout', 'note',
                'skipped', 'calories_burned', 'breakfast', 'lunch',
                'snacks', 'dinner'
            ]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.entries:
                writer.writerow(entry.to_dict())

    def add_entry(self, entry: WeightEntry) -> None:
        self.entries = [e for e in self.entries if e.date != entry.date]
        self.entries.append(entry)
        self.entries.sort(key=lambda x: x.date_obj)
        self.save_data()

    def delete_entry(self, date: str) -> None:
        self.entries = [e for e in self.entries if e.date != date]
        self.save_data()

    def get_recent_entries(self, count: int = 14) -> List[WeightEntry]:
        return sorted(self.entries, key=lambda x: x.date_obj, reverse=True)[:count]

    def get_entry_by_date(self, date: str) -> Optional[WeightEntry]:
        for entry in self.entries:
            if entry.date == date:
                return entry
        return None