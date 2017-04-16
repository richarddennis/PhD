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
    What if X nodes is not recieved ? - Query more DNS nodes etc - could do some modifications here

    Add in correct data into the Variables
    Start logging this data
    Comparision ?

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
query_connection_timeout = 5000 # Timeout when checking a node is alive (milliseconds)

min_node_respsonse_time_getAddr = 100 #100 milliseconds, quickest repsonse time seen during collection of data
max_node_respsonse_time_getAddr = (query_connection_timeout)- 1 #Max amount of time before timeout

Number_DNS_Seeds = 20    # No. of DNS seed nodes  ##REMEMBER COUNT STARTS FROM 0 !! SO 2 IS REALLY 3
client_connections = 8 # Max number of connections to live clients

query_connection_timeout = 500 # Timeout when checking a node is alive (milliseconds)
DNS_server_timeout = 300 # 30 seconds
dns_average_response = 10000 # Average respsonse from a DNS query (Use real network data here)
average_getAdrr_no_node_response = 100 #Number or nodes typically sent when a node requests a getAddr message

min_node_respsonse_time_getAddr = 100 #100 milliseconds, quickest repsonse time seen during collection of data
max_node_respsonse_time_getAddr = (query_connection_timeout)- 1 #Max amount of time before timeout


def get_Addr_response_time():
    "non linear distribution where values close to min are more frequent"
    response_time = int(min_node_respsonse_time_getAddr + (max_node_respsonse_time_getAddr - min_node_respsonse_time_getAddr) * pow(rand.random(), 2)) # Set min and max in variables
    return response_time

#Calls logic from Calculations.py
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


    "probability the DNS server is online"
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
            getAddr_logic() # Function which contains all the logic for the GetAddr
            # print('connection number %s opens a connection at %.2f.' % (name, env.now))
            yield env.process(cw.get_Addr(name))
            print('%s completes and terminates at %.2f.' % (name, env.now))


def setup(env, client_connections):
    """Create the intial connections, then keep creating a connection every x
    millisecond (Connection not live but spooled ready to be used *Does not
    effect the timing etc) """

    # Create the DNS bootsrap
    bootsrap_dns = Bootstrap_DNS(env, client_connections)

##If the number of servers is less than the number of simulationous connections, only create that many connections and do not spool anymore
#Else create the max simulationous connections and create a connection every x milliseconds untill number of connections == number of servers

    if Number_DNS_Seeds <= int(client_connections):
        print "Les seeds than needed connections"
        for i in range(Number_DNS_Seeds):
            env.process(connection_request(env, '%d' % i, bootsrap_dns))
    else:
        for i in range(client_connections):
            env.process(connection_request(env, '%d' % i, bootsrap_dns))
        while i < Number_DNS_Seeds:
            yield env.timeout(min_node_respsonse_time_getAddr)
            i += 1
            print "Creating / readying a new connection", i
            env.process(connection_request(env, '%d' % i, bootsrap_dns))




    #
    # # Create x initial connections to DNS servers
    # for i in range(client_connections):
    #     if i > Number_DNS_Seeds:
    #         break
    #     else:
    #         env.process(connection_request(env, '%d' % i, bootsrap_dns))
#
# #After every min timeout it will get ready another connection to be used, unless the number of connections is more than the DNS seeds as in which case this will not be needed
# #Need to replace the while true loop to stop the simulation running
#     while True:
#         yield env.timeout(min_node_respsonse_time_getAddr)
#         i += 1
#         if i < Number_DNS_Seeds:
#         # print "Creating / readying a new connection", i
#             env.process(connection_request(env, '%d' % i, bootsrap_dns))


# Setup and start the simulation
print('Starting bootstrap DNS simulator')
print ("\n\n\n")
print "Variables used in this expirement"
print ("\n")
print "query_connection_timeout" , query_connection_timeout
print "min_node_respsonse_time_getAddr", min_node_respsonse_time_getAddr
print "max_node_respsonse_time_getAddr", max_node_respsonse_time_getAddr
print "Number_DNS_Seeds (Starts at 0)", Number_DNS_Seeds
print "client_connections", client_connections
print "query_connection_timeout", query_connection_timeout
print "DNS_server_timeout", DNS_server_timeout
print "dns_average_response",dns_average_response
print "average_getAdrr_no_node_response", average_getAdrr_no_node_response
print "min_node_respsonse_time_getAddr", min_node_respsonse_time_getAddr
print "max_node_respsonse_time_getAddr", max_node_respsonse_time_getAddr
print ("\n\n")

# Create an environment and start the setup process
env = simpy.Environment()
env.process(setup(env, client_connections))

# Execute!
env.run()
print ("\n\n\n")
print ('Total simulation time : %d' %  env.now   + ' milliseconds')
# env.run(until=SIM_TIME) #Run untill simulation end time - NEED TO CHANGE THIS / REMOVE as simulation end depends on the network
