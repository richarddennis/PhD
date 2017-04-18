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

Prob_DNS_UP = 0.8  # Likelyhood the DNS server will be up
node_live_probability = 0.5 #Likelyhood the node will be up

bootstrap_node_list_recieved = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
average_getAdrr_no_node_response = 100 #Number or nodes typically sent when a node requests a getAddr message
network_ip_node_size = 5000 # Number of IP addresses / nodes that have been seen on the network in the past 2 weeks

min_node_to_complete_boot_strap = 1000 # Lowest number of nodes needed before the bootstrap proccess is considered completed

####    Storage Variables    ####
bootstrap_node_list_recieved = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
bootstrap_node_list_recieved_no_dups = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc

min_nodes_recieved_before_dns_boot_quit = 500 # Lowest number of NON duplicate nodes to be recieved untill the DNS bootstrap proccess can finish

# #Number of nodes recieved from a getAddr request (Not a constant - using live data (85% of nodes returned between 100 - 120 nodes))
# def number_of_nodes_recieved():

flag = False


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

def number_of_duplicates_in_list():
    global flag

    number_recieved = len(bootstrap_node_list_recieved)
    bootstrap_node_list_recieved_before = len(bootstrap_node_list_recieved_no_dups)

    " this method works in O(n^2) time and is thus very slow on large lists"
    for i in bootstrap_node_list_recieved:
        if i not in bootstrap_node_list_recieved_no_dups:
            bootstrap_node_list_recieved_no_dups.append(i)
    assert len(bootstrap_node_list_recieved_no_dups) >= bootstrap_node_list_recieved_before
    if  len(bootstrap_node_list_recieved_no_dups) >= min_node_to_complete_boot_strap  and flag is False:
        print "\n\n\n"
        print "recieved required nodes"
        print "\n\n\n"
        flag = True


def DnsUpProbability():
    #print ('In DnsUpProbability')
    up = (0 if rand.random() > Prob_DNS_UP else 1)
    # print up
    return up


def node_live_probability():
    #print ('In node_live_probability')
    up = (0 if rand.random() > Prob_DNS_UP else 1)
    # print up
    return up
