"""

Stop when X nodes are recieved ? - or wait untill all nodes have been attempted to be queried
What if X nodes is not recieved ? - Query more DNS nodes etc - could do some modifications here

"""
"""

*When is the boostrappng proccess really done ? - need to define this
                            - after a set peroid of time
                            - After x nodes has been recieved
                            - After x node queried
        Technincally only a single node online needs to be contactable for this system to work

Code read for expirements to run (Do them now or as more code is done?)

Expirements to do

    Standard Bitcoin model 3 DNS servers
        Variables to change
            Probability of DNS servers being up (simulate a DDOS attack against the DNS (Work out the cost of such an attack))
            Number of DNS servers ? (Don't go crazy, but varry this from 1 - x?)
            Number of nodes recieved back (average) (Could vary this a lot so sometimes get 10 others get 500 etc) - Resource impact (Bandwidth etc)
            Number of connections (Max) - no good until DNS server > 8 (Resource impact again)
            Malicious DNS ? - how to sim this? (Number of duplicate / fake nodes?)

    Our model - No set DNS servers
        Try to code the pool idea ! - how to simulate this ? TODO
        Variables to change
            Number of DNS servers
            Connections at one time
            Probability they are up
            Nodes recieved
            malicious nodes - how they can effect it
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

"1 SECOND IS 1000 MILLISECONDS"
# RANDOM_SEED = 42
milliseconds = 1000

query_connection_timeout = (30 * milliseconds ) # Timeout when checking a node is alive (milliseconds)

min_node_respsonse_time_getAddr = 500 #500 milliseconds, quickest repsonse time seen during collection of data
max_node_respsonse_time_getAddr = (query_connection_timeout)- 1 #Max amount of time before timeout

Number_DNS_Seeds = 30    # No. of DNS seed nodes  ##REMEMBER COUNT STARTS FROM 0 !! SO 2 IS REALLY 3
client_connections = 8 # Max number of connections to live clients

DNS_server_timeout = (30 * milliseconds ) # 30 seconds
average_getAdrr_no_node_response = 100 #Number or nodes typically sent when a node requests a getAddr message

text_file = open("DNS_Bootstrap_Results.txt", "a+")

#Var
def text_file_writing_variables(text_file, env):
    text_file.write("\n\n\n##############################################################")
    text_file.write("\n\nSimulation started at " + time.strftime("%c"))
    text_file.write("\nSimulation start time " + str(env.now))
    text_file.write("\nVariables used in this expirement\n")
    text_file.write("\nquery_connection_timeout " + str(query_connection_timeout))
    text_file.write("\nmin_node_respsonse_time_getAddr " + str(min_node_respsonse_time_getAddr))
    text_file.write("\nmax_node_respsonse_time_getAddr " + str(max_node_respsonse_time_getAddr))
    text_file.write("\nNumber_DNS_Seeds (Starts at 0) "+ str(Number_DNS_Seeds))
    text_file.write("\nclient_connections " + str( client_connections))
    text_file.write("\nDNS_server_timeout " + str(DNS_server_timeout))
    text_file.write("\naverage_getAdrr_no_node_response " + str(average_getAdrr_no_node_response))



def get_Addr_response_time():
    "non linear distribution where values close to min are more frequent"
    response_time = int(min_node_respsonse_time_getAddr + (max_node_respsonse_time_getAddr - min_node_respsonse_time_getAddr) * pow(rand.random(), 2)) # Set min and max in variables
    assert response_time >= min_node_respsonse_time_getAddr
    return response_time

#Calls logic from Calculations.py
def getAddr_logic():
    # Server responded with X number of nodes
    bootstrap_node_getAddr(text_file)
    number_of_duplicates_in_list(text_file)


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
        text_file.write("\nDNS node offline")
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
    text_file.write("\n%s is started at %.2f." % (name, env.now))
    ## 1 online, 0 offline
    if DnsUp == 0:
        with cw.machine.request() as request:
            print 'DNS DOWN %s' % (name)
            text_file.write("\nDNS DOWN %s" % (name))
            yield request
            before = env.now
            # print('%s is DOWN and starts the proccess at %.2f.' % (name, env.now))
            yield env.process(cw.dns_node_timeout(name))
            after = env.now
            assert (after - before) == DNS_server_timeout  # Make sure the DNS time out has been accurately added
            text_file.write("\n%s is DOWN and completes and terminates at %.2f." % (name, env.now))
            print('%s is DOWN and completes and terminates at %.2f.' % (name, env.now))
    else:
        with cw.machine.request() as request:

            yield request
            getAddr_logic() # Function which contains all the logic for the GetAddr
            # print('connection number %s opens a connection at %.2f.' % (name, env.now))
            yield env.process(cw.get_Addr(name))
            text_file.write("\n%s completes and terminates at %.2f." % (name, env.now))
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
        print "Less seeds than needed connections"
        text_file.write("\n\nLess seeds than needed connections")

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

def Bootstrap_DNS_Servers_simulation_call():
    # Setup and start the simulation
    now = time.strftime("%c")

    print('Starting bootstrap DNS simulator')
    print ("\n")

    # Create an environment and start the setup process
    env = simpy.Environment()
    env.process(setup(env, client_connections))

    text_file_writing_variables(text_file, env)

    # Execute!
    env.run()
    print ("\n")
    print('Total simulation time : %d' %  env.now   + ' milliseconds')
    print('Total simulation time : %d' %  (env.now/milliseconds)   + ' seconds')

    print ('len(bootstrap_node_list_recieved_no_dups)', len(bootstrap_node_list_recieved_no_dups))

    text_file.write('\n\nbootstrap_node_list_recieved ' + str(len(bootstrap_node_list_recieved)))
    text_file.write('\nbootstrap_node_list_recieved_no_dups ' + str(len(bootstrap_node_list_recieved_no_dups)))
    text_file.write('\n\n\nTotal simulation time : %d' %  env.now   + ' milliseconds')
    text_file.write('\n\n\nTotal simulation time : %d' %  (env.now/milliseconds)   + ' seconds')
    return env.now
