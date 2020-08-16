from Big_Matrix_Generator import big_matrix_generator
from DK_Optimizer_Value import dk_optimizer_value
from DK_Optimizer_Ownership import dk_optimizer_ownership
from Post_Game_Analysis import post_game_analysis
from DK_Optimizer_Ownership_StudLock import dk_optimizer_ownership_studlock

dk_optimizer_ownership_studlock('Week7', 'Week7/Ownership_Week7_Guess.csv')
post_game_analysis('Week7/ContestStandings_Week6.csv', 'Week7/All_Lineups_OwnershipStud_Week6.csv')
post_game_analysis('Week7/ContestStandings_Week6.csv', 'Week7/Ten_Lineups_Week7.csv')
dk_optimizer_ownership_studlock('Week7', 'Week6/Ownership_15perc_Week7.csv')
post_game_analysis('Week7/ContestStandings_Week6.csv', 'Week7/All_Lineups_OwnershipStud_Week6.csv')
post_game_analysis('Week7/ContestStandings_Week6.csv', 'Week7/Ten_Lineups_Week7.csv')