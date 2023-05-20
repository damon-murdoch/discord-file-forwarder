# External Libraries
from genericpath import isfile
from dotenv import load_dotenv
import os

# Discord
from discord.ext import commands
from discord.ext import tasks
import intents
import discord

# Internal Libraries
import util.common as common
import util.log as log

# This script is being called
if __name__ == '__main__':

    # Load environment variables
    load_dotenv()

    # Discord bot token (Error if not set)
    token = common.get_env('DISCORD_TOKEN', errorOnNull=True)

    # Get environment variable for folder path to forward
    path = common.get_env('MONITOR_PATH', default='monitor')

    # Get delay in seconds between checking the path for files
    delay = int(common.get_env('MONITOR_DELAY', default='5'))

    # Build full path to the directory
    WATCHDIR = os.path.join(os.getcwd(), path)

    # Channel to send messages to
    CHANNEL = None

    # Get all of the files in the
    # directory we are monitoring
    FILES = set(os.listdir(WATCHDIR))

    # Files which should be re-attempted
    RETRY = []

    # Bot startup event
    log.write_log("Bot starting ...", "info")

    # Wait for bot to start
    started = False

    # Discord Bot Object
    bot = commands.Bot(
        command_prefix="",
        intents=intents.intents
    )

    # On Ready Event

    @bot.event
    async def on_ready():

        global CHANNEL

        # Start the file loop
        upload_files.start()

        # Get discord channel id to forward to (Error on null)
        channel = common.get_env('DISCORD_CHANNEL', errorOnNull=True)

        log.write_log(f"Uploading to channel '{channel}' ...", "info")

        # Set the global channel object to the channel
        CHANNEL = bot.get_channel(channel)

        log.write_log("Bot ready.", "success")

    # Scheduled Task

    @tasks.loop(seconds=delay)
    async def upload_files():

        # Global Variables
        global FILES, RETRY, WATCHDIR, CHANNEL

        log.write_log(
            "Checking for new files ...",
            "info"
        )

        # Get the current files in the directory
        files = set(os.listdir(WATCHDIR))

        # Get the files which should be re-attempted
        retry = set(RETRY)

        # Empty the global array
        RETRY = []

        # Get the difference between the
        # two lists, and add the retry list
        diff = (files - FILES) | retry

        # At least one file found
        if len(diff) > 0:

            log.write_log(
                f"New files found: {len(diff)}",
                "success"
            )

            # Loop over the new files
            for file in diff:

                try:

                    # Get the full path to the new file
                    filepath = os.path.join(WATCHDIR, file)

                    # If the filepath exists
                    if os.path.isfile(filepath):

                        # Get the stats for the file
                        stats = os.stat(filepath)

                        # If the file's size is 0 bytes
                        if stats.st_size == 0:
                            raise Exception("File is empty / not finished!")

                        log.write_log(
                            f"Sending file: [{file}] ...",
                            "info"
                        )

                        # Send the file to the channel
                        await CHANNEL.send(file=discord.File(filepath))

                        log.write_log(
                            "File sent.",
                            "success"
                        )

                    else:  # Could not find file
                        raise Exception("File not found / not a file!")

                except Exception as e:  # Failed to read file

                    log.write_log(
                        f"Failed to send file: [{file}]! {str(e)}",
                        "error"
                    )

                    # Add the file to the retry list
                    RETRY.append(file)

                    log.write_log(
                        f"File [{file}] added to retry list.",
                        "info"
                    )

        else:  # Otherwise, no changes detected

            log.write_log(
                f"No new files.",
                "info"
            )

        # Update the files list
        FILES = files

        log.write_log(
            f"File list updated.",
            "success"
        )

    # Run the client using the discord token
    bot.run(token)
