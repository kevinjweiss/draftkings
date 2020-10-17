"""
Quicky script to scrape projections from fantasypros.com
"""

import pandas as pd
import os
import numpy as np
from itertools import combinations
from big_matrix import rank_tier

class Create_Lineup():
    
    def __init__(self, big_matrix_obj):
        pd.options.mode.chained_assignment = None
        self.week = big_matrix_obj.week
        self.big_matrix = big_matrix_obj.big_matrix
        self.path = big_matrix_obj.path
        self.positions = big_matrix_obj.positions
        
    def ownership_guess(self, auto):
        if auto == True:
            # Initialize Big Matrix & Blank Logic Dictionary
            big_matrix = self.big_matrix
            dict_list = []
            frames = []
            
            # QB/RB/WR/TE/DST
            dict_list.append({'Min_Tier': [3, '<'], 'Draft Kings_MID': [15, '>'], 'Draft Kings Value_MID': [325, '<'], 'Max_Spots': [3, 'M']})
            dict_list.append({'Min_Tier': [3, '<'], 'Draft Kings Value_MID_Tier': [6, '<'], 'Max_Spots': [10, 'M']})
            dict_list.append({'Draft Kings_MID': [8, '>'], 'Draft Kings Value_MID_Tier': [4, '<'], 'Max_Spots': [10, 'M']})
            dict_list.append({'Draft Kings_MID': [7, '>'], 'Draft Kings Value_MID': [400, '<'], 'Draft Kings Value_MID_Tier': [3, '<'], 'Max_Spots': [5, 'M']})
            dict_list.append({'Draft Kings_MID': [5, '>'], 'Draft Kings Value_MID_Tier': [3, '<'], 'Max_Spots': [3, 'M']})
            
            print('Targeted Players:')
            
            # Iterate through filter criteria for each DF
            for i, position in enumerate(self.positions):
                df = big_matrix[i]
                filter_dict = dict_list[i]
                
                for key in filter_dict:
                    if filter_dict[key][1] == '<':
                        df = df[df[key] < filter_dict[key][0]]
                    if filter_dict[key][1] == '>':
                        df = df[df[key] > filter_dict[key][0]]    
                    if filter_dict[key][1] == 'M':
                        df = df[:filter_dict[key][0]] 
                                    
                print('Position: ' + position.upper())
                
                for i in range(0, len(df.values)):
                    print(df['Player'].values[i])  
                print('')
                frames.append(df)  
            
            # Spit out DF to Ownership Guess File
            players_df = pd.concat(frames)
            players_df = players_df[['Player', 'Team', 'Position', 'Salary', 'Name + ID', 'Draft Kings_MIN', 'Draft Kings_MID', 'Draft Kings_MAX']]
            self.players_df = players_df
            players_df.to_csv(os.path.join(self.path, 'Ownership_Week' + str(self.week) + '_Guess_Auto.csv'))
        else: 
            players_df = pd.read_csv(os.path.join(self.path, 'Ownership_Week' + str(self.week) + '_Guess.csv'))
            self.players_df = players_df
            
    def create_all(self, salary_min, point_min):
        
        # Initialize Data Frames
        frames = []
        qb_all = []
        rb1_all = []
        rb2_all = []
        wr1_all = []
        wr2_all = []
        wr3_all = []
        te_all = []
        flex_all = []
        dst_all = []
        salary = []
        dk_min = []
        dk_mid = []
        dk_max = []
        
        # Columns Used For Lineup Creation
        columns = ['Player', 'Name + ID', 'Salary', 'Draft Kings_MIN', 
                   'Draft Kings_MID',	'Draft Kings_MAX']
        
        # Filter to players in ownership list and turn to NP Array for Speed
        for i, position in enumerate(self.positions):
            df = self.big_matrix[i][columns]
            df = df[df['Player'].isin(self.players_df['Player'])].reset_index()
            frames.append(df.values)

        # Initiate Lineup DF
        all_lineups = pd.DataFrame(columns=['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 
                                            'TE', 'Flex', 'DST', 'Salary', 'Draft Kings_MIN', 
                                            'Draft Kings_MID', 'Draft Kings_MAX'])
        i = 0
        
        # Setup Unique Combinations for Lineups - RB As Flex
        qb = list(combinations(range(len(frames[0])), 1))
        rb = list(combinations(range(len(frames[1])), 3))
        wr = list(combinations(range(len(frames[2])), 3))
        te = list(combinations(range(len(frames[3])), 1))
        dst = list(combinations(range(len(frames[4])), 1))
        
        for a in qb:
            for b in rb:
                for c in wr:
                    for d in te:
                        for e in dst:
                            temp_lineup = np.empty((9, 4))
                            temp_lineup[0,:] = frames[0][a[0], 3:]
                            temp_lineup[1,:] = frames[1][b[0], 3:]
                            temp_lineup[2,:] = frames[1][b[1], 3:]
                            temp_lineup[3,:] = frames[2][c[0], 3:]
                            temp_lineup[4,:] = frames[2][c[1], 3:]
                            temp_lineup[5,:] = frames[2][c[2], 3:]
                            temp_lineup[6,:] = frames[1][b[2], 3:]
                            temp_lineup[7,:] = frames[3][d[0], 3:]
                            temp_lineup[8,:] = frames[4][e[0], 3:]
                            
                            salary_sum = np.sum(temp_lineup[:, 0])
                            dk_min_sum = np.sum(temp_lineup[:, 1])
                            dk_mid_sum = np.sum(temp_lineup[:, 2])
                            dk_max_sum = np.sum(temp_lineup[:, 3])
                            
                            if salary_sum < 50001 and salary_sum > salary_min and dk_mid_sum > point_min:
                                qb_all.append(frames[0][a[0], 2])
                                rb1_all.append(frames[1][b[0], 2])
                                rb2_all.append(frames[1][b[1], 2])
                                wr1_all.append(frames[2][c[0], 2])
                                wr2_all.append(frames[2][c[1], 2])
                                wr3_all.append(frames[2][c[2], 2])
                                flex_all.append(frames[1][b[2], 2])
                                te_all.append(frames[3][d[0], 2])
                                dst_all.append(frames[4][e[0], 2])
                                salary.append(salary_sum)
                                dk_min.append(dk_min_sum)
                                dk_mid.append(dk_mid_sum)
                                dk_max.append(dk_max_sum)
        
        # Setup Unique Combinations for Lineups - WR As Flex
        qb = list(combinations(range(len(frames[0])), 1))
        rb = list(combinations(range(len(frames[1])), 2))
        wr = list(combinations(range(len(frames[2])), 4))
        te = list(combinations(range(len(frames[3])), 1))
        dst = list(combinations(range(len(frames[4])), 1))
        
        for a in qb:
            for b in rb:
                for c in wr:
                    for d in te:
                        for e in dst:
                            temp_lineup = np.empty((9, 4))
                            temp_lineup[0,:] = frames[0][a[0], 3:]
                            temp_lineup[1,:] = frames[1][b[0], 3:]
                            temp_lineup[2,:] = frames[1][b[1], 3:]
                            temp_lineup[3,:] = frames[2][c[0], 3:]
                            temp_lineup[4,:] = frames[2][c[1], 3:]
                            temp_lineup[5,:] = frames[2][c[2], 3:]
                            temp_lineup[6,:] = frames[2][c[3], 3:]
                            temp_lineup[7,:] = frames[3][d[0], 3:]
                            temp_lineup[8,:] = frames[4][e[0], 3:]
                            
                            salary_sum = np.sum(temp_lineup[:, 0])
                            dk_min_sum = np.sum(temp_lineup[:, 1])
                            dk_mid_sum = np.sum(temp_lineup[:, 2])
                            dk_max_sum = np.sum(temp_lineup[:, 3])
                            
                            if salary_sum < 50001 and salary_sum > salary_min and dk_mid_sum > point_min:
                                qb_all.append(frames[0][a[0], 2])
                                rb1_all.append(frames[1][b[0], 2])
                                rb2_all.append(frames[1][b[1], 2])
                                wr1_all.append(frames[2][c[0], 2])
                                wr2_all.append(frames[2][c[1], 2])
                                wr3_all.append(frames[2][c[2], 2])
                                flex_all.append(frames[2][c[3], 2])
                                te_all.append(frames[3][d[0], 2])
                                dst_all.append(frames[4][e[0], 2])
                                salary.append(salary_sum)
                                dk_min.append(dk_min_sum)
                                dk_mid.append(dk_mid_sum)
                                dk_max.append(dk_max_sum)
        
        # Setup DF To Output to CSV
        all_lineups['QB'] = qb_all
        all_lineups['RB1'] = rb1_all
        all_lineups['RB2'] = rb2_all
        all_lineups['WR1'] = wr1_all
        all_lineups['WR2'] = wr2_all
        all_lineups['WR3'] = wr3_all
        all_lineups['TE'] = te_all
        all_lineups['Flex'] = flex_all
        all_lineups['DST'] = dst_all
        all_lineups['Salary'] = salary
        all_lineups['Draft Kings_MIN'] = dk_min
        all_lineups['Draft Kings_MID'] = dk_mid
        all_lineups['Draft Kings_MAX'] = dk_max
        
        all_lineups['Draft Kings_MIN_Rank'], tier1 = rank_tier(10, 'Draft Kings_MIN', all_lineups, False)
        all_lineups['Draft Kings_MID_Rank'], tier2 = rank_tier(10, 'Draft Kings_MID', all_lineups, False)
        all_lineups['Draft Kings_MAX_Rank'], tier3 = rank_tier(10, 'Draft Kings_MAX', all_lineups, False)
        all_lineups['Raw Rank'] = all_lineups['Draft Kings_MIN_Rank'] + all_lineups['Draft Kings_MID_Rank'] + all_lineups['Draft Kings_MAX_Rank']
        rank4, tier4 = rank_tier(10, 'Raw Rank', all_lineups, True)
        all_lineups['Final Rank'] = rank4
        
        # Sort assign to object and output to CSV
        all_lineups = all_lineups.sort_values('Draft Kings_MID', ascending = False).reset_index(drop = True)
        self.all_lineups = all_lineups
        all_lineups.to_csv(os.path.join(self.path, 'All_Lineups_Week' + str(self.week) + '.csv'), index = False)
