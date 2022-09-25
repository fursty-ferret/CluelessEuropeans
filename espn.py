import requests
from cookies import swid, s2

year = '2018'
ID = '1649664'
main_url = 'https://fantasy.espn.com/apis/v3/games/ffl/seasons/' + year + '/segments/0/leagues/' + ID
mMatchup_url = 'https://fantasy.espn.com/apis/v3/games/ffl/leagueHistory/' + ID + '?seasonId=' + year + '?view=mMatchup'

r = requests.get(mMatchup_url, params={'view':'mMatchup'}, cookies={'swid': swid, 'espn_s2': s2})

rjson = r.json()
print(rjson)