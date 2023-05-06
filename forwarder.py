from genericpath import isfile
import os

import discord
from discord.ext import commands
from discord.ext import tasks

# File / Directory Watcher Classes
import watcher.dir_watcher as dir_watcher
import watcher.file_watcher as file_watcher

import util.log as log

import intents
import config

# This script is being called
if __name__ == '__main__':

    # List of watchers
    WATCHERS = []

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

        # Start the file loop
        upload_files.start()

        # Set the global channel object to the channel
        # CHANNEL = bot.get_channel(config.DISCORD_CHANNEL)
        for watcher in config.MONITOR:

            try:

                # Get the absolute path to the directory
                path = os.path.abspath(watcher["path"])

                # Get the discord channel id to forward to
                channel = watcher["channel"]

                # Path is a file
                if os.path.isfile(path):

                    # Create file watcher object
                    #WATCHERS.append(file_watcher.Watcher(path, channel))
                    pass

                # Path is a directory
                elif os.path.isdir(path):

                    # Create the dir watcher object
                    WATCHERS.append(dir_watcher.Watcher(path, channel))

                else:  # Not a file / folder
                    raise Exception(f"Not a file or folder: {path}!")

            except Exception as e:  # General failure

                log.write_log(
                    f"Watcher skipped: {str(e)}",
                    "error"
                )

        log.write_log("Bot ready.", "success")

    # Scheduled Task

    @tasks.loop(seconds=config.MONITOR_DELAY)
    async def upload_files():

        # List of file watchers
        global WATCHERS

        # Watcher Callback Function
        async def callback(content, channel, isfile: bool):

            try:

                # Get the channel with the id
                channel = bot.get_channel(channel)

                # Message is a file
                if isfile:

                    # Send the file to the channel
                    await channel.send(file=discord.File(content))

                else:  # Standard message

                    # Send the message to the channel
                    await channel.send(content)

                # Sent successfully
                return True

            # Failed to send message
            except Exception as e:

                log.write_log(
                    f"Failed to send message: {str(e)}",
                    "error"
                )

                # Failed to send
                return False

        # Loop over all of the watchers
        for watcher in WATCHERS:
            
            # Update the watcher using the callback
            watcher.update(callback)

    bot.run(config.DISCORD_TOKEN)
