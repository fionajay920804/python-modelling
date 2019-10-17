import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import os
import tkinter
from tkinter import filedialog
import networkx as nx

def show_result(G,new_observed_list,v_I, new_infected_list,new_asymp_list):
    
    root = tkinter.Tk()    # create a Tkinter.Tk() instance
    root.withdraw()       # hide a Tkinter.Tk() instance
    pic_path = filedialog.asksaveasfilename(title=u'path to save fig', filetypes=[("png", ".png")])
    root.quit()
    
    # plot output
    plt.figure(figsize=(9,16))
    
    # use viridis colour map, with grey for uninfected nodes
    my_cmap = plt.cm.get_cmap('viridis')
    my_cmap.set_under('0.8')
    
    # draw the observed outbreak contact network (nodes coloured by infection time)
    ax = plt.subplot(321)
    nx.draw_networkx(G, 
                     with_labels=False,
                     node_size=100,
                     node_color=list(
                             nx.get_node_attributes(G, 'c_observed').values()),
                     pos=nx.spring_layout(G),
                     cmap=plt.cm.viridis, 
                     vmin=0)
    ax.set_title('observed outbreak')
    ax.set_xticks([])
    ax.set_yticks([]) 
    

    # draw the true outbreak contact network (nodes coloured by infection time)
    ax = plt.subplot(322)
    nx.draw_networkx(G, 
                     with_labels=False,
                     node_size=100,
                     node_color=list(
                             nx.get_node_attributes(G, 'c_true').values()),
                     pos=nx.spring_layout(G),
                     cmap=plt.cm.viridis, 
                     vmin=0)
    ax.set_title('true outbreak')
    ax.set_xticks([])
    ax.set_yticks([]) 
    
    # draw the transmission tree
    ax = plt.subplot(323)
    tree = nx.DiGraph()
    tree.add_nodes_from([(k, v) for k, v in G.nodes(data=True)if v['t_I'] != None])
    tree.add_edges_from([(v['s_I'], i) for i, v in G.nodes(data=True) 
                if (v['s_I'] != None)])
    pos=nx.nx_agraph.graphviz_layout(tree, prog='dot')
    nodes = nx.draw_networkx_nodes(tree, 
                                   pos=pos, 
                                   node_size=50, 
                                   with_labels=False, 
                                   node_color=list(nx.get_node_attributes(tree, 't_I').values()),
                                   cmap=plt.cm.viridis, vmin=0)
    
    edges = nx.draw_networkx_edges(tree, pos=pos, node_size=50)
    plt.colorbar(nodes)
    ax.set_title('transmission tree')
    ax.set_xticks([])
    ax.set_yticks([])
    
    # plot incidence over time
    ax = plt.subplot(324)
    ax.bar(range(len(new_infected_list)), new_infected_list)
    ax.set_title('incidence')
    ax.set_xlabel('time')
    ax.set_ylabel('new cases')
    
    # plot prevalence over time
    ax = plt.subplot(325)
    ax.bar(range(len(v_I)), v_I)
    ax.set_title('prevalence')
    ax.set_xlabel('time')
    ax.set_ylabel('number infected')
    
    # plot prevalence over time
    ax = plt.subplot(326)
    ax.bar(range(len(new_observed_list)), new_observed_list)
    ax.set_title('new observed')
    ax.set_xlabel('time')
    ax.set_ylabel('number observed')
    
    plt.savefig(pic_path)
    
    print(''.format(os.path.join(os.getcwd(), )))


def parse_conifg(config_path):
    with open(config_path,'r') as f:
        data = [i.replace('\n','').split('=') for i in f.readlines()]
    
    params = {}
    for line in data:
        if line[0].strip() in ['show_pic','show_process']:
            if line[1].strip() == 'True':
                params[line[0].strip()] = True
            else:
                params[line[0].strip()] = False
        else:
            params[line[0].strip()] = float(line[1].strip())
    return params 