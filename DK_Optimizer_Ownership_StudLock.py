def dk_optimizer_ownership_studlock(year, week, player_target_file):
    import pandas as pd
    from Select_10_Lineups import select_ten_lineups
    from Create_All_Lineups import create_all_lineups
    from DK_Data_Import import dk_data_import
    
    "Minimum Lineup Point Threshold"
    point_thresh = 140

    "Value for Randomly picking 10 lineups: Must be bigger than 10 - Alter if not happy with randomly selected lineups"
    value = 25

    "Import In Big Matrix Data from Big Matrix Generator"
    big_matrix_data = pd.read_csv(year + '/' + week + '\BigMatrix_' + week + '.csv')
    big_matrix = pd.DataFrame(data=big_matrix_data)

    qb_df_small = big_matrix[big_matrix['Position'] == 'QB']
    rb_df_small = big_matrix[big_matrix['Position'] == 'RB']
    wr_df_small = big_matrix[big_matrix['Position'] == 'WR']
    te_df_small = big_matrix[big_matrix['Position'] == 'TE']
    dst_df_small = big_matrix[big_matrix['Position'] == 'DST']

    "Import Player Target CSV Input"
    player_target = dk_data_import(year, week, player_target_file, 2)
    
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
    all_lineups = create_all_lineups(qb_df_small, rb_df_small, wr_df_small, te_df_small, dst_df_small, point_thresh)

    "Sort by Points to get Studs"
    rb_df_studs = rb_df_small.drop(rb_df_small[rb_df_small.DK_Points < 24].index)
    rb_df_studs = rb_df_studs['Player']
    wr_df_studs = wr_df_small.drop(wr_df_small[wr_df_small.DK_Points < 24].index)
    wr_df_studs = wr_df_studs['Player']

    if (len(rb_df_studs)>0):
        all_lineups_new = pd.concat([all_lineups.drop(all_lineups[~all_lineups.RB1.isin(rb_df_studs)].index),
                                 all_lineups.drop(all_lineups[~all_lineups.RB2.isin(rb_df_studs)].index),
                                 all_lineups.drop(all_lineups[~all_lineups.Flex.isin(rb_df_studs)].index)])
        if len(all_lineups_new) > 10:
            all_lineups = all_lineups_new
        
    if(len(wr_df_studs)>0):
        all_lineups_new = pd.concat([all_lineups.drop(all_lineups[~all_lineups.WR1.isin(wr_df_studs)].index),
                                  all_lineups.drop(all_lineups[~all_lineups.WR2.isin(wr_df_studs)].index),
                                  all_lineups.drop(all_lineups[~all_lineups.WR3.isin(wr_df_studs)].index),
                                  all_lineups.drop(all_lineups[~all_lineups.Flex.isin(wr_df_studs)].index)])
        if len(all_lineups_new) > 10:
            all_lineups = all_lineups_new
        
    all_lineups.sort_values(by=['Points'], inplace=True, ascending=False)
    all_lineups = all_lineups.drop_duplicates(inplace=False)
    all_lineups = all_lineups.reset_index(drop=True)
    all_lineups.to_csv(year + '/' + week + '\All_Lineups_OwnershipStud_' + week + '.csv')

    "Select 10 Lineups"
    dk_lineups_upload = select_ten_lineups(year, week, all_lineups, value)
    dk_lineups_upload.to_csv(year + '/' + week + '\Ten_Lineup_Upload_File_OwnershipStud_' + week + '.csv', index=False)