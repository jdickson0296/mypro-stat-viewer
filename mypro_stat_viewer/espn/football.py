""" This file contains the ESPNFootball class which is used to interact with the ESPN API. """ ""
from espn_api.football import League


class ESPNFootball:
    """This class is used to interact with the ESPN API."""

    def __init__(
        self,
        league_id: int,
        year: int,
        private: bool = False,
        espn_s2: str = None,
        swid: str = None,
    ):
        self.league_id = league_id
        self.year = year

        if private:
            self.league = League(league_id, year, espn_s2, swid)
        else:
            self.league = League(league_id, year, private)

    def get_league(self):
        """Returns the league object."""
        return self.league

    def get_teams(self):
        """Returns a list of teams in the league."""
        return self.league.teams

    def get_team_count(self):
        """Returns the number of teams in the league."""
        return len(self.league.teams)

    def get_reg_season_count(self):
        """Returns the number of regular season weeks."""
        return self.league.settings.reg_season_count

    def get_team_roaster(self, team_id: int):
        """Returns the roster of a team."""
        return self.league.teams[team_id].roster
