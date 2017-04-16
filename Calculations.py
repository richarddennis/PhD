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


####    Storage Variables    ####
bootstrap_node_list_recieved = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
bootstrap_node_list_recieved_no_dups = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc


#Move into calculations.py when ready
#Number of nodes recieved (Bootstrap)
def bootstrap_node_getAddr():
    #Random generation of nodes (number represents a single node), from 1 to x for an average amount of nodes
    for i in range (average_getAdrr_no_node_response):
        bootstrap_node_list_recieved.append(rand.randrange(1,network_ip_node_size,1))
    print "bootstrap_node_list_recieved", len(bootstrap_node_list_recieved)

"""Removes all the duplicates contained from the recieved list, so the recieved
list is empty, the main list contains unique identities and it stores how many
duplicates were there, this is run every getAddr message"""

def number_of_duplicates_in_list():
    number_recieved = len(bootstrap_node_list_recieved)
    bootstrap_node_list_recieved_before = len(bootstrap_node_list_recieved_no_dups)

    " this method works in O(n^2) time and is thus very slow on large lists"
    for i in bootstrap_node_list_recieved:
        if i not in bootstrap_node_list_recieved_no_dups:
            bootstrap_node_list_recieved_no_dups.append(i)
    assert len(bootstrap_node_list_recieved_no_dups) >= bootstrap_node_list_recieved_before



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
