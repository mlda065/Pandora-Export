# This script was written by Matthew Davis in July 2017.
# It uses the Pandora library writte by Kevin Mehall <km@kevinmehall.net> and Christopher Eby <kreed@kreed.org>
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

# import requests
import json
import pprint as pp
import pandora
import getpass
# from multiprocessing import Pool

def getLikes():

    p = pandora.Pandora()

    client = pandora.data.client_keys[pandora.data.default_client_id]
    user = input("Enter your username (which is probably an email address)\n")
    pwd = getpass.getpass()
    print("Conecting ...")
    p.connect(client, user, pwd)
    print("Connected")

    print("Getting list of your stations")
    stations = p.get_stations()
    print("Got list of station names")

    print("Looking up thumbs for each station")
    info = [s.get_info(extended=True) for s in stations]

    # This doesn't work, because something isn't picklable
    # with Pool(4) as p:
    #     info = p.map(lambda s:s.get_info(extended=True), stations)
    print("Got thumbs for each station")

    print('Formatting results')
    station_base = [s['music'] for s in info if 'music' in s]


    # likes = {y:[x[y] for x in likes_raw if y in x] for y in ['artists','genres','songs']}
    # dislikes = {y:[x[y] for x in dislikes_raw if y in x] for y in ['artists','genres','songs']}

    data = {
        'thumbsUp':{
            'artists':[],
            'songs':[],
            'genres':[]
        },
        'thumbsDown':{
            'artists':[],
            'songs':[],
            'genres':[]
        }
    }

    for x in station_base:
        if 'songs' in x:
            songs = [{'name':s['artistName'],'artist':s['artistName']} for s in x['songs']]
            data['thumbsUp']['songs'].extend(songs)
        if 'genres' in x:
            genres = [g['genreName'] for g in x['genres']]
            data['thumbsUp']['genres'].extend(genres)
        if 'artists' in x:
            artists = [a['artistName'] for a in x['artists']]
            data['thumbsUp']['artists'].extend(artists)

    for direction in ['thumbsUp','thumbsDown']:
        for station in info:
            if 'feedback' in station:
                for x in station['feedback'][direction]:
                    if 'songName' in x:
                        data[direction]['songs'].append({'name':x['songName'],'artist':x['artistName']})
                    else:
                        assert('artistName' in x)
                        data[direction]['artists'].append(x['artistName'])


    # If you want the final output to be formatted a particular way
    # do that here

    return data

def saveLikes(data,fileName):
    print("Saving data to file %s" % fileName)
    with open(fileName, 'w') as fp:
        json.dump(data, fp, indent=3)
    print('saved data to %s' % fileName)

if __name__ == "__main__":

    data = getLikes()

    pp.pprint(data)

    fileName = "./output.json"
    saveLikes(data,fileName)
