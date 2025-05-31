from apscheduler.schedulers.background import BackgroundScheduler  
from apscheduler.triggers.interval import IntervalTrigger 
from apscheduler.schedulers.asyncio import AsyncIOScheduler



asyncscheduler = AsyncIOScheduler()
scheduler = BackgroundScheduler()



