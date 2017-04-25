"""
THis simulation measures how long it would take to test all the nodes recieved
during the bootstrapping proccess if they are online or not

**NOT currently taking into account more GetAddr recieved when querying these nodes

"""



"""
Expirements :

Time taken to query the entire network for all live nodes
Time take to find x live nodes
Average online / offline nodes
Impact more / less DNS nodes has on the bootstrap time
Percentage of duplicate nodes recieved
Number of simulationous connections effect it
Low resource users


TODO ------ How malicious nodes could attack this process
                How to code it basically
                    How to determine malicious nodes
            How to do turnover of nodes?

How many nodes are needed to contact before the whole network is discovered
Does network diversity matter? - can we simulate this some how (timings etc)


How is our model different from Bitcoin
Smaller messages = lower time ? - test this assumption

What is the point of this bit ? - do we do anything different
    Might come in handy to show how mobile nodes would effect this due to network churn?


TO code
#Do this code in calculations ?
Connect to nodes -
    if node is alive:
        add timing (random but weighted like crawled network)
        move to live node list
        Generate a new bunch of new nodes (Nuumber of nodes - variable)
        See how many of these nodes have been seen before (LOG THIS)
        Stop querying when live node list == network size
            Anything else ? - How to deal with malicious nodes etc?
    If node is dead / not repsonding:
        Add timeout to simulation timeout
        move node to
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

query_connection_timeout = (30 * milliseconds ) # Timeout when checking a node is alive (milliseconds)

min_node_respsonse_time_getAddr = 500 #500 milliseconds, quickest repsonse time seen during collection of data
max_node_respsonse_time_getAddr = (query_connection_timeout)- 1 #Max amount of time before timeout

client_connections = 8 # Max number of connections to live clients

DNS_server_timeout = (30 * milliseconds ) # 30 seconds
average_getAdrr_no_node_response = 100 #Number or nodes typically sent when a node requests a getAddr message

node_id_number = 0

"""
Start at new simulation time or carry on ? - could do either set up would be the same

"""
text_file = open("Bootstrap_getAddr_test_of_online.txt", "a+")

def get_Addr_response_time():
    "non linear distribution where values close to min are more frequent"
    response_time = int(min_node_respsonse_time_getAddr + (max_node_respsonse_time_getAddr - min_node_respsonse_time_getAddr) * pow(rand.random(), 2)) # Set min and max in variables
    assert response_time >= min_node_respsonse_time_getAddr
    return response_time


def offline_node_logic(env):
    #Deal with a server being offline - take a random id (doesn't matter which atm ?) - remove recieved list and store it into the dead node list
    node_offline(env, text_file)


def online_node_logic(env, name):
    node_online(env, text_file, name)

#Var
def text_file_writing_variables(text_file, env):
    text_file.write("\n\n\n##############################################################")
    text_file.write("\n\nSimulation started at " + time.strftime("%c"))
    text_file.write("\nSimulation start time " + str(env.now))
    text_file.write("\nVariables used in this expirement\n")
    text_file.write("\nquery_connection_timeout " + str(query_connection_timeout))
    text_file.write("\nmin_node_respsonse_time_getAddr " + str(min_node_respsonse_time_getAddr))
    text_file.write("\nmax_node_respsonse_time_getAddr " + str(max_node_respsonse_time_getAddr))
    text_file.write("\nclient_connections " + str( client_connections))
    text_file.write("\naverage_getAdrr_no_node_response " + str(average_getAdrr_no_node_response))
    text_file.write("\nNumber of nodes to start with (Node list from DNS setup) " + str(start_node_list_amount_recieved))
    text_file.write("\nProb_DNS_UP " +  str(Prob_DNS_UP))
    text_file.write("\nNode_live_probability " + str(node_live_probability))
    text_file.write("\nnetwork_ip_node_size " + str(network_ip_node_size))


class Bootstrap_getAddr(object):
    """Number of parallel connections , client_connections - LIMITED !
    """
    def __init__(self, env, client_connections):
        self.env = env
        self.machine = simpy.Resource(env, client_connections)
        # self.rand_delay = rand_delay

    #TODO - Add more logic here - move from list into live node list etc, do more than just get the timeout (OR Do we do that in a seperate function ?)
    def get_addr(self,DNS):
        """ Repsonse time is claculated from the get_Addr_response_time method"""
        response = get_Addr_response_time()
        "Adds the time recieved from the method to the simulation time"
        yield self.env.timeout(response)

    def dns_node_offline(self, DNS):
        "Timeout if the node is offine"
        yield self.env.timeout(DNS_server_timeout)


def connection_getaddr_node_request(env, name, cw):
    """
    First test if the ndoe is online or offline - could use different probability to DNS nodes (As per crawler results)

    """

    NodeUp = NodeUpPobability()# 1 is up, 0 is down

    if NodeUp == 0: #Node offline
        with cw.machine.request() as request:
            # print "node DOWN"
            text_file.write("\nNode %s DOWN " % (name))

            yield request
            print('%s is started at %.2f.' % (name, env.now))
            text_file.write("\n%s is started at %.2f." % (name, env.now))
            before = env.now
            # print "Node %s sent the request at %.2f" % (name, env.now)
            offline_node_logic(env)
            yield env.process(cw.dns_node_offline(name))
            after = env.now
            # print "Node %s recieved the request at %.2f" % (name, env.now)
            assert (after - before) == query_connection_timeout
            text_file.write("\n%s is DOWN and completes and terminates at %.2f." % (name, env.now))
            print('%s is DOWN and completes and terminates at %.2f.' % (name, env.now))

    else:
        with cw.machine.request() as request:
            # print "Node UP"
            text_file.write("\nNode %s UP " % (name))

            yield request
            print('%s is started at %.2f.' % (name, env.now))
            text_file.write("\n%s is started at %.2f." % (name, env.now))
            text_file.write("\nNode up %s" % (name))
            before = env.now
            # print "Node %s sent the request at %.2f" % (name, env.now)
            online_node_logic(env,name)
            yield env.process(cw.get_addr(name))
            after = env.now
            text_file.write("\n%s is UP and completes and terminates at %.2f." % (name, env.now))
            print('%s is UP and completes and terminates at %.2f.' % (name, env.now))
            # print "Node %s recieved the request at %.2f" % (name, env.now)


def setup(env, client_connections):
    """Create the intial connections, then keep creating a connection every x
    millisecond (Connection not live but spooled ready to be used *Does not
    effect the timing etc) """
    global node_id_number
    # Create the DNS bootsrap
    bootstrap_getAddr = Bootstrap_getAddr(env, client_connections)

    """
    Create x (client_connections),
    create new connections every x millisecond (Can create as many as possible as its just getting them ready (doesn't effect simulation time))
    When/how to stop ? - do it untill every node is queired ?
    """

    # Create X inital connections (Assuming all connections will be used to start with - doesn't effect simulation time etc if not used)
    # Each connection has an unique id - once used its never used again
    for node_id_number in range(client_connections):
        text_file.write("\n\nCreating the initial connections ready to be used")
        print "Creating / readying a initial connection", node_id_number
        text_file.write("\nCreating / readying a initial connection" + str(node_id_number))
        env.process(connection_getaddr_node_request(env, '%d' % node_id_number, bootstrap_getAddr))
        node_id_number = node_id_number + 1


    # # #Assuming the node list is not empty when the simulation is started (Should never be as this step would be pointless if it was)
    while bootstrap_node_list_recieved_no_dups != []:
        # print "Creating / readying connection ", node_id_number
        # text_file.write("\nCreating / readying connection "+ str(node_id_number))
        env.process(connection_getaddr_node_request(env, '%d' % node_id_number, bootstrap_getAddr)) #What if 8 finished at the same time, this would add a delay, maybe reduce the timout by 8?
        yield env.timeout(min_node_respsonse_time_getAddr)
        node_id_number = node_id_number + 1
    else:
        print "No nodes left to query - no more connections are being created"
        text_file.write('\nNo nodes left to query - no more connections are being created at %.2f.' % (env.now))

def Bootstrap_node_online_test_simulation(start_node_list_amount):
    global start_node_list_amount_recieved
    # Setup and start the simulation
    now = time.strftime("%c")

    #Generate a bunch of nodes (Value is how many nodes (None dups) to be created)
    generation_of_nodes(start_node_list_amount)
    start_node_list_amount_recieved = start_node_list_amount
    print('Starting the simulator to test if nodes are online')
    print ("\n")

    # # Create an environment and start the setup process
    env = simpy.Environment()
    env.process(setup(env, client_connections))

    text_file_writing_variables(text_file, env)
    # Execute!
    env.run()
    
    print ("\n")
    print('Total simulation time : %d' %  env.now   + ' milliseconds')
    print('Total simulation time : %d' %  (env.now/milliseconds)   + ' seconds')

    text_file.write('\n\n\nTotal simulation time : %d' %  env.now   + ' milliseconds')
    text_file.write('\n\n\nTotal simulation time : %d' %  (env.now/milliseconds)   + ' seconds')
    return env.now
