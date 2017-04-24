
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

total_number_of_blocks = 463351 # As of 24 April 2017
average_block_size = 0.948 # MB  - Again as of the 24 April 2017

query_connection_timeout = (30 * milliseconds ) # Timeout when checking a node is alive (milliseconds)

number_of_blocks_per_query = 2 #Get 2 blocks per request (CHANGE FOR EXPIREMENTS)

mini_repsonse_time_per_block_request = 500  # Milliseconds - Fastest response time recorded on the live network
max_repsonse_time_per_block_request = (query_connection_timeout)- 1 #Max amount of time before timeout

client_connections = 8 # Max number of connections to live clients

#Percentage of "low resource clients" to "high resource clients" #TODO - ENSURE ASSERT condition to make these values = 1
percentage_low_resource_client = 0.2
percentage_high_resource_client = 0.8

probability_of_malicious_block = 0.2 # Probability of recieving a malicious block - HOW TO IMPLEMENT?
probability_of_duplicate_block = 0.2 # Probability of recieving a duplicate block - HOW TO IMPLEMENT?

text_file = open("blockchain_download_simulation.txt", "a+")

node_id_number = 0

#Var
def text_file_writing_variables(text_file, env):
    text_file.write("\n\n\n##############################################################")
    text_file.write("\n\nSimulation started at " + time.strftime("%c"))
    text_file.write("\nSimulation start time " + str(env.now))
    text_file.write("\nVariables used in this expirement\n")
    text_file.write("\ntotal_number_of_blocks " + str(total_number_of_blocks))
    text_file.write("\naverage_block_size (MB)" + str(average_block_size))
    text_file.write("\nquery_connection_timeout " + str(query_connection_timeout))
    text_file.write("\nnumber_of_blocks_per_query " + str(number_of_blocks_per_query))
    text_file.write("\nmin_node_respsonse_time_getAddr " + str(min_node_respsonse_time_getAddr))
    text_file.write("\nmax_node_respsonse_time_getAddr " + str(max_node_respsonse_time_getAddr))
    text_file.write("\nclient_connections " + str(client_connections))
    text_file.write("\npercentage_low_resource_client " + str(percentage_low_resource_client))
    text_file.write("\npercentage_high_resource_client " + str(percentage_high_resource_client))
    text_file.write("\nprobability_of_malicious_block " + str(probability_of_malicious_block))
    text_file.write("\nprobability_of_duplicate_block " + str(probability_of_duplicate_block))
    text_file.write("\nProb_DNS_UP " +  str(Prob_DNS_UP))

    #Not sure if required in this section yet - remove if not needed later on
    text_file.write("\nNode_live_probability " + str(node_live_probability))
    text_file.write("\nnetwork_ip_node_size " + str(network_ip_node_size))


class Blockchain_blocks_download(object):
    """Number of parallel connections , client_connections - LIMITED !
    """
    def __init__(self, env, client_connections):
        self.env = env
        self.machine = simpy.Resource(env, client_connections)
        # self.rand_delay = rand_delay

def connection_download_block_request(env, name, cw):
    NodeUp = NodeUpPobability()# 1 is up, 0 is down


def setup(env, client_connections):
    """Create the intial connections, then keep creating a connection every x
    millisecond (Connection not live but spooled ready to be used *Does not
    effect the timing etc) """

    global node_id_number
    # Create the DNS bootsrap
    blockchain_blocks_download = Blockchain_blocks_download(env, client_connections)

    # Create X inital connections (Assuming all connections will be used to start with - doesn't effect simulation time etc if not used)
    # Each connection has an unique id - once used its never used again
    for node_id_number in range(client_connections):
        text_file.write("\n\nCreating the initial connections ready to be used")
        print "Creating / readying a initial connection", node_id_number
        text_file.write("\nCreating / readying a initial connection" + str(node_id_number))
        env.process(connection_download_block_request(env, '%d' % node_id_number, blockchain_blocks_download))
        node_id_number = node_id_number + 1

    #Doesn't really matter what method is used to generate / ready new connections so long as there is always a supply and they are ready to go
    #while len(block_list_downloaded_valid) != total_number_of_blocks:

def blockchain_download_simulation():
    # Setup and start the simulation
    now = time.strftime("%c")

    #TODO - Creation of the simulator ? Any nodes etc that need to be spooled up first ?

    print('Starting the simulator to test the download of the blockchain')
    print ("\n")

    # # # Create an environment and start the setup process
    env = simpy.Environment()
    env.process(setup(env, client_connections))
    #
    text_file_writing_variables(text_file, env)
    # Execute!
    env.run()
