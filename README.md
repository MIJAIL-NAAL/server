# Server for receiving metrics

The server must be able to receive put and get commands from clients, analyze them, and form a response according to the protocol.

<br>

### Server responses

<br>

Example of data storage on the server:


| key | value | timestamp |
| :---: | :---: | :---: |
| "server.cpu" | 2.0 | 1150864247 |
| "server.cpu" | 0.5 | 1150864248 |
| "other.cpu" | 0.5 | 1150864250 |

If request `get server.cpu\n`, the server will send the string:

> ok\nserver.cpu 2.0 1150864247\nserver.cpu 0.5 1150864248\n\n

<br>

If request `get *\n`, the server will send the string:

> ok\nserver.cpu 2.0 1150864247\nserver.cpu 0.5 1150864248\nother.cpu 3.0 1150864250\n\n

<br>

In the following cases:

- when a non-existing key is passed in the data request

- successful execution of the put data saving command

The server sends to client a string with the status "ok" and an empty field with the response data:

> ok\n\n

<br>

If invalid data is passed in the request parameter (for example: the request format is violated, an erroneous command or
the values of value and timestamp cannot be converted to the required data type), the server sends a string with
the response status "error" and the response data "wrong command":

> error\nwrong command\n\n

