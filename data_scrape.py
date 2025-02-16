from bs4 import BeautifulSoup
import re
import requests

class DataScrape:

    def __init__(self):
        pass
    
    def get_content(self, url):
        try:
            response = requests.get(url).content
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        else:
            response_content = BeautifulSoup(response, 'html.parser')
            response_content = str(response_content.prettify())
            return response_content

    def parse_team_page(self, content):
        team_dict = []
        urls = re.findall(r'<div class="col-lg-12 team-page-img">\n\s+<center>\n\s+<a href="(.*?)">.*?</div>', content, flags=re.DOTALL)

        for url in urls:
            url_content = self.get_content(url)

            team_info = {}
            team_info['team'] = re.search(r'<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 team-profile-data">.*?<h3>\s+(.*?)\s+</h3>.*?</div>', url_content, flags=re.DOTALL).group(1)
            team_info['coach'] = re.search(r'<h5 class="team-mgmt-header color-tmc">\s*HEAD COACH\s*</h5>\s*<h5 class="team-mgmt-data">\s*(.*?)\s*</h5>', url_content, flags=re.DOTALL).group(1)
            team_info['manager'] = re.search(r'<h5 class="team-mgmt-header color-tmc">\s*MANAGER\s*</h5>\s*<h5 class="team-mgmt-data">\s*(.*?)\s*</h5>', url_content, flags=re.DOTALL).group(1)
            team_info['url'] = url
            team_info['logo'] = re.search(r'<div class="col-lg-3 col-md-3 col-sm-6">\s*<center>\s*<img src="(.*?)"/>\s*</center>\s*</div>', url_content, flags=re.DOTALL).group(1)
            team_dict.append(team_info) 
            
        return team_dict
    
    def parse_player_page(self, content):
        player_dict = []
        urls = re.findall(r'<div class="col-lg-12 team-page-img">\n\s+<center>\n\s+<a href="(.*?)">.*?</div>', content, flags=re.DOTALL)

        for url in urls:
            url_content = self.get_content(url)
            team = re.search(r'<div class="col-lg-12 col-md-12 col-sm-12 col-xs-12 team-profile-data">.*?<h3>\s+(.*?)\s+</h3>.*?</div>', url_content, flags=re.DOTALL).group(1)
            players = re.findall(r'(<a class="p-link" href=".*?">.*?</a>)', url_content, flags=re.DOTALL)
            
            for player in players:
                player = re.sub(r'<br/>', ' ', player, flags=re.DOTALL)
                
                player_info = {}
                player_info['team'] = team
                player_info['name'] = re.search(r'<h4>(.*?)</h4>', player, flags=re.DOTALL).group(1)
                player_info['name'] = re.sub(r'\s+', r' ', player_info['name'], flags=re.DOTALL)
                player_info['number'] = re.search(r'<p>\s*(.*?) \|.*?\s*</p>', player, flags=re.DOTALL).group(1)
                player_info['position'] = re.search(r'<p>\s*.*? \|(.*?)\s*</p>', player, flags=re.DOTALL).group(1)
                player_info['url'] = re.search(r'href="(.*?)"', player, flags=re.DOTALL).group(1)
                player_info['mugshot'] = re.search(r'<img class=".*?" src="(.*?)"', player, flags=re.DOTALL).group(1)
                player_dict.append(player_info)

        return player_dict
    