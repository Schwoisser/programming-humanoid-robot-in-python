'''In this file you need to implement remote procedure call (RPC) server

* There are different RPC libraries for python, such as xmlrpclib, json-rpc. You are free to choose.
* The following functions have to be implemented and exported:
 * get_angle
 * set_angle
 * get_posture
 * execute_keyframes
 * get_transform
 * set_transform
* You can test RPC server with ipython before implementing agent_client.py
'''



from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple

# add PYTHONPATH
import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'kinematics'))

from inverse_kinematics import InverseKinematicsAgent
from jsonrpc import JSONRPCResponseManager, dispatcher

class ServerAgent(InverseKinematicsAgent):
    '''ServerAgent provides RPC service
    '''
    # YOUR CODE HERE
    # def __init__(self):
    #     p

    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        return self.joints[joint_name]


    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        self.target_joints[joint_name] = angle
        # YOUR CODE HERE

    def get_posture(self):
        '''return current posture of robot'''
        return self.recognize_posture()
        # YOUR CODE HERE

    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        self.forward_kinematics(keyframes)
        # YOUR CODE HERE

    def get_transform(self, name):
        '''get transform with given name
        '''
        return self.from_trans(name)

    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        self.set_transforms(effector_name, transform)
        # YOUR CODE HERE

    def echo(self,string):
        return string

@Request.application
def application(request):
    # Dispatcher is dictionary {<method_name>: callable}
    serverAgent = ServerAgent()
    dispatcher["get_angle"] = serverAgent.get_angle
    dispatcher["set_angle"] = serverAgent.set_angle
    dispatcher["get_posture"] = serverAgent.get_posture
    dispatcher["execute_keyframes"] = serverAgent.execute_keyframes
    dispatcher["get_transform"] = serverAgent.get_transform
    dispatcher["set_transform"] = serverAgent.set_transform
    dispatcher["echo"] = serverAgent.echo

    response = JSONRPCResponseManager.handle(
        request.data, dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('localhost', 4000, application)
