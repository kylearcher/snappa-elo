import math
import pandas as pd
import numpy as np

#Constants
file = "Snappa Games - Game List.csv"
#Test DATA
# players = ["Kyle", "Kurt", "Gabe", "Pete"]
#
# score = (4,7)
#
# player_dict = {"Kyle": 900, "Kurt":800, "Gabe":700, "Pete":800}

#### End Test Data
def parse_data(file):
    """
    takes a csv file, and parses the data into useabvle format.
    returns:
    player_dict = {"Kyle": 900, "Kurt":800, "Gabe":700, "Pete":800}
    game_list is a list of games.
    game = [["Kyle", "Kurt", "Gabe", "Pete"], (4,7)]
    """
    df = pd.DataFrame(pd.read_csv(file))
    #first build player dictionary
    name_dict = {}
    counter = 0
    for column in df:
        #if not a score column
        if counter != 2 and counter != 5:
            for name in df[column]:
                if name not in name_dict:
                    name_dict[name] = 800
        counter +=1


    #get a game list
    game_list = []
    num_rows = df.shape[0]
    for i in range(num_rows):
        row = df.iloc[i]
        names = [row[0],row[1],row[3],row[4]]
        score = (row[2], row[5])
        game = [names,score]
        game_list.append(game)


    return name_dict, game_list

def run_game(players, score, player_dict):
    """
    runs one game

    players: names of players in game
    ex:

    score: tuple of score, left team then right

    player_dict: dict of player names and elo ratings pre-game

    players 1 and 2 are on the same team, as are 3 and 4.
    """
    #get names and elos of players in game
    n_1, n_2, n_3, n_4 = players[0], players[1], players[2], players[3]
    s_1, s_2, s_3, s_4 = player_dict[n_1], player_dict[n_2], player_dict[n_3], player_dict[n_4]
    #compute the expected probability that team with players 1 and 2 win
    diff = (s_3 + s_4) - (s_1 + s_2)
    p_1 = (1.0 / (1.0 + 10.0**( diff / 400.0) ))
    p_2 = 1.0 - p_1
    #get Elo winner and loser
    if score[0] > score [1]:
        elo_w = s_1+s_2
        elo_l = s_3+s_4
        s_1, s_2 = 1, 0
    else:
        elo_w = s_3+s_4
        elo_l = s_1+s_2
        s_1, s_2 = 0, 1

    #Margin of victory multplier, uses difference is scores
    q = (2.2/((elo_w-elo_l)*.001+2.2))
    pd = abs(score[0]-score[1])
    movm = math.log(pd+1.0, math.e)*q

    #actual result is found by forumla below, K scales
    k = 50
    final_elo_1 = k*(s_1-p_1)*movm
    final_elo_2 = k*(s_2-p_2)*movm
    # print "The Elo change is:",final_elo_1

    #update dict
    player_dict[n_1] += final_elo_1
    player_dict[n_2] += final_elo_1
    player_dict[n_3] += final_elo_2
    player_dict[n_4] += final_elo_2

    return player_dict

def run_all_games(file):
    """
    runs all games, and prints a ranking list

    """
    #load data
    name_dict, game_list = parse_data(file)
    #build games played dict
    games_played_dict = {}
    for name in name_dict:
        games_played_dict[name] = 0

    #run all games
    for game in game_list:
        #add counts to games played
        for name in game[0]:
            games_played_dict[name] +=1
        #run game
        name_dict = run_game(game[0], game[1], name_dict)

    #sort
    rank_list = []
    for i in name_dict:
        rank_list.append([name_dict[i], i, games_played_dict[i]])
    rank_list.sort(reverse = True)

    #print
    print_game_output(rank_list)

    return

def print_game_output(rank_list):
    print "Snappa Power Rankings"
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~"
    for i in range(len(rank_list)):
        item = rank_list[i]
        #check how many games played
        if item[2] <=4:
            add_on = "***"
        else:
            add_on = ""
        #print line
        print str(i+1)+". "+item[1]+", Elo = "+str(round(item[0],3))+add_on

    print
    print
    print "*** indiciates less than 5 games played"

run_all_games(file)


# print run_game(players, score, player_dict)
