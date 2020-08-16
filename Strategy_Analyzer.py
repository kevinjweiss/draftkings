from Post_Game_Analysis import post_game_analysis
from DK_Optimizer_Ownership_StudLock import dk_optimizer_ownership_studlock

j =16
string = 'Week' + str(j)
#dk_optimizer_ownership_studlock(string, string + '/Ownership_' + string + '_Guess.csv')
post_game_analysis(string + '/ContestStandings_' + string + '.csv', string + '/All_Lineups_OwnershipStud_' + string + '.csv', string)