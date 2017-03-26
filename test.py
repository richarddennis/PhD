import random

bootstrap_node_list_recieved = [] #List of all nodes addresses recieved during the bootstrap peroid - Is a list so we can compare duplicatition probability etc
average_getAdrr_no_node_response = 100 #Number or nodes typically sent when a node requests a getAddr message
network_ip_node_size = 5000 # Number of IP addresses / nodes that have been seen on the network in the past 2 weeks


#Move into calculations.py when ready
#Number of nodes recieved (Bootstrap)
def bootstrap_node_getAddr():
    #### TODO ####
    #Random generation of nodes (number represents a single node), from 1 to x for an average amount of nodes
    # node_list=[random.randrange(1,network_ip_node_size,1) for _ in range (average_getAdrr_no_node_response)]
    for i in range (average_getAdrr_no_node_response):
        bootstrap_node_list_recieved.append(random.randrange(1,network_ip_node_size,1))
    print 'bootstrap_node_getAddr: ', bootstrap_node_list_recieved
    # return bootstrap_node_list_recieved

bootstrap_node_getAddr()
