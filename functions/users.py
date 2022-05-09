import os
import nextcord
import random
import math 
import json
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
    
    def __init__(self, user: nextcord.User):
        self.user = user
    
    def if_user_present(self):
        sql = """
            SELECT id
            FROM users
            WHERE id = %s;
            """
        cursor = db.execute_query(sql, (self.user.id,))
        if cursor.fetchall() == []:
            return False
        else:
            return True

    def get_user_profile(self):
        if self.if_user_present():
            sql = """
                SELECT id, gold, xp
                FROM users
                WHERE id = %s
                """
            cursor = db.execute_query(sql, (self.user.id,))
            profile_user = cursor.fetchall()[0]
            profile = {
                "user": {
                    "id": profile_user[0],
                    "gold": int(float(profile_user[1])),
                    "xp": int(float(profile_user[2]))
                }
            }
            sql = """
                SELECT crops, crop_type, farm_width, farm_height
                FROM farms
                WHERE user_id = %s
                """
            cursor = db.execute_query(sql, (self.user.id,))
            profile_farm = cursor.fetchall()[0]
            profile["farm"] = {
                "crops": json.loads(profile_farm[0]),
                "crop_type": json.loads(profile_farm[1]),
                "farm_width": profile_farm[2],
                "farm_height": profile_farm[3]
            }
            sql = """
                SELECT farm
                FROM commands_last_used
                WHERE user_id = %s
                """
            cursor = db.execute_query(sql, (self.user.id,))
            profile_commands_last_used = cursor.fetchall()[0]
            profile["commands_last_used"] = {
                "farm": int(profile_commands_last_used[0])
            }
            return profile
        else:
            return False

    def update_user_profile(self, new_profile):
        if self.if_user_present():
            update_users_query = """
                UPDATE 
                    users
                SET
                    gold = %s,
                    xp = %s
                WHERE
                    id = %s
                """
            value = (new_profile["user"]["gold"], new_profile["user"]["xp"], new_profile["user"]["id"])
            db.execute_query(update_users_query, value)
            db.conn.commit()
            update_farms_query = """
                UPDATE 
                    farms
                SET
                    crops = '%s',
                    crop_type = '%s',
                    farm_width = %s,
                    farm_height = %s
                WHERE
                    user_id = %s
                """
            value = (json.dumps(new_profile["farm"]["crops"]), json.dumps(new_profile["farm"]["crop_type"]), new_profile["farm"]["farm_width"], new_profile["farm"]["farm_height"], new_profile["user"]["id"])
            db.execute_query(update_farms_query, value)
            db.conn.commit()
            update_farms_query = """
                UPDATE 
                    commands_last_used
                SET
                    farm = %s
                WHERE
                    user_id = %s
                """
            value = (new_profile["commands_last_used"]["farm"], new_profile["user"]["id"])
            db.execute_query(update_farms_query, value)
            db.conn.commit()
            return new_profile
        else:
            return False

    def create_user_profile(self):
        if self.if_user_present() == False:
            new_profile = {
                "user": {
                    "id": self.user.id,
                    "gold": 1000,
                    "xp": 0
                },
                "farm": {
                    "crops": '["","","",""]',
                    "crop_type": '["","","",""]',
                    "farm_width": 2,
                    "farm_height": 2
                },
                "commands_last_used": {
                    "farm": int(datetime.now().timestamp())
                }
            }
            profile_user = [
                    new_profile["user"]["id"],
                    new_profile["user"]["gold"],
                    new_profile["user"]["xp"]
                ]
            sql = "INSERT INTO users (id, gold, xp) VALUES (%s, %s, %s)"
            db.execute_query(sql, profile_user)
            profile_farm = [
                new_profile["user"]["id"],
                new_profile["farm"]["crops"],
                new_profile["farm"]["crop_type"],
                new_profile["farm"]["farm_width"],
                new_profile["farm"]["farm_height"],
            ]
            sql = "INSERT INTO farms (user_id, crops, crop_type, farm_width, farm_height) VALUES (%s, %s, %s, %s, %s)"
            db.execute_query(sql, profile_farm)
            profile_commands = [
                new_profile["user"]["id"],
                new_profile["commands_last_used"]["farm"]
            ]
            sql = "INSERT INTO commands_last_used (user_id, farm) VALUES (%s, %s)"
            db.execute_query(sql, profile_commands)
            db.conn.commit()
            return new_profile
        else:
            return False

    def modify_gold(self, gold_to_modify: int):
        if self.if_user_present() == True:
            get_gold_query = """
                SELECT gold
                FROM users
                WHERE id = %s;
                """
            cursor = db.execute_query(get_gold_query, (self.user.id,))
            gold = int(cursor.fetchall()[0][0])
            gold += gold_to_modify
            update_gold_query = """
                UPDATE 
                    users
                SET
                    gold = %s
                WHERE
                    id = %s;
                """
            db.execute_query(update_gold_query, (gold, self.user.id,))
            db.conn.commit()
            return int(gold)
        else:
            return False
    
    def set_gold(self, gold_to_set: int):
        if self.if_user_present() == True:
            update_gold_query = """
                UPDATE 
                    users
                SET
                    gold = %s
                WHERE
                    id = %s;
                """
            db.execute_query(update_gold_query, (gold_to_set, self.user.id))
            db.conn.commit()
            return int(gold_to_set)
        else:
            return False