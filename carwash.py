"""
TODO

What is the DNS bootstrap proccess?
    Query x DNS servers
    See if they are online (probability based on live results)
    If alive
            #Live data use !
        Estimate the repsonse time
        Get X random node addresses
    If dead
        Add timeout time to the simulation time
    ############ COMPLETED ############

    TODO

    Stop when X nodes are recieved ? - or wait untill all nodes have been attempted to be queried

"""
import simpy
import math
# from random import *
import random
import random as rand

import sys, traceback
from math import *

from Calculations import *


# RANDOM_SEED = 42

SIM_TIME = 2000    # Simulation time in minutes

query_connection_timeout = 5000 # Timeout when checking a node is alive (milliseconds)

min_node_respsonse_time_getAddr = 100 #100 milliseconds, quickest repsonse time seen during collection of data
max_node_respsonse_time_getAddr = (query_connection_timeout)- 1 #Max amount of time before timeout


Number_DNS_Seeds = 3    # No. of DNS seed nodes
client_connections = 8 # Max number of connections to live clients

query_connection_timeout = 500 # Timeout when checking a node is alive (milliseconds)
DNS_server_timeout = 300 # 30 seconds
dns_average_response = 10000 # Average respsonse from a DNS query (Use real network data here)
average_getAdrr_no_node_response = 100 #Number or nodes typically sent when a node requests a getAddr message

min_node_respsonse_time_getAddr = 100 #100 milliseconds, quickest repsonse time seen during collection of data
max_node_respsonse_time_getAddr = (query_connection_timeout)- 1 #Max amount of time before timeout

####    Storage Variables    ####

bootstrap_node_list_recieved = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
bootstrap_node_list_recieved_no_dups = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc


def get_Addr_response_time():
    "non linear distribution where values close to min are more frequent"
    response_time = int(min_node_respsonse_time_getAddr + (max_node_respsonse_time_getAddr - min_node_respsonse_time_getAddr) * pow(rand.random(), 2)) # Set min and max in variables
    return response_time

#Move into calculations.py when ready
#Number of nodes recieved (Bootstrap)
def bootstrap_node_getAddr():
    #Random generation of nodes (number represents a single node), from 1 to x for an average amount of nodes
    for i in range (average_getAdrr_no_node_response):
        bootstrap_node_list_recieved.append(rand.randrange(1,network_ip_node_size,1))

"""Removes all the duplicates contained from the recieved list, so the recieved
list is empty, the main list contains unique identities and it stores how many
duplicates were there, this is run every getAddr message"""
def number_of_duplicates_in_list():
    # print 'len bootstrap_node_list_recieved BEFORE removing duplicates', len(bootstrap_node_list_recieved)
    # print 'bootstrap_node_list_recieved BEFORE removing duplicates', bootstrap_node_list_recieved
    number_recieved = len(bootstrap_node_list_recieved)
    bootstrap_node_list_recieved_before = len(bootstrap_node_list_recieved_no_dups)
    i = dict.fromkeys(bootstrap_node_list_recieved).keys()
    #Removes all the values from i to the bootstrap_node_list_recieved_no_dups variable
    x = 0
    while x < len(i):
        bootstrap_node_list_recieved_no_dups.append(i.pop(0))
        x = x + 1
    # print 'len bootstrap_node_list_recieved AFTER removing duplicates', len(bootstrap_node_list_recieved_no_dups)
    assert len(bootstrap_node_list_recieved_no_dups) >= bootstrap_node_list_recieved_before
    # print 'bootstrap_node_list_recieved AFTER removing duplicates', bootstrap_node_list_recieved_no_dups
    # print (number_recieved - len(bootstrap_node_list_recieved_no_dups)), 'duplicate nodes recieved during bootstrapping (Can be multiples of the same node)' # TODO Log this data?



##TODO add logic here for dealing with the recieved nodes from the getAddr
##TODO add logic to deal with duplicates nodes in the list etc
def getAddr_logic():
    # Server responded with X number of nodes
    bootstrap_node_getAddr()
    number_of_duplicates_in_list()


class Bootstrap_DNS(object):
    """Number of parallel connections , client_connections - LIMITED !
    """
    def __init__(self, env, client_connections):
        self.env = env
        self.machine = simpy.Resource(env, client_connections)
        # self.rand_delay = rand_delay

    """GetAddr proccess. It takes a ``get_addr``request, processes it and
    comes back with the simulation time used, this """
    def get_Addr(self, DNS):
        """ Repsonse time is claculated from the get_Addr_response_time method"""
        response = get_Addr_response_time()
        "Adds the time recieved from the method to the simulation time"
        yield self.env.timeout(response)

    def dns_node_timeout(self, DNS):
        "Timeout if the DNS node is offine"
        print "DNS node offline"
        yield self.env.timeout(DNS_server_timeout)

def connection_request(env, name, cw):
    """
    Each proccess arrives at the software requests a connections
    It then starts the connection to a node and requests a get_addr
    and waits for it to finish, once complete the proccess is terminated and never re started
    """
    print name
    # if int(name) > Number_DNS_Seeds: #Makes sure only the DNS nodes are quired even if there are more live connections ready
    #     print "Completed querying all DNS nodes"
    #     sys.exit()
    # else:
    #probability the DNS server is online
    DnsUp = DnsUpProbability()
    print('%s is started at %.2f.' % (name, env.now))
    ## 1 online, 0 offline
    if DnsUp == 0:
        with cw.machine.request() as request:
            print 'DNS DOWN %s' % (name)
            yield request
            before = env.now
            # print('%s is DOWN and starts the proccess at %.2f.' % (name, env.now))
            yield env.process(cw.dns_node_timeout(name))
            after = env.now
            assert (after - before) == DNS_server_timeout  # Make sure the DNS time out has been accurately added
            print('%s is DOWN and completes and terminates at %.2f.' % (name, env.now))
    else:
        with cw.machine.request() as request:
            yield request
            getAddr_logic() # FUnction which contains all the logic for the GetAddr
            # print('connection number %s opens a connection at %.2f.' % (name, env.now))
            yield env.process(cw.get_Addr(name))
            print('%s completes and terminates at %.2f.' % (name, env.now))


def setup(env, client_connections):
    """Create the intial connections, then keep creating a connection every x
    millisecond (Connection not live but spooled ready to be used *Does not
    effect the timing etc) """

    # Create the DNS bootsrap
    bootsrap_dns = Bootstrap_DNS(env, client_connections)
    # Create x initial connections to DNS servers

    #TODO Create a connection one at a time rather than all at once, will prevent 8 connections for 3 DNS servers for example -- i think
    for i in range(client_connections):
        if i > Number_DNS_Seeds:
            break
        else:
            env.process(connection_request(env, '%d' % i, bootsrap_dns))

#After every min timeout it will get ready another connection to be used, unless the number of connections is more than the DNS seeds as in which case this will not be needed
    while True:
        yield env.timeout(min_node_respsonse_time_getAddr)
        i += 1
        if i < Number_DNS_Seeds:
            # print "Creating / readying a new connection", i
            env.process(connection_request(env, '%d' % i, bootsrap_dns))


# Setup and start the simulation
# rand.seed(RANDOM_SEED)  # This helps reproducing the results

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, client_connections))

# Execute!
env.run()
# env.run(until=SIM_TIME) #Run untill simulation end time - NEED TO CHANGE THIS / REMOVE as simulation end depends on the network
