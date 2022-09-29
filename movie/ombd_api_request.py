import requests


def find_json_data(title, genre):
    title=title.lower().replace(' ','+')
    url = "http://www.omdbapi.com/?t={}&type={}&apikey=2e12d3e3".format(title, genre)
    response = requests.get(url)
    if response.status_code==200:
        json_data=response.json()
        return json_data
    else:
        return 'something wrong !'
data=find_json_data('django unchained', 'movie')
print(data['Ratings'][1]['Value'])