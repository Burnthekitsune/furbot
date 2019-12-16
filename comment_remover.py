import praw
bot_name = 'furbot_'
# this removes comments with a negative score


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


def removal():
    # OAuth
    bot = praw.Reddit(user_agent='Fur Bot Comment remover',
                      client_id='w0VJv_O15uALXw',
                      client_secret=get_secret(),
                      username=bot_name,
                      password=get_password())

    for submission in bot.redditor('furbot_').comments.controversial('week'):
        if submission.score < 0:
            print('Score: ' + str(submission.score))
            submission.delete()
