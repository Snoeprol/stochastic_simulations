"""
Queue time calculator
Mehmet Arkin & Mario van Rooij

Scenario:
  Users with different usage times
  have to be processed by a server with
  random usage times

inspired by: https://simpy.readthedocs.io/en/latest/examples/bank_renege.html
"""
import random
import simpy
import numpy as np
from sys import argv
from tqdm import tqdm

SPECIAL_DIST = False
PRIORITY = False
CONSTANT = False

NEW_CUSTOMERS = 50000  # Total number of customers
N = 1
avg_time = 1

# Irrelevant
MIN_PATIENCE = 1E5  # Min. customer patience
MAX_PATIENCE = 1E5  # Max. customer patience

def source(env, number, interval, server):
    """Source generates customers randomly"""
    for i in range(number):
        t = random.expovariate(1.0 / interval)
        c = customer(env, 'Customer%02d %02d' % (i, t), server)
        env.process(c)
        
        yield env.timeout(t)

times = []
customers = []
def customer(env, name, server):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    
    # Choose distribution to sample from
    if SPECIAL_DIST:
            z = np.random.rand()
            if z > 0.75:
                processing_time = random.expovariate(1.0 / (5 * avg_time))
            else:
                processing_time = random.expovariate(1.0 / avg_time)
    elif CONSTANT:
        processing_time = avg_time
        print(processing_time)
    else:
        processing_time = random.expovariate(1.0 / avg_time)
        times.append(processing_time)

    if PRIORITY:
        with server.request(priority= processing_time, preempt= True) as req:
            patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
            
            results = yield req | env.timeout(patience)
            
            wait = env.now - arrive
            
            if req in results:
                # Arrived at server
                waiting_times.append(wait)
                leave = env.now + processing_time
                
                yield env.timeout(processing_time)


            else:
                # Make sure no reneges
                print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))        
    else:

        with server.request() as req:
            patience = random.uniform(MIN_PATIENCE, MAX_PATIENCE)
            # Wait for the server or abort at the end of our tether
            results = yield req | env.timeout(patience)

            wait = env.now - arrive

            if req in results:
                # Now being processed by server
                waiting_times.append(wait)
                yield env.timeout(processing_time)


            else:
                # Make sure no reneges
                print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))

INTERVALS_CUSTOMERS = np.linspace(0.5,3,10)
for rho in INTERVALS_CUSTOMERS:
    INTERVAL_CUSTOMERS = rho
    file_times = open('workloadvariance' + str(rho) + '.csv', 'w')
    simulations = 100
    for _ in tqdm(range(simulations)):
        waiting_times = []
        # Setup and start the simulation
        random.seed(np.random.rand())
        env = simpy.Environment()

        # Start processes and run
        if PRIORITY:
            server = simpy.PriorityResource(env, capacity=N)
        else:
            server = simpy.Resource(env, capacity=N)
        
        env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, server))
        env.run()
        file_times.write(str(np.mean(waiting_times)) + "\n")
        print(np.mean(times))

    file_times.close()
