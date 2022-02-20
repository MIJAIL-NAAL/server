# Server for receiving and storing metrics in process memory

import asyncio
from collections import defaultdict


class StorageDataError(ValueError):
    pass


class Storage:
    """ A class for storing metrics in process memory """

    def __init__(self):
        self._storage = defaultdict(dict)

    def put(self, key, value, timestamp):
        self._storage[key][timestamp] = value

    def get(self, key):
        if key == '*':
            return dict(self._storage)
        if key in self._storage:
            return {"{}: {}".format(key,(dict(self._storage))[key])}
        
        return {}


class ClientServerProtocol(asyncio.Protocol):
    """ A class for implementing a server using asyncio """
    storage = Storage()
    
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        """ The data_received method is called when data is received in the socket """
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())

    def check_data(self, data):
        method, *params = data.split()

        if method == "put":
            key, value, timestamp = params
            value, timestamp = float(value), int(timestamp)
            self.storage.put(key, value, timestamp)
            return {}
        elif method == "get":
            key = params.pop()
            if params:
                raise StorageDataError
            return self.storage.get(key)
        else:
            raise StorageDataError

    def process_data(self, data):
        self.data = data

        try:
            request = self.data
            if not request.endswith("\n"):
                return

            raw_data = self.check_data(request.rstrip("\n"))

            message = ""

            for key, values in raw_data:
                message += "\n".join(f'{key} {value} {timestamp}' for timestamp, value in sorted(values))
                message += "\n"

            code = "ok"
        except (ValueError, UnicodeDecodeError, IndexError):
            message = "wrong command" + "\n"
            code = "error"

        response = f'{code}\n{message}\n'
        
        return response


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == "__main__":
    run_server("127.0.0.1", 8888)
