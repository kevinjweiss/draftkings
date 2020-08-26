# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 16:17:04 2020

@author: weissk
"""

import pandas as pd

year = '2018_Test'
weeks = ['Week6', 'Week7', 'Week8', 'Week9', 'Week10', 'Week13', 'Week14', 'Week15']

big_big_matrix = pd.DataFrame()

total_rb = 0
total_te = 0
total_wr = 0

for week in weeks:
    big_matrix = pd.read_csv(year + '/' + week + '/BigMatrix_' + week + '_Processed.csv')
    
    rb_ownership = big_matrix[big_matrix['Position'] == 'RB']['%Drafted'].sum()
    wr_ownership = big_matrix[big_matrix['Position'] == 'WR']['%Drafted'].sum()
    te_ownership = big_matrix[big_matrix['Position'] == 'TE']['%Drafted'].sum()
        
    total_rb = rb_ownership + total_rb
    total_wr = wr_ownership + total_wr
    total_te = te_ownership + total_te
    
year = '2019_Test'
weeks = ['Week1', 'Week2', 'Week3', 'Week4', 'Week5', 'Week6',
        'Week7', 'Week8', 'Week9', 'Week10', 'Week11', 'Week12',
        'Week13', 'Week14', 'Week15', 'Week16']

for week in weeks:
    big_matrix = pd.read_csv(year + '/' + week + '/BigMatrix_' + week + '_Processed.csv')
    
    rb_ownership = big_matrix[big_matrix['Position'] == 'RB']['%Drafted'].sum()
    wr_ownership = big_matrix[big_matrix['Position'] == 'WR']['%Drafted'].sum()
    te_ownership = big_matrix[big_matrix['Position'] == 'TE']['%Drafted'].sum()
       
    total_rb = rb_ownership + total_rb
    total_wr = wr_ownership + total_wr
    total_te = te_ownership + total_te
    
    big_big_matrix = big_big_matrix.append(big_matrix)

print(total_rb/24)
print(total_wr/24)
print(total_te/24)

big_big_matrix = big_big_matrix.drop(['Unnamed: 0','Unnamed: 0.1'], axis=1)

big_big_matrix_qb = big_big_matrix[big_big_matrix['Position'] == 'QB']
big_big_matrix_rb = big_big_matrix[big_big_matrix['Position'] == 'RB']
big_big_matrix_wr = big_big_matrix[big_big_matrix['Position'] == 'WR']
big_big_matrix_te = big_big_matrix[big_big_matrix['Position'] == 'TE']
big_big_matrix_dst = big_big_matrix[big_big_matrix['Position'] == 'DST']

big_big_matrix_qb.to_csv('big_matrix_qb.csv')
big_big_matrix_rb.to_csv('big_matrix_rb.csv')
big_big_matrix_wr.to_csv('big_matrix_wr.csv')
big_big_matrix_te.to_csv('big_matrix_te.csv')
big_big_matrix_dst.to_csv('big_matrix_dst.csv')
