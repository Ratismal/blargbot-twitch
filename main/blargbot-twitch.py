__module_name__ = "blargbot-twitch"
__module_version__ = "0.0.1"
__module_description__ = "Blargbot: Twitch Edition"

import hexchat
from datetime import datetime
import os
import yaml

try_base = False
dir = hexchat.get_info("configdir") + "/addons/blargbot/"

start_time = datetime.now()
eat_faces = False
authed_user = None
conf_dir = hexchat.get_info("configdir") + "/addons/blargbot-twitch.yaml"
if not os.path.isfile(conf_dir):
    f_pass = open(conf_dir, 'a')
    f_pass.write("pass: password\nsong_dir: null")
    f_pass.close()
f_pass = open(conf_dir, "r")
channel = "#hysteriaunleashed"
conf = yaml.load(f_pass)
# print(conf)
print conf["pass"]
password = None
song_dir = None

def reload_config():
    global password
    global song_dir
    global conf
    f_pass = open(conf_dir, "r")
    conf = yaml.load(f_pass)
    password = conf["pass"]
    song_dir = conf["song_dir"]


def say(message):
    hexchat.command("say " + message)


def on_mention(word, word_eol, userdata):
    if "thanks blargcat" in word[1].lower() or "thanks, blargcat" in word[1].lower() or "thank you blargcat" in word[1].lower() or "thank you, blargcat" in word[1].lower():
      say("No problem.")
    elif eat_faces:
        say("\00304I will eat your fucking face, " + hexchat.strip(word[0], len(word[0]), 3) + ".")
    return hexchat.EAT_NONE


def eat():
    global eat_faces
    if eat_faces:
        eat_faces = False
        say("I'm no longer hungry.")
    else:
        eat_faces = True
        say("I'm suddenly really hungry.")


def get_uptime(word):
    time_elapsed = datetime.now() - start_time
    s = time_elapsed.total_seconds()
    days, remainderD = divmod(s, 86400)
    hours, remainderH = divmod(remainderD, 3600)
    minutes, seconds = divmod(remainderH, 60)
    time_string = '%s days %s hours %s minutes %s seconds.' % (int(days), int(hours), int(minutes), int(seconds))
    say("Catter uptime: " + time_string)


def mail_send(word):
    sender = word[0]
    buffer_word = word[1]
    buffer_word = buffer_word.replace("mail send ", "", 1)
    index = buffer_word.index(" ")
    receiver = buffer_word[:index]
    buffer_word = buffer_word.replace(receiver + " ", "", 1)
    global dir
    f = open(dir + receiver.lower() + ".txt", 'a')
    sender = hexchat.strip(sender, len(sender), 3)
    timestamp = datetime.strftime(datetime.now(), '[%m/%d %H:%M] ')
    f.write(timestamp + sender + "> " + buffer_word + "\n")
    f.close()
    say("Message queued: '" + buffer_word + "' from " + sender + " at " + timestamp + ".")


def mail_read(word):
    receiver = word[0]
    receiver = hexchat.strip(receiver, len(receiver), 3)
    global dir
    if os.path.isfile(dir + receiver.lower() + ".txt"):
      f = open(dir + receiver.lower() + ".txt", 'r')
      if os.path.getsize(dir + receiver.lower() + ".txt") > 0:
          say("You received the following messages:")
          for line in f:
              line = line.replace('\n', "")
              say(line)
          say("To delete your messages, type '!mail delete'")
      else:
          say("You have no messages.")
    else:
      say("You have no messages.")

def mail_delete(word):
    receiver = word[0]
    receiver = hexchat.strip(receiver, len(receiver), 3)
    say("Deleting all of " + receiver.lower() + "'s messages")
    global dir
    if os.path.isfile(dir + receiver.lower() + ".txt"):
      f = open(dir + receiver.lower() + ".txt", 'r+')
      f.truncate()
      f.close()


def mail(word):
    if word[1] == "mail help" or word[1] == "mail":
        say("Mail commands: read, send, delete, help")
    elif word[1].startswith("mail send "):
        mail_send(word)
    elif word[1] == "mail read":
        mail_read(word)
    elif word[1] == "mail delete":
        mail_delete(word)
    else:
        say("Unknown command. Too many or too little parameters.")


def base_commands(word, word_eol, userdata):
    if word[1] == "help":
        say("Valid commands: help, currenttime, eat, time, uptime, douptime, version, mail")
    elif word[1] == "time":
        say("blargcat was started at " + datetime.strftime(start_time, '%Y-%m-%d %H:%M:%S'))
    elif word[1] == "currenttime":
        say("The current time for blargcat is " + datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S'))
    elif word[1] == "uptime":
        get_uptime(word)
    elif word[1] == "eat":
        eat()
    # elif word[1] == ".tps":
    #    say("TPS:\0033 19.97")
    # elif word[1] == ".list":
    #    say("\00312Online (2/20): \0034[Admin] \00315blargcat\0031, \0039[Member] \00315FacePolice")
    elif word[1] == "version":
        say("blargcat is running \0039" + __module_name__ + "\0031 version\0039 " + __module_version__)
    elif word[1].startswith("mail"):
        mail(word)
    elif word[1] == "douptime":
        say(".uptime")
    elif word[1] == "test":
        say("Test command received!")


def on_command(word, word_eol, userdata):
    if hexchat.get_info("network") == "Twitch":
      check = hexchat.strip(word[0], len(word[0]), 3).lower()
      if check == "hu_infinity" or check == "blockrim_realms" or check == "bogus_server":
        if '>' in word[1]:
          index = word[1].index('>') + 2
          word[1] = word[1][index:]
      if word[1].startswith(".") or word[1].startswith("!"):
        if word[1].startswith("."):
          word[1] = word[1].replace('.', '', 1)
        else:
          word[1] = word[1].replace('!', '', 1)
        base_commands(word, word_eol, userdata)
    return hexchat.EAT_NONE


if not os.path.exists(dir):
    os.makedirs(dir)

hexchat.hook_print("Channel Msg Hilight", on_mention)
hexchat.hook_print("Channel Message", on_command)


print("Script " + __module_name__ + " version " + __module_version__ + " successfully loaded")

print hexchat.get_info("network")