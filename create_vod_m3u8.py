#from flask import Flask, request, jsonify
import json
from urllib import response
import requests
import re
import os

server_hostname = 'https://my.flussonic.com'
username = 'admin'
password = 'admin'

#Get the list of VOD locations
vods = requests.get(server_hostname + '/streamer/api/v3/vods', auth=(username, password))
vods_json = vods.json()
vods_count = vods_json['estimated_count']
vods_list = []
for i in range(0, vods_count):
    vods_list.append(vods_json['vods'][i]['prefix'])

#Get all the files inside VOD location (only files in the root folder)
files_list = []
for vod_name in vods_list:
    files = requests.get(server_hostname + '/streamer/api/v3/vods/' + vod_name + '/storages/0/files', auth=(username, password))
    files_json = files.json()
    files_count = files_json['estimated_count']
    for item in range(0, files_count):
        is_directory = files_json['files'][item]['is_directory']
        name = files_json['files'][item]['name']
        if is_directory == False and re.search(r".mp4$|.mkv$", name):
            files_list.append(name)

#Function for m3u8 playlist generating
def generate_m3u8_plalist(input_files, output_playlist):
    with open(output_playlist, 'w') as playlist_file:
        for input_file in input_files:
            playlist_file.write(f'#EXTINF:-1 ,tvg-name="{os.path.basename(input_file)}" tvg-id="{os.path.basename(input_file)}",{os.path.basename(input_file)}\n')
            playlist_file.write(f'{server_hostname + "/" + input_file + "/index.m3u8"}\n')

input_files = files_list
output_playlist = 'vod_playlist.m3u8'
generate_m3u8_plalist(input_files, output_playlist)
print(f'HLS playslist is created: {output_playlist}')