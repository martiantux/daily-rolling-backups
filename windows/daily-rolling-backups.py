# Copyright (C) 2024 Bradley James Hammond / Distracted Labs
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# For inquiries, please contact martiantux@proton.me | hello@distractedlabs.cc.

import os
import shutil
from datetime import datetime, timedelta
import requests
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('config.ini')
SOURCE_DIR = config.get('Settings', 'SOURCE_DIR')
DAILY_TARGET_DIR = config.get('Settings', 'TARGET_DIR') + r'\daily'
WEEKLY_TARGET_DIR = config.get('Settings', 'TARGET_DIR') + r'\weekly'
DAILY_BACKUP_DAYS = config.getint('Settings', 'DAILY_BACKUP_DAYS')
WEEKLY_BACKUP_COUNT = config.getint('Settings', 'WEEKLY_BACKUP_DAYS')
WEEKLY_BACKUP_DAY = config.get('Settings', 'WEEKLY_BACKUP_DAY')
DISCORD_WEBHOOK_URL = config.get('Settings', 'DISCORD_WEBHOOK_URL')
LOG_TITLE = config.get('Settings', 'LOG_TITLE')
LOG_COLOR_HEX = config.get('Settings', 'LOG_COLOR').strip('#')
LOG_COLOR = int(LOG_COLOR_HEX, 16)

# Logging via Discord webhook
def post_to_discord(title, message):
    data = {
        "embeds": [
            {
                "title": title,
                "description": message,
                "color": LOG_COLOR
            }
        ]
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"Failed to post message to Discord: {response.text}")

def create_backup(source, daily_target, weekly_target, backup_day):
    today = datetime.now()
    daily_archive_name = f"daily_backup_{today.strftime('%Y%m%d')}.zip"
    weekly_archive_name = f"weekly_backup_{today.strftime('%Y%m%d')}.zip"

    # Daily backup
    daily_archive_path = os.path.join(daily_target, daily_archive_name)
    shutil.make_archive(daily_archive_path.replace('.zip', ''), 'zip', source)
    post_to_discord(LOG_TITLE, f"Daily backup created: {daily_archive_name}")

    # Weekly backup
    if today.strftime('%A').lower() == backup_day.lower():
        weekly_archive_path = os.path.join(weekly_target, weekly_archive_name)
        shutil.make_archive(weekly_archive_path.replace('.zip', ''), 'zip', source)
        post_to_discord(LOG_TITLE, f"Weekly backup created: {weekly_archive_name}")

# Purge expired backups
def cleanup_old_backups(target_dir, max_backups, backup_type):
    backups = [f for f in os.listdir(target_dir) if f.startswith(f"{backup_type}_backup_") and f.endswith(".zip")]
    backups.sort(reverse=True)
    old_backups = backups[max_backups:]

    for backup in old_backups:
        os.remove(os.path.join(target_dir, backup))
        post_to_discord(LOG_TITLE, f"Deleted old {backup_type} backup: {backup}, dated: {backup.split('_')[-1].split('.')[0]}")

if __name__ == "__main__":
    create_backup(SOURCE_DIR, DAILY_TARGET_DIR, WEEKLY_TARGET_DIR, WEEKLY_BACKUP_DAY)
    cleanup_old_backups(DAILY_TARGET_DIR, DAILY_BACKUP_DAYS, "daily")
    cleanup_old_backups(WEEKLY_TARGET_DIR, WEEKLY_BACKUP_COUNT, "weekly")
