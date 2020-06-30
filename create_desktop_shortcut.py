import os
import subprocess

subprocess.call(
    ['wget',
     'https://pbs.twimg.com/profile_images/960519710809972736/NJWxM0QH_400x400.jpg',
     '-O',
     'icon.jpg'])

file_name = "clip-translater.desktop"

with open(file_name) as f:
    lines = f.read()

lines = lines.replace(
    'Icon={}/icon.jpg',
    'Icon={}/icon.jpg'.format(os.getcwd()))

with open(file_name, mode='w') as f:
    f.write(lines)

subprocess.call([
    'ln',
    '-sf',
    '{}/clip-translater.desktop'.format(os.getcwd()),
    '/home/{}/Desktop/clip-translater.desktop'.format(os.environ.get('USER'))])
