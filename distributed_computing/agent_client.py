'''In this file you need to implement remote procedure call (RPC) client

* The agent_server.py has to be implemented first (at least one function is implemented and exported)
* Please implement functions in ClientAgent first, which should request remote call directly
* The PostHandler can be implement in the last step, it provides non-blocking functions, e.g. agent.post.execute_keyframes
 * Hints: [threading](https://docs.python.org/2/library/threading.html) may be needed for monitoring if the task is done
'''

import weakref
import requests
import json
import threading





class PostHandler(object):
    '''the post hander wraps function to be excuted in paralle
    '''
    def __init__(self, obj):
        self.proxy = weakref.proxy(obj)

    def execute_keyframes(self, keyframes):
        '''non-blocking call of ClientAgent.execute_keyframes'''
        t = threading.Thread(target=self.proxy.execute_keyframes(keyframes)
        t.daemon = True
        t.start()

    def set_transform(self, effector_name, transform):
        '''non-blocking call of ClientAgent.set_transform'''
        t = threading.Thread(target=self.proxy.set_transform(effector_name, transform))
        t.daemon = True
        t.start()



class ClientAgent(object):
    '''ClientAgent request RPC service from remote server
    '''
    # YOUR CODE HERE
    def __init__(self):
        self.post = PostHandler(self)
        self.url = "http://localhost:4000/jsonrpc"
        self.headers = {'content-type': 'application/json'}

    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        payload ={
                    "method": "get_angle",
                    "params": [joint_name],
                    "jsonrpc": "2.0",
                    "id": 0,
        }
        return requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()


    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        payload ={
                    "method": "set_angle",
                    "params": [joint_name, angle],
                    "jsonrpc": "2.0",
                    "id": 0,
        }
        return requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()


    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        payload ={
                    "method": "get_angle",
                    "params": [],
                    "jsonrpc": "2.0",
                    "id": 0,
        }
        return requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()


    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        payload ={
                    "method": "execute_keyframes",
                    "params": [keyframes],
                    "jsonrpc": "2.0",
                    "id": 0,
        }



    def get_transform(self, name):
        '''get transform with given name
        '''
        payload ={
                    "method": "get_transform",
                    "params": [name],
                    "jsonrpc": "2.0",
                    "id": 0,
        }
        return requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()



    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        payload ={
                    "method": "set_transform",
                    "params": [effector_name, transform],
                    "jsonrpc": "2.0",
                    "id": 0,
        }
        response = requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()



    def echo(self,string):
        payload = {
                    "method": "echo",
                    "params": [string],
                    "jsonrpc": "2.0",
                    "id": 0,
        }
        response = requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()
        print(response)

if __name__ == '__main__':
    agent = ClientAgent()
    agent.echo("Test")
    # TEST CODE HERE
