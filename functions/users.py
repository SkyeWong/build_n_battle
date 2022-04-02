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
        if cursor.fetchall() == []:
            return False
        else:
            return True

    def get_user_profile(self):
        sql = f"""
            SELECT id, gold, xp
            FROM users
            WHERE id = {self.user.id};
            """
        cursor = db.execute_query(sql)
        profile_user = cursor.fetchall()[0]
        print(f"profile_user:\t{profile_user}")
        profile = {
            "user": {
                "id": profile_user[0],
                "gold": profile_user[1],
                "xp": profile_user[2]
            }
        }
        print(f"profile with user:\t{profile}")
        sql = f"""
            SELECT crops, farm_width
            FROM farms
            WHERE user_id = {self.user.id};
            """
        cursor = db.execute_query(sql)
        print("executed query")
        profile_farm = cursor.fetchall()[0]
        print("fetching results...")
        print(f"profile_farm:\t{profile_farm}")
        profile["farm"] = {
            "crops": profile_farm[0],
            "farm_width": profile_farm[1]
        }
        sql = f"""
            SELECT farm
            FROM commands_last_used
            WHERE user_id = {self.user.id}
            """
        cursor = db.execute_query(sql)
        profile_commands_last_used = cursor.fetchall()[0]
        profile["commands_last_used"] = {
            "farm": profile_commands_last_used[0]
        }
        print(f"final profile:\t{profile}")
        return profile

    def update_user_profile(self, new_profile):
        if self.if_user_present():
            update_users_query = f"""
                UPDATE 
                    users
                SET
                    gold = {new_profile["user"]["gold"]},
                    xp = {new_profile["user"]["xp"]}
                WHERE
                    id = {str(new_profile["user"]["id"])}
                """
            db.execute_query(update_users_query)
            db.conn.commit()
            update_farms_query = f"""
                UPDATE 
                    farms
                SET
                    crops = {new_profile["farm"]["crops"]},
                    farm_width = {new_profile["farm"]["farm_width"]}
                WHERE
                    user_id = {str(new_profile["user"]["id"])}
                """
            db.execute_query(update_farms_query)
            db.conn.commit()

        else:
            profile_user = [
                new_profile["user"]["id"],
                new_profile["user"]["gold"],
                new_profile["user"]["xp"]
            ]
            print(profile_user)
            sql = "INSERT INTO users (id, gold, xp) VALUES (%s, %s, %s)"
            db.execute_query(sql, profile_user)
            print("users")
            profile_farm = [
                new_profile["user"]["id"],
                new_profile["farm"]["crops"],
                new_profile["farm"]["crop_type"],
                new_profile["farm"]["farm_width"],
                new_profile["farm"]["farm_height"],
            ]
            print(profile_farm)
            sql = "INSERT INTO farms (user_id, crops, crop_type, farm_width, farm_height) VALUES (%s, %s, %s)"
            db.execute_query(sql, profile_farm)
            print("farm")
            profile_commands = [
                new_profile["user"]["id"],
                new_profile["commands_last_used"]["farm"]
            ]
            sql = "INSERT INTO commands_last_used (user_id, farm) VALUES (%s, %s)"
            db.execute_query(sql, profile_commands)
            db.conn.commit()
        return new_profile
