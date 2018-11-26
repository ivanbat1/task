import zmq
import numpy as np


class zmq_python():

    def __init__(self):
        # Create ZMQ Context
        self.context = zmq.Context()

        # Create REQ Socket
        self.reqSocket = self.context.socket(zmq.REQ)
        self.reqSocket.connect("tcp://localhost:5557")

        # Create PULL Socket
        self.pullSocket = self.context.socket(zmq.PULL)
        self.pullSocket.connect("tcp://localhost:5558")

    def remote_send(self, socket, data):

        try:
            socket.send_string(data)
            msg_send = socket.recv_string()
            print (msg_send)

        except zmq.Again as e:
            print ("Waiting for PUSH from MetaTrader 4..")

    def remote_pull(self, socket):

        try:
            msg_pull = socket.recv(flags=zmq.NOBLOCK)
            return msg_pull

        except zmq.Again as e:
            print ("Waiting for PUSH from MetaTrader 4..")

    def get_data(self, symbol):
        '''
        only start_bar and end_bar as int
        '''
        self.data = "DATA|" + symbol
                    # + "|" + "PERIOD_" + timeframe + "|" + str(start_bar) + "|" + str(end_bar + 1)
        self.remote_send(self.reqSocket, self.data)
        prices = self.remote_pull(self.pullSocket)
        prices_str = str(prices)
        price_lst_1 = prices_str.split(',')
        price_lst = [i.split('|') for i in price_lst_1]
        # price_lst = prices_str.split('|')
        # price_lst = price_lst[::-1]
        # price_arr = np.array(price_lst)
        return price_lst
