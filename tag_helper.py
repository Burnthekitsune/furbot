# This is here to help code readability
# it helps furbot find relevant tags
# Thanks to \u\_PM_ME_GFUR_ for compiling the lists this bot uses

# Priority goes to gender, fetish, pairing, body, act, positions and then others.

tag_limit = 25

# Get the list from a text file.
def get_list(list_url):
    if isinstance(list_url, str):
        full_list = open(list_url, 'r').read()
        split_list = full_list.split('|')
        finished_list = list(filter(None, split_list))
        return finished_list

# Sort tags into categories, based on provided categories.
def find_tags(tags, search_list):
    tag_list = list()
    i = 0
    while i < len(tags):
        if tags[i] in search_list:
            tag_list.append(tags[i])
        i += 1
    return tag_list

def find_other_tags(tags, search_list):
    tag_list = list()
    i = 0
    while i < len(tags):
        if tags[i] not in search_list:
            tag_list.append(tags[i])
        i += 1
    
    return tag_list

# Starts the search
# Called by Furbot
def start_searching(tags):
    # start by filling all the tag lists.
    gender_tags = find_tags(tags, get_list('tag/gender.txt'))
    fetish_tags = find_tags(tags, get_list('tag/fetishes.txt'))
    pairing_tags = find_tags(tags, get_list('tag/pairings.txt'))
    body_tags = find_tags(tags, get_list('tag/body.txt'))
    act_tags = find_tags(tags, get_list('tag/sex_acts.txt'))
    position_tags = find_tags(tags, get_list('tag/positions.txt'))
    # If it was not caught before, it's not in a previous list.
    other_tags = find_other_tags(tags, gender_tags + fetish_tags + pairing_tags + body_tags + act_tags + position_tags)
    
    fixed_tag_list = gender_tags + fetish_tags + pairing_tags + body_tags + act_tags + position_tags + other_tags

    # Create the short list by slicing 
    short_list = fixed_tag_list[:tag_limit]

    #extra_tags = len(fixed_tag_list) - tag_count
    if len(fixed_tag_list) == tag_limit + 1:
        short_list.append('**^^^^And ^^^^' + str(extra_tags) + ' ^^^^other ^^^^tag**')
    elif len(fixed_tag_list) > tag_limit + 1:
        short_list.append('**^^^^And ^^^^' + str(extra_tags) + ' ^^^^other ^^^^tags**')
    return short_list


