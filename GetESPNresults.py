from cookies import *
from espn_api.football import League
import mysql.connector

db = mysql.connector.connect(
    host='192.168.1.121',
    user='andy',
    passwd='pihole19251',
    database='clueless'
)

mycursor = db.cursor()

class Clueless():
    def __init__(self, year):
        self.league = League(league_id='1649664', year=year, espn_s2=s2, swid=swid)
        self.year = year

    def add_seasons_to_db(self):
        for id in range(1,13):
            team = self.league.get_team_data(id)
            keyID = f"{self.year}-{id}"
            mycursor.execute('INSERT INTO owners VALUES (%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s)',(keyID, self.year, id, team.team_name, team.owner, team.team_abbrev, team.final_standing, team.points_for, team.points_against, team.wins, team.losses, team.ties))
            db.commit()
    
    def update_owners(self):
        mycursor.execute('SELECT unique(seasons.team_owner) FROM seasons')
        owners = mycursor.fetchall()
        for [owner] in owners:
            mycursor.execute('SELECT full_name FROM owners')
            data = mycursor.fetchall()
            names = []
            for [name] in data:
                names.append(name)
            mycursor.execute('SELECT sum(wins), sum(losses), sum(ties), id FROM seasons WHERE seasons.team_owner=%s', (owner,))
            results = mycursor.fetchall()[0]
            wins = results[0]
            losses = results[1]
            ties = results[2]
            id = results[3]
            championships = self.get_championships(owner)
            podiums = self.get_podiums(owner)
            percentage = self.get_win_percent(wins, losses, ties)
            if owner in names:
                mycursor.execute('UPDATE owners SET total_wins=%s, total_losses=%s, total_ties=%s, championships=%s, podiums=%s, win_percentage=%s WHERE full_name=%s', (wins, losses, ties, championships, podiums, percentage, owner))
                db.commit()
            else:
                mycursor.execute('INSERT INTO owners (full_name, team_id, total_wins, total_losses, total_ties, championships, podiums, win_percentage) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(owner, id, wins, losses, ties, championships, podiums, percentage))
                db.commit()

    def get_win_percent(wins, losses, ties):
        total = wins + losses + ties
        percentage = round(wins/total, 3)
        return percentage

    def get_championships(owner):
        mycursor.execute('SELECT count(standing) FROM seasons WHERE seasons.standing=1 AND seasons.team_owner=%s', (owner,))
        championships = mycursor.fetchall()[0][0]
        return championships

    def get_podiums(owner):
        mycursor.execute('SELECT count(standing) FROM seasons WHERE seasons.team_owner=%s AND (seasons.standing=1 OR seasons.standing=2 OR seasons.standing=3)', (owner,))
        podiums = mycursor.fetchall()[0][0]
        return podiums



    def get_name(self, name):
        dict = {}
        for i in range(1,13):
            name = self.league.get_team_data(i)
            dict.update({
                name:id
            })
        id = dict[name]
        return id

    def get_parsed_name(self, name):
        final_dict = {}
        print(name)
        for i in range(1,13):
            dict = {}
            team = self.league.get_team_data(i)
            id = team.team_id
            name = team.team_name
            owner = team.owner
            dict.update({
                'id':id,
                'name':name,
                'owner':owner
            })
            teamname = self.get_name(id)
            final_dict.update({
                teamname:dict
            })
        print(final_dict[name])
    
    def get_matchup_results(self, week):
        matchups = self.league.scoreboard(week)
        for i in range(len(matchups)):
            matchupNo = i+1
            matchup = matchups[i]
            print(f'{matchupNo} {matchup}')
        

clueless = Clueless(2019)
week = 1
clueless.get_matchup_results(week)
