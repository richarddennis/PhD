"""
THis simulation measures how long it would take to test all the nodes recieved
during the bootstrapping proccess if they are online or not

**NOT currently taking into account more GetAddr recieved when querying these nodes

"""

import simpy
import math
import time
# from random import *
import random
import random as rand
import os

import sys, traceback
from math import *

from Calculations import *

### TODO - WHAT VARIABLES DO I NEED TO COLLECT?

"1 SECOND IS 1000 MILLISECONDS"
# RANDOM_SEED = 42
milliseconds = 1000

query_connection_timeout = (30 * milliseconds ) # Timeout when checking a node is alive (milliseconds)

min_node_respsonse_time_getAddr = 500 #500 milliseconds, quickest repsonse time seen during collection of data
max_node_respsonse_time_getAddr = (query_connection_timeout)- 1 #Max amount of time before timeout

client_connections = 8 # Max number of connections to live clients

DNS_server_timeout = (30 * milliseconds ) # 30 seconds
average_getAdrr_no_node_response = 100 #Number or nodes typically sent when a node requests a getAddr message

####    Storage Variables    ####
live_node_list = [] #Array list of all live nodes
dead_node_list = []  #Array list of all dead nodes


"""
Start at new simulation time or carry on ? - could do either set up would be the same

"""
text_file = open("Bootstrap_getAddr_test_of_online.txt", "a+")


#Var
def text_file_writing_variables(text_file, env):
    text_file.write("\n\n\n##############################################################")
    text_file.write("\n\nSimulation started at " + time.strftime("%c"))
    text_file.write("\nSimulation start time " + str(env.now))
    text_file.write("\nVariables used in this expirement\n")
    text_file.write("\nquery_connection_timeout " + str(query_connection_timeout))
    text_file.write("\nmin_node_respsonse_time_getAddr " + str(min_node_respsonse_time_getAddr))
    text_file.write("\nmax_node_respsonse_time_getAddr " + str(max_node_respsonse_time_getAddr))
    text_file.write("\nclient_connections " + str( client_connections))
    text_file.write("\naverage_getAdrr_no_node_response " + str(average_getAdrr_no_node_response))


class Bootstrap_DNS(object):
    """Number of parallel connections , client_connections - LIMITED !
    """
    def __init__(self, env, client_connections):
        self.env = env
        self.machine = simpy.Resource(env, client_connections)
        # self.rand_delay = rand_delay






def Bootstrap_node_online_test_simulation():
    # Setup and start the simulation
    now = time.strftime("%c")


    print('Starting the simulator to test if nodes are online')
    print ("\n")

    # # Create an environment and start the setup process
    env = simpy.Environment()
    env.process(setup(env, client_connections))

    text_file_writing_variables(text_file, env)
    #
    #     # Execute!
    #     env.run()
    #     print ("\n")
    #     print('Total simulation time : %d' %  env.now   + ' milliseconds')
    #     print('Total simulation time : %d' %  (env.now/milliseconds)   + ' seconds')
    #
    #     print ('len(bootstrap_node_list_recieved_no_dups)', len(bootstrap_node_list_recieved_no_dups))
    #
    #     text_file.write('\n\nbootstrap_node_list_recieved ' + str(len(bootstrap_node_list_recieved)))
    #     text_file.write('\nbootstrap_node_list_recieved_no_dups ' + str(len(bootstrap_node_list_recieved_no_dups)))
    #     text_file.write('\n\n\nTotal simulation time : %d' %  env.now   + ' milliseconds')
    #     text_file.write('\n\n\nTotal simulation time : %d' %  (env.now/milliseconds)   + ' seconds')
    #     return env.now
