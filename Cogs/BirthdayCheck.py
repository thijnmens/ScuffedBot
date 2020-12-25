import discord, os, requests, json, firebase_admin, asyncio, schedule, time
from discord.ext import commands
from discord.utils import get
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db

dab = firestore.client()
check = False

#Check for birthdays
def get_birthdays():
    try:
        ref = dab.collection('collectionlist').document('data').get().get('collectionarray')
        amount = len(ref) - 1
    except Exception as e:
        print(e)

schedule.every().day.at("12:00").do(get_birthdays)

while check == False:
    schedule.run_pending()
    check = True
    break