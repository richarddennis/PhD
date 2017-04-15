
import simpy
import math
# from random import *
import random
import random as rand

import sys, traceback
from math import *

from Calculations import *

####    Variables   ####
Number_DNS_Seeds = 3    # No. of DNS seed nodes
client_connections = 8 # Max number of connections to live clients
network_size = 3000 # Number of live nodes on the network
query_connection_timeout = 5000 # Timeout when checking a node is alive (milliseconds)
DNS_server_timeout = 3000 # 30 seconds
network_ip_node_size = 5000 # Number of IP addresses / nodes that have been seen on the network in the past 2 weeks
blockchain_size = 100 # Number of confirmed blocks in the blockchain
dns_average_response = 10000 # Average respsonse from a DNS query (Use real network data here)
live_node_list_number_bootstrap = 10 # Number of nodes a node must connect to and verify is online before downloading the blockchain
average_getAdrr_no_node_response = 100 #Number or nodes typically sent when a node requests a getAddr message

min_node_respsonse_time_getAddr = 100 #100 milliseconds, quickest repsonse time seen during collection of data
max_node_respsonse_time_getAddr = (query_connection_timeout)- 1 #Max amount of time before timeout

min_block_respsonse_time_getAddr = 500 #500 milliseconds, quickest repsonse time seen during collection of data
max_block_respsonse_time_getAddr = (query_connection_timeout)- 1 #Max amount of time before timeout

####    Storage Variables    ####
live_node_list = [] #Array list of all live nodes
dead_node_list = []  #Array list of all dead nodes
bootstrap_node_list_recieved = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
bootstrap_node_list_recieved_no_dups = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
node_list_recieved_getAddr = [] # List of nodes recieved from a getAddr message (Not during the DNS stage), should always be empty before its called (Logic of getAddr_from_standard_nodes())
blocks_recieved = [] # List of all the blocks recieved (Duplicates, malicious all included here)

#Move into calculations.py when ready
#Number of nodes recieved (Bootstrap)
def bootstrap_node_getAddr():
    #### TODO ####
    #Random generation of nodes (number represents a single node), from 1 to x for an average amount of nodes
    for i in range (average_getAdrr_no_node_response):
        bootstrap_node_list_recieved.append(rand.randrange(1,network_ip_node_size,1))



def number_of_duplicates_in_list():
    # print 'len bootstrap_node_list_recieved BEFORE removing duplicates', len(bootstrap_node_list_recieved)
    print 'bootstrap_node_list_recieved BEFORE removing duplicates', bootstrap_node_list_recieved
    number_recieved = len(bootstrap_node_list_recieved)
    i = dict.fromkeys(bootstrap_node_list_recieved).keys()
    #Removes all the values from i to the bootstrap_node_list_recieved_no_dups variable
    x = 0
    while x < len(i):
        bootstrap_node_list_recieved_no_dups.append(i.pop(0))
        x = x + 1
    print 'len bootstrap_node_list_recieved AFTER removing duplicates', len(bootstrap_node_list_recieved_no_dups)
    # print 'bootstrap_node_list_recieved AFTER removing duplicates', bootstrap_node_list_recieved_no_dups
    print (number_recieved - len(bootstrap_node_list_recieved_no_dups)), 'duplicate nodes recieved during bootstrapping (Can be multiples of the same node)' # TODO Log this data?


#### TODO logic for getAddr from other nodes
def getAddr_from_standard_nodes():
    storage = []
    storage2 = []
    storage3 = []
    # print 'getAddr_from_standard_nodes'
    # print 'bootstrap_node_list_recieved before doing any logic (NOT DNS STAGE)' , bootstrap_node_list_recieved

    #Generate a bunch of random (BUT VALID / SEEN) node addresses (assuming each indivual number is a unique node)
    for i in range (average_getAdrr_no_node_response):
        node_list_recieved_getAddr.append(rand.randrange(1,network_ip_node_size,1))

    ## Now have a list full of nodes, need to compare them to the live / dead list and put them into the bootstrap_node_list_recieved_no_dups list
    # Remove all nodes which appear in live_node_list, dead_node_list and bootstrap_node_list_recieved_no_dups
    # Add nodes left to bootstrap_node_list_recieved_no_dups

    print 'node_list_recieved_getAddr len ', len(node_list_recieved_getAddr)
    #TODO do this in one function
    #Compares 3 lists and only if they are not currently in the list are they saved and used later on in this function
    storage = [item for item in node_list_recieved_getAddr if item not in live_node_list]
    storage2 = [item for item in storage if item not in dead_node_list]
    storage3 = [item for item in storage2 if item not in bootstrap_node_list_recieved_no_dups]

    # TODO
    ##Can use this for timing how long to find the whole network etc
    if len(storage3) == 0 :
        print 'No new nodes discovered from getAddr !!!'

    ##TODO Add logging of how many duplicate nodes was seen etc

    len_before_merge = len(bootstrap_node_list_recieved_no_dups) + len(storage3)

    #Removes from list of recieved nodes to a list for bootstrap_node_list_recieved_no_dups nodes
    while len(storage3) != 0:
        bootstrap_node_list_recieved_no_dups.append((storage3.pop(0)))

    assert len(storage3) == 0
    assert len(bootstrap_node_list_recieved_no_dups) == len_before_merge # Make sure all values been added correctly

    del node_list_recieved_getAddr[:] #Empty the recieved node list (Not needed but make things more efficent)
    assert len(node_list_recieved_getAddr) == 0 #Make sure the array containing the nodes recieved is empty (should be in other arrays)



#Use this to calculate a repsonse time (Average ? - Live network data use here)
def get_Addr_response_time():
    # print 'in get_Addr_response_time'
    # non linear distribution where values close to min are more frequent
    response_time = int(min_node_respsonse_time_getAddr + (max_node_respsonse_time_getAddr - min_node_respsonse_time_getAddr) * pow(random(), 2)) # Set min and max in variables
    print 'response_time is ', response_time , ' milliseconds'
    return response_time


##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
# Simulates the bootstrapping of the network - Querying DNS servers, getting a list of live nodes, then downloading the blockchain
##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################
class blockchain_dl(object):

    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):

    	yield self.env.process(query_dns_servers(env, self))
        number_of_duplicates_in_list()
    	no_live_connections = simpy.Store(env, capacity=client_connections) ## Number of live simulationous connections
        prod = env.process(blockchain_download(env, no_live_connections, self))


### TODO - add in logging this data into a file of some sort
def query_dns_servers(env, self):
    start_time = env.now
    i = 0
    for i in range (Number_DNS_Seeds):
        # while start_time < 6000:
	    print('CheckIpDns servers left to query %d' % (int(Number_DNS_Seeds) - int(i)))
        #probability the DNS server is online
	    DnsUp = DnsUpProbability()
    	    if DnsUp == 1: #DNS server alive
    	        	# print ('1')
                yield self.env.timeout(dns_average_response) # Appends the dns server reponse (Avg) to the simulation time
    	       	print 'Current system time is',(env.now)

    	       	# Server responded with X number of nodes
                bootstrap_node_getAddr()

    	       	#print (bootstrap_node_list_recieved)
                i = i + 1

    	    else:
    	      	print ("DNS server down !")
    	      	yield env.timeout(DNS_server_timeout)
                i = i + 1

def blockchain_download(env, store, self):
    print 'in blockchain_download'

    print ('Attempting to download the bc at :', env.now)
    #TODO - Logic (Take the blockchain length, randomly select a value from 1 to x (each valye represent a block), TODO add malicious blocks, add to simulation time how long it would take to download the block thus the whole blockchain)


    # Create a random number from 1 - no of blocks
    # Assume all are valid (for now)
    # Random time (Based on real results) as to how long to download the block
    # (Store into the array of downloaded blocks) - Sort out duplicates here
    # Repeat untill number of blocks in the array = total blocks in the b/c

    #Random generation of nodes (number represents a single node), from 1 to x for an average amount of nodes
    block_number = rand.randrange(1,blockchain_size,1)

    print 'block recieved no', block_number
    #
    # # Prevents duplication
    if block_number not in blocks_recieved:
        blocks_recieved.append(block_number)
    #

    print 'blocks_recieved', blocks_recieved
    # block_response_time = get_block_response_time()
    yield env.timeout(100)
    #
    #
    # if len(blocks_recieved) == blockchain_size:
    #     sys.exit()
    #



    # print 'Number of live nodes', len(live_node_list)
    # sys.exit()


#
# z = 0
# for z in range(100)
# Setup and start the simulation
print('Starting blockchain download simulator')
# print(random, type(random))
# print(random.__file__)
# help(random)

env = simpy.Environment()
blockchain_dl = blockchain_dl(env)

env.run()
print ("\n\n\n")
print ('Total simulation time : %d' %  env.now   + ' milliseconds')
