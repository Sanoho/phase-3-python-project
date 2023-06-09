import level1, impossible
import os, time, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.models import Base, User, Score


engine = create_engine('sqlite:///hangman_app.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind = engine)
session = Session()

white = "\033[1;37;49m"
red = "\033[1;31;49m"
yellow = "\033[1;33;49m"
green = "\033[1;32;49m"
magenta = "\033[1;35;49m"
cyan = "\033[1;36;49m"

os.system('clear')
opening = ["0.txt", "1.txt", "2.txt", "3.txt", "4.txt", "5.txt", "6.txt", "7.txt"]
jigsaw = ["Jigsaw1.txt", "Jigsaw2.txt"]
jklol = ["jklol1.txt", "jklol2.txt"]
quote = ["I.txt", "IW.txt", "IWA.txt", "IWAN.txt", "IWANT.txt", "IWANTT.txt", "IWANTTO.txt", "IWANTTOP.txt", "IWANTTOPL.txt", "IWANTTOPLA.txt", "IWANTTOPLAY.txt", "IWANTTOPLAYA.txt", "IWANTTOPLAYAG.txt", "IWANTTOPLAYAGA.txt", "IWANTTOPLAYAGAM.txt", "IWANTTOPLAYAGAME.txt", "IWANTTOPLAYAGAME..txt", "IWANTTOPLAYAGAME...txt", "IWANTTOPLAYAGAME....txt", "IWANTTOPLAYAGAME.....txt"]

def animator(filenames, delay = 1, repeat = 4):
    frames = []
    for name in filenames:
        with open (name, 'r', encoding = 'utf8') as f:
            frames.append(f.readlines())
    for i in range(repeat):
        for frame in frames:
            print(''.join(frame))
            time.sleep(delay)
            os.system('clear')
animator(quote, delay = 0.3, repeat = 1)
animator(jigsaw, delay = 0.4)
animator(jklol, delay = 0.4, repeat = 2)
animator(opening, delay = 0.4, repeat = 1)

message = f"""\t\t\t\t\t\t\t\t {green}WELCOME {magenta}TO {green}H{red}A{yellow}N{cyan}G{white}M{magenta}A{green}N{red}!\n
\t\t{white}Hangman is a classic word game in which you must guess as many secret words as you can before you run out of lives!\n"""

def title_typewriter(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.02)
title_typewriter(message)

ask_name = f"\n{magenta}Please enter your username:\n"
def prompt_username(ask_name):
    for char in ask_name:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.04)
prompt_username(ask_name)

username = input(f"{white}")

def find_or_create_user(username):
    user = session.query(User).filter(User.username == username).first()
    if user:
        return user
    else:
        user = User(username = username)
        session.add(user)
        session.commit()
        return user
user = find_or_create_user(username)


def input_username(username):
    welcome_message = f"\n{magenta}Welcome," + f"{white} {username}" + f"{magenta}!" + f"{magenta}\n\nPress {cyan}1 {magenta}to Play {green}H{red}A{yellow}N{cyan}G{white}M{magenta}A{green}N{red} {magenta}or Press {cyan}2 {magenta}to see the Current Leaderboard:\n"
    for char in welcome_message:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.03)
    
input_username(username)

def play():
    decision = input(f"{white}")
    if decision == "1":
        if username == 'wordsmith':
            impossible.main(user, animator)
        else:
            level1.main(user, animator)
    elif decision == "2":
        scores = session.query(Score).order_by(Score.score.desc()).limit(3)
        leaderboard_message = f"\n{white}Here are the top 3 high scores:\n {green}{[score for score in scores]}\n"
        for char in leaderboard_message:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03)
        input_username(username)
        play()
    else:
        print(f'{magenta}That is not a valid input.')
        print(f'{magenta}Press {cyan}1 {magenta}to {white}Play, {magenta}Press {cyan}2 {magenta}to {white}see Current Leaderboard.')
        play()

play()



