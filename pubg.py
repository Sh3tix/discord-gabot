import requests


api = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxZGM2NTQ1MC1jZjkyLTAxMzgtM2MyZS0yOTY2M2Y3ZDk5YjIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTk5MDgyNTE2LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InNoeXRpeDEyMDItZ21hIn0.mSPPWWLVUrcnv75OY90NtfHfbUWU4Ya4-zCZ-CZzNX8"

header = {
    "Authorization": f"Bearer {api}",
    "Accept": "application/vnd.api+json"
    }

def get_player_id(player):
    url = f"https://api.pubg.com/shards/steam/players?filter[playerNames]={player}"

    r = requests.get(url, headers=header)

    account_id = r.json()["data"][0]["id"]

    return account_id


def get_season_id():
    url = "https://api.pubg.com/shards/steam/seasons"

    r = requests.get(url, headers=header)

    season_id = r.json()["data"][-1]["id"]

    return season_id


def get_player_rank(player_id, season_id):
    url = f"https://api.pubg.com/shards/steam/players/{player_id}/seasons/{season_id}/ranked"

    r = requests.get(url, headers=header)

    tier = r.json()["data"]["attributes"]["rankedGameModeStats"]["squad-fpp"]["currentTier"]["tier"]
    sub_tier = r.json()["data"]["attributes"]["rankedGameModeStats"]["squad-fpp"]["currentTier"]["subTier"]

    rank = f"{tier} {sub_tier}"

    return rank


def get_player_rank_stats(player_id, season_id):

    url = f"https://api.pubg.com/shards/steam/players/{player_id}/seasons/{season_id}/ranked"

    r = requests.get(url, headers=header)

    wins = r.json()["data"]["attributes"]["rankedGameModeStats"]["squad-fpp"]["wins"]
    defeats = r.json()["data"]["attributes"]["rankedGameModeStats"]["squad-fpp"]["roundsPlayed"] - wins
    win_ratio = r.json()["data"]["attributes"]["rankedGameModeStats"]["squad-fpp"]["winRatio"]
    win_ratio = round(win_ratio, 2)

    kills = r.json()["data"]["attributes"]["rankedGameModeStats"]["squad-fpp"]["kills"]
    deaths = r.json()["data"]["attributes"]["rankedGameModeStats"]["squad-fpp"]["deaths"]
    kda = r.json()["data"]["attributes"]["rankedGameModeStats"]["squad-fpp"]["kda"]

    best_rank_point = r.json()["data"]["attributes"]["rankedGameModeStats"]["squad-fpp"]["bestRankPoint"]
    avg_rank = r.json()["data"]["attributes"]["rankedGameModeStats"]["squad-fpp"]["avgRank"]


    return {
    "wins": wins,
    "defeats": defeats,
    "win_ratio": win_ratio,
    "kills": kills,
    "deaths": deaths,
    "kda": kda,
    "best_rank_point": best_rank_point,
    "avg_rank": avg_rank
    }

