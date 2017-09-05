import praw
import requests
import time

# it sort of works XD


def get_secret():
    try:
        with open('secret.txt', 'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        print("Secret not found.")


def get_password():
    try:
        with open('password.txt', 'r') as file:
            return file.readline().strip()
    except FileNotFoundError:
        print("Password not found.")

bot = praw.Reddit(user_agent='Fur Bot v2',
                  client_id='w0VJv_O15uALXw',
                  client_secret=get_secret(),
                  username='furbot_',
                  password=get_password())

print(str(bot.user.me()) + ' is now running...')

subreddit = bot.subreddit('furry_irl')
comments = subreddit.stream.comments()
comment_count = 0
has_commented = False
basic_link = 'https://e621.net/post/atom?tags=order%3Arandom+rating%3Ae+-mlp+score%3A%3E25'
basic_sfw_link = 'https://e621.net/post/atom?tags=order%3Arandom+rating%3As+-mlp+score%3A%3E25'
wolf_link = 'https://e621.net/post/atom?tags=order%3Arandom+rating%3Ae+-mlp+score%3A%3E25+wolfthorn_(old_spice)'
tag_file = 'bannedtags.txt'


def wait():
    time.sleep(150)


def is_running():
    return True


def get_blacklist():
    full_list = open(tag_file).read()
    split_list = full_list.split('|')
    finished_list = list(filter(None, split_list))
    return finished_list


def check_id(given_id):
    file = open('id_list.txt', 'r')
    for line in file:
        if given_id in line:
            file.close()
            return False
        else:
            file.close()
            return True


def get_link(check_url, mode):
    r = requests.get(check_url)
    contents = str(r.content)
    sample = 'http://e621.net/post/show/'
    tag_sample = '<entry>'
    number = contents.find(sample)
    tag_number = contents.find(tag_sample) + 22
    if number < 0:
        if mode == 'search':
            return ('no results found, you may have an invalid tag, or all posts for your tags have a score below 25'
                    '\n It is also possible no posts have an explicit rating, this bot search for that bt default.')
        if mode == 'e621' or mode == 'e926':
            return 'An error has occurred, ' + mode + ' may be down'
        if mode == 'wolfthorn':
            return 'Oops, Wolfthorn cannot be found. He must be in the shower or something.'
    else:
        clipped = contents[number:]
        tag_clipped = contents[tag_number:]
        number_two = clipped.find('\"')
        tag_number_two = tag_clipped.find('<')
        url = clipped[:number_two]
        post_tags = tag_clipped[:tag_number_two]
        if mode == 'e926':
            url = url.replace('e621', 'e926')
        result = url_and_tags(url, post_tags)
        return result


def url_and_tags(url, post_tags):
    tag_list = " ^^^^".join(post_tags.split())
    tag_list = tag_list.replace('_', '\\_')
    tag_list = tag_list.replace('\\xc3\\xa9', 'é')
    body = '\n\n **^^^^Post ^^^^Tags:** ^^^^'
    return url + body + tag_list


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


# Checks for people with power over the bot
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


def remove_user(user):
    username = str(user)
    user_list = open('userlist.txt', 'a')
    user_list.write(username + '|')
    user_list.close()


def get_message(user_name, mode, search_tags, banned_tag):
    body = 'Something has gone horribly wrong with the code'
    if mode == 'e621':
        body = ('OwO, what\'s this? \n\n *pounces on ' + str(user_name) + '*'
                '\n\n&nbsp;\n\n I heard you say e621, so have some free porn, '
                'compliments of e621. (obviously nsfw) \n\n' + get_link(link, mode) + '\n\n'
                '---\n\n'
                )
    if mode == 'e926':
        body = ('Hello! :3 \n\n *hugs ' + str(user_name) + '*'
                '\n\n&nbsp;\n\n I heard you say e926, so have a picture, '
                'compliments of e926. \n\n' + get_link(sfw_link, mode) + '\n\n'
                '---\n\n'
                )
    if mode == 'search':
        tag_list = ' '.join(search_tags)
        body = ('Hi, ' + str(user_name) + '. Here is the results for your search for these search tags:'
                ' \n\n' + tag_list + '\n\n' + get_link(search(search_tags, banned_tag), mode) + '\n\n'
                '---\n\n')
    if mode == 'denied':
        body = ('Oops! Mod Daddy will beat me if I search something like that! Sorry!' + '\n\n'
                '---\n\n')
    if mode == 'blacklist':
        body = 'You have been blacklisted. Message Pixel871 if you want messages from the bot again \n\n---\n\n'
    if mode == 'ban':
        body = 'Successfully banned ' + search_tags + '\n\n---\n\n'
    if mode == 'ban fail':
        body = 'Failed to add to ban list, all tags are on list.\n\n---\n\n'
    if mode == 'not approved':
        body = 'I\'m sorry ' + str(author) + ', I\'m afraid I can\'t do that. \n\n---\n\n'
    if mode == 'wolfthorn':
        body = ('OwO Did I hear you mention Wolfthorn? \n\n&nbsp;\n\n Here is a picture of him '
                'compliments of e621. (obviously nsfw) \n\n' + get_link(wolf_link, mode) + '\n\n'
                '---\n\n'
                )
    footer = ('^^^OwO Count: ' + get_owo_count() + '\n\n^^^I am a bot, this is done automatically in furry_irl. What '
              'porn I post is random I was written as part of a joke, but as that joke '
              'failed, I was repurposed for another joke. if the bot goes rogue, '
              'shoot a message to Pixel871. '
              'To blacklist yourself, say "furbot stop". Comments from this bot that go below 0 will be deleted. \n\n'
              'Check out my [profile](https://www.reddit.com/user/furbot_/) for commands'
              ', bug reports, feature requests, and news')
    # split() returns a list of words, join() puts it back together
    full_message = body + " ^^^".join(footer.split())
    return full_message


def add_id(id_to_add):
    add = open('id_list.txt', 'a')
    add.write(str(id_to_add) + '|')
    add.close()


# no impure tags allowed :P
def check_tag(tag, banned_tags):
        if tag in banned_tags:
            print(tag + ' found')
            return False
        else:
            return True


def apply_blacklist(banned_tags):
    return '+-' + '+-'.join(banned_tags)


def search(search_tags, banned_tags):
    basic_url = 'https://e621.net/post/atom?tags=order%3Arandom+rating%3Ae+score%3A%3E25+'
    taglist = '+'.join(search_tags)
    blacklist = '+-' + '+-'.join(banned_tags)
    url = basic_url + taglist + blacklist
    return url


def add_to_blacklist(tag):
    taglist = open('bannedtags.txt', 'a')
    taglist.write(str(tag) + '|')
    taglist.close()


def owo_counter():
    owo_number = int(get_owo_count())
    owo_number += 1
    file = open('owo.txt', 'w')
    file.write(str(owo_number))
    file.close()


def get_owo_count():
    file = open('owo.txt', 'r')
    owo_number = file.readline()
    file.close()
    return owo_number


def check_owo(body):
    if 'owo' in body.lower() or '0w0' in body.lower():
        get_owo_count()


try:
    banned_tag_list = get_blacklist()
    link = basic_link + apply_blacklist(banned_tag_list)
    sfw_link = basic_sfw_link + apply_blacklist(banned_tag_list)
    for comment in comments:
        text = comment.body
        author = comment.author
        comment_id = comment.id
        if has_commented:
            wait()
            has_commented = False
        if 'furbot stop' in text.lower():
            if check_user(author):
                remove_user(author)
                print(str(author) + ' has been blacklisted')
                message = get_message(author, 'blacklist', '', banned_tag_list)
                comment.reply(message)
        if 'furbot search' in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(text)
                full = str(comment.body)
                add_id(comment_id)
                command = 'furbot search'
                lines = full.split('\n')
                i = 0
                found_command = False
                while i < len(lines) and not found_command:
                    current_line = lines[i].lower().find(command)
                    if current_line != -1:
                        command_line = lines[current_line]
                        found_command = True
                cut_spot = command_line.lower().find(command) + 14
                cut = command_line[cut_spot:]
                tags = cut.split()
                pure = True
                i = 0
                while i < len(tags) and pure:
                    pure = check_tag(tags[i], banned_tag_list)
                    i += 1
                if pure:
                    message = get_message(author, 'search', tags, banned_tag_list)
                    comment.reply(message)
                    comment_count += 1
                    print(comment_count)
                    wait()
                else:
                    message = get_message(author, 'denied', tags, banned_tag_list)
                    comment.reply(message)
                    comment_count += 1
                    print(comment_count)
                    wait()
        if 'e621' in text.lower() and 'http' not in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(text)
                has_commented = True
                comment_count += 1
                print(comment_count)
                message = get_message(author, 'e621', '', banned_tag_list)
                comment.reply(message)
                add_id(comment_id)
        if 'e926' in text.lower() and 'http' not in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(text)
                has_commented = True
                comment_count += 1
                print(comment_count)
                message = get_message(author, 'e926', '', banned_tag_list)
                comment.reply(message)
                add_id(comment_id)
        if 'wolfthorn' in text.lower() and 'http' not in text.lower():
            if check_id(comment_id) and check_user(author):
                check_owo(text)
                has_commented = True
                comment_count += 1
                print(comment_count)
                message = get_message(author, 'wolfthorn', '', banned_tag_list)
                comment.reply(message)
                add_id(comment_id)
        if str(author) == 'furbot_' and comment.score < 0:
            print('comment delete')
            comment.delete()
        if 'furbot ban' in text.lower() and check_id(comment_id):
            if check_approved(author):
                command = 'furbot ban'
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
                    message = get_message(author, 'ban', newly_banned_tags, '')
                    print('banned ' + newly_banned_tags)
                    comment.reply(message)
                else:
                    message = get_message(author, 'ban fail', newly_banned_tags, '')
                add_id(comment_id)
                comment.reply(message)
            else:
                message = get_message(author, 'not approved', '', '')
                add_id(comment_id)
                comment.reply(message)
                comment_count += 1
                print(comment_count)
                has_commented = True
        if check_id(comment_id) and ('owo' in text.lower() or '0w0' in text.lower()):
            if check_user(author):
                owo_counter()
                add_id(comment_id)
except requests.exceptions.HTTPError as e:
    print('waiting...')
    wait()
