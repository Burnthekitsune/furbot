import praw
import requests
import time

# it sort of works XD
# thanks for silentclowd for code help

bot = praw.Reddit(user_agent='Fur Bot v2',
                  client_id='w0VJv_O15uALXw',
                  client_secret='secret',
                  username='furbot_',
                  password='password')

print(str(bot.user.me()) + ' is now running...')

subreddit = bot.subreddit('furry_irl')

comments = subreddit.stream.comments()

comment_count = 0

has_commented = False

search_url = 'https://e621.net/post/atom?tags=order%3Arandom+rating%3Ae+-mlp+-gore+-scat+-feral+-cub+score%3A%3E100'


def wait():
    time.sleep(600)


def check_id(given_id):
    file = open('id_list.txt', 'r')
    for line in file:
        if given_id in line:
            file.close()
            return False
        else:
            file.close()
            return True


def get_link():
    r = requests.get(search_url)
    contents = str(r.content)
    sample = 'http://e621.net/post/show/'
    number = contents.find(sample)
    clipped = contents[number:]
    number_two = clipped.find('\"')
    url = clipped[:number_two]
    return url


def check_user(user):
    with open('userlist.txt', 'r') as file:
        username = str(user)
        for line in file:
            if username in line:
                return False


def remove_user(user):
    username = str(user)
    with open('userlist.txt', 'a') as user_list:
        user_list.write(username + '|')


def get_message(user_name):
    body = ('OwO, what\'s this? \n\n *pounces on ' + str(user_name) + '*'
            '\n\n&nbsp;\n\n I heard you say e621, so have some free, porn, '
            'compliments of e621. (obviously nsfw) \n\n' + get_link() + '\n\n'
            '---\n\n'
            )
    footer = ('I am a bot, this is done automatically in furry_irl. What porn '
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


for comment in comments:
    text = comment.body
    author = comment.author
    if has_commented:
        wait()
        has_commented = False
    if 'e621' in text.lower():
        comment_id = comment.id
        if 'http' in text.lower():
            add_id(comment_id)
        else:
            if check_id(comment_id) and check_user(author):
                has_commented = True
                comment_count += 1
                print(comment_count)
                message = get_message(author)
                comment.reply(message)
                add_id(comment_id)
    if 'furbot stop' in text.lower():
        if check_user(author):
            remove_user(author)
            print(str(author) + ' has been blacklisted')
            comment.reply('Adding you to the blacklist, as you request')
            add_id(comment_id)
    if str(author) == 'furbot_' and comment.score < 0:
        comment.delete()

