def import_target_players(week, player_target_file):
    import pandas as pd
    import numpy as np
    from itertools import combinations
    from Select_10_Lineups import select_ten_lineups
    from Create_All_Lineups import create_all_lineups

    "Import In Big Matrix Data from Big Matrix Generator"
    big_matrix_data = pd.read_csv('BigMatrix_' + week + '.csv')
    big_matrix = pd.DataFrame(data=big_matrix_data)

    qb_df_small = big_matrix[big_matrix['Position'] == 'QB']
    rb_df_small = big_matrix[big_matrix['Position'] == 'RB']
    wr_df_small = big_matrix[big_matrix['Position'] == 'WR']
    te_df_small = big_matrix[big_matrix['Position'] == 'TE']
    dst_df_small = big_matrix[big_matrix['Position'] == 'DST']

    "Import Player Target CSV Input"
    player_target_data = pd.read_csv(player_target_file)
    player_target = pd.DataFrame(data=player_target_data)

    "Rename Players with Name Suffixes preventing data matching"
    player_target['Player'] = player_target['Player'].str.replace(' III', '')
    player_target['Player'] = player_target['Player'].str.replace(' II', '')
    player_target['Player'] = player_target['Player'].str.replace(' Jr.', '')
    player_target['Player'] = player_target['Player'].str.replace(' Sr.', '')
    player_target['Player'] = player_target['Player'].str.replace('Will Fuller V', 'Will Fuller')
    player_target['Player'] = player_target['Player'].str.replace('Odell Beckham', 'Odell Beckham Jr.')
    player_target['Player'] = player_target['Player'].str.replace('Willie Snead IV', 'Willie Snead')
    player_target['Player'] = player_target['Player'].str.replace('DJ Chark Jr.', 'D.J. Chark')
    player_target['Player'] = player_target['Player'].str.replace('DK Metcalf', 'D.K. Metcalf')
    
    "Rename Defenses to Match Fantasy Pros Format"
    player_target['Player'] = player_target['Player'].str.replace('Steelers ', 'Pittsburgh Steelers', )
    player_target['Player'] = player_target['Player'].str.replace('Jaguars ', 'Jacksonville Jaguars', )
    player_target['Player'] = player_target['Player'].str.replace('Lions ', 'Detroit Lions')
    player_target['Player'] = player_target['Player'].str.replace('Ravens ', 'Baltimore Ravens')
    player_target['Player'] = player_target['Player'].str.replace('Titans ', 'Tennessee Titans')
    player_target['Player'] = player_target['Player'].str.replace('Vikings ', 'Minnesota Vikings')
    player_target['Player'] = player_target['Player'].str.replace('Seahawks ', 'Seattle Seahawks')
    player_target['Player'] = player_target['Player'].str.replace('Redskins ', 'Washington Redskins')
    player_target['Player'] = player_target['Player'].str.replace('Saints ', 'New Orleans Saints')
    player_target['Player'] = player_target['Player'].str.replace('Packers ', 'Green Bay Packers')
    player_target['Player'] = player_target['Player'].str.replace('Patriots ', 'New England Patriots')
    player_target['Player'] = player_target['Player'].str.replace('Rams ', 'Los Angeles Rams')
    player_target['Player'] = player_target['Player'].str.replace('Chargers ', 'Los Angeles Chargers')
    player_target['Player'] = player_target['Player'].str.replace('Bengals ', 'Cincinnati Bengals')
    player_target['Player'] = player_target['Player'].str.replace('Bears ', 'Chicago Bears')
    player_target['Player'] = player_target['Player'].str.replace('Jets ', 'New York Jets')
    player_target['Player'] = player_target['Player'].str.replace('Broncos ', 'Denver Broncos')
    player_target['Player'] = player_target['Player'].str.replace('Cowboys ', 'Dallas Cowboys')
    player_target['Player'] = player_target['Player'].str.replace('Panthers ', 'Carolina Panthers')
    player_target['Player'] = player_target['Player'].str.replace('Cardinals ', 'Arizona Cardinals')
    player_target['Player'] = player_target['Player'].str.replace('Dolphins ', 'Miami Dolphins')
    player_target['Player'] = player_target['Player'].str.replace('Falcons ', 'Atlanta Falcons')
    player_target['Player'] = player_target['Player'].str.replace('Bills ', 'Buffalo Bills')
    player_target['Player'] = player_target['Player'].str.replace('Chiefs ', 'Kansas City Chiefs')
    player_target['Player'] = player_target['Player'].str.replace('Eagles ', 'Philadelphia Eagles')
    player_target['Player'] = player_target['Player'].str.replace('Giants ', 'New York Giants')
    player_target['Player'] = player_target['Player'].str.replace('Colts ', 'Indianapolis Colts')
    player_target['Player'] = player_target['Player'].str.replace('Texans ', 'Houston Texans')
    player_target['Player'] = player_target['Player'].str.replace('49ers ', 'San Francisco 49ers')
    player_target['Player'] = player_target['Player'].str.replace('Buccaneers ', 'Tampa Bay Buccaneers')
    player_target['Player'] = player_target['Player'].str.replace('Raiders ', 'Oakland Raiders')
    player_target['Player'] = player_target['Player'].str.replace('Browns ', 'Cleveland Browns')

    "Drop all but targeted players from matrix of players"
    qb_df_small = qb_df_small[qb_df_small['Player'].isin(player_target['Player'])]
    qb_df_small = qb_df_small.reset_index(drop=True)
    rb_df_small = rb_df_small[rb_df_small['Player'].isin(player_target['Player'])]
    rb_df_small = rb_df_small.reset_index(drop=True)
    wr_df_small = wr_df_small[wr_df_small['Player'].isin(player_target['Player'])]
    wr_df_small = wr_df_small.reset_index(drop=True)
    te_df_small = te_df_small[te_df_small['Player'].isin(player_target['Player'])]
    te_df_small = te_df_small.reset_index(drop=True)
    dst_df_small = dst_df_small[dst_df_small['Player'].isin(player_target['Player'])]
    dst_df_small = dst_df_small.reset_index(drop=True)

    "Create All Possible Lineup Combinations"
    all_lineups = create_all_lineups(qb_df_small, rb_df_small, wr_df_small, te_df_small, dst_df_small)
    all_lineups.to_csv('All_Lineups_Ownership_' + week + '.csv')

    "Select 10 Lineups"
    dk_lineups_upload = select_ten_lineups(week, all_lineups)
    dk_lineups_upload.to_csv('10_Lineup_Upload_File_Ownership_' + week + '.csv')