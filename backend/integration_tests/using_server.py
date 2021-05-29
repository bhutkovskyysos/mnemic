"""Sample of using server to create a trace."""

import asyncio
import random

import dolon.trace_client as tc
import dolon.profiler as profiler

_CONN_STR = f'postgresql://postgres:postgres123@127.0.0.1:5432/mnemic'


@profiler.profiler
async def foo():
    await asyncio.sleep(random.uniform(0.1, 3))


@profiler.profiler
async def goo():
    await asyncio.sleep(random.uniform(0.1, 3))


async def backend_process():
    while True:
        asyncio.ensure_future(foo())
        asyncio.ensure_future(goo())
        await asyncio.sleep(0.1)


async def main():
    host = "127.0.0.1"
    port = 12012

    async with tc.MemoryDiagnostics() as mem_diag, tc.PostgresDiagnostics(
            conn_str=_CONN_STR) as db_diag:
        await tc.start_tracer(
            "func-profiler", 1, host, port,
            mem_diag.mem_allocation,
            tc.active_tasks
        )


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    asyncio.ensure_future(backend_process())
    loop.run_until_complete(main())
