from tqdm import tqdm
from simpy import Environment as env
from numpy.random import poisson
import simpy
import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
import pandas as pd

SHORTEST = False
SPECIAL_DISTRIBUTION = False
D = False

class Queue():

    def __init__(self, initial_customers, process_time, number_of_servers, arrival_rate, total_customers, save_statistics = False):

        self.initial_customers = initial_customers
        self.save_statistics = save_statistics
        self.number_of_servers = number_of_servers
        self.total_customers = total_customers
        self.create_servers()
        self.arrival_rate = arrival_rate
        self.generate_arrival_times(process_time)
   
        self.queue_list = []
        self.time_list = []

    def generate_arrival_times(self, process_time):
        '''Given rate of arrival and number of
        customers derives arrival times for those customers'''
        self.time = 0
        self.inter_arrival_times = []
        self.queue = []
        self.customers = []
        
        for i in range(self.total_customers):
            interval = np.random.exponential(1/self.arrival_rate)
            
            # Change id to line up with number of initial customers
            self.customers.append(Customer(i + self.initial_customers, self.time + interval, process_time))
            self.time += interval

            if self.save_statistics == True:
                self.inter_arrival_times.append(interval)
             
        if self.save_statistics == True:
            print("Average inter-arrival time: {:.2f}".format(np.mean(self.inter_arrival_times)))
            plt.hist(self.inter_arrival_times, bins = 30)
            plt.show()

        if self.save_statistics == True:
            self.arrival_times = [customer.arrival_time for customer in self.customers]
            plt.hist(self.arrival_times)
            plt.show()

    def create_servers(self):
        '''Creates servers with different processing
        times if available'''

        self.servers = []

        for i in range(self.number_of_servers):
            self.servers.append(Server(i))

    def process_customers(self):
        '''Proccesses the queue with the given initial conditions
        this is done by an event driven approach, where time is
        updated by discrete steps'''
        self.time = 0
        while not all([customer.processed for customer in self.customers]):

            # Someone in queue and machine available
            if len(self.queue) > 0 and self.servers_available():
                customer = self.select_customer()
                server = self.select_available_server(customer)
                

            else:
                # Someone in queue, but no machines
                if len(self.queue) > 0 and not self.servers_available():
                    min_free_machine_time = min([server.available_time for server in self.servers])
                    self.time = min_free_machine_time

                # Nobody in queue, jump to next arrival if it is later than machine availibility
                else:
                    min_next_customer_time = min([customer.arrival_time for customer in self.customers if customer.processed == False])
                    try:
                        min_free_machine_time = min([server.available_time for server in self.servers if server.busy == True])
                        self.time = min(min_next_customer_time, min_free_machine_time)
                    except:
                        self.time = min_next_customer_time
                    


            self.save_stats()
            self.update_queue()
            self.set_server_availability()
        
        self.time = max([server.available_time for server in self.servers])
        self.waiting_times = [customer.time_used for customer in self.customers]
    
    def select_customer(self):
        '''Selects a customer from the queue list
        and calculates the total times used in the process'''
        if SHORTEST:
            times = [customer.process_time for customer in self.queue]
            val, idx = min((val, idx) for (idx, val) in enumerate(times))
            customer = self.queue.pop(idx)
            customer.processed = True
            customer.calculate_time_used(self.time)
            return customer
        else:
            customer = self.queue.pop(0)
            customer.processed = True
            customer.calculate_time_used(self.time)
            return customer
    
    def select_customer_shortest_first(self):
        '''Selects a customer from the queue list
        and calculates the total times used in the process'''
        customer = self.queue.pop(0)
        customer.calculate_time_used(self.time)
        customer.processed = True
        return customer

    def servers_available(self):
        '''Determines if there are servers available in the server list'''
        available_servers = [server for server in self.servers if server.busy == False]
        if len(available_servers) > 0:
            return True
        else:
            return False
    
    def select_available_server(self, customer):
        '''Selects the first available router in the available router list'''
        available_servers = [server for server in self.servers if server.busy == False]
        server = available_servers[0]

        processing_time = customer.process_time
        server.available_time = self.time + processing_time
        server.busy = True
        return server
    
    def set_server_availability(self):
        '''Checks if a server is available or not'''
        for server in self.servers:
            if server.available_time <= self.time:
                server.busy = False

    def update_queue(self):
        '''Determines what customers are currently in the queue
        and returns a list with those customers'''
        x  =[customer for customer in self.customers if customer.arrival_time <= self.time and customer.processed == False]
        self.queue = [customer for customer in self.customers if customer.arrival_time <= self.time and customer.processed == False]

    def save_stats(self):
        '''Saves time and queue length of the model'''
        self.time_list.append(self.time)
        self.queue_list.append(len(self.queue))

class Server():
    
    def __init__(self, id):
        self.id = id
        self.busy = False
        self.available_time = 0

    def __repr__(self):
        if self.busy == True:
            return repr('Server ' + self.id + " is Busy")
        else:
            return repr('Server ' + self.id + " is Available")

class Customer():

    def __init__(self, id, arrival_time, process_time):
        self.id = id
        self.processed = False
        self.arrival_time = arrival_time
        self.generate_process_time(process_time)

    def __repr__(self):
        if self.processed == True:
            return repr('Customer ' + self.id + ' has been processed')
        else:
            return repr('Customer ' + self.id + 'still has to be processed')

    def generate_process_time(self, process_time):
        if D == False:
            if SPECIAL_DISTRIBUTION:
                U = np.random.rand()
                if U > 0.25:
                    self.process_time = np.random.exponential(process_time)
                else:
                    self.process_time = np.random.exponential(5 * process_time)

            else:
                self.process_time = np.random.exponential(process_time)
        else:
            self.process_time = D

    def calculate_time_used(self, start_time):
        self.time_used = start_time - self.arrival_time #+ process_time





# Statistics Q 2.
if __name__ == '__main__':
    '''
    # Statistics Q 3.

    n = 1000

    av_1 = []
    av_2 = []

    for i in tqdm(range(n)):

        SHORTEST = False
        
        queue = Queue(0, 1/4, 1, 2, 1500, False)
        queue.process_customers()

        SHORTEST = True

        queue_2 = Queue(0, 1/4, 1, 2, 1500, False)
        queue_2.process_customers()

        av_1.append(np.mean(queue.queue_list))
        av_2.append(np.mean(queue_2.queue_list))

    std_1 = np.std(av_1)
    std_2 = np.std(av_2)

    # 95% confidence

    int_1 = std_1 * 1.96 / np.sqrt(n)
    int_2 = std_2 * 1.96 / np.sqrt(n)

    print(std_1, std_2)
    
    print('Mean queuetime of queue 1: {:.2f}'.format(np.mean(av_1)))
    print('Mean queuetime of queue 2: {:.2f}'.format(np.mean(av_2)))

    print('95 percent confidence interval of queue 1: {:.2f}'.format(int_1))
    print('95 percent confidence interval of queue 2: {:.2f}'.format(int_2))

    df=pd.DataFrame({'queue 1':av_1,'queue 2':av_2})
    df.to_csv(r'times_short_vs_long.csv', index = False)
'''
    # Q 1
    n = 20
    load = 1
    av_1 = []
    av_2 = []
    av_3 = []

    av_cust_time_1 = []
    av_cust_time_2 = []
    av_cust_time_3 = []

    SPECIAL_DISTRIBUTION = False

    for i in tqdm(range(n)):

        SHORTEST = False
        
        queue = Queue(0, 1/4, 1, 1/2, 1000, False)
        queue.process_customers()

        queue_2 = Queue(0, 1/2, 2, 1/2, 1000, False)
        queue_2.process_customers()

        queue_3 = Queue(0, 1/1, 4, 1/2, 1000, False)
        queue_3.process_customers()

        av_1.append(np.mean(queue.queue_list))
        av_2.append(np.mean(queue_2.queue_list))
        av_3.append(np.mean(queue_3.queue_list))

        av_cust_time_1.append(np.mean(queue.waiting_times))
        av_cust_time_2.append(np.mean(queue_2.waiting_times))
        av_cust_time_3.append(np.mean(queue_3.waiting_times))

    df=pd.DataFrame({'queue 1':av_cust_time_1,'queue 2':av_cust_time_2, 'queue 3':av_cust_time_1})
    df.to_csv(r'1over8load.csv', index = False)

    std_1 = np.std(av_1)
    std_2 = np.std(av_2)
    std_3 = np.std(av_3)

    # 95% confidence

    int_1 = std_1 * 1.96 / np.sqrt(n)
    int_2 = std_2 * 1.96 / np.sqrt(n)
    int_3 = std_3 * 1.96 / np.sqrt(n)

    # Average queue length
    print('Mean queuelength of queue 1: {:.2f}'.format(np.mean(av_1)))
    print('Mean queuelength of queue 2: {:.2f}'.format(np.mean(av_2)))
    print('Mean queuelength of queue 3: {:.2f}'.format(np.mean(av_3)))

    print('95 percent confidence interval of queue 1: {:.2f}'.format(int_1))
    print('95 percent confidence interval of queue 2: {:.2f}'.format(int_2))
    print('95 percent confidence interval of queue 3: {:.2f}'.format(int_3))

    # Customer wait times
    std_1_cust = np.std(av_cust_time_1)
    std_2_cust = np.std(av_cust_time_2)
    std_3_cust = np.std(av_cust_time_3)

    int_1 = std_1_cust * 1.96 / np.sqrt(n)
    int_2 = std_2_cust * 1.96 / np.sqrt(n)
    int_3 = std_3_cust * 1.96 / np.sqrt(n)

    print('Mean queuetime of queue 1: {:.2f}'.format(np.mean(av_cust_time_1)))
    print('Mean queuetime of queue 2: {:.2f}'.format(np.mean(av_cust_time_2)))
    print('Mean queuetime of queue 3: {:.2f}'.format(np.mean(av_cust_time_3)))

    print('95 percent confidence interval of queue 1: {:.2f}'.format(int_1))
    print('95 percent confidence interval of queue 2: {:.2f}'.format(int_2))
    print('95 percent confidence interval of queue 3: {:.2f}'.format(int_3))


    # Q4.
    n = 100
    av_1 = []
    av_2 = []

    SPECIAL_DISTRIBUTION = True
    D = 1
    for i in tqdm(range(n)):
        
        queue = Queue(0, 1/4, 1, 3.5, 500, False)
        queue.process_customers()

        queue_2 = Queue(0, 1/4, 1, 3.5, 500, False)
        queue_2.process_customers()

        #av_1.append(np.mean(queue.queue_list))
        #av_2.append(np.mean(queue_2.queue_list))
        av_1.append(np.mean(queue.waiting_times))
        av_2.append(np.mean(queue_2.waiting_times))

    df=pd.DataFrame({'queue 1':av_1,'queue 2':av_2})
    df.to_csv(r'times3.csv', index = False)

    std_1 = np.std(av_1)
    std_2 = np.std(av_2)

    # 95% confidence

    int_1 = std_1 * 1.96 / np.sqrt(n)
    int_2 = std_2 * 1.96 / np.sqrt(n)

    print('Mean queuetime of queue 1: {:.2f}'.format(np.mean(av_1)))
    print('Mean queuetime of queue 2: {:.2f}'.format(np.mean(av_2)))

    print('95 percent confidence interval of queue 1: {:.2f}'.format(int_1))
    print('95 percent confidence interval of queue 2: {:.2f}'.format(int_2))
