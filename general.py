import mode

def prevent_freezing():
    # Patch mode to ensure we crash
    # Issue: https://github.com/robinhood/faust/issues/484

    original = mode.Worker._shutdown_loop
    def _and_die(self) -> None:
        try:
            original(self)
        finally:
            import os
            os._exit(1)
    mode.Worker._shutdown_loop = _and_die
