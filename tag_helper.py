# This is here to help code readability
# it helps furbot find relevant tags
# Thanks to \u\_PM_ME_GFUR_ for compiling the lists this bot uses

# Priority goes to gender, fetish, pairing, body, act, positions and then others.

tag_limit = 25


# A bunch of methods that prepare lists
def get_genders():
    full_list = open('tag/gender.txt', 'r').read()
    split_list = full_list.split('|')
    finished_list = list(filter(None, split_list))
    return finished_list


def get_pairings():
    full_list = open('tag/pairings.txt', 'r').read()
    split_list = full_list.split('|')
    finished_list = list(filter(None, split_list))
    return finished_list


def get_body():
    full_list = open('tag/body.txt', 'r').read()
    split_list = full_list.split('|')
    finished_list = list(filter(None, split_list))
    return finished_list


def get_acts():
    full_list = open('tag/sex_acts.txt', 'r').read()
    split_list = full_list.split('|')
    finished_list = list(filter(None, split_list))
    return finished_list


def get_positions():
    full_list = open('tag/positions.txt', 'r').read()
    split_list = full_list.split('|')
    finished_list = list(filter(None, split_list))
    return finished_list


def get_fetishes():
    full_list = open('tag/fetishes.txt', 'r').read()
    split_list = full_list.split('|')
    finished_list = list(filter(None, split_list))
    return finished_list


# A bunch of methods that find tags
def find_gender(tags):
    tag_list = list()
    i = 0
    while i < len(tags):
        if tags[i] in gender_list:
            tag_list.append(tags[i])
        i += 1
    return tag_list


def find_fetish(tags):
    tag_list = list()
    i = 0
    while i < len(tags):
        if tags[i] in fetish_list:
            tag_list.append(tags[i])
        i += 1
    return tag_list


def find_pairing(tags):
    tag_list = list()
    i = 0
    while i < len(tags):
        if tags[i] in pairing_list:
            tag_list.append(tags[i])
        i += 1
    return tag_list


def find_body(tags):
    tag_list = list()
    i = 0
    while i < len(tags):
        if tags[i] in body_list:
            tag_list.append(tags[i])
        i += 1
    return tag_list


def find_act(tags):
    tag_list = list()
    i = 0
    while i < len(tags):
        if tags[i] in act_list:
            tag_list.append(tags[i])
        i += 1
    return tag_list


def find_position(tags):
    tag_list = list()
    i = 0
    while i < len(tags):
        if tags[i] in position_list:
            tag_list.append(tags[i])
        i += 1
    return tag_list


def find_others(tags):
    tag_list = list()
    i = 0
    while i < len(tags):
        if tags[i] not in full_tag_list:
            tag_list.append(tags[i])
        i += 1
    return tag_list


# Starts the search
# Called by Furbot
def start_searching(tags):
    gender_tags = find_gender(tags)
    fetish_tags = find_fetish(tags)
    pairing_tags = find_pairing(tags)
    body_tags = find_body(tags)
    act_tags = find_act(tags)
    position_tags = find_position(tags)
    other_tags = find_others(tags)
    fixed_tag_list = gender_tags + fetish_tags + pairing_tags + body_tags + act_tags + position_tags + other_tags
    tag_count = 0
    short_list = list()
    while tag_count < tag_limit:
        short_list.append(fixed_tag_list[tag_count])
        tag_count += 1
    extra_tags = len(fixed_tag_list) - tag_count
    if extra_tags == 1:
        short_list.append('\n**^^^^And ^^^^' + str(extra_tags) + ' ^^^^other ^^^^tag**')
    if extra_tags > 1:
        short_list.append('\n**^^^^And ^^^^' + str(extra_tags) + ' ^^^^other ^^^^tags**')
    return short_list

gender_list = get_genders()
pairing_list = get_pairings()
body_list = get_body()
act_list = get_acts()
position_list = get_positions()
fetish_list = get_fetishes()
full_tag_list = gender_list + pairing_list + body_list + act_list + position_list + fetish_list
