"""
THis simulation measures how long it would take to test all the nodes recieved
during the bootstrapping proccess if they are online or not

**NOT currently taking into account more GetAddr recieved when querying these nodes

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
from Bootstrap_DNS_Servers import *

"1 SECOND IS 1000 MILLISECONDS"

### TODO - WHAT VARIABLES DO I NEED TO COLLECT?

"""
Take the list of recived nodes and connect to each one to see if they are online
If they are - add a random value to the simulation time
Else add a timeout to the simulation time
Do this untill every node is queried OR a fix value is reached?

Will need to store a list of live nodes and dead nodes
"""

####    Storage Variables    ####
live_node_list = [] #Array list of all live nodes
dead_node_list = []  #Array list of all dead nodes
