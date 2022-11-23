#python3

from Crypto.Hash import SHA256
from siftmtp import SiFT_MTP, SiFT_MTP_Error

class SiFT_DNL_Error(Exception):

    def __init__(self, err_msg):
        self.err_msg = err_msg

class SiFT_DNL:
    def __init__(self, mtp: SiFT_MTP):

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
        self.mtp.send_msg(self.mtp.type_dnload_req, "cancel")
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
        try:
            msg_type, msg_payload = self.mtp.receive_msg()
        except SiFT_MTP_Error as e:
            raise Exception('Unable to receive server to client download response --> ' + e.err_msg)
        # Check if the message type is the right one
        if msg_type != self.mtp.type_dnload_req:
            raise Exception('Download request expected, but received something else')

        if msg_payload != "cancel":
            # Read the file to send
            file = open(filepath, 'rb')
            chunk = file.read(self.size_fragment)
            file_size = 0
            h = SHA256.new()

            # Check
            while chunk:
                file_size += self.size_fragment
                chunk = file.read(self.size_fragment)
                h.update(chunk)
                self.mtp.send_msg(self.mtp.type_dnload_res_0, chunk)

            file_size += len(chunk)
            h.update(chunk)
            self.mtp.send_msg(self.mtp.type_dnload_res_1, chunk)

            file.close()





