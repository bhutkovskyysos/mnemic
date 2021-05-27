"""The trace client to record diagnostics."""

import asyncio
import os
import tracemalloc

import psutil

import dolon.impl.db_conn_impl as db_conn_impl
import dolon.impl.db_stats as db_stats
import dolon.impl.trace_client_impl as trace_client_impl


async def start_tracer(app_name, frequency, host, port, *diagnostics):
    """Starts a tracer.

    Any exception that will be caught will stop the application.

    :param str app_name: The application name that will tag the trace.
    :param int frequency: The sleep interval between consecutive traces.
    :param int port: The port to listen for messages.
    :param diagnostics: The diagnostic functions to record.
    """
    try:
        tc = trace_client_impl.TraceClientImpl(
            app_name,
            host,
            port,
            *diagnostics
        )
        async with tc:
            await tc.run(frequency)
    except Exception as ex:
        print(ex)
        exit(-1)


class PostgresDiagnostics(db_conn_impl.DbConnectionImpl):
    """Wraps memory diagnostics within an async context manager.

    :ivar str conn_str: The connection string to the database.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def live_msgs(self):
        """Returns the number of live messages in db."""
        return await db_stats.live_msgs_in_db.get_value(self)

    async def dead_msgs(self):
        """Returns the number of dead messages in db."""
        return await db_stats.dead_msgs_in_db.get_value(self)

    async def idle(self):
        """Returns the number of idle sessions in db."""
        return await db_stats.idle_in_db.get_value(self)

    async def dn_conn(self):
        """Returns the number of connections in db."""
        return await db_stats.conn_count_in_db.get_value(self)


class MemoryDiagnostics:
    """Wraps memory diagnostics within an async context manager."""

    async def __aenter__(self):
        """Enters the context."""
        tracemalloc.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exits from the context."""
        tracemalloc.stop()

    async def mem_allocation(self):
        """Returns the size of the allocated memory in Mb."""
        current, peak = tracemalloc.get_traced_memory()
        return current / 10 ** 6


async def active_tasks():
    """Returns the number of active tasks."""
    return len([task for task in asyncio.Task.all_tasks() if not task.done()])


async def cpu_percent():
    """Returns the CPU usage."""
    return psutil.cpu_percent()


async def virtual_memory_percent():
    """Returns the virtual memory percentage usage."""
    return psutil.virtual_memory().percent


async def memory_use():
    """Returns the virtual memory percentage usage."""
    pid = os.getpid()
    py = psutil.Process(pid)
    return py.memory_info()[0] / 2. ** 30
