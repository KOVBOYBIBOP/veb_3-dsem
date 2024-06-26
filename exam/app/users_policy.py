from flask_login import current_user

class UserPolicy:
    def __init__(self, record):
        self.record = record
    
    def statistic(self):
        return current_user.is_admin()

    def delete(self):
        return current_user.is_admin()

    def create(self):
        return current_user.is_admin()

    def edit(self):
        if current_user.is_admin():
            return True
        if current_user.is_moder():
            return True
        return False
