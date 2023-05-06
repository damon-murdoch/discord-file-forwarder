# File Configuration
LOG_FILE = 'forwarder.log'

# List of paths to monitor, and the channels to forward to
MONITOR = [
    {
        "path": "your_file_or_folder",
        "channel": 0
    }
]

# Seconds between checks
MONITOR_DELAY = 5

# API Token
DISCORD_TOKEN = 'discord_api_token'
