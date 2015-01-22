# Name: Alexander Ngo
# CSE 140
# HW 9

import os
import matplotlib.pyplot as plt
from pylab import imshow, show, get_cmap
import numpy as np
import sys

'''

season: 2 nested dicts of Season:game: a list of a dicts keys are categories
and values are it's corresponding value
example:
{06-07 Season:{20110705MIASEA:[plays: {categories: value}]}}}

player stats: a dictionary whos keys are players and values are list of dictionaries
who keys are categories and values are it's corresponding value
example:
{Alex English: [{Catergories:Value...}, {Catergories:Value...}, .....]}
'''




'''
takes a folder name and parses through each file which are box scores,
and creates/returns a dictionary who keys:values are seasons:games, and games
is a dict of games:plays and plays is a list of dicts whose keys are categories and values
are parse from the file
example: {06-07 Season:{20110705MIASEA:[plays: {categorie: value, categorie: value}]}}}
'''
def parse_boxscores(folder_name):
    # season : game : play : each categorie
    seasons = {}
    categories = ['a1', 'a2', 'a3', 'a4', 'a5', 'h1', 'h2', 'h3', 'h4', 'h5', 'period',
     'time', 'team', 'etype', 'assist', 'away', 'block', 'entered', 'home',
     'left', 'num', 'opponent', 'outof', 'player', 'points', 'possession',
     'reason', 'result', 'steal', 'type', 'x', 'y']
    #goes through each season
    for season in os.listdir(folder_name):
        season_path = os.path.join(folder_name, season)
        seasons[season] = {}

        #this particular season
        season = seasons[season]

        #each individual boxscore
        for boxscore in os.listdir(season_path):
            #truncates the ".csv"
            game_name = boxscore[:-3]
            season[game_name] = []
            #this particular game
            game = season[game_name]

            box_path = os.path.join(season_path, boxscore)
            box_scores = open(box_path)
            #each individual play
            for play in box_scores:
                play_dict = {}
                #gets a list of each value in the play
                play = play.split(",")
                #skip if it's the first line(categories)
                if(play[0] == "a1"):
                    continue
                for idx in range(11, len(categories)):
                    #occasionally encounter oddly formated data
                    try:
                        play_dict[categories[idx]] = play[idx]
                    except:
                        play_dict = {}

                if(play_dict != {}):
                    game.append(play_dict)
                
    return seasons

'''
takes a folder name and for all the player stat files in that folder, parses through them,
and returns a dictionary whose key:values are player names : list, the list contains a
dictionary for every season this player played and the key:value are categories : to their
corresponding value from that season
Example {Alex English: [{Catergories:Value...}, {Catergories:Value...}, .....]
'''
def parse_player_stats(folder_name):
    players = {}

    for player in os.listdir(folder_name):
        categories = []
        player_path = os.path.join(folder_name, player)
        #puts the player's name as a key
        players[player[:-3]] = []
        player_stat_list = players[player[:-3]]
        stats = open(player_path)
        #each row is a season
        for season in stats:
            stat_dict = {}
            #separates the stats
            season = season.strip().split(",")
            if categories == []:
                categories = [category.strip() for category in season][:-1]
            else:
                for idx in range(2, len(categories)):
                    try:
                        stat_dict[categories[idx]] = season[idx]
                    except:
                        break
            if(stat_dict != {}):

                player_stat_list.append(stat_dict)            
        
    return players
        
        
'''
takes seasons and returns a list of tuples for each season, each tuple
consisting of (total_shots, shots in the paint)
'''
def shot_total(seasons):
    shot_totals = []
    for season in seasons:
        total = 0
        paint = 0
        a = {}
        for game in seasons[season].values():
            for play in game:
                #if it is a shot
                if play["x"] != "":
                    total += 1
                    #if it is in the paint
                    if (in_paint(play)):
                        paint +=1
            a[season] = (total, paint)
        shot_totals.append(a)
    return shot_totals

'''
takes in a dictionary and check it's coordinates then returns if it is in the paint
'''
def in_paint(play):
    return (int(play["x"]) >= 17 and int(play["x"]) <= 34 and
            int(play["y"]) <= 19)

'''
takes seasons and returns a list of dicts, each dict representing a season as keys and a list of
tuples of shot locations (x, y) coordinates as values
''' 
def shot_locations(seasons):
    seas = []
    for season in seasons.keys():
        shot_location = {}
        for game in seasons[season].values():
            shot_list = []
            for play in game:
                #if it is a shot
                if play["x"] != "":
                    shot_list.append(((play["x"], play["y"])))
            shot_location[season] = shot_list
        seas.append(shot_location)
    return seas

'''
takes in a list of dict who keys are a season and values a list of tuple shot coordinates
and saves a scatter plot for each dict(season) in a file called "season_name Scatterplot.png"
'''
def create_scatter(shot_locations):
    for season in shot_locations:
        season_name = [season_name for season_name in season][0]
        season = season.values()[0]
        #gets the x coordinates into a list
        x = [int(elt[0]) for elt in season]
        #gets the y coordinates into a list
        y = [int(elt[1]) for elt in season]
        
        x = np.array(x)
        y = np.array(y)                                                           
        
        plt.clf()
        fname = season_name + " Scatterplot"
        graph_labels("x", "y", fname)
        
        plt.scatter(x, y)
        plt.savefig(fname + ".png")


'''
takes in a list of dict who keys are a season and values a list of tuple shot coordinates
and creates a scatter plot for each dict(season) in a file called "season_name Heat Map.png"
'''
def create_heatmap(shot_location):
    for season in shot_location:
        season_name = [season_name for season_name in season][0]
        season = season.values()[0]

        #gets the x coordinates into a list
        x = [int(elt[0]) for elt in season]
        #gets the y coordinates into a list
        y = [int(elt[1]) for elt in season]
        
        x = np.array(x)
        y = np.array(y)
        fname = season_name + " Heat Map"
        plt.clf()
        graph_labels("x", "y", fname)
        
        heatmap, throw, throw = np.histogram2d(y, x, bins=50)
        plt.imshow(heatmap, cmap=get_cmap("RdBu"), origin='lower')
        plt.savefig(fname + ".png")
    
'''
takes a x label, y label, and optionally a title, then puts those onto the graph
'''
def graph_labels(x_label, y_label, title = ""):
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)



'''
takes seasons, and a type, where type is the streak that you want to look for and
returns a list of shot tuples (x,y) where x and y and coordinates
'''
def streak_finder(seasons, type):
    if type.lower() == "cold":
        type = "missed"
    else:
        type = "made"

    streaks = []
    for season in seasons.values():
        for game in season.values():
            #puts all of the shots into a list
            all_shots = shot_aggregate(game)
            cur_streaks = []
            for idx in range(len(all_shots)):
                name = all_shots[idx][0]
                result = all_shots[idx][1]
                #if not already on a streak
                #checks if this shot results in the beginning of a streak
                #we are looking for
                if (name not in [elt[0] for elt in cur_streaks] and
                result == type):
                    total = 0
                    #reversed because we want to start from recent  to oldest
                    for shots in reversed(all_shots[:idx]):
                        if(shots[0] == name):
                            #if he makes a shot while we are looking for a cold streak
                            #or vice-versa
                            if(shots[1] != type):
                                break
                            else:
                                total += 1
                                if total > 3:
                                    cur_streaks.append((name, 0, 0))
                #if the player is on a streak          
                elif(name in [elt[0] for elt in cur_streaks]):
                    #finds the index at which the player is in the list
                    index = [elt[0] for elt in cur_streaks].index(name)
                    #based on result, creates new tuple, who's values are
                    #incremented accordingly
                    if(result == "missed"):
                        cur_streaks[index] = (name, cur_streaks[index][1],
                                              cur_streaks[index][2] + 1)
                    else:
                        cur_streaks[index] = (name, cur_streaks[index][1] + 1,
                                              cur_streaks[index][2] + 1)
            #ignores any with less than 3 and appends a shot tuple (x,y) 
            streaks += [(elt[1], elt[2]) for elt in cur_streaks if elt[2] > 2]
    return streaks


'''
Takes in seasons, a begin date tuple, and end date tuple. The first value is the month
and the second the day. Returns a list of dictionaries where each key is a team and
the value is their average turnovers per game
'''
def to_total(seasons, begin_date = (9, 1), end_date = (7 , 1)):
    to_totals = []
    for season in seasons.values():
        team_to = {}
        for game in season:
            #date of the game
            game_date =  (int(game[4:6]), int(game[6:8])) 
            #only if the date of the game falls within the begin and end date
            if(is_between(game_date, begin_date, end_date)):
                team1 = game[-7:-4]
                team2 = game[-4:-1]
                
                
                to1 = 0
                to2 = 0
                #updates to1 and to2 to their respective turnover counts for that game
                for play in season[game]:
                    if(play["etype"] == "turnover"):
                        if(play["team"] == team1):
                            to1 +=1
                        else:
                            to2 += 1
                            
                    if(team1 not in team_to):
                        team_to[team1] = to1
                    else:
                        #finding average
                        team_to[team1] = (to1 + team_to[team1]) / 2.0

                    if(team2 not in team_to):
                        team_to[team2] = to2
                    else:
                        #finding average
                        team_to[team2] = (to2 + team_to[team2]) / 2.0

        to_totals.append(team_to)
    return to_totals
'''
returns true if the date if between begin and end and false otherwise.
'''
def is_between(date, begin, end):
    if(begin > end):
        return date > begin or date < end
    else:
        return date > begin and date < end

                                
                
'''
takes in a game which  of list of dictionaries and returns a list of all shot results in
that game in the form a tuple (player, result)
'''
def shot_aggregate(game):
    shots = []
    for play in game:
        if play["etype"] == "shot":
            shots.append((play["player"], play["result"]))
    return shots
    

'''
takes in a list of 2-pair tuples and returns the net change in the ratios
of paint_shots:total_shots between seasons 
'''
def to_ratios(shot_totals):
    total_change = 0
    for idx in range(len(shot_totals) - 1):
        #first ratio
        a = shot_totals[idx].values()[0][1] / float(shot_totals[idx].values()[0][0])
        #ratio from the season directly after
        b = shot_totals[idx + 1].values()[0][1] / float(shot_totals[idx + 1].values()[0][0])
        total_change += b - a
    return total_change

'''
takes in a list of tuples representing a shot coordinate and a type of streak ("cold" or "hot"),
and returns a tuple of the total people who had that type of streak and how many of them it
affected
'''
def total_affected(streak, type_of_streak):
    total = 0
    affected = 0
    if type_of_streak == "cold":
        for shooting in streak:
            total += 1
            if(to_percentage(shooting) <= .3):
                affected +=1
    #if it is a "hot" streak
    else:
        for shooting in streak:
            total += 1
            if(to_percentage(shooting) >= .5):
                affected +=1

    return (affected, total)

'''
takes in a before and after, which are both lists of dictionaries , and returns
the total number of comparisons and the number of teams did worse "after" than "before"
in the same season.
'''
def compare_before_after(before, after):
    total = 0
    worse = 0
    for idx in range(len(before)):
        for team in before[idx].keys():
            total += 1
            #worse if after value if more than before value
            if(before[idx][team] < after[idx][team]):
                worse += 1
    return (worse, total)

'''
takes in a val tuple, a list of labels, and a file name then creates
a pie chart with the values and percentages, and corresponding labels
then saves it to "fname"
'''
def create_pie_chart(val, labels, fname):
    values = [val[0], val[1] - val[0]]
    '''
    allows both percentage and
    values to be printed
    '''
    def own_autopct(pct):
        total = sum(values)
        val = int(pct*total/100.0)
        return '{p:.2f}%  ({v:d})'.format(p = pct,v = val)
    
    plt.clf()
    plt.title(fname[:-4])
    plt.pie(values, labels=labels, autopct=own_autopct)
    plt.savefig(fname)
    
    
'''
takes in a 2-pair tuple and converts and returns it to a percentage
'''
def to_percentage(shot_tup):
    return int(shot_tup[0]) / float(shot_tup[1])
            
def main():
    #if no arguments or ran from client
    if (len(sys.argv) == 1):
        box_scores_folder = "Box Scores"
    else:
        #sets the folders to the corresponding argument passed in
        #command prompt
        box_scores_folder = sys.argv[1]

    seasons = parse_boxscores(box_scores_folder)
    shot_totals = sorted(shot_total(seasons))
    print "Season Shot Total:", shot_totals
    print
    shot_location = shot_locations(seasons)
    shot_ratio = to_ratios(shot_totals)
    print "Net Shot Ratio Difference:", shot_ratio
    print
    create_heatmap(shot_location)
    create_scatter(shot_location)


    cold_streaks = streak_finder(seasons, "cold")
    hot_streaks = streak_finder(seasons, "hot")
    cold_affected = total_affected(cold_streaks, "cold")
    print "Cold Streaks, Affected:", cold_affected
    create_pie_chart(cold_affected, ["Affected", "No effect"], "Cold Streak Chart.png")
    print
    hot_affected = total_affected(hot_streaks, "hot")
    print "Hot Streaks, Affected:", hot_affected
    create_pie_chart(hot_affected, ["Affected", "No effect"], "Hot Streaks Chart.png")
    print
    
    
    before = to_total(seasons, (9, 1), (3, 1))
    after =  to_total(seasons, (3, 1))
    compare = compare_before_after(before, after)
    print "Total teams compared, Teams worse after:", compare_before_after(before, after)
    create_pie_chart(compare, ["Worse", "Same or Better"], "TO Pie Chart.png")


if __name__ == "__main__":
    main()

