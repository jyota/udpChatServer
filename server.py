import socket
import json
import yaml
from simpledb import SimpleDb

class UDPServer(object):
    def __init__(self,host,port):
        self._host = host
        self._port = port

    def __enter__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self._host,self._port))
        self._sock = sock
        return sock

    def __exit__(self,*exc_info):
        if exc_info[0]:
            import traceback
            traceback.print_exception(*exc_info)
        self._sock.close()

if __name__ == '__main__':
    with open('config.yaml', 'r') as fp:
        options = yaml.load(fp)

    host = options.get('server').get('host') 
    port = options.get('server').get('port') 
    database = SimpleDb(options.get('server').get('user_message_cache_size', 10))

    with UDPServer(host,port) as s:
        while True:
            msg, addr = s.recvfrom(1024)
            try:
                data_received = json.loads(msg.decode().strip())
                action = data_received.get('action')
                if action == 'register':
                    register_result = database.register_user(data_received.get('username'), addr)
                    s.sendto(json.dumps(register_result).encode(), addr)
                elif action == 'get_user_id':
                    user_query_result = database.get_user_id_from_username(data_received.get('username'))
                    s.sendto(json.dumps(user_query_result).encode(), addr)
                elif action == 'send':
                    send_result = database.assign_message_to_user_id(data_received.get('user_id'), data_received.get('target_user_id'), data_received.get('message'))
                    s.sendto(json.dumps(send_result).encode(), addr)
                elif action == 'get':
                    get_result = database.get_message_for_user_id(data_received.get('user_id'))
                    if 'value' in get_result:
                        get_result['value'] = get_result.get('value').get_dict()
                    print(get_result)
                    s.sendto(json.dumps(get_result).encode(), addr)
                elif action == 'get_user_list':
                    get_users_result = database.get_user_list()
                    s.sendto(json.dumps(get_users_result).encode(), addr)
            except:
                print("Tossing invalid {} message from: {}".format(msg, addr)) 
                raise

