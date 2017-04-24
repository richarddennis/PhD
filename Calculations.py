##############################################################################
#### File containing the calculations / probability calucaltions for other
#### files


#### The default request timeout is 30s
#### Assuming time is in milliseconds

import simpy
import math
# from random import *
import random
import random as rand

import sys, traceback
from math import *
####    Variables   ####
milliseconds = 1000

Prob_DNS_UP = 0.8  # Likelyhood the DNS server will be up
node_live_probability = 0.7 #Likelyhood the node will be up

bootstrap_node_list_recieved = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
average_getAdrr_no_node_response = 100 #Number or nodes typically sent when a node requests a getAddr message
network_ip_node_size = 5000 # Number of IP addresses / nodes that have been seen on the network in the past 2 weeks

min_node_to_complete_boot_strap = 1000 # Lowest number of nodes needed before the bootstrap proccess is considered completed

####    Storage Variables    ####
bootstrap_node_list_recieved = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
bootstrap_node_list_recieved_no_dups = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc

total_node_list = [] #List of every node that has been recieved on the network

live_node_list = [] #Array list of all live nodes
dead_node_list = []  #Array list of all dead nodes

min_nodes_recieved_before_dns_boot_quit = 500 # Lowest number of NON duplicate nodes to be recieved untill the DNS bootstrap proccess can finish

flag = False
complete_flag = False

#Move into calculations.py when ready
#Number of nodes recieved (Bootstrap)
def bootstrap_node_getAddr(text_file):
    #Random generation of nodes (number represents a single node), from 1 to x for an average amount of nodes
    for i in range (average_getAdrr_no_node_response):
        bootstrap_node_list_recieved.append(rand.randrange(1,network_ip_node_size,1))
    print "bootstrap_node_list_recieved", len(bootstrap_node_list_recieved)
    text_file.write("\nbootstrap_node_list_recieved " + str(len(bootstrap_node_list_recieved)))

"""Removes all the duplicates contained from the recieved list, so the recieved
list is empty, the main list contains unique identities and it stores how many
duplicates were there, this is run every getAddr message"""

def number_of_duplicates_in_list(text_file):
    global flag

    number_recieved = len(bootstrap_node_list_recieved)
    bootstrap_node_list_recieved_before = len(bootstrap_node_list_recieved_no_dups)

    " this method works in O(n^2) time and is thus very slow on large lists"
    for i in bootstrap_node_list_recieved:
        if i not in bootstrap_node_list_recieved_no_dups:
            bootstrap_node_list_recieved_no_dups.append(i)
    assert len(bootstrap_node_list_recieved_no_dups) >= bootstrap_node_list_recieved_before
    if  len(bootstrap_node_list_recieved_no_dups) >= min_node_to_complete_boot_strap  and flag is False:
        text_file.write("\n\n\n")
        text_file.write("recieved required nodes")
        text_file.write("\n\n\n")

        print "\n\n\n"
        print "recieved required nodes"
        print "\n\n\n"
        flag = True


def node_offline(env, text_file):
    global complete_flag

    #Remove the first node in the list of recieved nodes,
    # print "len(bootstrap_node_list_recieved_no_dups) offline", len(bootstrap_node_list_recieved_no_dups)
    if len(bootstrap_node_list_recieved_no_dups) != 0:
        dead_node = bootstrap_node_list_recieved_no_dups.pop(0)
        # print dead_node
        dead_node_list.append(dead_node)
        #Once all the nodes have been discovered, log this into the file - While on the real network we would still collect data, there aint much point, and becuase of this we do not alter the times once the whole netwok has been found
    elif complete_flag == False:
        print "\n\nAll nodes on the network have been discovered - but not queried yet"
        print "Took %s nodes queried to discover the whole network" %(name)
        text_file.write("\n\nAll nodes on the network have been discovered - but not queried yet\n\n")
        text_file.write("Took %s nodes queried to discover the whole network" %(name))
        print "\n\n\n"
        complete_flag = True

        print ("\n")
        print('Total simulation time : %d' %  env.now   + ' milliseconds')
        print('Total simulation time : %d' %  (env.now/milliseconds)   + ' seconds')
        print('Total simulation time : %d' %  ((env.now/milliseconds)/60)   + ' minutes')

        text_file.write('\n\n\nTotal simulation time : %d' %  env.now   + ' milliseconds')
        text_file.write('\n\n\nTotal simulation time : %d' %  (env.now/milliseconds)   + ' seconds')
        text_file.write('\n\n\nTotal simulation time : %d' %  ((env.now/milliseconds)/60)   + ' minutes')
        sys.exit()
    "What to log ? - if anything ? do we care what nodes are down ?"

"""
This section deals with the handling of the getAddr logic
Deals with if there are any more nodes to get - No point downloading more nodes if the whole node list is already found / stored to be queried
if list is not found, donwload more nodes
make sure the nodes where are generated are not added to the "be queried list" if they have already been queried
"""
def node_online(env, text_file,name):
    global complete_flag
    # print "len(bootstrap_node_list_recieved_no_dups)", len(bootstrap_node_list_recieved_no_dups)

    if len(bootstrap_node_list_recieved_no_dups) != 0:
        live_node_list.append(bootstrap_node_list_recieved_no_dups.pop(0))

        #If all the nodes have eithere been queried or are in the list to be queried there is no point search for more
        if (len(bootstrap_node_list_recieved_no_dups)+ len(live_node_list) + len(dead_node_list)) <= network_ip_node_size:
            generation_of_getaddr_reply_nodes(text_file)
        #Once all the nodes have been discovered, log this into the file - While on the real network we would still collect data, there aint much point, and becuase of this we do not alter the times once the whole netwok has been found
        elif complete_flag == False:
            print "\n\nAll nodes on the network have been discovered - but not queried yet"
            print "Took %s nodes queried to discover the whole network" %(name)
            text_file.write("\n\nAll nodes on the network have been discovered - but not queried yet\n\n")
            text_file.write("Took %s nodes queried to discover the whole network" %(name))
            print "\n\n\n"
            complete_flag = True
            # sys.exit()
    else:
        print "All nodes queried"
        text_file.write("\n\nAll nodes queried\n\n")

        print("\n\nTotal number of live nodes : " + str(len(live_node_list)))
        print("\n\nTotal number of dead nodes : " + str(len(dead_node_list)))

        text_file.write("\n\nAll nodes queried\n\n")
        text_file.write("\n\nTotal number of live nodes : " + str(len(live_node_list)))
        text_file.write("\n\nTotal number of dead nodes : " + str(len(dead_node_list)))

        print ("\n")
        print('Total simulation time : %d' %  env.now   + ' milliseconds')
        print('Total simulation time : %d' %  (env.now/milliseconds)   + ' seconds')
        print('Total simulation time : %d' %  ((env.now/milliseconds)/60)   + ' minutes')

        text_file.write('\n\n\nTotal simulation time : %d' %  env.now   + ' milliseconds')
        text_file.write('\n\n\nTotal simulation time : %d' %  (env.now/milliseconds)   + ' seconds')
        text_file.write('\n\n\nTotal simulation time : %d' %  ((env.now/milliseconds)/60)   + ' minutes')

        sys.exit()


def generation_of_getaddr_reply_nodes(text_file):
    global bootstrap_node_list_recieved
    # print "Called generation_of_getaddr_reply_nodes(text_file)"
    #Generate a bunch of random (BUT VALID / SEEN) node addresses (assuming each indivual number is a unique node)
    for i in range (average_getAdrr_no_node_response):
        bootstrap_node_list_recieved.append(rand.randrange(1,network_ip_node_size,1))

    "--------------------------------------------------------"
    #TODO - LOG THE NUMBER OF DUPLICATES / SEEN BEFORE NODES
    "--------------------------------------------------------"
    #
    #Remove duplicates
    for i in bootstrap_node_list_recieved:
        if i not in bootstrap_node_list_recieved_no_dups:
            bootstrap_node_list_recieved_no_dups.append(i)

    bootstrap_node_list_recieved = []

    #Goes through the whole recieved list of nodes, and compares these to any nodes that have already been queried and if they are found to be live removes them from the list
    for i in bootstrap_node_list_recieved_no_dups:
        if i in live_node_list:
            bootstrap_node_list_recieved_no_dups.remove(i)
            # print "duplicate live node -- removing"
            text_file.write("\nduplicate live node -- removing")

    for i in bootstrap_node_list_recieved_no_dups:
        if i in dead_node_list:
            bootstrap_node_list_recieved_no_dups.remove(i)
            text_file.write("\nduplicate dead node -- removing")
            # print "duplicate dead node -- removing"


def node_crawler_finish(text_file):
    print node_crawler_finish
    #TODO - Call this every time a query is done to make sure the network has been full queried


"""
Generate a random array with x values (This is to simulate the DNS setup procedure - allows expirments such as what if only 10 nodes was recieved during DNS etc)
Need to ensure no duplicates in the list

Only run at setup of the simulation (getAddr test)
"""
def generation_of_nodes(start_node_list_amount):
    while len(bootstrap_node_list_recieved_no_dups) != start_node_list_amount:
        bootstrap_node_list_recieved = rand.sample(range(1, network_ip_node_size), start_node_list_amount)

        #Remove duplicates
        for i in bootstrap_node_list_recieved:
            if i not in bootstrap_node_list_recieved_no_dups:
                bootstrap_node_list_recieved_no_dups.append(i)

    #Make sure the correct number of nodes are generated
    assert start_node_list_amount == len(bootstrap_node_list_recieved_no_dups)

def NodeUpPobability():
    #print ('In DnsUpProbability')
    r_number =rand.uniform(0, 1)
    # print r_number
    #Was playing up so re arranged the code - not the cleanest but works
    if r_number >= node_live_probability:
        up = 0
    else:
        up = 1

    return up


def DnsUpProbability():
    #print ('In DnsUpProbability')
    up = (0 if rand.random() > Prob_DNS_UP else 1)
    # print up
    return up
