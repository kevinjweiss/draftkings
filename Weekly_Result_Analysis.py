from Big_Matrix_Generator import big_matrix_generator

from Post_Game_Analysis import post_game_analysis
from DK_Optimizer_Ownership_StudLock import dk_optimizer_ownership_studlock

year = '2019'
week = 'Week16'

big_matrix_generator(year, week)
dk_optimizer_ownership_studlock(year, week, year + '/' + week + '/Ownership_' + week + '_Guess.csv')
post_game_analysis(year, year + '/' + week + '/ContestStandings_' + week + '.csv', year + '/' + week + '/All_Lineups_OwnershipStud_' + week + '.csv', week)