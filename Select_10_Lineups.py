def select_ten_lineups(week, all_lineups, value):
    import pandas as pd
    import numpy as np
    from DK_Data_Import import dk_data_import

    "Create 10 lineup dataframe"
    opt_lineup = pd.DataFrame(np.random.randint(low=0, high=10, size=(10,9)),columns=['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE', 'Flex', 'DST'])

    "Select Optimal Lineups Randomly from Remaining List -- Adjust 'value' to get different lineup selection"
    num_lineups = len(all_lineups)
    multiplier = int(num_lineups/value)

    for i in range (0,10):
        opt_lineup.loc[i] = all_lineups.loc[multiplier*i]

    "Turn Optimal Lineups into Draft Kings ID Format"
    dk_lineups_upload = pd.DataFrame(np.random.randint(low=0, high=10, size=(10,9)),columns=['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE', 'Flex', 'DST'])

    "Import in Draft Kings Data"
    dk_df = dk_data_import(week, week + '/Ownership_' + week + '_Guess.csv', 1)

    for i in range (0,10):
        dk_lineups_upload.loc[i,'QB'] = dk_df.loc[dk_df[dk_df['Player'] == opt_lineup.loc[i, 'QB']].index.values[0], 'Name + ID']
        dk_lineups_upload.loc[i,'RB1'] = dk_df.loc[dk_df[dk_df['Player'] == opt_lineup.loc[i, 'RB1']].index.values[0], 'Name + ID']
        dk_lineups_upload.loc[i,'RB2'] = dk_df.loc[dk_df[dk_df['Player'] == opt_lineup.loc[i, 'RB2']].index.values[0], 'Name + ID']
        dk_lineups_upload.loc[i,'WR1'] = dk_df.loc[dk_df[dk_df['Player'] == opt_lineup.loc[i, 'WR1']].index.values[0], 'Name + ID']
        dk_lineups_upload.loc[i,'WR2'] = dk_df.loc[dk_df[dk_df['Player'] == opt_lineup.loc[i, 'WR2']].index.values[0], 'Name + ID']
        dk_lineups_upload.loc[i,'WR3'] = dk_df.loc[dk_df[dk_df['Player'] == opt_lineup.loc[i, 'WR3']].index.values[0], 'Name + ID']
        dk_lineups_upload.loc[i,'TE'] = dk_df.loc[dk_df[dk_df['Player'] == opt_lineup.loc[i, 'TE']].index.values[0], 'Name + ID']
        dk_lineups_upload.loc[i,'Flex'] = dk_df.loc[dk_df[dk_df['Player'] == opt_lineup.loc[i, 'Flex']].index.values[0], 'Name + ID']
        dk_lineups_upload.loc[i,'DST'] = dk_df.loc[dk_df[dk_df['Player'] == opt_lineup.loc[i, 'DST']].index.values[0], 'Name + ID']
    
    return dk_lineups_upload
