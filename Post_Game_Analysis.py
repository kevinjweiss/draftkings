def post_game_analysis(year, results, lineups, week):

    import pandas as pd
    import seaborn as sns
    import matplotlib.pyplot as plt
    from DK_Data_Import import dk_data_import
    
    'Read in Result and Lineup Files'
    result_data = dk_data_import(year, week, results, 2)
    all_lineups = pd.read_csv(lineups)

    'Initialize Point Vectors'
    dk_competitor_points = result_data['Points']
    python_lineup_points = []
    counter = 0

    'Calculate Winning Point Threshold'
    temp_df = result_data[result_data['Rank']>.435*len(dk_competitor_points)]
    temp_df = temp_df.reset_index(drop=True)
    point_thresh = temp_df.loc[0, 'Points']
    
    "Create Result Data DF by Position"
    qb = result_data.rename(columns={'Player':'QB'})
    rb1 = result_data.rename(columns={'Player':'RB1'})
    rb2 = result_data.rename(columns={'Player':'RB2'})
    wr1 = result_data.rename(columns={'Player':'WR1'})
    wr2 = result_data.rename(columns={'Player':'WR2'})
    wr3 = result_data.rename(columns={'Player':'WR3'})
    te = result_data.rename(columns={'Player':'TE'})
    flex = result_data.rename(columns={'Player':'Flex'})
    dst = result_data.rename(columns={'Player':'DST'})

    qb_points = all_lineups.merge(qb, on='QB', how='left')
    rb1_points = all_lineups.merge(rb1, on='RB1', how='left')
    rb2_points = all_lineups.merge(rb2, on='RB2', how='left')
    wr1_points = all_lineups.merge(wr1, on='WR1', how='left')
    wr2_points = all_lineups.merge(wr2, on='WR2', how='left')
    wr3_points = all_lineups.merge(wr3, on='WR3', how='left')
    te_points = all_lineups.merge(te, on='TE', how='left')
    flex_points = all_lineups.merge(flex, on='Flex', how='left')
    dst_points = all_lineups.merge(dst, on='DST', how='left')
    
    python_lineup_points = qb_points['FPTS'].values + rb1_points['FPTS'].values + rb2_points['FPTS'].values + wr1_points['FPTS'].values + wr2_points['FPTS'].values \
                 + wr3_points['FPTS'].values + te_points['FPTS'].values + flex_points['FPTS'].values + dst_points['FPTS'].values
    
    python_lineup_ownership = qb_points['%Drafted'].values + rb1_points['%Drafted'].values + rb2_points['%Drafted'].values + wr1_points['%Drafted'].values + wr2_points['%Drafted'].values \
                 + wr3_points['%Drafted'].values + te_points['%Drafted'].values + flex_points['%Drafted'].values + dst_points['%Drafted'].values
    
    all_lineups = all_lineups.assign(Actual_Points = python_lineup_points)
    all_lineups = all_lineups.assign(Ownership = python_lineup_ownership)
    
    for i in range (0,len(python_lineup_points)):
        if python_lineup_points[i] > point_thresh:
            counter = counter + 1

    all_lineups.to_csv(year + '/' + week + '/All_Lineups_' + week + '_Processed.csv')
    
    win_percent = counter*100/len(python_lineup_points)
    profit = win_percent - 50

    plt.figure(1)
    sns.distplot(python_lineup_points)
    sns.distplot(dk_competitor_points)
    plt.show()

    return profit
