"""

#############################################################################################################################################
BITCOIN REQUIRES YOU TO DOWNLOAD THE WHOLE BLOCKCHAIN **BEFORE** PARTICIPATING IN THE NETWORK ! (Do not include *light* clients in this)
############################################################################################################################################
Current 4 days + to download the blockchain !

a block every 0.75 seconds atm (does not take into account multiple connections)
(With 8 connections, a block is recieved on average every 6 seconds (this includes CPU / RAM time) - QUAD CORE CPU + SSD - RAM usage is high)

How to download the blockchain ? - next stage
          Do we start downloading the blockchain at the query node stage, or wait for x nodes, or from zero ?


          what will we need to log / Variables
          How block size effects ! <---- VERY IMPORTANT
          Latency <--- How to demo this
          Low / High resource users / nodes <-- how to comapre / demo this
          How to deal with fake blocks ?
          Duplicate block recieved
          How many blocks from a single node do you recieve

          DO you only get block from a node once or can you repeat and use the same node more than once ? - how to sim?


Blockchain -
  Connect to x nodes (Code if they are online / offline - depends on how they are done depends on percentage of up nodes - I.E if using the up node list from the boostrap process we can assume a higher percentage of up nodes than starting from scratch)
  Depend on the resources of the node download a block (Low reource users would have a higher delay proccessing the request, I.E slower search / internet - How much slower TBD)
  How to check the block is valid ? - Radonmly generate a number for x to z and if not in here it is not valid? - Easy to model (Do not worry about encryption here yet)

Conect to node - download x blocks - if valid save them else discard them - repeat untill block number = blockchain size

What expirements can we do ?
            How the number of blocks per node sent back impacts ? (this wouldnt be linear as a lot of the timing is network based)
            Percentage of malicious blocks recieved, how this impacts on time
            Percentage of duplicate blocks recieved
                Are malicious / duplicate blocks kinda the same thing ? - same method for both ?
            Blocksize (How to measure (take results from network start to now and use this to predict delay etc?))
            Repeating node connections ?  - how it effects results if you connect to x node rather than the whole network etc, which is quicker?

# Difference between a new node joining and an old node etc <--- important to code

#Client now has to use CPU /HDD power to check the blocks are valid --- GOOD TEST FOR LOW RESOURCE USERS (What delay here ?)


#############
BITCOIN REQUIRES YOU TO DOWNLOAD THE WHOLE BLOCKCHAIN **BEFORE** PARTICIPATING IN THE NETWORK ! (Do not include *light* clients in this)


## Attack to show - currently every user is not a client too - if a node has a limited number of connections, could be prevented from being online - how much resources needed to do this attack ? etc (single pc with 10,000 connections for example could take out 1/4 of the network )


## Compare methods for downloading the blockchain - I.E. Random download of data like currentl or in order etc

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


text_file = open("blockchain_download_simulation.txt", "a+")

connection_id_number = 0

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
    text_file.write("\nmin_repsonse_time_per_block_request " + str(min_repsonse_time_per_block_request))
    text_file.write("\nmax_repsonse_time_per_block_request " + str(max_repsonse_time_per_block_request))
    text_file.write("\nclient_connections " + str(client_connections))
    text_file.write("\npercentage_low_resource_client " + str(percentage_low_resource_client))
    text_file.write("\npercentage_high_resource_client " + str(percentage_high_resource_client))
    text_file.write("\nprobability_of_malicious_block " + str(probability_of_malicious_block))
    text_file.write("\nprobability_of_duplicate_block " + str(probability_of_duplicate_block))
    text_file.write("\nProb_DNS_UP " +  str(Prob_DNS_UP))

    #Not sure if required in this section yet - remove if not needed later on
    text_file.write("\nNode_live_probability " + str(node_live_probability))
    text_file.write("\nnetwork_ip_node_size " + str(network_ip_node_size))

def block_download_logic(env, name):
    block_download(env, text_file, name)


class Blockchain_blocks_download(object):
    """Number of parallel connections , client_connections - LIMITED !
    """
    def __init__(self, env, client_connections):
        self.env = env
        self.machine = simpy.Resource(env, client_connections)

    def get_block(self,name):
        """ Repsonse time is claculated from the get_Addr_response_time method"""
        # print "get_block"
        node = Probability_of_low_resource_nodes()

        #TODO Log this
        if node == 1:
            print "high resource node"
            # node_timing = node_timing_fast(average_block_response_computational_time_high_resource, min_block_response_computational_time, max_block_response_computational_time)
            # timing = node_timing[0]
            # # timing = node_timing(average_block_response_computational_time_high_resource, min_block_response_computational_time, max_block_response_computational_time)
            # "Adds the time recieved from the method to the simulation time"
            # text_file.write("\n%s block was recieved from a HIGH resource node with timing  %.2f." % (name, timing))
            # print "high resource node timing - ", timing
            # yield self.env.timeout(timing)
            yield self.env.timeout(average_block_response_computational_time_high_resource)

        else:
            print "low resource node"
            # timing = node_timing(average_block_response_computational_time_low_resource, min_block_response_computational_time, max_block_response_computational_time)
            "Adds the time recieved from the method to the simulation time"
            # text_file.write("\n%s block was recieved from a LOW resource node with timing  %.2f." % (name, timing))
            # print "low resource node timing - ", timing
            yield self.env.timeout(average_block_response_computational_time_low_resource)


    def dns_node_offline(self, DNS):
        "Timeout if the node is offine"
        yield self.env.timeout(query_connection_timeout)

def connection_download_block_request(env, name, cw):
    #NodeUp = NodeUpPobability()# 1 is up, 0 is down

    NodeUp = 1

    #Implmented but not used currently as assume all nodes are up (Based on the node list from bootstrap for example)
    if NodeUp == 0: #Node offline
        with cw.machine.request() as request:
            text_file.write("\nNode %s DOWN " % (name))
            yield request
            print('%s is started at %.2f.' % (name, env.now))
            text_file.write("\n%s is started at %.2f." % (name, env.now))
            before = env.now
            yield env.process(cw.dns_node_offline(name))
            after = env.now
            assert (after - before) == query_connection_timeout
            text_file.write("\n%s is DOWN and completes and terminates at %.2f." % (name, env.now))
            print('%s is DOWN and completes and terminates at %.2f.' % (name, env.now))
    else:
        with cw.machine.request() as request:
            text_file.write("\nNode %s UP " % (name))

            yield request
            print('%s requested blocks at %.2f.' % (name, env.now))
            text_file.write("\n%s requested blocks at %.2f." % (name, env.now))
            before = env.now

            # i = 0
            # if i > recieved_blocks_per_query:
            #     block_download_logic(env,name) # If each node downloads
            #     i = i + 1
            block_download_logic(env, name)
            yield env.process(cw.get_block(name))
            after = env.now
            text_file.write("\n%s completed block request (may or maynot be succesfful) and terminates at %.2f." % (name, env.now))
            print('%s completed block request (may or maynot be succesfful) and terminates at %.2f.' % (name, env.now))

def setup(env, client_connections):
    """Create the intial connections, then keep creating a connection every x
    millisecond (Connection not live but spooled ready to be used *Does not
    effect the timing etc) """

    global connection_id_number
    # Create the DNS bootsrap
    blockchain_blocks_download = Blockchain_blocks_download(env, client_connections)

    # Create X inital connections (Assuming all connections will be used to start with - doesn't effect simulation time etc if not used)
    # Each connection has an unique id - once used its never used again
    for connection_id_number in range(client_connections):
        text_file.write("\n\nCreating the initial connections ready to be used")
        print "Creating / readying a initial connection", connection_id_number
        text_file.write("\nCreating / readying a initial connection" + str(connection_id_number))
        env.process(connection_download_block_request(env, '%d' % connection_id_number, blockchain_blocks_download))
        connection_id_number = connection_id_number + 1


        ########## CHANGE TO WHILE
    #Doesn't really matter what method is used to generate / ready new connections so long as there is always a supply and they are ready to go
    while len(block_list_downloaded_valid) != total_number_of_blocks:
        env.process(connection_download_block_request(env, '%d' % connection_id_number, blockchain_blocks_download))
        yield env.timeout(min_repsonse_time_per_block_request)
        connection_id_number = connection_id_number + 1

    else:
        print "All blocks have been downloaded - no need for any more connections to nodes"
        text_file.write('\nAll blocks have been downloaded - no need for any more connections to nodes - finished at %.2f.' % (env.now))


def blockchain_download_simulation():

    # Setup and start the simulation
    now = time.strftime("%c")

    assert percentage_low_resource_client + percentage_high_resource_client == 1

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


    print ("\n")

    print('Total simulation time : %d' %  env.now   + ' milliseconds')
    print('Total simulation time : %d' %  (env.now/milliseconds)   + ' seconds')

    text_file.write('\n\n\nTotal simulation time : %d' %  env.now   + ' milliseconds')
    text_file.write('\n\n\nTotal simulation time : %d' %  (env.now/milliseconds)   + ' seconds')
