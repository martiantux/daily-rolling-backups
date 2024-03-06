# Daily and Weekly Code Backups

A basic Python script that I wrote for making and maintaining daily and weekly rolling backups in zip archives of my code/project directories I keep off-cloud due to lots of tiny files for things such as git, etc. The script generates daily and weekly backups, stores them in specified directories, and maintains a configured number of backups before rolling over and deleting the oldest backups.

## Features

- Creates daily backups of the specified source directory.
- Generates additional weekly backups on a configured day of the week.
- Maintains a set number of daily and weekly backups, automatically deleting the oldest ones beyond the configured count.
- Logs operations and statuses to a Discord channel via webhook, including backup creation and deletion details, with embed colour/title config.

## Configuration

Before running the script, ensure you've set up the `config.ini` file with your specific settings:

- `SOURCE_DIR`: The directory containing your code projects to be backed up.
- `TARGET_DIR`: The target directory where backup archives will be stored. This directory will contain subdirectories for daily and weekly backups. Tip: Use a cloud solution.
- `DAILY_BACKUP_DAYS`: The number of daily backups to keep before purging the oldest.
- `WEEKLY_BACKUP_DAYS`: The number of weekly backups to keep before purging the oldest.
- `WEEKLY_BACKUP_DAY`: The day of the week to perform weekly backups (e.g., `Wednesday`).
- `DISCORD_WEBHOOK_URL`: The webhook URL for logging to a Discord channel.
- `LOG_PREFIX`: A prefix for log messages to easily identify them in Discord.
- `LOG_COLOR`: The color of the embed in the Discord message, specified in hexadecimal format (e.g., `#58C4DD`).

## Usage

### Testing / One-off run

To run the backup script, use the following command in your command prompt or PowerShell, adjusting the path to where your script is located:

```cmd
python path\to\your\script\daily_weekly_backups.py
```

### Automating on Windows

To set up automatic daily runs of the backup script, follow these brief steps:

* Open Task Scheduler: Start > Windows Administrative Tools > Task Scheduler
* Create a New Task: Action > Create Task
* Name the task (e.g., "Project Backups")
* Set the Trigger: Triggers tab > New
* Set to Daily and choose your time
* Set the Action: Actions tab > New
* Program/script: path to your Python executable
* Add arguments: path to the script
* Save

## License and Credits

This project, developed by Bradley James Hammond (Martian Tux) and Distracted Labs, is licensed under the GNU General Public License v3.0. Full license text is available in the [LICENSE](LICENSE) file.

Contributions, feedback, and adaptations are welcome in accordance with the terms of this license. Please credit and provide a link back to the original source when using this project or its components.

For inquiries or further information, contact martiantux@proton.me or hello@distractedlabs.cc.

Stay connected and support my projects:
- [Follow on Instagram](https://instagram.com/martiantux)
- [Chat on Telegram](https://t.me/martiantux)
- [Support on Patreon](https://patreon.com/martiantux)
