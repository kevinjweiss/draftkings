from Big_Matrix_Generator import big_matrix_generator
from DK_Optimizer_Ownership_StudLock import dk_optimizer_ownership_studlock
from Create_Ownership_Guess import create_ownership_guess

year = '2020'
week = 'Week1'

big_matrix_generator(year, week)
create_ownership_guess(year, week)
dk_optimizer_ownership_studlock(year, week, year + '/' + week + '/Ownership_' + week + '_Guess_Auto.csv')
