
"""
Quicky script to scrape projections from fantasypros.com
"""

import requests
import pandas as pd
import csv
import os
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scoring_dict import create_dict
from sklearn.mixture import GaussianMixture

class Big_Matrix():
    
    def __init__(self, year, week, group_id, scoring, positions):
        pd.options.mode.chained_assignment = None
        self.week = week
        self.year = year
        self.group_id = group_id
        self.scoring = scoring
        self.positions = positions
        
        # Define path for files and create directory if it doesn't exist
        self.path = os.path.join(str(year), 'Week' + str(week))
        if not os.path.exists(self.path):
            os.mkdir(self.path)
           
    def fp_scrape(self):
        
        # Setup some parameters to scrape
        base_url = 'http://www.fantasypros.com/nfl/projections'
        week = self.week
        
        fp_df = []
        for position in self.positions:
        
            url = '%s/%s.php' % (base_url, position)
            params = {
                'max-yes': 'true',
                'min-yes': 'true',
                'scoring': 'STD',
                'week': week
            }
            text = requests.get(url, params=params).text
            
            if position != 'dst':
                df = pd.io.html.read_html(text,attrs={'id': 'data'}, header=1)[0]
                df['Team'] = df['Player'].apply(lambda x: x.split()[-2])
                df['Player'] = df['Player'].apply(lambda x: ' '.join(x.split()[0:2]))
                df['Player'] = df['Player'].str.replace('.', '')
            else:
                df = pd.io.html.read_html(text,attrs={'id': 'data'})[0]
                df['Player'] = df['Player'].apply(lambda x: ' '.join(x.split()[:-1]))
                df['Player'] = df['Player'].apply(lambda x: ' '.join(x.split()[-1:]))
            
            for column in df.columns.values:
                if column != 'Player' and column !='Team':
                    for i in range(0, len(df[column])):
                        string1 = df.loc[i, column]
                        dec1 = string1.find('.')
                        string2 = string1[:dec1+2]
                        string3 = string1[dec1+2:]
                        dec2 = string3.find('.')
                        string4 = string3[:dec2+2]
                        string5 = string3[dec2+2:]
                        
                        df.loc[i, column + '_MAX'] = float(string4)
                        df.loc[i, column + '_MIN'] = float(string5)
                        df.loc[i, column + '_MID'] = float(string2)
                    df = df.drop(column, axis=1)
                    
            df['Week'] = week
            df['Position'] = position.upper()
            
            path_1 = os.path.join(self.path, 'FantasyPros_Fantasy_Football_Projections_' + position.upper() + '_Week' + str(self.week) + '.csv')
            
            df.to_csv(path_1)
            fp_df.append(df)
            
            self.fp_df = fp_df
        
        return fp_df
        
    def score(self, scoring):
        
        # Define Scoring System
        pt_dict = create_dict(scoring)
        
        # Setup Min/Mid/Max list to loop through
        list = ['_MIN', '_MID', '_MAX']
        
        # Setup Blank List of Frames
        frames = []
        
        # Loop Through Positions
        for i, df in enumerate(self.fp_df):
            
            # Loop Through Min/Mid/Max Projections
            for sfx in list:
                
                if i == 0:
                    # QB: Calculate Draft King Points based on Projected Stats
                    bonus = (df.loc[:,'YDS' + sfx]*(pt_dict['PASSBONUS']/((1-pt_dict['BONUS_RAMP'])*pt_dict['PASSTHRESH'])) - pt_dict['PASSBONUS']/(1-pt_dict['BONUS_RAMP']) + pt_dict['PASSBONUS']).clip(0, pt_dict['PASSBONUS'])
                    df[scoring + sfx] = df.loc[:,'TDS' + sfx]*pt_dict['PASSTD'] + df.loc[:,'YDS' + sfx]*pt_dict['PASSYD'] + df.loc[:,'INTS' + sfx]*pt_dict['INT'] + df.loc[:,'YDS.1' + sfx]*pt_dict['RUSHYD'] + df.loc[:,'TDS.1' + sfx]*pt_dict['RUSHTD'] + df.loc[:,'FL' + sfx]*pt_dict['FL'] + bonus
            
                if i == 1:
                    # RB: Calculate Draft King Points based on Projected Stats
                    bonus = (df.loc[:,'YDS' + sfx]*(pt_dict['RUSHBONUS']/((1-pt_dict['BONUS_RAMP'])*pt_dict['RUSHTHRESH'])) - pt_dict['RUSHBONUS']/(1-pt_dict['BONUS_RAMP']) + pt_dict['RUSHBONUS']).clip(0, pt_dict['RUSHBONUS'])
                    df[scoring + sfx] = df.loc[:,'YDS' + sfx]*pt_dict['RUSHYD'] + df.loc[:,'TDS' + sfx]*pt_dict['RUSHTD'] + df.loc[:,'REC' + sfx]*pt_dict['REC'] + df.loc[:,'YDS.1' + sfx]*pt_dict['CATCHYD'] + df.loc[:,'TDS.1' + sfx]*pt_dict['CATCHTD'] + df.loc[:,'FL' + sfx]*pt_dict['FL'] + bonus
                
                if i == 2 or i ==3:
                    # WR & TE: Calculate Draft King Points based on Projected Stats
                    bonus = (df.loc[:,'YDS' + sfx]*(pt_dict['RECBONUS']/((1-pt_dict['BONUS_RAMP'])*pt_dict['RECTHRESH'])) - pt_dict['RECBONUS']/(1-pt_dict['BONUS_RAMP']) + pt_dict['RECBONUS']).clip(0, pt_dict['RECBONUS'])
                    df[scoring + sfx] = df.loc[:,'REC' + sfx]*pt_dict['REC'] + df.loc[:,'YDS' + sfx]*pt_dict['CATCHYD'] + df.loc[:,'TDS' + sfx]*pt_dict['CATCHTD'] + df.loc[:,'FL' + sfx]*pt_dict['FL'] + bonus
            
                if i == 4:
                    # DST: Calculate Draft King Points based on Projected Stats
                    points_func = interp1d(pt_dict['POINTS_AGAINST'], pt_dict['FANTASY_POINTS'], fill_value='extrapolate')
                    yards_func = interp1d(pt_dict['YARDS_AGAINST'], pt_dict['FANTASY_POINTS_2'], fill_value='extrapolate')
                    dst_bonus = points_func(df.loc[:, 'PA' + sfx])
                    dst_bonus_2 = yards_func(df.loc[:, 'YDS AGN' + sfx])
                    df[scoring + sfx] = df.loc[:,'SACK' + sfx]*pt_dict['SACK'] + df.loc[:,'INT' + sfx]*pt_dict['DEFINT'] + df.loc[:,'FR' + sfx]*pt_dict['FR'] + df.loc[:,'TD' + sfx]*pt_dict['DEFTD'] + df.loc[:,'SAFETY' + sfx]*pt_dict['SAFETY'] + dst_bonus + dst_bonus_2
            
            frames.append(df)

        self.fp_df = frames
        
        return self.fp_df
      
    def plot_ranking(self, df_in, list, ascending):
        
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
                df = df_in[i].sort_values(item + '_MID', ascending=ascending)
                df = df[df[item + '_MID'] > thresh].reset_index()
                
                rank, tier = rank_tier(8, item + '_MID', df, ascending)
                cmap = cm.get_cmap("plasma")
                colors = [cmap(k/8) for k in tier]
                
                index = -(df.index.values + 1)
                median = df[item + '_MID']
                low_error = df[item + '_MIN']
                high_error = df[item + '_MAX']
                plt.xlim([min(low_error)*.9, min(max(high_error), 1000/1.1)*1.1])  
                plt.xlabel('Projection')
                plt.yticks(index, df['Player'])
                ax.scatter(median, index, c = colors, label = tier)
                ax.hlines(index, low_error, high_error, colors = colors)

                fig.savefig(os.path.join(self.path, position.upper() + '_' + item + '.png'), bbox_inches = 'tight')
               
                
    def dk_scrape(self):
        
        path = os.path.join(self.path, 'DKSalaries_Week' + str(self.week) + '.csv')
        
        if not os.path.isfile(path):
            # URL Which Links to Export to CSV button on DK Website
            url = 'https://www.draftkings.com/lineup/getavailableplayerscsv?contestTypeId=21&draftGroupId=' + str(self.group_id)
            
            session=requests.Session()
            data=session.get(url).content.decode('utf-8').splitlines()
            dk_df = pd.DataFrame(csv.DictReader(data), dtype = 'float')
        
        else:
            # Read from existing CSV file
            dk_df = pd.read_csv(path)
            
        # Rename Columns to match Fantasy Pros for Data Merging
        dk_df.rename(columns={'Name':'Player'}, inplace=True)
        dk_df.rename(columns={'TeamAbbrev':'Team'}, inplace=True)
        dk_df['Team'] = dk_df['Team'].str.replace('JAX', 'JAC')
        
        # Remove name suffix (JR/SR/III etc)
        dk_df['Player'] = dk_df['Player'].apply(lambda x: ' '.join(x.split()[0:2]))
        dk_df['Player'] = dk_df['Player'].str.replace('.', '')
        dk_df['Player'] = dk_df['Player'].str.replace('WAS Football', 'Team')
        self.dk_df = dk_df
        
        # Output to CSV
        dk_df.to_csv(path)

        return dk_df
    
    def dk_merge(self):
        
        # Find players with salary assigned but no stat projections
        # This is to ensure there are no pairing issues - manual check is requried
        excluded_players = []
        excluded_salary = []
        excluded_position = []
    
        dk_df = self.dk_df
        frames = []
        
        # Set up Columns to Keep
        columns = ['Player', 'Team', 'Position', 'Salary', 'Name + ID', 'AvgPointsPerGame']
        
        for i in self.scoring:
            for j in ['_MIN', '_MID', '_MAX']:
                columns.append(i + j)
                
        # Merge Fantasy Pro Data With Draft Kings Data
        for i, position in enumerate(self.positions):
            
            df = self.fp_df[i]
            dk_df_small = self.dk_df[dk_df['Position'] == position.upper()].reset_index(drop=True)
            
            if position != 'dst':
                df = df.merge(dk_df, on=['Player', 'Team', 'Position'])
            else:
                df = df.merge(dk_df, on=['Player', 'Position'])
            
            df = df[columns]
            frames.append(df)
                        
            # Check for players with salary assigned but no stat projections for pairing issues
            # Doing this before filtering for value so guys with low projections don't get counted here
            for i in range (0,len(dk_df_small)):
                if True not in df['Player'].str.contains(dk_df_small.loc[i, 'Player']).values:
                    excluded_players.append(dk_df_small.loc[i, 'Player'])
                    excluded_salary.append(dk_df_small.loc[i, 'Salary'])
                    excluded_position.append(dk_df_small.loc[i, 'Position'])
        
        # Save Big Matrix
        self.big_matrix = frames

        # Turn excluded players into df, sort by salarh, and output to CSV for manual check
        # Most players with high salaries *should* be hurt
        # Be on the lookout for players with JR, SR, III or other suffixes
        excluded_df = pd.DataFrame({'Player': excluded_players, 'Salary': excluded_salary, 'Position': excluded_position})
        excluded_df = excluded_df.sort_values('Salary', ascending=False)
        excluded_df.to_csv(os.path.join(self.path, 'Excluded_Players_Week' + str(self.week) + '.csv')) 

    def value_tier(self):
        
        frames = []
        
        # Loop through Positions
        for i, position in enumerate(self.positions):
            
            # Initialize data structures
            df = self.big_matrix[i]
            vector = ['_MIN', '_MID', '_MAX']
            
            for j in range(0, len(vector)):
                df['Draft Kings Value' + vector[-j + 2]] = df['Salary']/df['Draft Kings' + vector[j]]
    
            # Filter Out Low Value Players
            df = df[df['Draft Kings Value_MID'] < 600]
            
            # Team Points Rank & Tier
            rank, tier = rank_tier(8, 'Draft Kings_MID', df, False)
            df['Draft Kings_MID_Rank'] = rank
            df['Draft Kings_MID_Tier'] = tier
            rank, tier = rank_tier(8, 'Draft Kings Value_MID', df, True)
            df['Draft Kings Value_MID_Rank'] = rank
            df['Draft Kings Value_MID_Tier'] = tier
            
            # Add additional columns to help with player classification
            df['Min_Tier'] = df[['Draft Kings_MID_Tier','Draft Kings Value_MID_Tier']].min(axis=1)
            df['Add_Tier'] = df['Draft Kings_MID_Tier'] + df['Draft Kings Value_MID_Tier']
            
            # Sort by value for final Output
            df = df.sort_values('Draft Kings Value_MID', ascending = True).reset_index(drop = True)
            
            # Append to rest of position dfs
            frames.append(df)
            
        # Spit out Big Matrix
        self.big_matrix = frames
        big_matrix = pd.concat(frames)
        big_matrix.to_csv(os.path.join(self.path, 'BigMatrix_Week' + str(self.week) + '.csv'), index = False)
        
def rank_tier(num_tiers, channel_name, df, ascending):
    df = df.copy()
    df['orig_index'] = df.index
    df = df.sort_values(by=[channel_name], ascending=ascending).reset_index()
    df['rank'] = df.index + 1    
    gmm = GaussianMixture(n_components=num_tiers)
    data = df[channel_name].to_numpy().reshape(-1, 1)
    gmm.fit(data)
    tiers = gmm.predict(data)
    unique = pd.unique(tiers)
    tier_dict = {}
    for i, value in enumerate(unique):
        tier_dict[value] = i + 1
    df['tier'] = [tier_dict.get(tier) for tier in tiers]
    df = df.sort_values('orig_index')
    rank = df['rank'].values
    tier = df['tier'].values
    
    return rank, tier