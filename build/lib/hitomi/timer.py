import time

class TimerManager:
    def __init__(self, callback=None):
        """
        Initializes the TimerManager object.

        Args:
            callback (function, optional): The callback function to be called every second. Defaults to None.
        """
        self.callback = callback
        self.is_general_purpose = callback is None
        self.started  = False
        self.completed = True
        self.running = False

    def start(self, hrs=0, mints=0, secs= 10):
        """
        Starts the timer.

        Args:
            hrs (int, optional): The number of hours to count down from. Defaults to 0.
            mints (int, optional): The number of minutes to count down from. Defaults to 0.
            secs (int, optional): The number of seconds to count down from. Defaults to 10.
        """
        if not self.started:
            self.completed = False
            self.running = True
            self.started = True
            while (hrs > 0 or mints > 0 or secs > 0) and not self.completed:
                if self.running:
                    if self.callback:  # Check if a callback function is provided
                        self.callback(hrs, mints, secs)
                    time.sleep(1)
                    secs -= 1

                    if secs < 0:
                        secs = 59
                        mints -= 1

                        if mints < 0:
                            mints = 59
                            hrs -= 1

            self.callback(0, 0, 0) # Call the callback function with 0 values when the timer is completed
            time.sleep(1)

    def reset_vars(self):
        """
        Resets the timer variables to their initial state.
        """
        if  self.started:
            self.completed = True
            self.running = False
            self.started = False

    def alter_status(self):
        """
        Alters the running status of the timer (pauses or resumes).
        """
        if not self.completed:
            self.running = not self.running

    def stop(self):
        """
        Stops the timer.
        """
        if self.started:
            self.reset_vars()

def own_callback(hrs, mints, secs):
    print(hrs, mints, secs)
