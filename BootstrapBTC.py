#### Bootstrap simulator to simulate the bootstrapping of nodes onto the BTC
#### network - done following the bitcoin protocol and documentation
####
#### BTC chosen for the base bootstrap model due to all blockchain based
#### networks currently using this bootstrap model
####

#### Variables - (Will add more when they are thought of)
####    Blockchain Size
####    Block size ? (Not sure yet if needed?)
####    Number of nodes on the networks
####    Number of DNS seeds
####    Percentage of malicious nodes
####    Network age
####    Average block Size
####    Average number of IP addresses recieved from getAddr
####    Number / Percentage of non repsonding / dead nodes
####    Bandwidth
####    Number of new nodes joining (1, 100 etc)
####    If node is new or previously been on the networks
####    Number of nodes to be compromised to sybil attack bootstrap
####    Amount of resources each node has (RAM, Bandwidth etc)

#### Will store all data into a folder, and then each run will generate a new
#### file (txt or tsv?) containing the measurements
#### Measurements - (Will add more when they are thought of)
####    Time taken (Download blockchain, find nodes etc)
####    Resources used
####    Log everything !

#### The default request timeout is 30s
#### Assuming time is in milliseconds

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


####    Storage Variables    ####
live_node_list = [] #Array list of all live nodes
dead_node_list = []  #Array list of all dead nodes
bootstrap_node_list_recieved = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
bootstrap_node_list_recieved_no_dups = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
node_list_recieved_getAddr = [] # List of nodes recieved from a getAddr message (Not during the DNS stage), should always be empty before its called (Logic of getAddr_from_standard_nodes())

#Move into calculations.py when ready
#Number of nodes recieved (Bootstrap)
def bootstrap_node_getAddr():
    #### TODO ####
    #Random generation of nodes (number represents a single node), from 1 to x for an average amount of nodes
    # node_list=[random.randrange(1,network_ip_node_size,1) for _ in range (average_getAdrr_no_node_response)]
    for i in range (average_getAdrr_no_node_response):
        bootstrap_node_list_recieved.append(rand.randrange(1,network_ip_node_size,1))
    # print 'bootstrap_node_getAddr: ', bootstrap_node_list_recieved
    # return bootstrap_node_list_recieved


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




def blockchain_download():
    print 'in blockchain_download'
    #TODO - Logic (Take the blockchain length, randomly select a value from 1 to x (each valye represent a block), TODO add malicious blocks, add to simulation time how long it would take to download the block thus the whole blockchain)
    # Seperate this into multiple functions ( How many simulationous downloads etc (duplicate blocks etc))


######
# Simulates the bootstrapping of the network - Querying DNS servers, getting a list of live nodes, then downloading the blockchain
######
class Bootstrap(object):

    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):

    	yield self.env.process(query_dns_servers(env, self))
        number_of_duplicates_in_list()
        print 'bootstrap_node_list_recieved_no_dups',bootstrap_node_list_recieved_no_dups
    	no_live_connections = simpy.Store(env, capacity=client_connections) ## Number of live simulationous connections
        prod = env.process(connecting_to_nodes(env, no_live_connections, self))

def blockchain_download_start(env, self):
    print 'blockchain_download_start'
    no_live_connections_bc = simpy.Store(env, capacity=client_connections) ## Number of live simulationous connections
    bc_dl = env.process(blockchain_download(env, no_live_connections_bc, self))

### TODO - add in logging this data into a file of some sort
def query_dns_servers(env, self):
    start_time = env.now
    i = 0
    for i in range (Number_DNS_Seeds):
        # while start_time < 6000:
	    print('CheckIpDns servers left to query %d' % (int(Number_DNS_Seeds) - int(i)))

        #probability the DNS server is online
	    DnsUp = DnsUpProbability()

#### If DNS server is alive, add repsonse time for a getAddr request to the sim time,
#### store a number of addresses recieved from the getAddr message, move onto the next DNS server
#### When to stop ? - when x nodes are recieved or at a set time ? (60 seconds bootstrap time on BTC) ***Do this on the call not on the function?

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


#### Here the bootstrap process will attempt to connect to x many nodes using x simulationous connections untill x live nodes are in the database
def connecting_to_nodes(env, store, self):
    print ('Connecting to nodes at simulation time :', env.now)
    # print bootstrap_node_list_recieved_no_dups
    print 'Number of nodes in list', len(bootstrap_node_list_recieved_no_dups)
    print 'System time is ', env.now

    # assert len(bootstrap_node_list_recieved_no_dups) > 0 #Make sures there nodes in the list else fails (Mostly for testing purposes)
    # sys.exit()

    while len(bootstrap_node_list_recieved_no_dups) > 0:
        if len(live_node_list) == live_node_list_number_bootstrap:
            blockchain_download_start(env,self)
            # break
        print ('Number of live nodes connected to', len(live_node_list))
        print ('Number of nodes still to query', len(bootstrap_node_list_recieved_no_dups))

        live_dead = node_live_probability()
        print ('Node is 1 up, 0 down :',live_dead)
        # IF NOT ONLINE
        if live_dead == 0:
            yield env.timeout(query_connection_timeout) # How long to wait untill assume the server is offline
            # write_to_text(('Node not online / responding'))
            print ('Node not online / responding')

            #Removes from list of recieved nodes to a list for dead nodes
            dead_node_list.append((bootstrap_node_list_recieved_no_dups.pop(0)))

        else:
                #ONLINE / REPSONDING
                print ('Node online')
                response_time = get_Addr_response_time()
                yield env.timeout(response_time)

                #Removes from list of recieved nodes to a list for LIVE nodes
                live_node_list.append((bootstrap_node_list_recieved_no_dups.pop(0)))

                getAddr_from_standard_nodes()

                #TODO - add a way on generating more nodes recieved from the getAddr


# #### Here the bootstrap process will attempt to connect to x many nodes using x simulationous connections and download the blockchain
def blockchain_download(env, store, self):
    print ('Attempting to download the bc at :', env.now)
    # print 'Number of live nodes', len(live_node_list)
    sys.exit()


####################################################################
####################################################################
#
# z = 0
# for z in range(100)
# Setup and start the simulation
print('Starting bootstrap simulator')
# print(random, type(random))
# print(random.__file__)
# help(random)

env = simpy.Environment()
bootstrap = Bootstrap(env)

env.run()
print ("\n\n\n")
print 'Dead node list', dead_node_list
print ('Total simulation time : %d' %  env.now   + ' milliseconds')
