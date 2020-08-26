from Big_Matrix_Generator import big_matrix_generator

from Post_Game_Analysis import post_game_analysis
from DK_Optimizer_Ownership_StudLock import dk_optimizer_ownership_studlock
from Create_Ownership_Guess import create_ownership_guess
from Big_Matrix_Process_Results import big_matrix_process_results

year = '2018_Test'
weeks = ['Week6', 'Week7', 'Week8', 'Week9', 'Week10', 'Week13', 'Week14', 'Week15']

balance = 100

for week in weeks:
    print(week)
    big_matrix_generator(year, week)
    create_ownership_guess(year, week)
    dk_optimizer_ownership_studlock(year, week, year + '/' + week + '/Ownership_' + week + '_Guess_Auto.csv')
    big_matrix_process_results(year, year + '/' + week + '/ContestStandings_' + week + '.csv', year + '/' + week + '/BigMatrix_' + week + '.csv', week)
    profit = post_game_analysis(year, year + '/' + week + '/ContestStandings_' + week + '.csv', year + '/' + week + '/All_Lineups_OwnershipStud_' + week + '.csv', week)
    balance = balance + profit
    print(balance)
    
year = '2019_Test'
weeks = ['Week1', 'Week2', 'Week3', 'Week4', 'Week5', 'Week6',
        'Week7', 'Week8', 'Week9', 'Week10', 'Week11', 'Week12',
        'Week13', 'Week14', 'Week15', 'Week16']

for week in weeks:
    print(week)
    big_matrix_generator(year, week)
    create_ownership_guess(year, week)
    dk_optimizer_ownership_studlock(year, week, year + '/' + week + '/Ownership_' + week + '_Guess_Auto.csv')
    big_matrix_process_results(year, year + '/' + week + '/ContestStandings_' + week + '.csv', year + '/' + week + '/BigMatrix_' + week + '.csv', week)
    profit = post_game_analysis(year, year + '/' + week + '/ContestStandings_' + week + '.csv', year + '/' + week + '/All_Lineups_OwnershipStud_' + week + '.csv', week)
    balance = balance + profit
    print(balance)
    
