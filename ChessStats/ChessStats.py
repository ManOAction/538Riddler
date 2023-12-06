import requests
import time
from icecream import ic
from bs4 import BeautifulSoup

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver import Edge


from webdriver_manager.microsoft import EdgeChromiumDriverManager

options = EdgeOptions()
options.use_chromium = True  # Important for using the chromium version of Edge
options.add_argument("--headless")
options.add_argument("--ignore-certificate-errors")
options.add_argument("--allow-insecure-localhost")
options.add_argument("--log-level=3")

TournamentURL = "https://api.chess.com/pub/tournament/kramnik-039-s-spreadsheet"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


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


ListOfGroups = []
ListOfGameURLS = []
DictOfPlayers = {}


class Player:
    def __init__(self, name):
        self.name = name
        self.MoveCount = 0
        self.TotalMoveTime = 0
        self.AverageMoveTime = 0

    def __str__(self):
        return f"{self.name} {self.MoveCount} {self.TotalMoveTime} {self.AverageMoveTime}"

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

    # ic(f"White Player: {WhitePlayer.name}")
    # ic(f"Black Player: {BlackPlayer.name}")

    url = f"https://www.chess.com/game/daily/{GameNumber}"

    ic(f"Processing this game: {url}")
    driver.get(url)

    time.sleep(5)

    # This is not working correctly, it can't ever find the elements.
    # try:
    #     wait = WebDriverWait(driver, 10)
    #     # wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'move')))
    #     wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'time-white')))
    # except Exception as errmsg:
    #     ic(errmsg)
    #     print("Error waiting for page to load.")
    #     return False
    # finally:
    #     driver.quit()

    soup = BeautifulSoup(driver.page_source, "html.parser")

    for move in soup.find_all("div", class_="move"):
        white_move_div = move.find("div", class_="time-white")
        white_move_time = white_move_div["data-time"] if white_move_div else None

        if white_move_time:
            WhitePlayer.addMove(int(white_move_time))

        black_move_time = (
            move.find("div", class_="time-black")["data-time"]
            if move.find("div", class_="time-black")
            else None
        )
        if black_move_time:
            BlackPlayer.addMove(int(black_move_time))

    return True


def format_time(time):
    seconds = time // 10
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    hours = str(hours).zfill(1)
    minutes = str(minutes).zfill(2)
    seconds = str(seconds).zfill(2)

    return f"{hours}h {minutes}m {seconds}s"


# Fetch Tournament Info
try:
    TournamentInfo = requests.get(TournamentURL, headers=headers).json()
except Exception as errmsg:
    ic(errmsg)
    print("Error converting tournament info to JSON.")
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

# ic(ListOfGroups)

# Here I was overriding the ListOfGroups with a single group to use only the second round.
# ['https://api.chess.com/pub/tournament/fischer-nonrandom/1/1',
# 'https://api.chess.com/pub/tournament/fischer-nonrandom/1/2',
# 'https://api.chess.com/pub/tournament/fischer-nonrandom/2/1']

# ListOfGroups = [
#     "https://api.chess.com/pub/tournament/fischer-nonrandom/2/1",
# ]

for group in ListOfGroups:
    GroupInfo = requests.get(group, headers=headers).json()
    for game in GroupInfo["games"]:
        ListOfGameURLS.append(game["url"])

ListOfGameNumbers = [GameURL.split("/")[-1] for GameURL in ListOfGameURLS]


with Edge(service=Service(EdgeChromiumDriverManager().install()), options=options) as driver:
    for game in ListOfGameNumbers:
        AnalyzeGamePlayingTime(game, driver)


for player in DictOfPlayers.values():
    if player.MoveCount > 0:
        player.RecalcAverageMoveTime()


SortedList = sorted(DictOfPlayers.items(), key=lambda x: x[1].AverageMoveTime, reverse=True)

print(f"{'Player Name':<15} {'Moves':>6} {'Total Time':>15} | {'Avg. Move Time':>15}")
print("-" * 65)

for player_name, player_obj in SortedList:
    formatted_total_time = format_time(player_obj.TotalMoveTime)
    formatted_avg_time = format_time(player_obj.TotalMoveTime // player_obj.MoveCount)
    print(
        f"{player_name:<15} {player_obj.MoveCount:>6} {formatted_total_time:>15} | {formatted_avg_time:>15}"
    )
