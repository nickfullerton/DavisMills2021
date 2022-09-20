import json
from collections import defaultdict


def show_data(lst):
    i = 0

    while i < len(lst):

        x1, y1 = lst[i]

        if 'Attempt' in x1:
            x1 = x1[:-7]
            print(f"{x1} - 0/{y1}")
            i += 1
        elif 'Attempt' not in x1:
            x1, y1 = lst[i]
            x2, y2 = lst[i + 1]
            print(f"{x1} - {y1}/{y2}")
            i += 2
        else:
            i += 1

    print()


def show_plain_data(lst):
    for value in lst:
        x, y = value
        print(f"{x} - {y}")
    print()

def getStats(i, j):

    completions = 0
    attempts = 0
    yards = 0
    air_yards = 0
    td = 0
    interceptions = 0
    sacks = 0
    sack_yards = 0

    players_rushed = defaultdict(int)
    men_in_box = defaultdict(int)
    qb_at_snap = defaultdict(int)
    pass_route = defaultdict(int)
    incompletion_type = defaultdict(int)
    pass_type = defaultdict(int)
    play_direction = defaultdict(int)
    down_distance = defaultdict(int)

    for w in range(i, j+1):
        file = f"../2021Games/game{w}.json"
        f = open(file)

        data = json.load(f)

        f.close()

        for quarter in data['periods']:  # Loop through all quarters
            for possession in quarter['pbp']:  # Loop through all possessions
                if 'events' in possession.keys():  # Make sure possession dict has events key
                    for event in possession['events']:  # Loop through every event of the possession
                        if 'play_type' in event.keys() and event[
                            'play_type'] == 'pass':  # make sure its a play and the play is a pass
                            if 'start_situation' in event.keys() and (event['start_situation']['possession'][
                                                                          'alias'] == 'HOU'):  # make sure Houston has possession
                                stat = None  # Get the stat dict that will contain passing information
                                for statistics in event['statistics']:
                                    if statistics['stat_type'] == 'pass':
                                        stat = statistics
                                        break

                                if 'nullified' not in stat.keys() and stat != None and stat['player'][
                                    'name'] == "Davis Mills":  # make sure there was no penalties

                                    down = event['start_situation']['down']
                                    yfd = event['start_situation']['yfd']

                                    if 'sack_yards' in stat.keys():
                                        sacks += 1
                                        sack_yards += int(stat['sack_yards'])

                                    if 'complete' in stat.keys() and stat['complete'] == 1:

                                        if 'att_yards' in stat.keys():
                                            attempt_yards = int(stat['att_yards'])

                                        if 'play_direction' in event.keys():
                                            direction = str(event['play_direction'])

                                        air_yards += attempt_yards
                                        completions += int(stat['complete'])
                                        players_rushed[str(event['players_rushed'])] += 1
                                        men_in_box[str(event['men_in_box'])] += 1
                                        qb_at_snap[str(event['qb_at_snap'])] += 1
                                        pass_route[str(event['pass_route'])] += 1

                                        if event['play_action']:
                                            pass_type['Play Action'] += 1
                                        elif event['run_pass_option']:
                                            pass_type['RPO'] += 1
                                        else:
                                            pass_type['Drop Back'] += 1

                                        if int(yfd) <= 3:
                                            down_distance[str(down) + ' Short'] += 1
                                        elif int(yfd) >= 8:
                                            down_distance[str(down) + ' Long'] += 1
                                        else:
                                            down_distance[str(down) + ' Medium'] += 1

                                        if attempt_yards <= 9:
                                            play_direction[direction + ' Short'] += 1
                                        elif attempt_yards >= 21:
                                            play_direction[direction + ' Long'] += 1
                                        else:
                                            play_direction[direction + ' Medium'] += 1

                                    if 'attempt' in stat.keys():

                                        if 'att_yards' in stat.keys():
                                            attempt_yards = int(stat['att_yards'])
                                        else:
                                            attempt_yards = "None"

                                        if 'play_direction' in event.keys():
                                            direction = str(event['play_direction'])
                                        else:
                                            direction = "None"

                                        attempts += int(stat['attempt'])
                                        players_rushed[str(event['players_rushed']) + ' Attempt'] += 1
                                        men_in_box[str(event['men_in_box']) + " Attempt"] += 1
                                        qb_at_snap[str(event['qb_at_snap']) + " Attempt"] += 1

                                        if 'pass_route' in event.keys():
                                            pass_route[str(event['pass_route']) + " Attempt"] += 1

                                        if event['play_action']:
                                            pass_type['Play Action Attempt'] += 1
                                        elif event['run_pass_option']:
                                            pass_type['RPO Attempt'] += 1
                                        else:
                                            pass_type['Drop Back Attempt'] += 1

                                        if int(yfd) <= 3:
                                            down_distance[str(down) + ' Short Attempt'] += 1
                                        elif int(yfd) >= 8:
                                            down_distance[str(down) + ' Long Attempt'] += 1
                                        else:
                                            down_distance[str(down) + ' Medium Attempt'] += 1

                                        if attempt_yards == "None":
                                            play_direction[direction + " Attempt"] += 1
                                        elif attempt_yards <= 9:
                                            play_direction[direction + ' Short Attempt'] += 1
                                        elif attempt_yards >= 21:
                                            play_direction[direction + ' Long Attempt'] += 1
                                        else:
                                            play_direction[direction + ' Medium Attempt'] += 1

                                    if 'incompletion_type' in stat.keys():
                                        incompletion_type[stat['incompletion_type']] += 1

                                    if 'yards' in stat.keys():
                                        yards += int(stat['yards'])

                                    if 'touchdown' in stat.keys():
                                        td += 1

                                    if 'interception' in stat.keys():
                                        interceptions += 1

    players_rushed = sorted(players_rushed.items())
    men_in_box = sorted(men_in_box.items())
    qb_at_snap = sorted(qb_at_snap.items())
    pass_route = sorted(pass_route.items())
    incompletion_type = sorted(incompletion_type.items())
    pass_type = sorted(pass_type.items())
    play_direction = sorted(play_direction.items())
    down_distance = sorted(down_distance.items())

    comp_percent = (round(completions / attempts * 100, 1)) if attempts != 0 else 0
    air_to_yards = (round(air_yards / yards * 100, 1)) if yards != 0 else 0
    print(
        f"Completions: {completions} - Attempts: {attempts} - Completion %: {comp_percent}% - Air Yards: {air_yards} - Yards: {yards}  - Air/Passing Yards: {air_to_yards}% - TD: {td} - Int: {interceptions} - Sacks: {sacks}/{abs(sack_yards)}")
    print()
    print("Players Rushed - Completions/Attempts")
    show_data(players_rushed)
    print("Men in Box - Completions/Attempts")
    show_data(men_in_box)
    print("QB at Snap - Completions/Attempts")
    show_data(qb_at_snap)
    print("Route - Completions/Attempts")
    show_data(pass_route)
    print("Incompletion Types - Amount")
    show_plain_data(incompletion_type)
    print("Pass Type - Completions/Attempts")
    show_data(pass_type)
    print("Pass Direction - Completions/Attempts")
    show_data(play_direction)
    print("Down and Distance - Completions/Attempts")
    show_data(down_distance)
