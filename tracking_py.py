#!/usr/bin/env python

import asyncio
import websockets
import logging
import json
import atexit
import time
import concurrent
import positioning

PORT = 5678
logging.basicConfig(level="INFO")

sockets = set()
loop = asyncio.get_event_loop()

async def on_connect(socket, path):
    logging.info('Socket connected')
    sockets.add(socket)
    try:
        while True:
            message = await socket.recv()
            logging.warning('Ignoring received message: %s', message)
    except:
        sockets.remove(socket)
        logging.info('Socket disconnected (maybe in response to closing handshake)')

async def on_track(position):
    logging.info('Sending position update: %s', position)
    for socket in sockets:
        await socket.send(position)

if __name__ == "__main__":
    logging.info("Starting capture loop...")
    start_positioning = positioning.track(on_track)
    logging.info("Starting websocket server...")
    start_server = websockets.serve(on_connect, port=PORT)

    loop.run_until_complete(start_positioning)
    loop.run_until_complete(start_server)

    logging.info('All started. Listening on port: %d', PORT)
    loop.run_forever()
