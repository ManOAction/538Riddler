import requests
import time
from icecream import ic
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.EdgeOptions()
options.use_chromium = True  # This line is important as Edge has a non-chromium and a chromium version
options.headless = True
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-insecure-localhost')
options.add_argument('--log-level=3')

#
# The Tournament ID is the last part of the URL, then you need to rephrease it in this format:
# https://www.chess.com/tournament/-33rd-chesscom-quick-knockouts-1401-1600
# Transfers into: https://api.chess.com/pub/tournament/-33rd-chesscom-quick-knockouts-1401-1600
# This one of ours https://www.chess.com/tournament/regular-chess-4
# Transfers into: https://api.chess.com/pub/tournament/regular-chess-4
# https://api.chess.com/pub/tournament/{url-ID}

# god-bless-with-true
# checkers-is-for-tramps
# pop-acta-chess-tournament


TournamentURL = "https://api.chess.com/pub/tournament/fischer-nonrandom"  # Remember to change this to api.chess instead of www.chess
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


ListOfGroups = []
ListOfGameURLS = []
DictOfPlayers = {}

# Make class of player
class Player:
    def __init__(self, name):
        self.name = name
        self.MoveCount = 0
        self.TotalMoveTime = 0
        self.AverageMoveTime = 0

    def __str__(self):
        return f"{self.name} {self.MoveCount} {self.TotalMoveTime} {self.AverageMoveTime}"

    # Make method to append a move to the move count
    def addMove(self, MoveTime):
        self.MoveCount += 1
        self.TotalMoveTime += MoveTime

    def RecalcAverageMoveTime(self):
        self.AverageMoveTime = round((self.TotalMoveTime / self.MoveCount / 10 / 60 / 60), 2)


def AnalyzeGamePlayingTime(GameNumber, driver):
    url = f"https://www.chess.com/callback/daily/game/{GameNumber}"
    GameInfo = requests.get(url, headers=headers).json()

    WhitePlayer = DictOfPlayers.get(f"{GameInfo['game']['pgnHeaders']['White'].lower()}")
    BlackPlayer = DictOfPlayers[f"{GameInfo['game']['pgnHeaders']['Black'].lower()}"]

    # print(f"White Player: {WhitePlayer.name}")
    # print(f"Black Player: {BlackPlayer.name}")

    url = f"https://www.chess.com/game/daily/{GameNumber}"

    ic(f"Processing this game: {url}")
    driver.get(url)

    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for move in soup.find_all('div', class_='move'):
        white_move_div = move.find('div', class_='time-white')
        white_move_time = white_move_div['data-time'] if white_move_div else None

        if white_move_time:
            WhitePlayer.addMove(int(white_move_time))

        black_move_time = move.find('div', class_='time-black')['data-time'] if move.find('div', class_='time-black') else None
        if black_move_time:
            BlackPlayer.addMove(int(black_move_time))

    return True


TournamentInfo = requests.get(TournamentURL, headers=headers)
try:
    TournamentInfo = TournamentInfo.json()
except Exception as errmsg:
    ic(errmsg)
    print("Error converting Tourney Info to JSON.")
    ic(TournamentInfo)
    ic(TournamentInfo.text)
    exit()

# Instantiate Player Classes
for player in TournamentInfo["players"]:
    name = player["username"]
    DictOfPlayers[name] = Player(name)

# ic(DictOfPlayers)

# Get all the game URLs
for GameRound in TournamentInfo["rounds"]:
    RoundInfo = requests.get(GameRound, headers=headers).json()

    for group in RoundInfo["groups"]:
        ListOfGroups.append(group)

for group in ListOfGroups:
    GroupInfo = requests.get(group, headers=headers).json()
    for game in GroupInfo["games"]:
        ListOfGameURLS.append(game["url"])

ListOfGameNumbers = [GameURL.split('/')[-1] for GameURL in ListOfGameURLS]

# Analyze the average playing times in the tournament
with webdriver.Edge(options=options) as driver:
    for game in ListOfGameNumbers:
        AnalyzeGamePlayingTime(game, driver)

# Recalculate Average Move Time for All Players in Dict
for player in DictOfPlayers.values():
    player.RecalcAverageMoveTime()

# Sort the Dict by Average Move Time
SortedList = sorted(DictOfPlayers.items(), key=lambda x: x[1].AverageMoveTime, reverse=True)

# Print the Sorted Dict0
for player_name, player_obj in SortedList:
    print(player_name, player_obj.MoveCount, player_obj.TotalMoveTime, player_obj.AverageMoveTime)
