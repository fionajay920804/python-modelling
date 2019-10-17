
'''
step 1:
    get and parse config file

step 2:
    input some varibales to do simulation

step 3:
    do simulation

step 4:
    show result
'''

from Base import gen_one_result
from tools import parse_conifg
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import pandas as pd
import tkinter
from tkinter import filedialog
import os
import re


def run():
    # get and aparse config file
    root = tkinter.Tk()    # create a Tkinter.Tk() instance
    root.withdraw()       # hide Tkinter.Tk() instance
    config_path = filedialog.askopenfilename(
                title=u'choose config file:', 
                initialdir=(os.path.expanduser(os.getcwd()))
                ) # choose config file
    
    observed_data_path = filedialog.askopenfilename(
                title=u'choose observed data:', 
                initialdir=(os.path.expanduser(os.getcwd()))
                ) # choose config file
    
    root.quit()
    
    params = parse_conifg(config_path) # parse config file
    params['show_pic'] = False
    params['show_process'] = False
    df_observed = pd.read_csv(observed_data_path, encoding = 'utf-8')
    
    # Calculate the range of valid simulation results
    h = df_observed.groupby('time_observed').count()
    p = df_observed.groupby('infected_period').count() 

    avg_I = h['node_id'].mean()
    std_I = h['node_id'].std()
    
    avg_P = p['node_id'].mean()
    std_P = p['node_id'].std()
    
    avg_I_min = avg_I-std_I/5
    avg_I_max = avg_I+std_I/5
    
    avg_P_min = avg_P-std_P/5
    avg_P_max = avg_P+std_P/5
    # Enter the parameters to be simulated, separated by Spaces
    # p q symp_prob_threshold
    variables = input('Please input variables (separated with blank space) to be simulated:')
    variables = [i.strip() for i in re.split('\s+',variables)]

    
    var_range = {'q':[0.01, 0.5],
                 'g':[0.01, 0.5],
                 'symp_prob_threshold':[0.01, 0.7]} # set the range of value
    var_rec = {i:[] for i in variables}
    epochs = input('Please input epochs to do the simulation (default 100):')
    if epochs == '':
        epochs = 100
    else:
        epochs = int(epochs)
    print('####################  Simulating  ####################')
    for i in range(epochs):
        if i%10 == 0:
            print('It is at step {}!'.format(i))
        # assign variables
        for v in variables:
            low = var_range[v][0]
            high = var_range[v][1]
            params[v] = np.random.uniform(low = low, high = high)
        
        # do simulation
        try:
            df_observed, _ = gen_one_result(params)
            # 
            if df_observed.shape[0]<10:
                continue
            avg_I = df_observed.groupby('t_observed').count()['node_id'].mean()
            avg_P = df_observed.groupby('infected_period').count()['node_id'].mean()
            
            if avg_I>avg_I_min and avg_I<avg_I_max and avg_P>avg_P_min and avg_P<avg_P_max:
                for v in variables:
                    var_rec[v].append(params[v])
        except:
            pass
                
    for v in variables:
        root = tkinter.Tk()    # create a Tkinter.Tk() instance
        root.withdraw()       # hide Tkinter.Tk() instance
        pic_path = filedialog.asksaveasfilename(title=u'path to save fig of {}'.format(v),
                                                filetypes=[("png", ".png")])
        root.quit()
    
        plt.figure(figsize = (9, 6))
        plt.hist(var_rec[v])
        plt.title(v)
        plt.savefig(pic_path)
        
        print('The estimated value of {} is: {}!'.format(v, np.mean(var_rec[v])))
        

if __name__ == '__main__':
    run()


