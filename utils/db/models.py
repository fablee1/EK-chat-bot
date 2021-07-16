from datetime import datetime


class UserModel:
    def __init__(self, id, full_name, username, createdAt=datetime.now()):
        self._id = id
        self.full_name = full_name
        self.username = username
        self.reputation = 0
        self.rep_given = 0
        self.rep_limit = 0
        self.address = None
        self.admin = False
        self.createdAt = createdAt

class AchievementModel:
    def __init__(self, goal=None, message=None, is_prize=False):
        self.goal = goal
        self.message = message
        self.is_prize = is_prize
        self.prize_name = 'Приз неопределён'

class PrizeModel:
    def __init__(self):
        self.start_date = datetime.now()
        self.status = "active"
        self.participants = []