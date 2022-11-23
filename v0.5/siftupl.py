#python3

from Crypto.Hash import SHA256
from siftmtp import SiFT_MTP, SiFT_MTP_Error

class SiFT_UPL_Error(Exception):

    def __init__(self, err_msg):
        self.err_msg = err_msg

class SiFT_UPL:
    def __init__(self, mtp: SiFT_MTP):

        self.DEBUG = False
        # --------- CONSTANTS ------------
        self.delimiter = '\n'
        self.coding = 'utf-8'
        self.size_fragment = 1024
        # --------- STATE ------------
        self.mtp = mtp

    # The server uses this
    # builds an upload response from a dictionary
    def build_upload_res(self, upl_res_struct):
        upl_res_str = upl_res_struct['file_hash'].hex()
        upl_res_str += self.delimiter + str(upl_res_struct['file_size'])
        return upl_res_str.encode(self.coding)

    # The client uses this
    # parses an upload response into a dictionary
    def parse_upload_res(self, upl_res):

        upl_res_fields = upl_res.decode(self.coding).split(self.delimiter)
        upl_res_struct = {}
        upl_res_struct['file_hash'] = bytes.fromhex(upl_res_fields[0])
        upl_res_struct['file_size'] = int(upl_res_fields[1])
        return upl_res_struct


    # uploads file at filepath in fragments to the server (to be used by the client)
    def handle_upload_client(self, filepath):

        # TODO: implement this function!
        file = open(filepath, 'rb')
        chunk = file.read(self.size_fragment)
        file_size = 0
        h = SHA256.new()


        while chunk and len(chunk) > 1024:
            file_size += self.size_fragment
            chunk = file.read(self.size_fragment)
            chunk = chunk.decode("utf-8")
            self.mtp.send_msg(self.mtp.type_upload_req_0, chunk)
            h.update(chunk)

        file_size += len(chunk)
        self.mtp.send_msg(self.mtp.type_upload_req_1, chunk)
        h.update(chunk)
        file.close()

        # trying to receive a upload respoonse
        try:
            msg_type, msg_payload = self.mtp.receive_msg()
        except SiFT_MTP_Error as e:
            raise Exception('Unable to receive server to client response --> ' + e.err_msg)

        # # DEBUG
        # if self.DEBUG:
        #     print('Incoming payload (' + str(len(msg_payload)) + '):')
        #     print(msg_payload[:max(512, len(msg_payload))].decode('utf-8'))
        #     print('------------------------------------------')
        # # DEBUG

        if msg_type != self.mtp.type_upload_res:
            raise Exception('Login response expected, but received something else')

        # processing login response
        message_res_struct = self.parse_upload_res(msg_payload)

        # checking request_hash receiveid in the login response
        if message_res_struct['file_hash'] != h.digest():
            raise Exception('Verification of login response failed')



        # Fragment size of 1024 bytes => self.size_fragment
        # Cut the file into those bytes
        # Each segment is uploaded by request_0, only the last one us uploaded by request_1
        # Compute the size of the uploaded file and its SHA-256 hash value


    # handles a file upload on the server (to be used by the server)
    def handle_upload_server(self, filepath):

        # try:
        #     msg_type, msg_payload = self.mtp.receive_msg()
        # except SiFT_MTP_Error as e:
        #     raise Exception('Unable to receive login request --> ' + e.err_msg)

        # file = open(filepath, "a")
        # file.write(msg_payload)
        # file.close()


        # TODO: implement this function!
        type, body = self.mtp.receive_msg()
        if not (type == self.mtp.type_upload_req_0 or type == self.mtp.type_upload_req_1):
            raise Exception("Expect request")

        file = open(filepath, "a")

        file_size = 0
        h = SHA256.new()
        content = ""

        if type == self.mtp.type_upload_req_0:
            while type == self.mtp.type_upload_req_0:
                file.write(body)
                content += body
                # Check if it is one
                type, body = self.mtp.receive_msg()


        # file = open(filepath, 'rb')
        # chunk = file.read(self.size_fragment)
        type, body = self.mtp.receive_msg()
        file.write(body)
        content += body

        file.close()

        h.update(content)
        #
        # while chunk and len(chunk) > 1024:
        #     file_size += self.size_fragment
        #     chunk = file.read(self.size_fragment)
        #     chunk = chunk.decode("utf-8")
        #     h.update(chunk)
        # 
        # file_size += len(chunk)
        # h.update()
        #
        # file.close()

        struct = {}
        struct["file_hash"] = h.digest()
        struct["file_size"] = file_size

        response = self.build_upload_res(struct)

        try:
            self.mtp.send_msg(self.mtp.type_upload_res, response)
        except SiFT_MTP_Error as e:
            raise Exception('Unable to send server response --> ' + e.err_msg)




