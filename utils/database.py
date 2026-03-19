import os
import asyncio
import sqlite3
import discord

from datetime import datetime
from utils.discordbot import Bot

databases = [
    "afk",
    "banished",
    "userdata"
]

class Database():
    def __init__(cls, *args, **kargs):
        super().__init__(*args, **kargs)
        
    @classmethod
    def init(cls):
        ## Create databases
        if not os.path.exists(f"data"):
            os.mkdir("data")
        
        # User Data
        if not os.path.exists(f"data/user_data.db"):
            usr_conn = sqlite3.connect(f"data/user_data.db")

            usr_conn.execute(f"CREATE TABLE afk_users (user_id INT, name TEXT, message TEXT, since TEXT)")
            usr_conn.execute(f"CREATE TABLE cooldown (user_id INT, since TEXT)")
            usr_conn.execute(f"CREATE TABLE user_data (user_id INT, alise TEXT, job TEXT, tokens INT, wallet INT, bank INT)")

            usr_conn.close()

        # Banished
        if not os.path.exists(f"data/banished.db"):
            ban_conn = sqlite3.connect(f"data/banished.db")
            ban_cursor = ban_conn.cursor()

            ban_cursor.execute(f"CREATE TABLE banished_ids (user_id INT)")
            ban_cursor.execute(f"CREATE TABLE banished_words_bypasses (bypass TEXT)")
            ban_cursor.execute(f"CREATE TABLE banished_flagmsg (word TEXT)")
            ban_cursor.execute(f"CREATE TABLE banished_words_noignore (word TEXT, message TEXT)")
            ban_cursor.execute(f"CREATE TABLE banished_words (word TEXT, message TEXT)")

            ban_conn.close()

        cls.banished_conn = sqlite3.connect(f"data/banished.db", timeout=30)
        cls.userdata_conn = sqlite3.connect(f"data/user_data.db", timeout=30)
        
        cls.banished_conn.execute("PRAGMA journal_mode=WAL;")
        cls.userdata_conn.execute("PRAGMA journal_mode=WAL;")


    banished_conn = None
    userdata_conn = None

    write_lock = asyncio.Lock()

    def create_databases(logger):
        print("Removed(?)")

    def get_afks():
        cursor = Database.userdata_conn.cursor()

        cursor.execute("SELECT * FROM afk_users")
        users_raw = cursor.fetchall()

        result = {
            "users": []
        }

        for user in users_raw:
            result['users'].append({
                'user_id': user[0],
                'name': user[1],
                'message': user[2],
                'since': user[3]
            })

        return result
    
    def get_banished():
        cursor = Database.banished_conn.cursor()

        cursor.execute("SELECT * FROM banished_ids")
        resultBanishedIds = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_words_bypasses")
        resultBypassesRaw = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_flagmsg")
        resultFlagMsgRaw = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_words_noignore")
        resultNoIgnoreRaw = cursor.fetchall()

        cursor.execute("SELECT * FROM banished_words")
        resultBanishedWordsRaw = cursor.fetchall()

        result = {
            "ids": [],
            "bypasses": [],
            "flagmsg": [],
            "noignore": {},
            "words": {}
        }

        for id in resultBanishedIds:
            result['ids'].append(id[0])
        for bypass in resultBypassesRaw:
            result['bypasses'].append(bypass[0])
        for flag in resultFlagMsgRaw:
            result['flagmsg'].append(flag[0])

        for noignore in resultNoIgnoreRaw:
            result["noignore"][noignore[0]] = noignore[1]
        for banished in resultBanishedWordsRaw:
            result["words"][banished[0]] = banished[1]
        
        return result
