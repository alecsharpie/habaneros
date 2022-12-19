# credit: http://stackoverflow.com/a/5925525/1944784


def _html_to_str(elem):
    text = ''
    for e in elem.descendants:
        if isinstance(e, str):
            text += e.strip()
        elif e.name == 'br' or e.name == 'p':
            text += '\n'
    return text


def _filter_team_of_interest(soup, team_name):

    for game in soup.find_all('div', class_='row align-items-center'):

        date_col = game.find('div', 'col-lg-5')
        if date_col:

            date_elem = date_col.find(
                'div', 'col-md pb-3 pb-lg-0 text-center text-md-left')

            date = _html_to_str(date_elem)
            date, time = date.split('\n')

        result_col = game.find('div', 'col-lg-3 pb-3 pb-lg-0 text-center')
        if result_col:

            result = result_col.find('div').text
            if not any(char.isdigit() for char in result):
                result = None

            teams = {
                team.text: team.get('href')
                for team in result_col.find_all('a')
            }

            if teams.get('Habaneros F.C.', None):
                teams.pop('Habaneros F.C.')

                opponent = {
                    'name': list(teams.keys())[0],
                    'url': list(teams.values())[0]
                }

                game_dict = {
                    'Date': date,
                    'Time': time,
                    'Result': result,
                    'Opponent': opponent
                }

                return game_dict
