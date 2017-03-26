import simpy
import math
import random

#import random #Causing module error
from random import random, randint
from math import *

def DnsUpProbability():
    print ('In DnsUpProbability')
    up = (0 if random() > 0.8 else 1)
    return up

#Generates and sends back a list of nodes seen on the network recently (could contain malicious nodes) - repsonse to a getAddr message TODO : use real data
def network_node_ip_response():
	node_list = []
	node_list_size = 30 #change to be random

	while len(node_list) < node_list_size:
		node_list.append(randint(0, network_ip_node_size))
	
	return node_list

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