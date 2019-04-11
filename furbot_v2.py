# -*- coding: utf-8 -*-

import time
import praw
import requests
import tag_helper
import re

# gotta have a user agent for the request
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, '
                  'ike Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
bot_name = 'furbot_'


def get_secret():
    try:
        with open('secret.txt', 'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        print("Secret not found. Please put the secret ID in the new file, secret.txt")
        open('secret.txt', 'x')


# Nor do I share the password. It is in password.txt
def get_password():
    try:
        with open('password.txt', 'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        print("Password not found. Please put a password in the new file, password.txt")
        open('password.txt', 'x')


# The OAuth bit
bot = praw.Reddit(user_agent='Fur Bot v2',
                  client_id='w0VJv_O15uALXw',
                  client_secret=get_secret(),
                  username=bot_name,
                  password=get_password())


# A nice notice that the bot is running
print(str(bot.user.me()) + ' is now running...')
# Some default stuff
subreddit = bot.subreddit('furry_irl+furrystarterpacks+furrypasta')
comments = subreddit.stream.comments()
comment_count = 0
has_commented = False
basic_link = 'https://e621.net/post/atom?tags=order%3Arandom+rating%3Ae+score%3A%3E25'
basic_sfw_link = 'https://e621.net/post/atom?tags=order%3Arandom+rating%3As+score%3A%3E25'
basic_furbot_link = 'https://e621.net/post/atom?tags=order%3Arandom+furbot'


# Prevents the bot from getting spammy.
# Has saved me when the bot replied to itself for a new function.
def wait():
    time.sleep(5)


# Gets the tag blacklist from the tag_file.
def get_blacklist():
    full_list = open('bannedtags.txt', 'r').read()
    split_list = full_list.split('|')
    finished_list = list(filter(None, split_list))
    return finished_list


# Checks comment ID to see if it is new.
def check_id(given_id):
    file = open('id_list.txt', 'r')
    for line in file:
        if given_id in line:
            file.close()
            return False
        else:
            file.close()
            return True


# Gets a link for the bot to reply with.
def get_link(check_url, mode):
    r = requests.get(check_url, headers=header)
    contents = str(r.content)
    sample = 'http://e621.net/post/show/'
    tag_sample = '<entry>'
    source_sample = 'https://static'
    number = contents.find(sample)
    tag_number = contents.find(tag_sample) + 22
    source_number = contents.find(source_sample)
    if number < 0:
        if mode == 'search':
            return ('no results found, you may have an invalid tag, or all posts for your tags have a score below 25'
                    '\n It is also possible no posts have an explicit rating, this bot search for that with this mode.')
        if mode == 'sfw search':
            return ('no results found, you may have an invalid tag, or all posts for your tags have a score below 25'
                    '\n It is also possible no posts have an safe rating, this bot search for that with this mode.')
        if mode == 'mild search':
            return ('no results found, you may have an invalid tag, or all posts for your tags have a score below 25'
                    '\n It is also possible no posts have an questionable rating, this bot search for that with this'
                    ' mode.')
        if mode == 'furbot':
            return 'Sorry, I think something went wrong with e621.'
        if mode == 'e621' or mode == 'e926':
            return 'An error has occurred, ' + mode + ' may be down'
        else:
            return 'Oops, some part of the hidden command broke.'
    else:
        clipped = contents[number:]
        tag_clipped = contents[tag_number:]
        source_clipped = contents[source_number:]
        number_two = clipped.find('\"')
        tag_number_two = tag_clipped.find('<')
        source_number_two = source_clipped.find('\"')
        url = clipped[:number_two]
        post_tags = tag_clipped[:tag_number_two - 1]
        basic_source = source_clipped[:source_number_two]
        if basic_source == 'https://static1.e621.net/images/download-preview.png':
            source = 'flash'
        else:
            source = get_source(url, basic_source)
        if mode == 'e926':
            url = url.replace('e621', 'e926')
            source = source.replace('e621', 'e926')
        url = url.replace('http://', 'https://')
        source = source.replace('http://', 'https://')
        result = url_and_tags(url, source, post_tags)
        return result


# Helper method to find the direct url of the post
def get_source(post_url, sample):
    r = requests.get(post_url, headers=header)
    contents = str(r.content)
    basic_sample = '/preview/'
    post_id_cut_spot = sample.find(basic_sample) + 9
    post_id_part = sample[post_id_cut_spot:]
    post_id_cut_spot_two = post_id_part.find('.')
    post_id = post_id_part[:post_id_cut_spot_two]
    id_length = len(post_id)
    contents_cut_spot = contents.find(post_id)
    contents_cut = contents[contents_cut_spot + id_length + 10:]
    contents_cut_spot = contents_cut.find('https://static1.e621.net/data/' + post_id)
    contents_cut_more = contents_cut[contents_cut_spot:]
    contents_cut_spot = contents_cut_more.find('\"')
    contents_final_cut = contents_cut_more[:contents_cut_spot]
    return contents_final_cut


# Does some cleanup to tag massive tag list and adds it to the URL and sends it back.
# Calls tag_hyper.py to do the sorting
def url_and_tags(url, source, post_tags):
    full_tag_list = post_tags.split()
    if len(full_tag_list) > 25:
        better_tag_list = tag_helper.start_searching(full_tag_list)
        tag_list = " ^^^^".join(better_tag_list)
        tag_list = tag_list.replace('^^^^**', '\n**')
    else:
        tag_list = " ^^^^".join(full_tag_list)
    tag_list = tag_list.replace('_', '\\_')
    tag_list = tag_list.replace('\\xc3\\xa9', 'é')
    body = '\n\n **^^^^Post ^^^^Tags:** ^^^^'
    post_url = '[Post](' + str(url) + ') | '
    source_url = 'Sorry, this is a flash animation. A direct link would download it.'
    if source != 'flash':
        source_url = '[Direct Link](' + str(source) + ')'
    return post_url + source_url + body + tag_list


# Checks if a user has blacklisted themselves.
def check_user(user):
    file = open('userlist.txt', 'r')
    username = str(user)
    for line in file:
        if username in line:
            file.close()
            return False
        else:
            file.close()
            return True


# Checks for people with power over the bot.
def check_approved(user):
    file = open('approved_users.txt', 'r')
    username = str(user)
    for line in file:
        if username in line:
            file.close()
            return True
        else:
            file.close()
            return False


# This is for fun custom stuff with custom_messages.txt
def bonus_message(user):
    file = open('custom_messages.txt', 'r')
    username = str(user).lower()
    user_list = file.readlines()
    found_name = False
    response = ''
    j = 0
    while j < len(user_list) and not found_name:
        message_split = user_list[j].split('|')
        if username == message_split[0].lower():
            response = message_split[1] + '\n\n'
            found_name = True
        j += 1
    file.close()
    return response


# Blacklists a user
def remove_user(user):
    username = str(user)
    user_list = open('userlist.txt', 'a')
    user_list.write(username + '|')
    user_list.close()


# For hidden commands
# Added to allow easier expansion
def hidden_command(comment_body):
    file = open('bonus_commands.txt', 'r')
    file_lines = file.readlines()
    j = 0
    found_hidden_command = False
    comment_mode = ''
    comment_tag = ''
    response = ''
    while j < len(file_lines) and not found_hidden_command:
        message_split = file_lines[j].split('|')
        if ' ' + message_split[0] + ' ' in comment_body:
            found_hidden_command = True
            comment_mode = message_split[1]
            if comment_mode == 'search':
                comment_tag = message_split[2]
                response = message_split[3]
            else:
                response = message_split[2]
        j += 1
    if found_hidden_command:
        full_info = hidden_command_comment(comment_mode, response, comment_tag)
        return full_info
    else:
        return ''


# sets up comments for hidden commands
def hidden_command_comment(comment_mode, response, comment_tag):
    if comment_mode == 'search':
        comment_response = response + get_message('', 'hidden_search', comment_tag)
    else:
        comment_response = response + get_message('', 'hidden_response', '')
    return comment_response


# This makes the reply that the bot gives, this is the real meat of the bot.
def get_message(user_name, mode, search_tags):
    body = 'Something has gone horribly wrong with the code!\n\n---\n\n'
    bonus = bonus_message(user_name)
    if bonus == '':
        if mode == 'e621':
            bonus = 'OwO, what\'s this?\n\n'
        if mode == 'e926':
            bonus = 'Hello! :3\n\n'
    if mode == 'e621':
        body = ('*pounces on ' + str(user_name) + '*'
                '\n\n&nbsp;\n\n I heard you say e621, so have some free porn, '
                'compliments of e621. (obviously nsfw) \n\n' + get_link(link, mode) + '\n\n'
                '---\n\n'
                )
    if mode == 'e926':
        body = ('*hugs ' + str(user_name) + '*'
                '\n\n&nbsp;\n\n I heard you say e926, so have a picture, '
                'compliments of e926. \n\n' + get_link(sfw_link, mode) + '\n\n'
                '---\n\n'
                )
    if mode == 'search' or mode == 'sfw search' or mode == 'mild search':
        tag_list = ' '.join(search_tags)
        body = ('Hi, ' + str(user_name) + '. Here is the results for your search for these search tags:'
                ' \n\n' + tag_list + '\n\n' + get_link(search(search_tags, banned_tag_list, mode), mode) + '\n\n'
                '---\n\n')
    if mode == 'denied':
        body = ('Oops! Mod Daddy will beat me if I search something like that! Sorry!' + '\n\n'
                '---\n\n')
    if mode == 'cheese':
        body = ('Sorry, I am too smart to fall for that one' + '\n\n'
                '---\n\n')
    if mode == 'blacklist':
        body = 'You have been blacklisted. Message Pixel871 if you want messages from the bot again \n\n---\n\n'
    if mode == 'ban':
        body = 'Successfully banned ' + search_tags + 'git reset --hard'
    if mode == 'ban fail':
        body = 'Failed to add to ban list, all tags are on list.\n\n---\n\n'
    if mode == 'not approved':
        body = 'I\'m sorry ' + str(author) + ', I\'m afraid I can\'t do that. \n\n---\n\n'
    if mode == 'hidden_search':
        body = ('\n\n' + get_link(basic_link, mode) + '\n\n'
                '---\n\n')
    if mode == 'hidden_response':
        body = '\n\n---\n\n'
    if mode == 'owo':
        body = 'Congratulations, ' + str(author) + '! That was the **' + get_owo_count() + 'th** owo since I ' \
                'started to track them.\n\n---\n\n'
    if mode == 'furbot':
        body = '\>///< Okay, I guess if you want to see me. \n\n' + get_link(basic_furbot_link, mode) + '\n\n---\n\n'
    if mode == 'good bot':
        body = 'Thank you, ' + author + '! I am glad I could be helpful. \\^^\n\n---\n\n'
    if mode == 'bad bot':
        body = 'I am sorry to disappoint you ' + author + ', but it isn\' my fault. I just do what I am told.' \
               '\n\n---\n\n'
    footer = ('**^^^OwO Count: ' + get_owo_count() + '** \n\n I am a bot, this is done automatically in furry_irl. '
              'To blacklist yourself, say "furbot blacklist me". Comments from this bot that go below 0 will be deleted'
              '. \n\nCheck out my [profile](https://www.reddit.com/user/furbot_/) for commands'
              ', bug reports, feature requests, and news.'
              ' I am made by Pixel871, contact him if something happens to me.')
    full_message = bonus + body + " ^^^".join(footer.split())
    return full_message


# Adds an ID to the list.
# Sadly due to PRAW, this is the best way to record comments the bot has replied to.
# Checking comment replies doesn't always work if a comment has a lot of replies
def add_id(id_to_add):
    add = open('id_list.txt', 'a')
    add.write(str(id_to_add) + '|')
    add.close()


# No impure tags allowed.
# If a tag is blacklisted, this stops it from being searched.
def check_tag(tag, banned_tags):
        if tag in banned_tags:
            print(tag + ' found')
            return False
        else:
            return True


# Prevents people from altering a search parameters.
def check_cheese(tag):
    if 'score' in tag:
        return True
    else:
        return False


# Adds the blacklist to a search.
def apply_blacklist(banned_tags):
    return '+-' + '+-'.join(banned_tags)


# Does some tweaking to the search.
def search(search_tags, banned_tags, mode):
    basic_url = 'https://e621.net/post/atom?tags=order%3Arandom+score%3A%3E25'
    if mode == 'search':
        basic_url += '+rating%3Ae+'
    if mode == 'sfw search':
        basic_url += '+rating%3As+'
    if mode == 'mild search':
        basic_url += '+rating%3Aq+'
    taglist = '+'.join(search_tags)
    blacklist = '+-' + '+-'.join(banned_tags)
    url = basic_url + taglist + blacklist
    return url


# Adds a tag to the blacklist.
def add_to_blacklist(tag):
    taglist = open('bannedtags.txt', 'a')
    taglist.write(str(tag) + '|')
    taglist.close()


# Adds 1 owo to the counter.
def owo_counter():
    owo_number = int(get_owo_count())
    owo_number += 1
    file = open('owo.txt', 'w')
    file.write(str(owo_number))
    file.close()


# Counts the number of owo's
def get_owo_count():
    file = open('owo.txt', 'r')
    owo_number = file.readline()
    file.close()
    return owo_number


# Checks for owo and replies if it is divisible by 100.
def check_owo(owo_comment):
    owo_text = owo_comment.body
    if 'owo' in owo_text.lower() or '0w0' in owo_text.lower():
        owo_counter()
        owo_num = int(get_owo_count())
        if owo_num % 100 == 0:
            owo_message = get_message(comment.author, 'owo', '')
            owo_comment.reply(owo_message)
            print(str(owo_comment.author) + ' has said the ' + str(owo_num) + 'th owo!')
            add_owo_list(owo_num, str(owo_comment.author))


# adds an owo number and username to the scoreboard
def add_owo_list(owo_num, username):
    username = '/u/' + username.replace('\\_', '_')
    if owo_num % 10 == 1:
        owo_value = str(owo_num) + 'st'
    else:
        owo_value = str(owo_num) + 'th'
    add = open('owo_leaderboard.txt', 'a')
    add.write('* ' + owo_value + ' - ' + username)
    add.close()


# The bot itself.
# Due to how I have changed it, it doesn't need the try, but as soon as I remove it, it crashes.
# So it stays, as it doesn't alter anything.
try:
    banned_tag_list = get_blacklist()
    link = basic_link + apply_blacklist(banned_tag_list)
    sfw_link = basic_sfw_link + apply_blacklist(banned_tag_list)
    for comment in comments:
        text = comment.body
        author = str(comment.author)
        author = author.replace('_', '\\_')
        comment_id = comment.id
        comment_id = re.sub('[^0-9a-zA-Z]+', '*', comment_id)
        if has_commented:
            wait()
            has_commented = False
        if 'furbot blacklist me' in text.lower():
            if check_user(author):
                remove_user(author)
                print(str(author) + ' has been blacklisted')
                message = get_message(author, 'blacklist', '')
                comment.reply(message)
        elif 'furbot search furbot' in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(comment)
                has_commented = True
                add_id(comment_id)
                comment_count += 1
                print(comment_count)
                message = get_message(author, 'furbot', '')
                comment.reply(message)
        elif 'furbot search ' in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(comment)
                add_id(comment_id)
                full = text
                command = 'furbot search'
                lines = full.split('\n')
                i = 0
                found_command = False
                command_line = ''
                while i < len(lines) and not found_command:
                    current_line = lines[i].lower().find(command)
                    if current_line != -1:
                        command_line = lines[i]
                        found_command = True
                    i += 1
                command_line = command_line.replace('.', '')
                command_line = command_line.replace(',', '')
                cut_spot = command_line.lower().find(command) + 14
                cut = command_line[cut_spot:]
                tags = cut.split()
                pure = True
                cheese = False
                i = 0
                while i < len(tags) and pure:
                    pure = check_tag(tags[i], banned_tag_list)
                    cheese = check_cheese(tags[i])
                    i += 1
                if pure and not cheese:
                    message = get_message(author, 'search', tags)
                    comment.reply(message)
                    comment_count += 1
                    print(comment_count)
                    wait()
                elif not pure:
                    message = get_message(author, 'denied', tags)
                    comment.reply(message)
                    comment_count += 1
                    print(comment_count)
                    wait()
                elif cheese:
                    message = get_message(author, 'cheese', tags)
                    comment.reply(message)
                    comment_count += 1
                    print(comment_count)
                    wait()
        elif 'furbot sfw search ' in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(comment)
                add_id(comment_id)
                full = text
                command = 'furbot sfw search'
                lines = full.split('\n')
                i = 0
                found_command = False
                command_line = ''
                while i < len(lines) and not found_command:
                    current_line = lines[i].lower().find(command)
                    if current_line != -1:
                        command_line = lines[i]
                        found_command = True
                    i += 1
                command_line = command_line.replace('.', '')
                command_line = command_line.replace(',', '')
                cut_spot = command_line.lower().find(command) + 18
                cut = command_line[cut_spot:]
                tags = cut.split()
                pure = True
                cheese = False
                i = 0
                while i < len(tags) and pure and not cheese:
                    pure = check_tag(tags[i], banned_tag_list)
                    cheese = check_cheese(tags[i])
                    i += 1
                if pure and not cheese:
                    message = get_message(author, 'sfw search', tags)
                    message = message.replace('e621.net', 'e926.net')
                    comment.reply(message)
                    comment_count += 1
                    print(comment_count)
                    wait()
                elif not pure:
                    message = get_message(author, 'denied', tags)
                    comment.reply(message)
                    comment_count += 1
                    print(comment_count)
                    wait()
                elif cheese:
                    message = get_message(author, 'cheese', tags)
                    comment.reply(message)
                    comment_count += 1
                    print(comment_count)
                    wait()
        elif 'furbot mild search ' in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(comment)
                add_id(comment_id)
                full = text
                command = 'furbot mild search'
                lines = full.split('\n')
                i = 0
                found_command = False
                command_line = ''
                while i < len(lines) and not found_command:
                    current_line = lines[i].lower().find(command)
                    if current_line != -1:
                        command_line = lines[i]
                        found_command = True
                    i += 1
                command_line = command_line.replace('.', '')
                command_line = command_line.replace(',', '')
                cut_spot = command_line.lower().find(command) + 19
                cut = command_line[cut_spot:]
                tags = cut.split()
                pure = True
                cheese = False
                i = 0
                while i < len(tags) and pure and not cheese:
                    pure = check_tag(tags[i], banned_tag_list)
                    cheese = check_cheese(tags[i])
                    i += 1
                if pure and not cheese:
                    message = get_message(author, 'mild search', tags)
                    comment.reply(message)
                    comment_count += 1
                    print(comment_count)
                    wait()
                elif not pure:
                    message = get_message(author, 'denied', tags)
                    comment.reply(message)
                    comment_count += 1
                    print(comment_count)
                    wait()
                elif cheese:
                    message = get_message(author, 'cheese', tags)
                    comment.reply(message)
                    comment_count += 1
                    print(comment_count)
                    wait()
        elif 'e621' in text.lower() and 'http' not in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(comment)
                has_commented = True
                add_id(comment_id)
                comment_count += 1
                print(comment_count)
                message = get_message(author, 'e621', '')
                comment.reply(message)
        elif 'e926' in text.lower() and 'http' not in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(comment)
                has_commented = True
                add_id(comment_id)
                comment_count += 1
                print(comment_count)
                message = get_message(author, 'e926', '')
                comment.reply(message)
        elif 'good bot' in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(comment)
                parent = comment.parent()
                if str(parent.author) == bot_name:
                    has_commented = True
                    print("Good bot")
                    add_id(comment_id)
                    message = get_message(author, 'good bot', '')
                    comment.reply(message)
        elif 'bad bot' in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(comment)
                parent = comment.parent()
                if str(parent.author) == bot_name:
                    has_commented = True
                    print("Bad bot")
                    add_id(comment_id)
                    message = get_message(author, 'bad bot', '')
                    comment.reply(message)
        elif str(author) == 'furbot_' and comment.score < 0:
            print('comment delete')
            comment.delete()
        elif 'furbot ban' in text.lower() and check_id(comment_id):
            if check_approved(author):
                command = 'furbot ban'
                full = text
                cut_spot = full.lower().find(command) + 14
                cut = full[cut_spot:]
                cut_spot = cut.find('\n')
                if cut_spot == -1:
                    tags = cut.split()
                else:
                    final_cut = cut[:cut_spot]
                    stripped = final_cut.strip()
                    tags = stripped.split()
                    tags = [i for i in tags if i != '']
                i = 0
                newly_banned_tags = ''
                while i < len(tags):
                    new_tag = check_tag(tags[i], banned_tag_list)
                    if new_tag:
                        add_to_blacklist(tags[i])
                        newly_banned_tags += tags[i] + ' '
                    i += 1
                banned_tag_list = get_blacklist()
                if newly_banned_tags != '':
                    message = get_message(author, 'ban', newly_banned_tags)
                    print('banned ' + newly_banned_tags)
                    comment.reply(message)
                else:
                    message = get_message(author, 'ban fail', newly_banned_tags)
                add_id(comment_id)
                comment.reply(message)
            else:
                message = get_message(author, 'not approved', '')
                add_id(comment_id)
                comment.reply(message)
                comment_count += 1
                print(comment_count)
                has_commented = True
        elif check_id(comment_id) and check_user(author):
            check_hidden_command = hidden_command(text.lower())
            if check_hidden_command != '':
                add_id(comment_id)
                check_owo(comment)
                comment.reply(check_hidden_command)
                has_commented = True
        elif check_id(comment_id) and ('owo' in text.lower() or '0w0' in text.lower()):
                if check_user(author):
                    add_id(comment_id)
                    check_owo(comment)
except requests.exceptions.HTTPError as e:
    print('waiting...')
    wait()
