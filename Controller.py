import simpy
import math
import time
# from random import *
import random
import random as rand
import os

import sys, traceback
from math import *
from Bootstrap_DNS_Servers import *
from Bootstrap_getAddr_test_of_online import *
from blockchain_download import *

#Calls the simulation of the DNS bootstrapping model
# SIM_TIME_after_DNS_Bootstrap = Bootstrap_DNS_Servers_simulation_call()

# """
# Pre populate the nodes list - Can either use data from the DNS bootstrap or new -
# this will allow us to test how the DNS proccess effects the crawling of the network etc
# """
# start_node_list_amount = 10
# Node_online_simulation = Bootstrap_node_online_test_simulation(start_node_list_amount)

blockchain_download_simulation_run = blockchain_download_simulation()
