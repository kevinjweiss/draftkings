# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 16:42:21 2020

@author: queis
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from big_matrix import rank_tier
  
class Post_Process():
    
    def __init__(self, year, week, positions):
        self.week = week
        self.year = year
        self.positions = positions
        self.path = os.path.join(str(year), 'Week' + str(week))
        self.big_matrix = pd.read_csv(os.path.join(self.path, 'BigMatrix_Week' + str(week) + '.csv'))
        self.all_lineups = pd.read_csv(os.path.join(self.path, 'All_Lineups_Week' + str(week) + '.csv'))
        
        # Read and process Result Data
        result_data = pd.read_csv(os.path.join(self.path, 'ContestStandings_Week' + str(week) + '.csv'))
        self.result_data = result_data[['Player', 'Roster Position',	'%Drafted',	'FPTS']].dropna()
        
        # Calculate Point Threshold
        temp_df = result_data[result_data['Rank']>.435*len(result_data['Points'])]
        temp_df = temp_df.reset_index(drop=True)
        self.point_thresh = temp_df.loc[0, 'Points']
    
    def big_matrix_process(self):
        # Read In Data
        result_data = self.result_data
        big_matrix = self.big_matrix
        
        # Rename players in results file to match big matrix
        result_data['Player'] = result_data['Player'].apply(lambda x: ' '.join(x.split()[0:2]))
        result_data['Player'] = result_data['Player'].str.replace('.', '')
        result_data['Player'] = result_data['Player'].str.replace('WAS Football', 'Team')
        
        # Initialize Big Matrix Columns
        big_matrix['FPTS'] = 0
        big_matrix['%Drafted'] = 0
        big_matrix['Real_Value'] = 0
        
        # Loop Through Big Matrix and assign results to columns
        for i in range(len(big_matrix)):
            
            # Locate Player In Results Data
            player = big_matrix.loc[i, 'Player']
            index = result_data.index[result_data['Player'] == player].values
            
            # Set Points to points column, set to 0 if player can't be found
            points = result_data.loc[index, 'FPTS'].values
            if points.size ==0:
                points = 0
            big_matrix.loc[i, 'FPTS'] = points
            
            # Set Ownership to ownership column, set to 0 if player can't be found
            ownership = result_data.loc[index, '%Drafted'].values
            if ownership.size ==0:
                ownership = 0
            else:
                ownership = float(np.asscalar(ownership).rstrip("%"))
            big_matrix.loc[i, '%Drafted'] = ownership
            
            # Calculate Actual Value
            if points>1:
                big_matrix.loc[i, 'Real_Value'] = big_matrix.loc[i, 'Salary']/points
            else:
                big_matrix.loc[i, 'Real_Value'] = 1000
        
        self.big_matrix_process = big_matrix
        big_matrix.to_csv(os.path.join(self.path, 'BigMatrix_Week' + str(self.week) + '_Processed.csv'))
        
    def big_matrix_process_plot(self, df_in, list, ascending):
         
        # Loop through Positions
        for i, position in enumerate(self.positions):
            
            if position == 'qb':
                thresh = 15
            if position == 'wr':
                thresh = 10
            if position == 'rb':
                thresh - 8
            if position == 'rb' or position == 'te' or position == 'dst':
                thresh = 5
            
            # Loop through Scoring Systems
            for item in list:
                with plt.style.context('ggplot'):
                    fig, ax = plt.subplots(figsize=(12, 12))
                plt.title(position.upper())
                df = df_in[df_in['Position'].str.contains(position.upper())]
                df = df.sort_values(item + '_MID', ascending=ascending)
                df = df[df[item + '_MID'] > thresh].reset_index()
                
                rank, tier = rank_tier(8, item + '_MID', df, ascending)
                cmap = cm.get_cmap("plasma")
                colors = [cmap(k/8) for k in tier]
                
                index = -(df.index.values + 1)
                median = df[item + '_MID']
                low_error = df[item + '_MIN']
                high_error = df[item + '_MAX']
                plt.xlabel('Projection')
                
                ax.scatter(median, index, c = colors, label = tier)
                ax.hlines(index, low_error, high_error, colors = colors)
                plt.yticks(index, df['Player'])
                size = (1000*(df['%Drafted']/100)).clip(50, 1000)
                plt.xlim([min(df['Real_Value'])*.9, min(max(df['Real_Value'])*1.15, 2000)]) 
                ax.scatter(df['Real_Value'], index, marker = '*', color = 'y', s = size)
               
                fig.savefig(os.path.join(self.path, position.upper() + '_' + item + '_Processed.png'))
        
    def all_lineup_process(self):
        all_lineups = self.all_lineups
        big_matrix_process = self.big_matrix_process
        
        columns = ['QB','RB1','RB2','WR1','WR2','WR3','TE','Flex','DST']

        for i, column in enumerate(columns):
            temp = big_matrix_process.rename(columns={'Name + ID':column})

            if i == 0:
                points_sum = all_lineups.merge(temp, on=column, how='left')['FPTS']
                ownership_sum = all_lineups.merge(temp, on=column, how='left')['%Drafted']
            else:
                points_sum += all_lineups.merge(temp,  on=column, how='left')['FPTS']
                ownership_sum += all_lineups.merge(temp,  on=column, how='left')['%Drafted']
        
        all_lineups['FPTS'] = points_sum
        all_lineups['%Drafted'] = ownership_sum/len(columns)
        
        all_lineups.to_csv(os.path.join(self.path, 'All_Lineups_' + str(self.week) + '_Processed.csv'))
        self.all_lineups_process = all_lineups
        
    def all_lineup_process_plot(self):
        alp = self.all_lineups_process
        
        with plt.style.context('ggplot'):
            fig, ax = plt.subplots(nrows = 2, ncols = 4, figsize=(24, 12))
        
        ax = ax.ravel()
        
        ax[0].scatter(alp['Draft Kings_MIN'], alp['%Drafted'])
        ax[0].set_title('Min Projection vs. Average Ownership')
        ax[1].scatter(alp['Draft Kings_MID'], alp['%Drafted'])
        ax[1].set_title('Mid Projection vs. Average Ownership')
        ax[2].scatter(alp['Draft Kings_MAX'], alp['%Drafted'])
        ax[2].set_title('Max Projection vs. Average Ownership')
        ax[3].scatter(alp['Final Rank'], alp['%Drafted'])
        ax[3].set_title('Rank vs. Average Ownership')        
        
        ax[4].scatter(alp['Draft Kings_MIN'], alp['FPTS'])
        ax[4].axhline(self.point_thresh)
        ax[4].set_title('Min Projection vs. Actual Points')
        ax[5].scatter(alp['Draft Kings_MID'], alp['FPTS'])
        ax[5].axhline(self.point_thresh)
        ax[5].set_title('Mid Projection vs. Actual Points')
        ax[6].scatter(alp['Draft Kings_MAX'], alp['FPTS'])
        ax[6].axhline(self.point_thresh)
        ax[6].set_title('Max Projection vs. Actual Points')
        ax[7].scatter(alp['Final Rank'], alp['FPTS'])
        ax[7].axhline(self.point_thresh)
        ax[7].set_title('Rank vs. Actual Points')
        
        fig.savefig(os.path.join(self.path, 'All_Lineups_Processed.png'))
        
    def success(self, num_lineups):
        print(self.week)
        
        alp = self.all_lineups_process
        thresh = self.point_thresh
        
        sub1 = alp[alp['Draft Kings_MIN_Rank']<num_lineups+1]
        sub2 = alp[alp['Draft Kings_MID_Rank']<num_lineups+1]
        sub3 = alp[alp['Draft Kings_MAX_Rank']<num_lineups+1]
        sub4 = alp[alp['Final Rank']<num_lineups+1]
        
        subs = [sub1, sub2, sub3, sub4]
        
        for sub in subs:
            win = sub[sub['FPTS']>thresh]
            print(len(win)/len(sub))
        
        
        