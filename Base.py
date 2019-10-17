
import numpy as np
import networkx as nx
from numpy import random
import pandas as pd
import matplotlib
matplotlib.use("TkAgg") # this just for solving the problem of using this package in mac
import matplotlib.pyplot as plt
import os
import tkinter
from tkinter import filedialog
from tools import show_result

def get_initial_node(params):
    # get input value from dictionary
    comm_size = int(params['comm_size'])
    num_comms = int(params['num_comms'])
    p_in = params['p_in']
    p_out = params['p_out']
    latent_days_threshold = params['latent_days_threshold']
    infected_days_threshold = params['infected_days_threshold']
    symp_prob_threshold = params['symp_prob_threshold']
    
    # initial the social network
    G = nx.random_partition_graph([comm_size] * num_comms, p_in, p_out)

    # initialise network attributes, assign some attributes to each nodes with initial values
    nx.set_node_attributes(G, 'S', 'state')     # disease state
    nx.set_node_attributes(G, None, 't_I')        # time of infection
    nx.set_node_attributes(G, None, 's_I')      # source of infection
    nx.set_node_attributes(G, 0, 'latent_period')      # latent time
    nx.set_node_attributes(G, 0, 'infected_period')      # infected time
    nx.set_node_attributes(G, None, 'symptomatic')      # whether symptomatic
    nx.set_node_attributes(G, 0, 'c_observed')      # the color of observed infected time
    nx.set_node_attributes(G, 0, 'c_true')      # the color of true infected time
    nx.set_node_attributes(G, 0, 't_observed')      # infected time of observed

    # choose a single node as the initial infected node of all nodes, assign it status I
    seed_node = np.random.randint(num_comms * comm_size)
    G.node[seed_node]['state'] = 'I' 
    G.node[seed_node]['t_I'] = 1 # means that observation starts at its beginning
    G.node[seed_node]['s_I'] = seed_node
    
    # random select a infected day
    N = random.randint(infected_days_threshold)
    G.node[seed_node]['symptomatic'] = 1 # 0 means you're asymptomatic, and 1 means you're symptomatic
    G.node[seed_node]['latent_period'] = random.randint(latent_days_threshold) # random select a latent period
    G.node[seed_node]['infected_period'] = N

    # next_state is used to set the state of next time stamp
    nx.set_node_attributes(G, nx.get_node_attributes(G, 'state'), 'next_state')
    return G, seed_node

   
def gen_one_result(params):
       
    latent_days_threshold = params['latent_days_threshold']
    symp_prob_threshold = params['symp_prob_threshold']
    infected_days_threshold = params['infected_days_threshold']
    latent_days_threshold = params['latent_days_threshold']
    show_pic = params['show_pic']
    show_process = params['show_process']
    L_to_I_prob = params['L_to_I_prob']
    observed_prob_threshold = params['observed_prob_threshold']
    q = params['q']
    g = params['g']
    
    G, seed_node = get_initial_node(params)
    # simulate an outbreak on the network
    t = 0      # time step
    v_I = [1]   # vector to keep track of prevalence (current number of infections in each time step)
    v_symp = [1] # infected and symptoms
    v_asymp = [0] # Infected but asymptomatic
    
    new_infected_list = [1] #Newly infected
    new_symp_list = [1] # Newly infected people with symptoms
    new_asymp_list = [0] # New asymptomatic infections
    new_recover_list = [] # The number of newly recovered
    new_observed_list = [] # The number of newly observed infection
    
    t = 0
    while True:
        
        t += 1
        new_observed = 0
        new_latent = 0
        new_symp = 0
        new_asymp = 0
        new_recover = 0
        if show_process:
            print('\nIt is at day {}!'.format(t))
        for n,v in G.nodes(data=True):
            # if a node have recovered, just pass it
            if G.node[n]['state'] == 'R':
                pass
            
            # state from S to L
            if G.node[n]['state'] == 'S':
                infect_prob, src_nodes = calc_get_infected_prob(G, n, q) # calculate the probabilty of infected
                if random.rand()>infect_prob: # Less than q is not infected
                    pass
                elif len(src_nodes)==0:
                        pass
                else:
                    if show_process:
                        print('{} from S to L!'.format(n))
                    G.node[n]['t_I'] = t # set infected time
                    G.node[n]['next_state'] = 'L' # set next state as latent state
                    G.node[n]['latent_period'] = 1 
                    G.node[n]['s_I'] = src_nodes[random.randint(len(src_nodes))] # random select a node as source
                    new_latent += 1 # record the number of new infections
            
            # state from L to I        
            if G.node[n]['state'] == 'L':
                G.node[n]['latent_period'] += 1
                latent_days =  G.node[n]['latent_period']
                if latent_days < latent_days_threshold:
                    u = random.rand()
                    if u < L_to_I_prob:
                        G.node[n]['next_state'] = 'I'
                        symp_prob = calc_symp_prob()
                        if symp_prob<symp_prob_threshold: # lower means symptomatic, larger means asymptomatic
                            if show_process:
                                print('{} from L to I symp'.format(n))
                            G.node[n]['symptomatic'] = 1 # 1 means you're symptomatic
                            new_symp += 1
                        else:
                            if show_process:
                                print('{} from L to I asymp'.format(n))
                            G.node[n]['symptomatic'] = 0 # 0 means you're asymptomatic
                            new_asymp += 1
                else:
                    G.node[n]['next_state'] = 'I'
                    symp_prob = calc_symp_prob()
                    
                    if symp_prob<symp_prob_threshold:
                        if show_process:
                            print('{} from L to I symp'.format(n))
                        G.node[n]['symptomatic'] = 1
                        new_symp += 1
                    else:
                        if show_process:
                            print('{} from L to I asymp'.format(n))
                        G.node[n]['symptomatic'] = 0
                        new_asymp += 1
            # state from I ro R        
            if G.node[n]['state'] == 'I':
                G.node[n]['infected_period'] += 1
                infected_days = G.node[n]['infected_period']
                # probabilty of being observed
                if G.node[n]['t_observed'] == 0 and G.node[n]['symptomatic'] == 1:
                     observed_probability = np.random.rand()
                     if observed_probability < observed_prob_threshold:
                         G.node[n]['t_observed'] = t
                         new_observed += 1

                # whether it recover
                if infected_days > infected_days_threshold:
                    if show_process:
                        print('{} Removed!'.format(n))
                    G.node[n]['next_state'] = 'R'
                    new_recover+=1
                else:
                    recover_prob = calc_get_recovered_prob()
                    if recover_prob>g:
                        pass
                    else:
                        if show_process:
                            print('{} Removed!'.format(n))
                        G.node[n]['next_state'] = 'R'
                        new_recover+=1
        
        # update the state of each node
        nx.set_node_attributes(G, nx.get_node_attributes(G, 'next_state'), 'state')               
       
                    
        n_I = [n for n,v in G.nodes(data=True) if v['state'] in ['I','L']]
        n_symp = [n for n,v in G.nodes(data=True) if v['state'] in ['I','L'] and v['symptomatic'] == 1]
        n_asymp = [n for n,v in G.nodes(data=True) if v['state'] in ['I','L'] and v['symptomatic'] == 0]
        v_I.append(len(n_I)) # Total number of infections each 
        v_symp.append(len(n_symp)) # Total number of symptomatic infections each day 
        v_asymp.append(len(n_asymp)) # Total number of asymptomatic infections each day
        new_infected_list.append(new_latent) # New infections each day
        new_symp_list.append(new_symp) # Number of new infections with symptoms each day
        new_asymp_list.append(new_asymp) # Number of asymptomatic new infections each day
        new_recover_list.append(new_recover) # Number of newly recovered each day
        new_observed_list.append(new_observed) # Number of newly observed infection each day 
        
        if not n_I:
            break
    if show_pic is True:
        # Showing infections those symptomatic and observed
        for n, v in G.nodes(data=True):
            if v['t_observed'] > 0:
                G.node[n]['c_observed'] = G.node[n]['t_observed'] # set the color according to the day of observed
            else :
                G.node[n]['c_observed'] = -2

        # Showing infection but no symptoms
        for n, v in G.nodes(data=True):
            if not v['t_I'] == None:
                G.node[n]['c_true'] = G.node[n]['t_I'] # set the color according to the day of infected
            else :
                G.node[n]['c_true'] = -2
        show_result(G,new_observed_list,v_I, new_infected_list,new_asymp_list)
    
    # Record symptomatic infection data
    d_observed = {}
    for n, v in G.nodes(data=True):
        if v['t_observed'] > 0:
            d_observed[n] = v

    # Record asymptomatic infection data
    d_true = {}
    for n, v in G.nodes(data=True):
        if not v['t_I'] == None:
            d_true[n] = v
    
    
    # The symptomatic and asymptomatic data were respectively organized into dataframe format and then save it
    # CSV files can be opened directly in excel
    df_observed = pd.DataFrame(d_observed).T
    df_observed['node_id'] = df_observed.index
    #df_symp.to_csv('symp_results.csv')
    
    df_true = pd.DataFrame(d_true).T
    df_true['node_id'] = df_true.index
    #df_asymp.to_csv('asymp_results.csv')
    
    return df_observed, df_true


def calc_get_infected_prob(G, n, q):
    # Choose people from those you come into contact with. If they are infected, you may become infected. If they are not, you will not become infected
    neighbor_list = []
    for edge in G.edges():
        if n in edge:
            node_idx = list(edge)
            node_idx.remove(n)
            neighbor_list.append(node_idx[0])
    if len(neighbor_list) == 0:
        return n
    else:
        # I'm going to pick a bunch of random places
        contact_nums = random.randint(len(neighbor_list))
        idx = []
        while True:
            u = random.randint(len(neighbor_list))
            if u not in idx:
                idx.append(u)
            if len(idx)>=contact_nums:
                break
        # Pick a few people
        src_nodes = []
        for i in idx:
            if G.node[neighbor_list[i-1]]['state'] in ['L','I']:
                src_nodes.append(neighbor_list[i-1])  
        if len(src_nodes) == 0:
            return 0,[] #They don't get infected
        # (1-q) The probability that a node touched will not be infected
        # (1-q)**len(src_node) The probability of not getting infected with that many people, so the probability of getting infected is just 1 minus it
        infect_prob = 1 - (1-q)**len(src_nodes)
#        print('infect_prob is:', infect_prob)
        return infect_prob, src_nodes


def calc_symp_prob():
    return random.rand()

def calc_get_recovered_prob():
    return random.rand()







