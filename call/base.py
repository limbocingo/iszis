from socket import SOL_SOCKET, SO_REUSEADDR
from socket import socket

from .util import Utilities


class BaseApplication(socket):
    """A base for creating a socket server.

    Public methods of the class:
        - `start`: Start the .
        - `request`: Information sended to the client.

    Private methods of the class:
        - `socket`: Accepts the requests gived and handle it.
    """

    def __init__(self, address: str, port: int) -> None:
        """Initializator of the :class:`BaseServer` class.

        Public class variables:
            - `address`: IP where the socket server will be executed.
            - `port`: Where will listen the requests.

        Private class variables:
            - `status`: Status of the current server.
        """
        #: Address and port where all the
        #: requests will be made.
        self.address = address
        self.port = port

        #: The current status of the socket,
        #: it can be two values `True` or `False`.
        #: `True` is that the server is on and
        #: `False` is the opposite of `True`.
        self.__status = False

        #: Initialize the socket
        #: and specifie the level of the
        #: current socket (TCP).
        super().__init__()
        self.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def response(self, request) -> bytes: return None

    def start(self) -> None:
        """
        Run you'r socket server &
        call the :func:`switcher` and the :func:`socket` functions.
        """
        try:
            print(f'''* Server is using Cast
* WARNING: This framework isn't a hundred percent confirmed
           that on production will work properly.
* Running on {self.address}:{self.port} (Press Q to quit) 
            ''')
            self.__socket()
            self.__switcher()

        except Exception as exception:
            print('ERROR!\n',
                  'An exception ocurred during the execution of a important function,\n',
                  'please create a issue on the github page of the code and paste the next:',
                  '\n\n' + str(exception)
                  )

    @Utilities.process
    def __socket(self) -> None:
        """
        Accept the requests gived on the port gived and
        send information gived in function :func:`request`.
        """
        self.bind((self.address, self.port))
        self.listen()

        try:
            self.__status = True
            client, address = self.accept()
            while self.__status:
                try:
                    # response gived to the request maked
                    response: bytes = self.response(
                        {
                            'address': address,
                            'receive': client.recv(16384)
                        }
                    )

                    client.send(response)
                    client.close()

                except OSError as exception:
                    # raise a error when the current request was already closed
                    # and make a new accept for the new request incoming
                    if not exception.winerror.__eq__(10038):
                        raise exception
                    client, address = self.accept()

        except KeyboardInterrupt:
            print('Warn!\n',
                  'The keyboard interrupt is disabled so you can\'t\n',
                  'make combinations like this CTRL+C or CTRL+Z.')

        except OSError as exception:
            if not exception.winerror.__eq__(10038):
                raise exception
            pass

    @Utilities.process
    def __switcher(self):
        """
        Is seeing if the key `Q` is pressed
        for closing the socket server.
        """
        from keyboard import is_pressed

        while not is_pressed('q'):
            self.__status = True
        else:
            self.__status = False
            self.close()
