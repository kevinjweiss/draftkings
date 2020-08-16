def big_matrix_generator(week):
    import pandas as pd
    from DK_Data_Import import dk_data_import

    "Import Draft Kings Data"
    dk_df = dk_data_import(week, week + '/Ownership_' + week + '_Guess.csv', 1)

    "Import QB Fantasy Pro Data and Merge in DK Salary"
    qb_data = pd.read_csv(week + '/FantasyPros_Fantasy_Football_Projections_QB_' + week + '.csv')
    qb_df = pd.DataFrame(data = qb_data)
    qb_df = qb_df.merge(dk_df,on=['Player', 'Team'])

    "Import RB Fantasy Pro Data and Merge in DK Salary"
    rb_data = pd.read_csv(week + '/FantasyPros_Fantasy_Football_Projections_RB_' + week + '.csv')
    rb_df = pd.DataFrame(data = rb_data)
    rb_df = rb_df.merge(dk_df,on=['Player', 'Team'])

    "Import WR Fantasy Pro Data and Merge in DK Salary"
    wr_data = pd.read_csv(week + '/FantasyPros_Fantasy_Football_Projections_WR_' + week + '.csv')
    wr_df = pd.DataFrame(data = wr_data)
    wr_df = wr_df.merge(dk_df,on=['Player', 'Team'])

    "Import TE Fantasy Pro Data and Merge in DK Salary"
    te_data = pd.read_csv(week + '/FantasyPros_Fantasy_Football_Projections_TE_' + week + '.csv')
    te_df = pd.DataFrame(data = te_data)
    te_df = te_df.merge(dk_df,on=['Player', 'Team'])

    "Import DEF Fantasy Pro Data and Merge in DK Salary"
    dst_data = pd.read_csv(week + '/FantasyPros_Fantasy_Football_Projections_DST_' + week + '.csv')
    dst_df = pd.DataFrame(data = dst_data)
    dst_df = dst_df.merge(dk_df,on=['Player'])

    "Draft King Scoring"
    PASSTD = 4
    PASSYD = 0.04
    PASSTHRESH = 300
    PASSBONUS = 3
    INT = -1
    RUSHTD = 6
    RUSHYD = 0.1
    RUSHTHRESH = 100
    RUSHBONUS = 3
    REC = 1
    CATCHTD = 6
    CATCHYD = 0.1
    RECTHRESH = 100
    RECBONUS = 3
    FL = -1
    SACK = 1
    DEFINT = 2
    FR = 2
    DEFTD = 6
    SAFETY = 2

    "QB: Calculate Draft King Points based on Projected Stats"
    qb_dk_points = qb_df.loc[:,'TDS']*PASSTD + qb_df.loc[:,'YDS']*PASSYD + qb_df.loc[:,'INTS']*INT + qb_df.loc[:,'YDS.1']*RUSHYD + qb_df.loc[:,'TDS.1']*RUSHTD + qb_df.loc[:,'FL']*FL
    qb_df = qb_df.assign(DK_Points = qb_dk_points)

    "QB: Bonus Points ramping up from 70% bonus threshold"
    for x in range(len(qb_dk_points)):
        if qb_df.loc[x,'YDS']>PASSTHRESH:
            qb_df.ix[x,'DK_Points'] = qb_df.ix[x, 'DK_Points'] + PASSBONUS
        elif qb_df.loc[x,'YDS']>PASSTHRESH*.9:
            qb_df.ix[x, 'DK_Points'] = qb_df.ix[x, 'DK_Points'] + PASSBONUS*.66
        elif qb_df.loc[x,'YDS']>PASSTHRESH*.8:
            qb_df.ix[x, 'DK_Points'] = qb_df.ix[x, 'DK_Points'] + PASSBONUS*.33

    "QB: Calculate Value"
    qb_dk_value = qb_df['Salary']/qb_df['DK_Points']
    qb_df = qb_df.assign(DK_Value = qb_dk_value)

    "RB: Calculate Draft King Points based on Projected Stats"
    rb_dk_points = rb_df.loc[:,'YDS']*RUSHYD + rb_df.loc[:,'TDS']*RUSHTD + rb_df.loc[:,'REC']*REC + rb_df.loc[:,'YDS.1']*CATCHYD + rb_df.loc[:,'TDS.1']*CATCHTD + rb_df.loc[:,'FL']*FL
    rb_df = rb_df.assign(DK_Points = rb_dk_points)

    "RB: Bonus Points ramping up from 80% bonus threshold"
    for x in range(len(rb_dk_points)):
        if rb_df.loc[x,'YDS']>RUSHTHRESH:
            rb_df.ix[x,'DK_Points'] = rb_df.ix[x, 'DK_Points'] + RUSHBONUS
        elif rb_df.loc[x,'YDS']>RUSHTHRESH*.9:
            rb_df.ix[x, 'DK_Points'] = rb_df.ix[x, 'DK_Points'] + RUSHBONUS*.66
        elif rb_df.loc[x,'YDS']>RUSHTHRESH*.8:
            rb_df.ix[x, 'DK_Points'] = rb_df.ix[x, 'DK_Points'] + RUSHBONUS*.33

    "RB: Calculate Value"
    rb_dk_value = rb_df['Salary']/rb_df['DK_Points']
    rb_df = rb_df.assign(DK_Value = rb_dk_value)

    "WR: Calculate Draft King Points based on Projected Stats"
    wr_dk_points = wr_df.loc[:,'REC']*REC + wr_df.loc[:,'YDS']*CATCHYD + wr_df.loc[:,'TDS']*CATCHTD + wr_df.loc[:,'FL']*FL
    wr_df = wr_df.assign(DK_Points = wr_dk_points)

    "WR: Bonus Points ramping up from 80% bonus threshold"
    for x in range(len(wr_dk_points)):
        if wr_df.loc[x,'YDS']>RECTHRESH:
            wr_df.ix[x,'DK_Points'] = wr_df.ix[x, 'DK_Points'] + RECBONUS
        elif wr_df.loc[x,'YDS']>RECTHRESH*.9:
            wr_df.ix[x, 'DK_Points'] = wr_df.ix[x, 'DK_Points'] + RECBONUS*.66
        elif wr_df.loc[x,'YDS']>RECTHRESH*.8:
            wr_df.ix[x, 'DK_Points'] = wr_df.ix[x, 'DK_Points'] + RECBONUS*.33

    "WR: Calculate Value"
    wr_dk_value = wr_df['Salary']/wr_df['DK_Points']
    wr_df = wr_df.assign(DK_Value = wr_dk_value)

    "TE: Calculate Draft King Points based on Projected Stats"
    te_dk_points = te_df.loc[:,'REC']*REC + te_df.loc[:,'YDS']*CATCHYD + te_df.loc[:,'TDS']*CATCHTD + te_df.loc[:,'FL']*FL
    te_df = te_df.assign(DK_Points = te_dk_points)

    "TE: Bonus Points ramping up from 80% bonus threshold"
    for x in range(len(te_dk_points)):
        if te_df.loc[x,'YDS']>RECTHRESH:
            te_df.ix[x,'DK_Points'] = te_df.ix[x, 'DK_Points'] + RECBONUS
        elif te_df.loc[x,'YDS']>RECTHRESH*.9:
            te_df.ix[x, 'DK_Points'] = te_df.ix[x, 'DK_Points'] + RECBONUS*.66
        elif te_df.loc[x,'YDS']>RECTHRESH*.8:
            te_df.ix[x, 'DK_Points'] = te_df.ix[x, 'DK_Points'] + RECBONUS*.33

    "TE: Calculate Value"
    te_dk_value = te_df['Salary']/te_df['DK_Points']
    te_df = te_df.assign(DK_Value = te_dk_value)

    "DST: Calculate Draft King Points based on Projected Stats"
    dst_dk_points = dst_df.loc[:,'SACK']*SACK + dst_df.loc[:,'INT']*DEFINT + dst_df.loc[:,'FR']*FR + dst_df.loc[:,'TD']*DEFTD + dst_df.loc[:,'SAFETY']*SAFETY
    dst_df = dst_df.assign(DK_Points = dst_dk_points)

    "DST: Points Allowed Draft Kings Logic"
    for x in range(len(dst_dk_points)):
        if dst_df.loc[x, 'PA']>34:
            dst_df.ix[x,'DK_Points'] = dst_df.ix[x, 'DK_Points'] - 4
        elif dst_df.loc[x, 'PA'] > 27:
            dst_df.ix[x, 'DK_Points'] = dst_df.ix[x, 'DK_Points'] - 1
        elif dst_df.loc[x, 'PA'] > 20:
            dst_df.ix[x, 'DK_Points'] = dst_df.ix[x, 'DK_Points'] + 0
        elif dst_df.loc[x, 'PA'] > 13:
            dst_df.ix[x, 'DK_Points'] = dst_df.ix[x, 'DK_Points'] + 1
        elif dst_df.loc[x, 'PA'] > 7:
            dst_df.ix[x, 'DK_Points'] = dst_df.ix[x, 'DK_Points'] + 4
        elif dst_df.loc[x, 'PA'] > 0:
            dst_df.ix[x, 'DK_Points'] = dst_df.ix[x, 'DK_Points'] + 7

    "DST: Calculate Value"
    dst_dk_value = dst_df['Salary']/dst_df['DK_Points']
    dst_df = dst_df.assign(DK_Value = dst_dk_value)

    "Shorten Dataframes to useful columns"
    qb_df_small = qb_df[['Player', 'Position', 'Salary', 'DK_Points', 'DK_Value']].sort_values(by=['DK_Value']).reset_index(drop=True)
    rb_df_small = rb_df[['Player', 'Position','Salary', 'DK_Points', 'DK_Value']].sort_values(by=['DK_Value']).reset_index(drop=True)
    wr_df_small = wr_df[['Player', 'Position','Salary', 'DK_Points', 'DK_Value']].sort_values(by=['DK_Value']).reset_index(drop=True)
    te_df_small = te_df[['Player', 'Position','Salary', 'DK_Points', 'DK_Value']].sort_values(by=['DK_Value']).reset_index(drop=True)
    dst_df_small = dst_df[['Player', 'Position','Salary', 'DK_Points', 'DK_Value']].sort_values(by=['DK_Value']).reset_index(drop=True)

    "Merge Data Frames into big matrix for output"
    merge = [qb_df_small, rb_df_small, wr_df_small, te_df_small, dst_df_small]
    big_matrix = pd.concat(merge)
    big_matrix = big_matrix.reset_index(drop=True)

    "Compile list on DK Salary but not being analyzed and export to CSV - This list should be inactivies and injured players only"
    excluded_players = []
    excluded_salary = []

    for i in range (0,len(dk_df)):
        if True not in big_matrix['Player'].str.contains(dk_df.loc[i, 'Player']).values:
            excluded_players.append(dk_df.loc[i, 'Player'])
            excluded_salary.append(dk_df.loc[i, 'Salary'])

    excluded_df = pd.DataFrame({'Player': excluded_players, 'Salary': excluded_salary})
    excluded_df.to_csv(week + '\Excluded_Players_' + week + '.csv')

    "Write to CSV and eliminate low scoring players"
    big_matrix = big_matrix.drop(big_matrix[big_matrix.DK_Points < 5].index)
    big_matrix = big_matrix.reset_index(drop=True)
    big_matrix.to_csv(week + '\BigMatrix_' + week + '.csv')