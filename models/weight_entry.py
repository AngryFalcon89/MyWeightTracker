from datetime import datetime
from typing import Optional, Dict, Any

class WeightEntry:
    def __init__(self, 
                 date: str,
                 pre_gym: Optional[float] = None,
                 post_gym: Optional[float] = None,
                 preworkout: str = "Normal",
                 note: str = "",
                 skipped: bool = False,
                 calories_burned: Optional[int] = None,
                 breakfast: str = "",
                 lunch: str = "",
                 snacks: str = "",
                 dinner: str = ""):
        self.date = date
        self.pre_gym = pre_gym
        self.post_gym = post_gym
        self.preworkout = preworkout
        self.note = note
        self.skipped = skipped
        self.calories_burned = calories_burned
        self.breakfast = breakfast
        self.lunch = lunch
        self.snacks = snacks
        self.dinner = dinner

    @property
    def date_obj(self) -> datetime:
        return datetime.strptime(self.date, "%d-%m-%Y")

    @property
    def weight_diff(self) -> Optional[float]:
        if self.post_gym and self.pre_gym:
            return self.post_gym - self.pre_gym
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'date': self.date,
            'pre_gym': str(self.pre_gym) if self.pre_gym else '',
            'post_gym': str(self.post_gym) if self.post_gym else '',
            'preworkout': self.preworkout,
            'note': self.note,
            'skipped': str(self.skipped),
            'calories_burned': str(self.calories_burned) if self.calories_burned else '',
            'breakfast': self.breakfast,
            'lunch': self.lunch,
            'snacks': self.snacks,
            'dinner': self.dinner
        }