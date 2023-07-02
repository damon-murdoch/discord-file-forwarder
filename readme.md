## Discord File Forwarder
## Created by Damon Murdoch ([@SirScrubbington](https://twitter.com/SirScrubbington))

## Description

This script implements a Discord bot that monitors a specified directory for new files 
and automatically uploads them to a designated Discord channel. The bot is built 
using the Discord.py library and utilizes the dotenv library for managing environment variables.

### Version
The latest revision for this software is 1.0.

### Language
Python 3.x

### Date Created
Sunday, 2 July 2023 4:04:20 PM

### Prerequisites

- Python 3.x installed on your system.
- Discord bot token obtained from the Discord Developer Portal.
- Discord channel ID where the files will be uploaded.

### Setup

1. Ensure Python is installed

Make sure you have Python 3.x installed on your system. You can download the latest 
version of Python from the official website: https://www.python.org/downloads/

2. Install Dependencies

Open a terminal or command prompt and navigate to the directory where you have saved 
the script. Then, install the required dependencies by running the following command:

```
pip install -r requirements.txt
```

This command will install the necessary dependencies, including Discord.py and dotenv.

3. Set up Environment Variables

Create a `.env` file in the same directory as the script. In 
the `.env` file, set the following environment variables:

   - `DISCORD_TOKEN`: Your Discord bot token.
   - `DISCORD_CHANNEL`: The Discord channel ID where the files will be uploaded.
   - `MONITOR_PATH` (Optional): The path to the directory you want to monitor for new files. By default, it is set to "monitor" in the current working directory.
   - `MONITOR_DELAY` (Optional): The delay in seconds between each check for new files. By default, it is set to 5 seconds.

4. Run the Script: Open a terminal or command prompt and navigate to the directory 
where you have saved the script. Then, execute the following command to run the script:

```
python file_monitor_bot.py
```

The bot will start and connect to Discord. It will continuously monitor the specified 
directory for new files. When a new file is detected, it will be automatically 
uploaded to the specified Discord channel. The bot will log its activities to 
the console, indicating the status of each file upload attempt.

Make sure to keep the script running for the bot to remain active and monitor the directory.

Feel free to customize the script according to your needs, such as modifying 
the file monitoring path, delay, or adding additional functionality.

## Future Changes
A list of future planned changes are listed below.

| Change Description | Priority |
| ------------------ | -------- | 
| No planned changes | -        |

### Problems or improvements
If you have any suggested fixes or improvements for this project, please 
feel free to open an issue [here](../../issues).

### Sponsor Me
If you would like to sponsor this project, please feel free to 
make a donation [here](https://www.paypal.com/paypalme/sirsc).

