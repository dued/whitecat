#!/usr/bin/env python3

import asyncio
import logging
import os
import random

from dns.resolver import Resolver

logging.root.setLevel(logging.INFO)

mode = os.environ["MODE"]
ports = os.environ["PORT"].split()
ip = target = os.environ["TARGET"]

# Resolve target si es requerido
if os.environ["PRE_RESOLVE"] == "1":
    resolver = Resolver()
    resolver.nameservers = os.environ["NAMESERVERS"].split()
    ip = random.choice([answer.address for answer in resolver.query(target)])
    logging.info("Resolved %s to %s", target, ip)


@asyncio.coroutine
async def netcat(port):
    # Usamos la versión BusyBox (persistente) de netcat server en modo escucha 
    command = ["socat"]
    # Verbose mode
    if os.environ["VERBOSE"] == "1":
        command.append("-v")
    command += [f"{mode}-listen:{port},fork,reuseaddr",
                f"{mode}-connect:{ip}:{port}"]
    # Crea el proceso y espera hasta que salga
    logging.info("Whitecat ejecutando: %s", " ".join(command))
    process = await asyncio.create_subprocess_exec(*command)
    await process.wait()


# Wait until all proxies exited, if they ever do
# Espere hasta que salgan todos los proxies, si alguna vez lo hacen
try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*map(netcat, ports)))
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
