import requests
from cookies import swid, s2

year = '2022'
ID = '1649664'
url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/2022/segments/0/leagues/1213692?forTeamId=12&scoringPeriodId=5&view=mRoster'
main_url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + year + '/segments/0/leagues/' + ID
second_url = 'https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/' + ID + '?seasonId=' + year

r = requests.get(url,cookies={'swid': swid, 'espn_s2': s2})

params={"view": "mTeam"}

rjson = r.json()
print(rjson['teams'][0])