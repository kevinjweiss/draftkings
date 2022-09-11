# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 13:55:32 2020

@author: queis
"""

def create_dict(scoring):
# Draft Kings Scoring
    if scoring == 'Draft Kings':
        
        BONUS_RAMP = 0.8 # Instead of using exact bonus threshold, bonus ramps in from threshold (decimel of percent form) to reward players with projectsions just below bonus threshold
        
        # Passing
        PASSTD = 4
        PASSYD = 0.04
        PASSTHRESH = 300
        PASSBONUS = 3
        INT = -1
        
        # Rushing
        RUSHTD = 6
        RUSHYD = 0.1
        RUSHTHRESH = 100
        RUSHBONUS = 3
        FL = -1
        
        # Receiving
        REC = 1
        CATCHTD = 6
        CATCHYD = 0.1
        RECTHRESH = 100
        RECBONUS = 3
        
        # Kicking
        FG = 0
        XPT = 0
        
        # Defense
        SACK = 1
        DEFINT = 2
        FR = 2
        DEFTD = 6
        SAFETY = 2
        
        # POINTS AGAINST = Points scored threshold, FANTASY POINTS = Fantasy points if above threshold
        POINTS_AGAINST = [34, 27, 20, 13, 7, 0]
        FANTASY_POINTS = [-4, -1, 0, 1, 5, 7]
        
        # YARDS AGAINST = Yards against threshold, FANTASY POiNTS 2 = Fantasy points if above threshold
        YARDS_AGAINST = [100, 200, 300, 400, 450, 500, 550, 700]
        FANTASY_POINTS_2 = [0, 0, 0, 0, 0, 0, 0, 0]
        
    # Dynasty League 0.5 PPR Scoring
    if scoring == 'Dynasty':
        
        BONUS_RAMP = 0 # Instead of using exact bonus threshold, bonus ramps in from threshold (decimel of percent form) to reward players with projectsions just below bonus threshold
        
        # Passing
        PASSTD = 4
        PASSYD = 0.04
        PASSTHRESH = 300
        PASSBONUS = 0
        INT = -2
        
        # Rushing
        RUSHTD = 6
        RUSHYD = 0.1
        RUSHTHRESH = 100
        RUSHBONUS = 0
        FL = -2
        
        # Receiving
        REC = 0.5
        CATCHTD = 6
        CATCHYD = 0.1
        RECTHRESH = 100
        RECBONUS = 0
        
        # Kicking
        FG = 3
        XPT = 1
        
        # Defense
        SACK = 1
        DEFINT = 2
        FR = 2
        DEFTD = 6
        SAFETY = 2
        
        # POINTS AGAINST = Points scored threshold, FANTASY POINTS = Fantasy points if above threshold
        POINTS_AGAINST = [40, 34, 27, 20, 13, 6, 0]
        FANTASY_POINTS = [-4, -1, 0, 1, 3, 4, 5]
        
        # YARDS AGAINST = Yards against threshold, FANTASY POiNTS 2 = Fantasy points if above threshold
        YARDS_AGAINST = [100, 200, 300, 400, 450, 500, 550, 700]
        FANTASY_POINTS_2 = [5, 3, 2, -1, -3, -5, -6, -7]
    
    # Redraft League 1 PPR Scoring
    if scoring == 'Redraft':
        
        BONUS_RAMP = 0 # Instead of using exact bonus threshold, bonus ramps in from threshold (decimel of percent form) to reward players with projectsions just below bonus threshold
        
        # Passing
        PASSTD = 4
        PASSYD = 0.04
        PASSTHRESH = 300
        PASSBONUS = 0
        INT = -1
        
        # Rushing
        RUSHTD = 6
        RUSHYD = 0.1
        RUSHTHRESH = 100
        RUSHBONUS = 0
        FL = -2
        
        # Receiving
        REC = 1
        CATCHTD = 6
        CATCHYD = 0.1
        RECTHRESH = 100
        RECBONUS = 0
        
        # Kicking
        FG = 3
        XPT = 1
        
        # Defense
        SACK = 1
        DEFINT = 2
        FR = 2
        DEFTD = 6
        SAFETY = 2
        
        # POINTS AGAINST = Points scored threshold, FANTASY POINTS = Fantasy points if above threshold
        POINTS_AGAINST = [40, 34, 27, 20, 13, 6, 0]
        FANTASY_POINTS = [-4, -1, 0, 1, 4, 7, 10]
        
        # YARDS AGAINST = Yards against threshold, FANTASY POiNTS 2 = Fantasy points if above threshold
        YARDS_AGAINST = [100, 200, 300, 400, 450, 500, 550, 700]
        FANTASY_POINTS_2 = [0, 0, 0, 0, 0, 0, 0, 0]
        
    points_dict = {'BONUS_RAMP': BONUS_RAMP,
                    'PASSTD': PASSTD,
                    'PASSYD': PASSYD,
                    'PASSTHRESH': PASSTHRESH,
                    'PASSBONUS': PASSBONUS,
                    'INT': INT,
                    'RUSHTD': RUSHTD,
                    'RUSHYD': RUSHYD,
                    'RUSHTHRESH': RUSHTHRESH,
                    'RUSHBONUS': RUSHBONUS,
                    'FL': FL,
                    'REC': REC,
                    'CATCHTD': CATCHTD,
                    'CATCHYD': CATCHYD,
                    'RECTHRESH': RECTHRESH,
                    'RECBONUS': RECBONUS,
                    'SACK': SACK,
                    'DEFINT': DEFINT,
                    'FR': FR,
                    'DEFTD': DEFTD,
                    'SAFETY': SAFETY,
                    'POINTS_AGAINST': POINTS_AGAINST,
                    'FANTASY_POINTS': FANTASY_POINTS,
                    'YARDS_AGAINST': YARDS_AGAINST,
                    'FANTASY_POINTS_2': FANTASY_POINTS_2} 
    
    return points_dict