import simpy

"""
####################################################################
So far in this section of code we are not looking at the clients 
recieved by the nodes in repsonse from the getAddr message
####################################################################
"""

def connections(env, store):
    for i in range(100):
        yield env.timeout(2)
        yield store.put('response %s' % i)
#        print('Produced spam at', env.now)


def client(name, env, store):
    while True:
        yield env.timeout(1) # Time to process a request / search from the list etc
        print(name, 'sending a getaddr request at', env.now)
        item = yield store.get()
        print(name, 'got', item, 'at', env.now)


env = simpy.Environment()
no_live_connections = simpy.Store(env, capacity=8)

prod = env.process(connections(env, no_live_connections))
client = [env.process(client(i, env, no_live_connections)) for i in range(8)]

env.run()
print ('Total simulation time : %d' %  env.now   + ' seconds')

