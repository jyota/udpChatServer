import socket
import json
import yaml
from simpledb import SimpleDb

if __name__ == '__main__':
    with open('config.yaml', 'r') as fp:
        options = yaml.load(fp)

    host = options.get('server').get('host') 
    port = options.get('server').get('port') 
    database = SimpleDb(options.get('server').get('user_message_cache_size', 10))

    register_test = database.register_user('test_udp_user', '127.0.0.1')
    assert register_test.get('status') == 'ok'
    assert register_test.get('value') == 0
    register_test2 = database.register_user('test_udp_user2', '127.0.0.9')
    assert register_test2.get('status') == 'ok'
    assert register_test2.get('value') == 1
    user_id_test = database.get_user_id_from_username('test_udp_user')
    assert user_id_test.get('value') == 0
    user_list_test = database.get_user_list()
    assert 'test_udp_user' in user_list_test and 'test_udp_user2' in user_list_test
    msg_assign_test = database.assign_message_to_user_id(0, 'This is a fantastic UDP chat and I will keep using it daily.')
    assert msg_assign_test.get('status_msg') == 'assigned'
    msg_retrieve_test = database.get_message_for_user_id(0)
    assert msg_retrieve_test.get('status') == 'ok' and msg_retrieve_test.get('value') == 'This is a fantastic UDP chat and I will keep using it daily.'
    print("All OK.")

