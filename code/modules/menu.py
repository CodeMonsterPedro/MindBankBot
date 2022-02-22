from certifi import where
import config
from aiogram import Bot, Dispatcher, executor, types
from DBController import DBController
from datetime import datetime


'''
state 0 - initial state
state 1 - additional data output
state 2 - tools
state 3 - add\edit
state 4 - stages


'''

class Menu:

    def __init__(self, bot):
        self.state = 0
        self.bot = bot
        self.db = DBController()
        self.mainTemplate = ""

    def initialMessage(self):
        today = datetime.today()
        reminders = self.db.getReminders(where='''DAY(reminder_datetime)={} AND
        MONTH(reminder_datetime)={} AND YEAR(reminder_datetime)={} ORDER BY
         reminder_datetime'''.foramt(str(today.day), str(today.month), str(today.year)))
        tasks = self.db.getTasks()
        text = ""
        startHour = 5
        startMinute = '0'
        if reminders[0][2].hours > 5:
            startHour = reminders[0][2].hours
        for i in range((24-startHour) * 2):
            s = '{}:{}0  {}  \n'.format(str(startHour), startMinute, )
        self.bot.send_message(config.MAIN_USER_ID, text, disable_notification=False)

    async def send_message(self, user_id: int = config.MAIN_USER_ID, text: str = 'Hi', disable_notification: bool = False) -> bool:
        try:
            await self.bot.send_message(user_id, text, disable_notification=disable_notification)
        except:
            return True
        return False
