
import simpy
import sys, traceback

x = 15

def car(env):
      while True:
         print env.now
         if env.now >= x:
             print "test"
             print env.now
             sys.exit()
         print('Start parking at %d' % env.now)
         parking_duration = 5
         yield env.timeout(parking_duration)
         if env.now >= x:
             print "test"
             print env.now
             print "SImulation end time", env.now
             sys.exit()
         print('Start driving at %d' % env.now)
         trip_duration = 2
         yield env.timeout(trip_duration)


env = simpy.Environment()
env.process(car(env))
env.run()
