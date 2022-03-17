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
    """Functions about users."""
    
    def __init__(self, user):
        self.user = user
    
    def if_user_present(self):
        sql = f"""
            SELECT id, gold, xp
            FROM users
            WHERE id = {self.user.id};
            """
        cursor = db.execute_query(sql)
        if cursor.fetchall() != []:
            return True
        else:
            return False

    def get_user_profile(self):
        sql = f"""
            SELECT id, gold, xp, farm_last_used
            FROM users
            WHERE id = {self.user.id};
            """
        cursor = db.execute_query(sql)
        profile_user = cursor.fetchall()[0]
        profile = {
            "user": {
                "id": profile_user[0],
                "gold": profile_user[1],
                "xp": profile_user[2],
                "farm_last_used": profile_user[3]
            }
        }
        sql = f"""
            SELECT crops, farm_width
            FROM farms
            WHERE user_id = {self.user.id};
            """
        cursor = db.execute_query(sql)
        profile_farm = cursor.fetchall()[0]
        profile["farm"] = {
            "crops": profile_farm[0],
            "farm_width": profile_farm[1]
        }
        return profile

    def update_user_profile(self, new_profile):
        if self.if_user_present():
            sql = f"""
                UPDATE 
                    users
                SET
                    gold = {new_profile[1]},
                    xp = {new_profile[2]}
                    farm_last_used = {new_profile[3]}
                WHERE
                    id = {str(new_profile[0])}
                """
            db.execute_query(sql)
        else:
            sql = "INSERT INTO users (id, gold, xp) VALUES (%s, %s, %s)"
            db.execute_query(sql, new_profile)
        db.conn.commit()
        return new_profile
