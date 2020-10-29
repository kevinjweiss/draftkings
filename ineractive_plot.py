# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 15:33:43 2020

@author: queis
"""

import pandas as pd
import matplotlib.pyplot as plt
from big_matrix import rank_tier
import matplotlib.cm as cm
from matplotlib.widgets import RadioButtons

df = pd.read_csv('2020/Week7/BigMatrix_Week7.csv')
position = 'WR'
item = 'Draft Kings'

# Loop through Positions
if position == 'QB':
    thresh = 15
if position == 'RB':
    thresh - 8
if position == 'WR':
    thresh = 8
if position == 'TE':
    thresh = 5
if position == 'DST':
    thresh = 5
   
# Loop through Scoring Systems
with plt.style.context('ggplot'):
    fig, ax = plt.subplots(figsize=(12, 12))
plt.title(position.upper())

radio = RadioButtons(ax, ('QB', 'RB', 'WR', 'TE', 'DST'))

df_pos = df[df['Position'] == position]
df_pos = df_pos.sort_values(item + '_MID', ascending=False)
df_pos = df_pos[df_pos[item + '_MID'] > thresh].reset_index()

rank, tier = rank_tier(8, item + '_MID', df_pos, False)
cmap = cm.get_cmap("plasma")
colors = [cmap(k/8) for k in tier]

index = -(df_pos.index.values + 1)
median = df_pos[item + '_MID']
low_error = df_pos[item + '_MIN']
high_error = df_pos[item + '_MAX']
plt.xlim([min(low_error)*.9, min(max(high_error), 1000/1.1)*1.1])  
plt.xlabel('Projection')
plt.yticks(index, df_pos['Player'])
ax.scatter(median, index, c = colors, label = tier)
ax.hlines(index, low_error, high_error, colors = colors)