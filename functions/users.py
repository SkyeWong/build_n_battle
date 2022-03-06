import os
import nextcord
import random
import main
import math 
from main import bot
from datetime import datetime
from nextcord.ext import commands
from nextcord import Embed
from nextcord.ui import Button, View
import database as db
from typing import Optional
import nextcord

class Users():
    """Functions about users.
    """
    
    def if_user_present(self, user):
        sql = f"""
            SELECT id, gold, xp
            FROM users
            WHERE id = {user.id};
            """
        cursor = db.execute_query(sql)
        if cursor.fetchall() != []:
            return True
        else:
            return False

    def get_user_profile(self, user):
        sql = f"""
            SELECT id, gold, xp
            FROM users
            WHERE id = {user.id};
            """
        cursor = db.execute_query(sql)
        return cursor.fetchall()[0]

    def update_user_profile(self, user, new_profile):
        if self.if_user_present(user):
            sql = f"""
                UPDATE 
                    users
                SET
                    gold = {new_profile[1]},
                    xp = {new_profile[2]}
                WHERE
                    id = {str(new_profile[0])}
                """
            db.execute_query(sql)
            db.conn.commit()
        else:
            sql = "INSERT INTO users (id, gold, xp) VALUES (%s, %s, %s)"
            db.execute_query(sql, new_profile)
            db.conn.commit()
        return new_profile
