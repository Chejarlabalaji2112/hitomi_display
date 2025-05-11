import time

class StopwatchManager:
    def __init__(self, callback=None):
        """
        Initializes the StopwatchManager object.

        Args:
            callback (function, optional): The callback function to be called every second. Defaults to None.
        """
        self.callback = callback
        self.is_started = False
        self.is_running = False
        self.is_stop = False
        self.time_stamp = False

    def start(self):
        """
        Starts the stopwatch.
        """
        hrs = mints = secs = 0
        self.is_started = self.is_running = True
        while not self.is_stop: # Loop until the stopwatch is stopped
            if self.is_running: # Check if the stopwatch is running
                if self.callback: # Check if a callback function is provided
                    if self.time_stamp:
                        self.callback(hrs, mints, secs, self.time_stamp)
                        self.time_stamp = False
                    else:
                        self.callback(hrs, mints, secs)
                secs += 1
                time.sleep(1)

                if secs > 59:
                    secs = 0
                    mints += 1

                    if mints > 59:
                        mints = 0
                        hrs += 1

        self.callback(0,0,0) # Call the callback function with 0 values when the stopwatch is stopped
        time.sleep(1)
        self.reset_vars()


    def alter(self):
        """
        Alters the running status of the stopwatch (pauses or resumes).
        """
        if self.is_started:
            self.is_running = not self.is_running

    def stop(self):
        """
        Stops the stopwatch.
        """
        if self.is_started:
            self.is_stop = True

    def reset_vars(self):
        """
        Resets the stopwatch variables to their initial state.
        """
        self.is_stop = False
        self.is_started = False
        self.is_running = False
