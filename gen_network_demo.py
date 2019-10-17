
from Base import gen_one_result
from tools import parse_conifg
import tkinter
from tkinter import filedialog
import os

# open config file
def run():
    root = tkinter.Tk()    # create a Tkinter.Tk() instance
    root.withdraw()       # hide Tkinter.Tk() instance
    config_path = filedialog.askopenfilename(
                title=u'choose config file', 
                initialdir=(os.path.expanduser(os.getcwd()))
                ) # choose config file
    root.quit()
    
    params = parse_conifg(config_path) # parse config file

    # rename the columns of oubreak files
    df_observed, df_true = gen_one_result(params)
    cols = ["node_id","block","infected_period",
            "latent_period","s_I","state","symptomatic","t_I",'t_observed']
    new_cols = ["node_id","community_id","infected_period",
            "latent_period","source_Infected","state","symptomatic","time_infected",'time_observed']
    df_observed = df_observed[cols]
    df_true = df_true[cols]
    
    df_observed.columns = new_cols
    df_true.columns = new_cols
    
    # save file in CSV format
    df_observed.to_csv('observed_outbreak.csv')
    df_true.to_csv('true_outbreak.csv')

if __name__ == '__main__':
    run()
