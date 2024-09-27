from pymongo import MongoClient
from pyrogram.types import Message
from pyrogram import Client, filters
from datetime import datetime
from env import DATABASE_URL, OWNER_ID


# Connect to MongoDB
client = None
db = None
users_collection = None
if DATABASE_URL:
    client = MongoClient(DATABASE_URL)
    db = client["Sessions_String_Bot"]  # Replace with your DB name
    users_collection = db["users"]  # Users collection
    print("Database Connected.")
else:
    print("Running Without DB.")

@Client.on_message(~filters.service, group=1)
async def track_users(_, msg: Message):
    if msg.from_user is None or users_collection is None:
        return  # Ignore messages without a valid user or if collection is not found

    user_id = msg.from_user.id
    first_name = msg.from_user.first_name
    username = msg.from_user.username

    # Upsert user info
    users_collection.update_one(
        {"user_id": user_id},  # Filter for existing user
        {"$set": {  # Update fields
            "first_name": first_name,
            "username": username,
            "date_added": datetime.utcnow()
        }},
        upsert=True  # Insert if not found
    )

@Client.on_message(filters.user(OWNER_ID) & filters.command("stats"))
async def get_stats(_, msg: Message):
    if users_collection is None:  # Check if users_collection exists
        await msg.reply("User collection is not available.", quote=True)
        return

    user_count = users_collection.count_documents({})
    await msg.reply(f"Total Users: {user_count}", quote=True)
