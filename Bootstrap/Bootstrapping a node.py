#We do not calculate the start up of the clients - we do not feel this is important and does not effect the results in any way
#Assume all network traffic etc ues the Unix timeouts 

"""

Node query the DNS server ()

"""


#The default request timeout is 30s 
#Assuming time is in seconds

import simpy
import math
import random

#import random #Causing module error
from random import random, randint
from math import *

## Import other files to be used
from calculations import *


#Variables
#RANDOM_SEED = 42
CheckIpDns = 3 #Number of DNS servers used during the bootstrap process
DnsServerUpProb = 0.8 #(80% likelyhood the DNS server will be up)
client_connections = 8 # Default in bitcoin client
query_connection_timeout = 50 # Specify connection timeout in milliseconds (default: 5000) (To query nodes to get a node list / see if they are online)
live_node_list = [] #Array list of all live nodes 
network_size = 3000 #(Max) number of nodes on the network
network_ip_node_size = 100000 #Number of IP addresses / nodes that have been seen on the network in the past 2 weeks (USE REAL DATA)
bootstrap_node_list = [] #Array list containing node id's recieved when a get_Addr message is sent to a node during the bootstrap process 
number_of__blockchain_blocks = 100 # Number of confirmed blocks in the blockchain
total_number_of_blocks = 100 #Number of confirmed blocks in the blockchain

def DnsUpProbability():
    print ('In DnsUpProbability')
    up = (0 if random() > 0.8 else 1)
    return up

def BlockProbability():
    prob = (0 if random() > 0.7 else 1)
    return prob

#Generates and sends back a list of nodes seen on the network recently (could contain malicious nodes) - repsonse to a getAddr message TODO : use real data
def network_node_ip_response(bootstrap_node_list):
	node_list_size = 30 #change to be random
	i = 0
	while (i < node_list_size):
		bootstrap_node_list.append(randint(0, network_ip_node_size))
		i = i + 1
	return bootstrap_node_list

def get_Addr_response_time():
	response_time = randint(0,50)
	return response_time

def node_live_probability():
	live_dead = (0 if random() > 0.7 else 1)
	return live_dead

#Use standard / normal distribution to accuratly calculate this using the values collected from the real network - TODO
def DnsLatency():
	print ('In DnsLatency')
	return (10)

def number_of_nodes_sent_backup():
	print ('')
	return (100)	

def server_timeout():
	print ('Timeout / Server down')
	return (30)	

#Use standard / normal distribution to accuratly calculate this using the values collected from the real network - TODO
def node_list_recieved():
	print ('node lists')
	return (20)

def write_to_text(data):
    with open("data.txt", "a") as myfile:
        myfile.write(str(data))
        myfile.write("\n")
        myfile.close()
    return 1

class Bootstrap(object):

    def __init__(self, env):
        self.env = env
        self.action = env.process(self.run())

    def run(self):
    	print('Running Routable Ip Address check')
    	yield self.env.process(RoutableIpAdd(env, self))
    	no_live_connections = simpy.Store(env, capacity=8) # Follows the bitcoin protocol here - only a max of 8 live connections
    	prod = env.process(connections(env, no_live_connections, self))
    	clients = [env.process(client(i, env, no_live_connections, self)) for i in range(8)]


    # #Use standard / normal distribution to accuratly calculate this using the values collected from the real network
    # def DnsServerResponse(self):
    # 	yield self.env.timeout(10)
		

def RoutableIpAdd(env, self):
	for i in range (CheckIpDns):
	    print('CheckIpDns servers left to query %d' % (int(CheckIpDns) - int(i)))
	    DnsUp = DnsUpProbability()

	    if DnsUp == 1:
	        #Server is up - figure out how long the server took to repsond
	        	# print ('1')
	       	Latency = DnsLatency()
	       	yield env.timeout(Latency)
	       	print(env.now) 
	       	
	       	# Server responded with X number of nodes
	       	network_node_ip_response(bootstrap_node_list)

	       	# print (bootstrap_node_list)
	       	# print len(bootstrap_node_list)
	    else:
	      	print ("DNS server down !")
	      	yield env.timeout(server_timeout())


"""
####################################################################
So far in this section of code we are not looking at the clients 
recieved by the nodes in repsonse from the getAddr message
####################################################################
"""

def connections(env, store, self):
    #crawl_all_network = 5323
    while True:
        if len(live_node_list) == 1000: break # Currently not working
        # if len(bootstrap_node_list) == 0: break # Currently not working

        for i in range(len(bootstrap_node_list)):
            if len(live_node_list) == 1000: break # Currently not working

            live_dead = node_live_probability()
            
            # IF NOT ONLINE
            if live_dead == 0:
                yield env.timeout(50)
                write_to_text(('Node not online / responding'))
                # print ('Node not online / responding')
                yield store.put('response %s' % i)

                #Makes sure list not empty
                if bootstrap_node_list:
                    # print ('Removing a node from the list')
                    #Remove the node from the list of peers to test
                    (bootstrap_node_list.pop(0))

            else:
                #ONLINE / REPSONDING
                response_time = get_Addr_response_time()
                yield env.timeout(response_time)
                yield store.put('response %s' % i)

                #print ('LENGTH OF live_node_list %s' % len(live_node_list))
                #Makes sure list not empty
                if bootstrap_node_list:
                    # print ('Removing a node from the list')
                    #Remove the node from the list of peers to test
                    live_node_list.append(bootstrap_node_list.pop(0))
                    network_node_ip_response(bootstrap_node_list) 

        		
def client(name, env, store, self):
    while True:
        yield env.timeout(1) # Time to process a request / search from the list etc
        print(name, 'sending a getaddr request at', env.now)
        write_to_text((name, 'sending a getaddr request at', env.now))
        item = yield store.get()
        print(name, 'got', item, 'at', env.now)
        write_to_text((name, 'got', item, 'at', env.now))


####################################################################
####################################################################


"""
####################################################################
This section attempts to download the blockchain
####################################################################
"""

# def connections(env, store, self):
    # while True:
    #         if len(blockchain) == 1000: break # Currently not working

                
def client_bc(name, env, store, self):
    while True:
        yield env.timeout(1) # Time to process a request / search from the list etc
        print(name, 'sending a request for a block at', env.now)
        item = yield store.get()
        print(name, 'got', item, 'at', env.now)


####################################################################
####################################################################


# Setup and start the simulation
print('Starting bootstrap simulator')

env = simpy.Environment()
bootstrap = Bootstrap(env)

env.run()
print ("\n\n\n")
print ('Total simulation time : %d' %  env.now   + ' seconds')
print ('Total simulation time : %d' %  (((env.now)/60)/60)   + ' hours \n\n\n')

write_to_text( ('Total simulation time : %d' %  env.now   + ' seconds'))
# print len(bootstrap_node_list)
# print live_node_list
# print len(live_node_list)


