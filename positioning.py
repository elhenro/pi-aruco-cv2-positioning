
import asyncio
import logging
import time
import concurrent

# Create a limited thread pool. Ensure at any time only one thread accesses the camera.
executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)

# async factory function to spawn a PositioningSystem in a new thread
async def track(on_update):
    ps = PositioningSystem(on_update)

    loop = asyncio.get_event_loop()
    loop.run_in_executor(executor, ps.start)
    return ps

class PositioningSystem:
    def __init__(self, on_update):
        self._on_update = on_update
        self._running = False

    def start(self):
        self._running = True

        # per default there is not event loop in a forked thread, so we create
        # one and add the capture routine
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self._capture());
        loop.run_forever()
        self._loop = loop

    def stop(self):
        self._running = False

    # main capture function
    async def _capture(self):
        # here comes the actual capture loop
        while self._running:
            time.sleep(3);
            if callable(self._on_update):
                await self._on_update("tick")
        # don't forget to close the camera here
