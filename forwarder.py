import os

import discord
from discord.ext import commands
from discord.ext import tasks

import util.log as log

import intents
import config

# This script is being called
if __name__ == '__main__':

    # Full path to the directory
    WATCHDIR = os.path.join(
        os.getcwd(),
        config.MONITOR_PATH
    )

    # Channel to send messages to
    CHANNEL = None

    # Get all of the files in the
    # directory we are monitoring
    FILES = set(os.listdir(WATCHDIR))

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

        # Set the global channel object to the channel
        CHANNEL = bot.get_channel(config.DISCORD_CHANNEL)

        log.write_log("Bot ready.", "success")

    # Scheduled Task

    @tasks.loop(seconds=config.MONITOR_DELAY)
    async def upload_files():

        # Global Variables
        global FILES, WATCHDIR, CHANNEL

        log.write_log(
            "Checking for new files ...",
            "info"
        )

        # Get the current files in the directory
        files = set(os.listdir(WATCHDIR))

        # Get the difference between the two lists
        diff = files - FILES

        # At least one file found
        if len(diff) > 0:

            log.write_log(
                f"New files found: {len(diff)}",
                "success"
            )

            # Loop over the new files
            for file in diff:

                # Get the full path to the new file
                filepath = os.path.join(WATCHDIR, file)

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
    bot.run(config.DISCORD_TOKEN)
