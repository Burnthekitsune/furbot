import urllib

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

search_url = 'https://e621.net/post/atom?tags=order%3Arandom+rating%3Ae+-mlp+-gore+-scat+-feral+-cub+score%3A%3E100'


def wait():
    time.sleep(300)


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
    number = contents.find(sample)
    if number < 0:
        if mode == 'e621':
            return 'And error has occurred, e621 may be down'
        if mode == 'search':
            return 'no results found, you may have an invalid tag. Or all posts for your tags have a score below 100'
    else:
        clipped = contents[number:]
        number_two = clipped.find('\"')
        url = clipped[:number_two]
        return url


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


def remove_user(user):
    username = str(user)
    user_list = open('userlist.txt', 'a')
    user_list.write(username + '|')
    user_list.close()


def get_message(user_name, mode, search_tags):
    if mode == 'e621':
        body = ('OwO, what\'s this? \n\n *pounces on ' + str(user_name) + '*'
                '\n\n&nbsp;\n\n I heard you say e621, so have some free, porn, '
                'compliments of e621. (obviously nsfw) \n\n' + get_link(search_url, mode) + '\n\n'
                '---\n\n'
                )
    if mode == 'search':
        tag_list = ' '.join(search_tags)
        body = ('Hi, ' + str(user_name) + '. Here is the results for your search for these search tags:'
                ' \n\n' + tag_list + '\n\n' + get_link(search(search_tags), mode) + '\n\n'
                '---\n\n')
    if mode == 'denied':
        body = ('Oops! Mod Daddy will beat me if I search something like that! Sorry!)' + '\n\n'
                '---\n\n')
    if mode == 'blacklist':
        body = 'You have been blacklisted. Message Pixel871 if you want messages from the bot again \n\n---\n\n'
    footer = ('&nbsp; I am a bot, this is done automatically in furry_irl. What porn '
              'I post is random I was written as part of a joke, but as that joke '
              'failed, I was repurposed for another joke. if the bot goes rogue, '
              'shoot a message to Pixel871. '
              'To blacklist yourself, say "furbot stop". Comments from this bot that go below 0 will be deleted.')

    # split() returns a list of words, join() puts it back together
    full_message = body + " ^^^".join(footer.split())
    return full_message


def add_id(id_to_add):
    add = open('id_list.txt', 'a')
    add.write(str(id_to_add) + '|')
    add.close()


# no impure tags allowed :P
def check_tag(tag):
    file = open('bannedtags.txt', 'r')
    tag_name = str(tag)
    for line in file:
        if tag_name in line:
            file.close()
            return False
        else:
            file.close()
            return True


def search(search_tags):
    basic_url = 'https://e621.net/post/atom?tags=order%3Arandom+rating%3Ae+score%3A%3E100+'
    taglist = '+'.join(search_tags)
    blacklist = '+-gore+-scat+-feral+-cub'
    url = basic_url + taglist + blacklist
    return url


try:
    for comment in comments:
        text = comment.body
        author = comment.author
        comment_id = comment.id
        if has_commented:
            wait()
            has_commented = False
        if 'e621' in text.lower():
            if 'http' in text.lower() and check_id(comment_id):
                add_id(comment_id)
            else:
                if check_id(comment_id) and check_user(author):
                    has_commented = True
                    comment_count += 1
                    print(comment_count)
                    message = get_message(author, 'e621', '')
                    comment.reply(message)
                    add_id(comment_id)
        if 'furbot stop' in text.lower():
            if check_user(author):
                remove_user(author)
                print(str(author) + ' has been blacklisted')
                message = get_message(author, 'blacklist', '')
                comment.reply(message)
        if 'furbot search' in text.lower():
            if check_id(comment_id) and check_user(author):
                full = str(comment.body)
                command = 'furbot search'
                cut_spot = full.find(command) + 14
                cut = full[cut_spot:]
                cut_spot = cut.find('\n')
                if cut_spot == -1:
                    tags = cut.split()
                else:
                    final_cut = cut[:cut_spot]
                    stripped = final_cut.strip()
                    tags = stripped.split()
                pure = True
                i = 0
                while i < len(tags) and pure:
                    pure = check_tag(tags[i])
                    i += 1
                if pure:
                    message = get_message(author, 'search', tags)
                    comment.reply(message)
                    add_id(comment_id)
                    comment_count += 1
                    print(comment_count)
                    wait()
                else:
                    message = get_message(author, 'denied', tags)
                    comment.reply(message)
                    add_id(comment_id)
                    comment_count += 1
                    print(comment_count)
                    wait()
        if str(author) == 'furbot_' and comment.score < 0:
            print('comment delete')
            comment.delete()
except urllib.error.URLError as e:
    print('waiting...')
    wait()
