def dk_data_import(year, week, player_target_file, toggle):
    'Toggle = 1 if reading in Draft Kings Data'
    'Toggle = 2 if reading in Target Players Data'
    
    import pandas as pd

    "Import in Draft Kings Salary"
    if toggle == 1:  
        "Import Draft Kings Salary Input File"
        dk_data = pd.read_csv(year + '/' + week + '/DKSalaries_' + week + '.csv')
        dk_df = pd.DataFrame(data = dk_data)
        
        "Rename Columns to match Fantasy Pros for Data Merging"
        dk_df.rename(columns={'Name':'Player'}, inplace=True)
        dk_df.rename(columns={'TeamAbbrev':'Team'}, inplace=True)
        
        "Rename Team Abbreviations preventing data matching"
        dk_df['Team'] = dk_df['Team'].str.replace('JAX', 'JAC')
        
    if toggle == 2:
        "Import Player Target CSV Input"
        dk_data = pd.read_csv(player_target_file)
        dk_df = pd.DataFrame(data = dk_data) 
    
    "Rename Players with Name Suffixes preventing data matching"
    dk_df['Player'] = dk_df['Player'].str.replace(' III', '')
    dk_df['Player'] = dk_df['Player'].str.replace(' II', '')
    dk_df['Player'] = dk_df['Player'].str.replace(' Jr.', '')
    dk_df['Player'] = dk_df['Player'].str.replace(' Sr.', '')
    dk_df['Player'] = dk_df['Player'].str.replace('Will Fuller V', 'Will Fuller')
    dk_df['Player'] = dk_df['Player'].str.replace('Odell Beckham', 'Odell Beckham Jr.')
    dk_df['Player'] = dk_df['Player'].str.replace('Willie Snead IV', 'Willie Snead')
    dk_df['Player'] = dk_df['Player'].str.replace('Mitchell Trubisky', 'Mitch Trubisky')
    dk_df['Player'] = dk_df['Player'].str.replace('DJ Chark', 'D.J. Chark')
    dk_df['Player'] = dk_df['Player'].str.replace('DK Metcalf', 'D.K. Metcalf')
    dk_df['Player'] = dk_df['Player'].str.replace('DJ Moore', 'D.J. Moore')
    dk_df['Player'] = dk_df['Player'].str.replace('DeVante Parker', 'Devante Parker')
    dk_df['Player'] = dk_df['Player'].str.replace('Benny Snell', 'Benny Snell Jr.')
    dk_df['Player'] = dk_df['Player'].str.replace('Ronald Jones', 'Ronald Jones II')
    
    "Rename Defenses to Match Fantasy Pros Format"
    dk_df['Player'] = dk_df['Player'].str.replace('Steelers ', 'Pittsburgh Steelers', )
    dk_df['Player'] = dk_df['Player'].str.replace('Jaguars ', 'Jacksonville Jaguars', )
    dk_df['Player'] = dk_df['Player'].str.replace('Lions ', 'Detroit Lions')
    dk_df['Player'] = dk_df['Player'].str.replace('Ravens ', 'Baltimore Ravens')
    dk_df['Player'] = dk_df['Player'].str.replace('Titans ', 'Tennessee Titans')
    dk_df['Player'] = dk_df['Player'].str.replace('Vikings ', 'Minnesota Vikings')
    dk_df['Player'] = dk_df['Player'].str.replace('Seahawks ', 'Seattle Seahawks')
    dk_df['Player'] = dk_df['Player'].str.replace('Redskins ', 'Washington Redskins')
    dk_df['Player'] = dk_df['Player'].str.replace('Saints ', 'New Orleans Saints')
    dk_df['Player'] = dk_df['Player'].str.replace('Packers ', 'Green Bay Packers')
    dk_df['Player'] = dk_df['Player'].str.replace('Patriots ', 'New England Patriots')
    dk_df['Player'] = dk_df['Player'].str.replace('Rams ', 'Los Angeles Rams')
    dk_df['Player'] = dk_df['Player'].str.replace('Chargers ', 'Los Angeles Chargers')
    dk_df['Player'] = dk_df['Player'].str.replace('Bengals ', 'Cincinnati Bengals')
    dk_df['Player'] = dk_df['Player'].str.replace('Bears ', 'Chicago Bears')
    dk_df['Player'] = dk_df['Player'].str.replace('Jets ', 'New York Jets')
    dk_df['Player'] = dk_df['Player'].str.replace('Broncos ', 'Denver Broncos')
    dk_df['Player'] = dk_df['Player'].str.replace('Cowboys ', 'Dallas Cowboys')
    dk_df['Player'] = dk_df['Player'].str.replace('Panthers ', 'Carolina Panthers')
    dk_df['Player'] = dk_df['Player'].str.replace('Cardinals ', 'Arizona Cardinals')
    dk_df['Player'] = dk_df['Player'].str.replace('Dolphins ', 'Miami Dolphins')
    dk_df['Player'] = dk_df['Player'].str.replace('Falcons ', 'Atlanta Falcons')
    dk_df['Player'] = dk_df['Player'].str.replace('Bills ', 'Buffalo Bills')
    dk_df['Player'] = dk_df['Player'].str.replace('Chiefs ', 'Kansas City Chiefs')
    dk_df['Player'] = dk_df['Player'].str.replace('Eagles ', 'Philadelphia Eagles')
    dk_df['Player'] = dk_df['Player'].str.replace('Giants ', 'New York Giants')
    dk_df['Player'] = dk_df['Player'].str.replace('Colts ', 'Indianapolis Colts')
    dk_df['Player'] = dk_df['Player'].str.replace('Texans ', 'Houston Texans')
    dk_df['Player'] = dk_df['Player'].str.replace('49ers ', 'San Francisco 49ers')
    dk_df['Player'] = dk_df['Player'].str.replace('Buccaneers ', 'Tampa Bay Buccaneers')
    dk_df['Player'] = dk_df['Player'].str.replace('Raiders ', 'Oakland Raiders')
    dk_df['Player'] = dk_df['Player'].str.replace('Browns ', 'Cleveland Browns')

    return dk_df
