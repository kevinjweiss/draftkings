def create_ownership_guess(year, week):
    import pandas as pd
    from DK_Data_Import import dk_data_import
    import numpy as np
    
    "Initiate player List"
    player_list = []
    
    "Import In Big Matrix Data from Big Matrix Generator"
    big_matrix_data = pd.read_csv(year + '/' + week + '\BigMatrix_' + week + '.csv')
    big_matrix = pd.DataFrame(data=big_matrix_data)

    qb_df_small = big_matrix[big_matrix['Position'] == 'QB'].reset_index(drop = True)
    rb_df_small = big_matrix[big_matrix['Position'] == 'RB'].reset_index(drop = True)
    wr_df_small = big_matrix[big_matrix['Position'] == 'WR'].reset_index(drop = True)
    te_df_small = big_matrix[big_matrix['Position'] == 'TE'].reset_index(drop = True)
    dst_df_small = big_matrix[big_matrix['Position'] == 'DST'].reset_index(drop = True)

    "Filter out QBs who will not be owned"
    qbs = np.array([qb_df_small[qb_df_small['Points Rank'] == 1]['Player'].values, 
                   qb_df_small[qb_df_small['Value Rank'] == 1]['Player'].values,
                   qb_df_small[qb_df_small['Value Rank'] == 2]['Player'].values])

    rbs = np.array([rb_df_small[rb_df_small['Points Rank'] == 1]['Player'].values, 
                rb_df_small[rb_df_small['Points Rank'] == 2]['Player'].values,     
                rb_df_small[rb_df_small['Points Rank'] == 3]['Player'].values,     
                rb_df_small[rb_df_small['Points Rank'] == 4]['Player'].values,                  
                rb_df_small[rb_df_small['Value Rank'] == 1]['Player'].values,
                rb_df_small[rb_df_small['Value Rank'] == 2]['Player'].values,
                rb_df_small[rb_df_small['Value Rank'] == 3]['Player'].values,
                rb_df_small[rb_df_small['Value Rank'] == 4]['Player'].values])
    
    wrs = np.array([wr_df_small[wr_df_small['Points Rank'] == 1]['Player'].values, 
                wr_df_small[wr_df_small['Points Rank'] == 2]['Player'].values,     
                wr_df_small[wr_df_small['Points Rank'] == 3]['Player'].values,     
                wr_df_small[wr_df_small['Points Rank'] == 4]['Player'].values,                  
                wr_df_small[wr_df_small['Value Rank'] == 1]['Player'].values,
                wr_df_small[wr_df_small['Value Rank'] == 2]['Player'].values,
                wr_df_small[wr_df_small['Value Rank'] == 3]['Player'].values,
                wr_df_small[wr_df_small['Value Rank'] == 4]['Player'].values])
    
    tes = np.array([te_df_small[te_df_small['Value Rank'] == 1]['Player'].values, 
            te_df_small[te_df_small['Value Rank'] == 2]['Player'].values,
            te_df_small[te_df_small['Value Rank'] == 3]['Player'].values])
    
    dsts = np.array([dst_df_small[dst_df_small['Value Rank'] == 1]['Player'].values, 
        dst_df_small[dst_df_small['Value Rank'] == 2]['Player'].values])
    
    players_1 = np.append(qbs, rbs)
    players_2 = np.append(players_1, wrs)
    players_3 = np.append(tes, dsts)
    players = np.append(players_2, players_3)
    
    players_df = pd.DataFrame(data = players, columns = ['Player'])
    players_df.drop_duplicates(inplace = True)
    players_df.to_csv(year + '/' + week + '\Ownership_' + week + '_Guess_Auto.csv')