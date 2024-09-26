from pymongo import MongoClient
from pyrogram.types import Message
from pyrogram import Client, filters
import datetime
from env import DATABASE_URL, OWNER_ID

# Connect to MongoDB if DATABASE_URL is set
client = MongoClient(DATABASE_URL) if DATABASE_URL else None
db = client["Sessions_String_Bot"] if client else None  # Replace with your DB name
users_collection = db["users"] if db is not None else None  # Users collection

@Client.on_message(~filters.service, group=1)
async def track_users(_, msg: Message):
    if users_collection is None or msg.from_user is None:
        return  # Ignore messages without a valid user

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    username = msg.from_user.username

    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({
            "user_id": user_id,
            "first_name": first_name,
            "username": username,
            "date_added": datetime.utcnow()
        })


@Client.on_message(filters.user(OWNER_ID) & filters.command("stats"))
async def get_stats(_, msg: Message):
    if not users_collection:
        return

    user_count = users_collection.count_documents({})
    await msg.reply(f"Total Users: {user_count}", quote=True)
