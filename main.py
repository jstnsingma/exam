from data_scrape import DataScrape
from export import ExportData

URL = "https://www.pba.ph/teams"

if __name__ == "__main__":
    data = DataScrape()
    export = ExportData()
    content = data.get_content(URL)

    team_data = data.parse_team_page(content)
    export.export_to_csv(team_data, 'teams')

    player_data = data.parse_player_page(content)
    export.export_to_csv(player_data, 'players')
    