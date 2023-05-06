import os

# Logging Function
import util.log as log


class Watcher:

    # Constructor
    def __init__(self, path, channel):

        # List of files currently present
        self.files = []

        # List of files to retry
        self.retry = []

        # Path to check for files
        self.path = path

        # Channel ID to send content to
        self.channel = channel

    # Get the new files in the folder,
    # pass the result to the callback
    def update(self, callback):

        log.write_log(
            "Checking for new files ...",
            "info"
        )

        # Get the current files in the directory
        files = set(os.listdir(self.path))

        # Get the files which should be re-attempted
        retry = set(self.retry)

        # Empty the retry list
        self.retry = []

        # Get the difference between the
        # two lists, and add the retry list
        diff = (files - self.files) | retry

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
                    filepath = os.path.join(self.path, file)

                    # If the filepath exists
                    if os.path.isfile(filepath):

                        # Get the stats for the file
                        stats = os.stat(filepath)

                        # If the file's size is 0 bytes
                        if stats.st_size == 0:
                            raise Exception("File is empty / not finished!")

                        # Pass the filename, channel to the callback
                        if (callback(filepath, self.channel, True)):
                            log.write_log(
                                f"File [{file}] sent successfully.",
                                "success"
                            )
                        else:  # Failed to send the file
                            raise Exception("Failed to send message!")

                    else:  # Could not find file
                        raise Exception("File not found / not a file!")

                except Exception as e:  # Failed to read file

                    log.write_log(
                        f"Failed to send file: [{file}]! {str(e)}",
                        "error"
                    )

                    # Add the file to the retry list
                    self.retry.append(file)

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
        self.files = files

        log.write_log(
            f"File list updated.",
            "success"
        )
