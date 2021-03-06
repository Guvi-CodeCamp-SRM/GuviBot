import asyncio
import datetime
from utils import postReminder
from dbmongo import db
from utils import premeetReminder
from utils import postmeetReminder
import pytz

Task_details = db.connection()
async def remainder(Client):
        
        try:
            data = Task_details.discord.find()
            for eachTask in data:
                presentTime=datetime.datetime.now().timestamp()
                if presentTime>eachTask['deadline']:
                    await postReminder.send_after_reminder(Client, eachTask)
                    Task_details.discord.delete_one(eachTask)

            data = Task_details.Data.find()
            for eachMeet in data:
                id = eachMeet["ids"]
                presentTime = datetime.datetime.now().timestamp()
                if presentTime > eachMeet["TimeStamp"]-1800 and eachMeet["Reminder"] == 2:
                    Task_details.Data.update_one(
                        {"ids": str(id)}, {"$inc": {"Reminder": -1}})
                    await premeetReminder.send_before_reminder(Client, eachMeet)
                if presentTime > eachMeet["TimeStamp"] and eachMeet["Reminder"] == 1:
                    await postmeetReminder.send_after_reminder(Client, eachMeet)
                    Task_details.Data.delete_one(eachMeet)
            await asyncio.sleep(10)
            await remainder(Client)
        except:
            print('Error occured')
            await asyncio.sleep(10)
            await remainder(Client)
