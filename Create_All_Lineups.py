def create_all_lineups(qb_df_small, rb_df_small, wr_df_small, te_df_small, dst_df_small, point_thresh):
    import pandas as pd
    import numpy as np
    from itertools import combinations

    "Data frame to vectors to allow for much faster looping"
    qb_player = qb_df_small['Player'].values
    rb_player = rb_df_small['Player'].values
    wr_player = wr_df_small['Player'].values
    te_player = te_df_small['Player'].values
    dst_player = dst_df_small['Player'].values

    qb_salary = qb_df_small['Salary'].values
    rb_salary = rb_df_small['Salary'].values
    wr_salary = wr_df_small['Salary'].values
    te_salary = te_df_small['Salary'].values
    dst_salary = dst_df_small['Salary'].values

    qb_points = qb_df_small['DK_Points'].values
    rb_points = rb_df_small['DK_Points'].values
    wr_points = wr_df_small['DK_Points'].values
    te_points = te_df_small['DK_Points'].values
    dst_points = dst_df_small['DK_Points'].values
    
    "Initialize Vectors for all possible all_lineupss under salary requirements"
    qb_all = []
    rb1_all = []
    rb2_all = []
    wr1_all = []
    wr2_all = []
    wr3_all = []
    te1_all = []
    flex_all = []
    dst1_all = []
    points_all = []
    salary_all = []

    "Setup unique combinations (avoid duplicates with multiple slots) - RB As Flex"
    qb = list(combinations(range(len(qb_df_small)), 1))
    rb = list(combinations(range(len(rb_df_small)), 3))
    wr = list(combinations(range(len(wr_df_small)), 3))
    te = list(combinations(range(len(te_df_small)), 1))
    dst = list(combinations(range(len(dst_df_small)), 1))

    for a in qb:
        for b in rb:
            for c in wr:
                for d in te:
                    for e in dst:
                        total_salary = qb_salary[a[0]] + rb_salary[b[0]] + rb_salary[b[1]] + wr_salary[c[0]] + wr_salary[
                            c[1]] + wr_salary[c[2]] + rb_salary[b[2]] + te_salary[d[0]] + dst_salary[e[0]]
                        if total_salary < 50001 and total_salary > 49499:
                            total_points = qb_points[a[0]] + rb_points[b[0]] + rb_points[b[1]] + wr_points[c[0]] + \
                                           wr_points[c[1]] + wr_points[c[2]] + rb_points[b[2]] + te_points[d[0]] + \
                                           dst_points[e[0]]
                            if total_points > point_thresh:
                                qb_all.append(qb_player[a[0]])
                                rb1_all.append(rb_player[b[0]])
                                rb2_all.append(rb_player[b[1]])
                                wr1_all.append(wr_player[c[0]])
                                wr2_all.append(wr_player[c[1]])
                                wr3_all.append(wr_player[c[2]])
                                te1_all.append(te_player[d[0]])
                                flex_all.append(rb_player[b[2]])
                                dst1_all.append(dst_player[e[0]])
                                points_all.append(total_points)
                                salary_all.append(total_salary)

    "Setup unique combinations (avoid duplicates with multiple slots) - WR As Flex"
    rb = list(combinations(range(len(rb_df_small)), 2))
    wr = list(combinations(range(len(wr_df_small)), 4))

    for a in qb:
        for b in rb:
            for c in wr:
                for d in te:
                    for e in dst:
                        total_salary = qb_salary[a[0]] + rb_salary[b[0]] + rb_salary[b[1]] + wr_salary[c[0]] + wr_salary[
                            c[1]] + wr_salary[c[2]] + wr_salary[c[3]] + te_salary[d[0]] + dst_salary[e[0]]
                        if total_salary < 50001 and total_salary > 49499:
                            total_points = qb_points[a[0]] + rb_points[b[0]] + rb_points[b[1]] + wr_points[c[0]] + \
                                           wr_points[c[1]] + wr_points[c[2]] + wr_points[c[3]] + te_points[d[0]] + \
                                           dst_points[e[0]]
                            if total_points > point_thresh:
                                qb_all.append(qb_player[a[0]])
                                rb1_all.append(rb_player[b[0]])
                                rb2_all.append(rb_player[b[1]])
                                wr1_all.append(wr_player[c[0]])
                                wr2_all.append(wr_player[c[1]])
                                wr3_all.append(wr_player[c[2]])
                                te1_all.append(te_player[d[0]])
                                flex_all.append(wr_player[c[3]])
                                dst1_all.append(dst_player[e[0]])
                                points_all.append(total_points)
                                salary_all.append(total_salary)

    "Setup unique combinations (avoid duplicates with multiple slots) - TE As Flex"
    wr = list(combinations(range(len(wr_df_small)), 3))
    te = list(combinations(range(len(te_df_small)), 2))

    for a in qb:
        for b in rb:
            for c in wr:
                for d in te:
                    for e in dst:
                        total_salary = qb_salary[a[0]] + rb_salary[b[0]] + rb_salary[b[1]] + wr_salary[c[0]] + wr_salary[
                            c[1]] + wr_salary[c[2]] + te_salary[d[0]] + te_salary[d[1]] + dst_salary[e[0]]
                        if total_salary < 50001 and total_salary > 49499:
                            total_points = qb_points[a[0]] + rb_points[b[0]] + rb_points[b[1]] + wr_points[c[0]] + \
                                           wr_points[c[1]] + wr_points[c[2]] + te_points[d[0]] + te_points[d[1]] + \
                                           dst_points[e[0]]
                            if total_points > point_thresh:
                                qb_all.append(qb_player[a[0]])
                                rb1_all.append(rb_player[b[0]])
                                rb2_all.append(rb_player[b[1]])
                                wr1_all.append(wr_player[c[0]])
                                wr2_all.append(wr_player[c[1]])
                                wr3_all.append(wr_player[c[2]])
                                te1_all.append(te_player[d[0]])
                                flex_all.append(te_player[d[1]])
                                dst1_all.append(dst_player[e[0]])
                                points_all.append(total_points)
                                salary_all.append(total_salary)
    
    "Assign Vectors back to data frame to write to CSV"
    all_lineups = pd.DataFrame(np.random.randint(low=0, high=10, size=(len(qb_all),11)),columns=['QB', 'RB1', 'RB2', 'WR1', 'WR2', 'WR3', 'TE', 'Flex', 'DST', 'Points', 'Salary'])
    all_lineups['QB'] = qb_all
    all_lineups['RB1'] = rb1_all
    all_lineups['RB2'] = rb2_all
    all_lineups['WR1'] = wr1_all
    all_lineups['WR2'] = wr2_all
    all_lineups['WR3'] = wr3_all
    all_lineups['TE'] = te1_all
    all_lineups['Flex'] = flex_all
    all_lineups['DST'] = dst1_all
    all_lineups['Points'] = points_all
    all_lineups['Salary'] = salary_all
    all_lineups.sort_values(by=['Points'], inplace=True, ascending=False)
    
    "Drop Low Scoring Lineups & Lineups that don't utilize the Salary Cap"
    all_lineups = all_lineups.reset_index(drop=True)
    return all_lineups