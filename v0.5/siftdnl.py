#python3

from Crypto.Hash import SHA256
from siftmtp import SiFT_MTP, SiFT_MTP_Error

class SiFT_DNL_Error(Exception):

    def __init__(self, err_msg):
        self.err_msg = err_msg

class SiFT_DNL:
    def __init__(self, mtp):

        self.DEBUG = False
        # --------- CONSTANTS ------------
        self.size_fragment = 1024
        self.coding = 'utf-8'
        self.ready = 'ready'
        self.cancel = 'cancel'
        # --------- STATE ------------
        self.mtp = mtp


    # cancels file download by the client (to be used by the client)
    def cancel_download_client(self):
        # The client sends cancel, dnload_req
        # TODO: implement this function!



    # handles file download at the client (to be used by the client)
    def handle_download_client(self, filepath):
        # Recieve and saves the messages
        # TODO: implement this function!

        # return file_hash


    # handles a file download on the server (to be used by the server)
    def handle_download_server(self, filepath):
        # If the client says ready, split the message and send them in chunks to clients
        # TODO: implement this function!


