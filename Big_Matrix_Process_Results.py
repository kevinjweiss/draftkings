def big_matrix_process_results(year, results, big_matrix, week):

    import pandas as pd
    import numpy as np
    import seaborn as sns
    import matplotlib.pyplot as plt
    from DK_Data_Import import dk_data_import
    
    'Read in Result and Lineup Files'
    result_data = dk_data_import(year, week, results, 2)
    big_matrix = pd.read_csv(big_matrix)

    'Initialize Point Vectors'
    dk_competitor_points = result_data['Points']
    python_lineup_points = []
    
    big_matrix['FPTS'] = 0
    big_matrix['%Drafted'] = 0
    big_matrix['Real_Value'] = 0

    for i in range(len(big_matrix)):
        player = big_matrix.loc[i, 'Player']
        index = result_data.index[result_data['Player'] == player].values
        
        points = result_data.loc[index, 'FPTS'].values
        if points.size ==0:
            points = 0
        big_matrix.loc[i, 'FPTS'] = points
        
        ownership = result_data.loc[index, '%Drafted'].values
        if ownership.size ==0:
            ownership = 0
        else:
            ownership = float(np.asscalar(ownership).rstrip("%"))
        big_matrix.loc[i, '%Drafted'] = ownership
        
        if points>1:
            big_matrix.loc[i, 'Real_Value'] = big_matrix.loc[i, 'Salary']/points
        else:
            big_matrix.loc[i, 'Real_Value'] = 9999
        
    big_matrix.to_csv(year + '/' + week + '/BigMatrix_' + week + '_Processed.csv')
