import billboard
import requests

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

def get_list(list, date):
    songs = []

    chart = billboard.ChartData(list, date=date)

    for i in chart.entries:
        name = i.title
        artist = i.artist
        songs.append((name, artist))

    return songs

def get_spotify_id(song_info, limit = 1):
    spotify_token = 'BQBwOK7HMbheAO49r7tx-qbBqfr9drqGuSM2vuPIpw5tHbaPIieYBMDel_xNZlCyv07eKJJC-ZXPe0ivaJOlyBXGbcpnAM3-znOK6XuuhqFZphqClrDjHK1sRzKwdN7yStbL_I2yB_SBMH4nxqaJWrA13dIo_Mm7FgLGIzkF-SPS-epuAA'
    base_url = 'https://api.spotify.com/v1/search'
    query = "?q={}&artist={}&type=track&limit={}".format(song_info[0], song_info[1], limit)

    url = base_url + query

    response = requests.get(url, auth=BearerAuth(spotify_token))
    json_data = response.json()
    # json_object = json.loads(json_data)
    # json_formatted = json.dumps(json_data, indent=2)
    # print(json_data)
    id_string = json_data['tracks']['items'][0]['uri']
    print(id_string)
    print(id_string[14:])
    id = id_string[14:]

    return id

# def main():

list = 'hot-100'
date = '1950-03-22'

test_list = get_list(list, date)
get_spotify_id(test_list[0])
# print(test_list)







