import praw
import requests
import time

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


def get_message(user_name):
    text1 = 'OwO, what\'s this? \n\n *pounces on ' + str(user_name) + '*'
    text2 = '\n\n&nbsp;\n\n I heard you say e621, so have some free, porn, compliments of e621. (obviously nsfw) \n\n'
    text3 = get_link()
    text_break = '---'
    text4 = '\n\n&nbsp;\n\n^^^^I ^^^^am ^^^^a ^^^^bot, ' \
            '^^^^this ^^^^is ^^^^done ^^^^automatically ^^^^in ^^^^furry_irl.' \
            ' ^^^^What ^^^^porn ^^^^I ^^^^post ^^^^is ^^^^random'
    text5 = '\n^^^^I ^^^^was ^^^^written ^^^^as ^^^^part ^^^^of ^^^^a ^^^^joke, ' \
            '^^^^but ^^^^as ^^^^that ^^^^joke ^^^^failed, ' \
            '^^^^I ^^^^was ^^^^repurposed ^^^^for ^^^^another ^^^^joke.'
    text6 = '\n^^^^if ^^^^the ^^^^bot ^^^^goes ^^^^rogue ^^^^or ^^^^the ^^^^mods ^^^^of' \
            ' ^^^^furry_irl ^^^^want ^^^^it ^^^^shut ^^^^down,' \
            ' ^^^^shoot ^^^^a ^^^^message ^^^^to ^^^^Pixel871'
    text7 = '\n^^^^To ^^^^blacklist ^^^^yourself, ^^^^say ^^^^\'furbot stop\''
    full_message = text1 + text2 + text3 + text_break + text4 + text5 + text6 + text7
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
