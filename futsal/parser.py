from futsal.utils import _html_to_str
import pandas as pd


def parse_positions_table(soup):
    data = []

    table = soup.find('table',
                      attrs={'class': 'table table-hover font-size-sm mb-0'})

    table_head = table.find('thead')

    col_names = [ele.text.strip() for ele in table_head.find_all('th')]

    table_body = table.find('tbody')

    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        record = {
            name: ele.text.strip()
            for name, ele in zip(col_names, cols) if ele
        }
        record.update({
            'Position':
            int(record['Team'].split('\n')[0].strip(r' |.')),
            'Team':
            record['Team'].split('\n')[1].strip()
        })
        data.append(record)

    return pd.DataFrame(data).set_index('Team')


# print(get_table())


def parse_history(soup):

    data = []

    for game in soup.find_all('div', class_='row align-items-center'):

        date_col = game.find('div', 'col-lg-5')
        if date_col:

            date_elem = date_col.find('div', class_='col-md pb-3 pb-lg-0 text-center text-md-left')

            date = _html_to_str(date_elem)

            round_id, date, time = date.split('\n')

        result_col = game.find('div', class_='col-lg-3 pb-3 pb-lg-0 text-center')

        if result_col and result_col.find('div', class_='badge'):

            results_block = result_col.find_all('div')[1].text.strip()

            result = results_block.replace(' - ', '-').split(' ')[1]

            score = results_block.replace(' - ', '-').split(' ')[0].split("-")

            if result == "Won":
                home_score = max(score)
                away_score = min(score)
            elif result == "Loss":
                home_score = min(score)
                away_score = max(score)
            else:
                home_score = score[0]
                away_score = score[1]

            team = result_col.find('a').text

            game_dict = {
                'round_id': round_id,
                'Date': date,
                'Time': time,
                'Home': home_score,
                'Away': away_score,
                'Result': result,
                'Team': team
            }

            data.append(game_dict)

    return pd.DataFrame(data).set_index('Team')


test = 'https://www.revolutionise.com.au/futsalhqsuper5s/teams/7347/&t=103296'

# print(parse_history(get_history(test)))
