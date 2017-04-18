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
from Bootstrap_DNS_Servers import *

"1 SECOND IS 1000 MILLISECONDS"

### TODO - WHAT VARIABLES DO I NEED TO COLLECT?


####    Storage Variables    ####
live_node_list = [] #Array list of all live nodes
dead_node_list = []  #Array list of all dead nodes


"""
Start at new simulation time or carry on ? - could do either set up would be the same

"""



def Bootstrap_node_online_test_simulation(sim_time_start):
    # Setup and start the simulation
    now = time.strftime("%c")


    print('Starting the simulator to test if nodes are online')
    print ("\n")

    # Create an environment and start the setup process
    env = simpy.Environment()

    # env.process(setup(env, client_connections))
    #
    #     text_file_writing_variables(text_file, env)
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
