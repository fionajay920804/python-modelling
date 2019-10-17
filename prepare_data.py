
import tkinter
from tkinter import filedialog
import os
from Base import gen_one_result
from tools import parse_conifg

# 1 Generate a specific result
def run():
    # get and parse config file
    root = tkinter.Tk()    # create a Tkinter.Tk() instance
    root.withdraw()       # hide Tkinter.Tk() instance
    config_path = filedialog.askopenfilename(
                title=u'choose config file', 
                initialdir=(os.path.expanduser(os.getcwd()))
                ) # choose config file
    root.quit()
    
    params = parse_conifg(config_path) # parse config file
    params['show_pic'] = False # do not show photo
    params['show_process'] = False # do not show any state change peocess

    # redefine the columns name of the outbreak file
    df_observed, df_true = gen_one_result(params)
    cols = ["node_id","block","infected_period",
            "latent_period","s_I","state","symptomatic","t_I",'t_observed']
    new_cols = ["node_id","community_id","infected_period",
            "latent_period","source_Infected","state","symptomatic","time_infected",'time_observed']
    df_observed = df_observed[cols]
    
    df_observed.columns = new_cols
    
    # choose path to save generated obdserved result
    root = tkinter.Tk()    # create a Tkinter.Tk() instance
    root.withdraw()       # hide a Tkinter.Tk() instance
    csv_path = filedialog.asksaveasfilename(title=u'path to save observed data:', 
                                            filetypes=[("csv", ".csv")])
    root.quit()
    
    df_observed.to_csv(csv_path,encoding = 'utf-8')

if __name__ == '__main__':
    run()