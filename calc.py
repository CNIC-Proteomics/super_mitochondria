import os
import logging
import pandas
import numpy as np
import re
from string import ascii_letters
import seaborn as sns
import matplotlib.pyplot as plt


__author__ = 'jmrodriguezc'


class calculate:
    '''
    Extract the correlation values
    '''

    def __init__(self, i, s, m=None):
        # handle I/O files
        self.infile = i
        # extract input data ( as dataframe )
        # set index with the first column
        self.df = pandas.read_excel(self.infile, sheet_name=s, na_values=['NA'])
        c = str(self.df.columns[0])
        self.df = self.df.set_index(c)
        # get method
        if m is None:
            self.method = 'pearson'
        else:
            self.method = m
        # ouput config
        self.out_header = ['Qi','Qj','Rij']
        self.df_corr = pandas.DataFrame()
        
    def _append_correlation(self, shared_lst, combos):
        for combo in combos:        
            # get index
            qi = combo[0]
            qj = combo[1]
            # create the correlation
            dfi = self.df.loc[qi,:]
            dfj = self.df.loc[qj,:]
            corr = dfi.corr(dfj, method=self.method)            
            # append the list of values into shared list
            shared_lst.append([qi,qj,corr])

    def correlation(self, method=None):
        '''
        Calculate the correlation
        '''
        # get method if it exists: Priority
        if method is not None:
            self.method = method
        # create the correlation: 
        self.df_corr = self.df.corr(method=self.method)

    def create_heatmap(self, graphfile):
        '''
        Create heatmap
        '''        
        corr = self.df_corr

        # Generate a mask for the upper triangle
        mask = np.zeros_like(corr)
        mask[np.triu_indices_from(mask)] = True
        # Set up the matplotlib figure
        f, ax = plt.subplots(figsize=(11, 9))
        # Generate a custom diverging colormap
        cmap = sns.diverging_palette(220, 10, as_cmap=True)
        # Draw the heatmap with the mask and correct aspect ratio
        # sns.heatmap(corr, mask=mask, cmap=cmap, vmin=0, vmax=1, square=True, annot=True, fmt='.4g')
        sns.heatmap(corr, mask=mask, cmap=cmap, vmin=0, vmax=1, linewidths=.1, cbar_kws={"shrink": .5}, square=True, annot=True, fmt='.4g')

        plt.savefig(graphfile, tight_layout=True)

    def to_csv(self, outfile):
        '''
        Print to CSV sorting by score
        '''
        # sort dataframe by correlation score (Third column)
        if not self.df_corr.empty:
            self.df_corr.to_csv(outfile)
        else:
            logging.error("Empty output")