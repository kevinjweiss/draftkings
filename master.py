# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 14:48:00 2020

@author: queis
"""

from big_matrix import Big_Matrix
from lineup_creator import Create_Lineup
from post_process import Post_Process

# Year and Week For Data Organization
years = [2022]
weeks = ['1']

for year in years:
    for week in weeks:
        # Draft Kings Lineups -- Create Lineups -- Pick Slate -- End of URL
        group_id = 42776
        
        # Scoring Systems - Need to be setup by name in scoring_dict.py
        scoring = ['HALF_PPR']
        
        # Positions
        positions = ['qb', 'rb', 'wr', 'te', 'k', 'dst']
        
        # Initiate Object with necessary information required across modules
        bm_obj = Big_Matrix(year, week, group_id, scoring, positions)
        
        # Scrape Fantasy Pros for Stat Projections and put into dataframe
        bm_obj.fp_scrape_proj()
        
        # Score using stat projections and designated Scoring Systems
        # Add projected points min, mid, and max to data frame
        for i in range(0, len(scoring)):
            bm_obj.score_proj(scoring[i])
        
        # Plot Scoring for all positions and scoring systems using min/max/mid values
        bm_obj.plot_ranking(bm_obj.fp_df_proj, scoring, False)
        
        # # Scrape Draft Kings for Salary information and IDs for uploading later
        # bm_obj.dk_scrape()
        
        # # Merge Draft Kings w/ FP DK Scoring and Calculate Value
        # bm_obj.dk_merge()
        
        # # Calculate Value and Tier and plot based on value
        # bm_obj.value_tier()
        # bm_obj.plot_ranking(bm_obj.big_matrix, ['Draft Kings Value'], True)
        
        # # Create Lineup Object
        # lineup_obj = Create_Lineup(bm_obj)
        
        # # Narrow down Player List to Ownership Guess
        # # True for autogenerated, False for manually input
        # # Generally start with auto, then do manual after web analysis
        # lineup_obj.ownership_guess(True)
        
        # # Create All Possible Lineups from Big Matrix List
        # lineup_obj.create_all(salary_min = 49499, point_min = 130)
        
        # Create Post Process Object
        # process_obj = Post_Process(year, week, positions)
        # process_obj.big_matrix_process()
        # process_obj.big_matrix_process_plot(process_obj.big_matrix_process, ['Draft Kings Value'], True)
        # process_obj.all_lineup_process()
        # process_obj.all_lineup_process_plot()
        # process_obj.success(10)



