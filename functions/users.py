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
        sql = f"""
            SELECT id, gold, xp
            FROM users
            WHERE id = {self.user.id};
            """
        cursor = db.execute_query(sql)
        if cursor.fetchall() == []:
            return False
        else:
            return True

    def get_user_profile(self):
        if self.if_user_present():
            sql = f"""
                SELECT id, gold, xp
                FROM users
                WHERE id = {self.user.id};
                """
            cursor = db.execute_query(sql)
            profile_user = cursor.fetchall()[0]
            profile = {
                "user": {
                    "id": profile_user[0],
                    "gold": int(float(profile_user[1])),
                    "xp": int(float(profile_user[2]))
                }
            }
            sql = f"""
                SELECT crops, crop_type, farm_width, farm_height
                FROM farms
                WHERE user_id = {self.user.id};
                """
            cursor = db.execute_query(sql)
            profile_farm = cursor.fetchall()[0]
            profile["farm"] = {
                "crops": json.loads(profile_farm[0]),
                "crop_type": json.loads(profile_farm[1]),
                "farm_width": profile_farm[2],
                "farm_height": profile_farm[3]
            }
            sql = f"""
                SELECT farm
                FROM commands_last_used
                WHERE user_id = {self.user.id}
                """
            cursor = db.execute_query(sql)
            profile_commands_last_used = cursor.fetchall()[0]
            profile["commands_last_used"] = {
                "farm": int(profile_commands_last_used[0])
            }
            return profile
        else:
            return False

    def update_user_profile(self, new_profile):
        if self.if_user_present():
            update_users_query = f"""
                UPDATE 
                    users
                SET
                    gold = {str(new_profile["user"]["gold"])},
                    xp = {str(new_profile["user"]["xp"])}
                WHERE
                    id = {str(new_profile["user"]["id"])}
                """
            db.execute_query(update_users_query)
            db.conn.commit()
            update_farms_query = f"""
                UPDATE 
                    farms
                SET
                    crops = '{json.dumps(new_profile["farm"]["crops"])}',
                    crop_type = '{json.dumps(new_profile["farm"]["crop_type"])}',
                    farm_width = {new_profile["farm"]["farm_width"]},
                    farm_height = {new_profile["farm"]["farm_height"]}
                WHERE
                    user_id = {str(new_profile["user"]["id"])}
                """
            db.execute_query(update_farms_query)
            db.conn.commit()
            update_farms_query = f"""
                UPDATE 
                    commands_last_used
                SET
                    farm = {new_profile["commands_last_used"]["farm"]}
                WHERE
                    user_id = {str(new_profile["user"]["id"])}
                """
            db.execute_query(update_farms_query)
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
            get_gold_query = f"""
                SELECT gold
                FROM users
                WHERE id = "{self.user.id}"
            """
            cursor = db.execute_query(get_gold_query)
            gold = int(cursor.fetchall()[0][0])
            gold += gold_to_modify
            update_gold_query = f"""
                UPDATE 
                    users
                SET
                    gold = {str(gold)},
                WHERE
                    id = "{str(self.user.id)}"
                """
            db.execute_query(update_gold_query)
            db.conn.commit()
            return gold
        else:
            return False
    
    def set_gold(self, gold_to_set: int):
        if self.if_user_present() == True:
            update_gold_query = f"""
                UPDATE 
                    users
                SET
                    gold = {str(gold_to_set)},
                WHERE
                    id = "{str(self.user.id)}"
                """
            db.execute_query(update_gold_query)
            db.conn.commit()
            return gold_to_set
        else:
            return False