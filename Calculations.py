##############################################################################
#### File containing the calculations / probability calucaltions for other
#### files


#### The default request timeout is 30s
#### Assuming time is in milliseconds

import simpy
import math

#import random #Causing module error
from random import random, randint

from math import *

####    Variables   ####

Prob_DNS_UP = 0.8  # Likelyhood the DNS server will be up
node_live_probability = 0.5 #Likelyhood the node will be up

bootstrap_node_list_recieved = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
average_getAdrr_no_node_response = 100 #Number or nodes typically sent when a node requests a getAddr message
network_ip_node_size = 5000 # Number of IP addresses / nodes that have been seen on the network in the past 2 weeks




def DnsUpProbability():
    #print ('In DnsUpProbability')
    up = (0 if random() > Prob_DNS_UP else 1)
    print up
    return up


def node_live_probability():
    #print ('In node_live_probability')
    up = (0 if random() > Prob_DNS_UP else 1)
    print up
    return up
