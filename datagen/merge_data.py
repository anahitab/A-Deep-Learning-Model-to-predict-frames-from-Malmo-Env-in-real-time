#!/usr/bin/python

import numpy as np

import os
import re

print 'loading biomes...'
biomes = np.genfromtxt('data/biomes.txt', skip_header=1)
X = biomes[:,0]
Y = biomes[:,1]
BiomeID = biomes[:,2]

print 'indexing biomes...'
biomes_by_position = {}
for i in range(biomes.shape[0]):
    biomes_by_position[(X[i], Y[i])] = BiomeID[i]


print 'writing output...'
fout = open('data/images.txt', 'w+')
fout.write('imagePath\tbiomeID\n')

for image in os.listdir('data/images'):
    match = re.match(r".+_(-?\d+)_(-?\d+)\..*", image)
    if not match:
        raise Exception('invalid image name')
    
    x = int(match.group(1))
    y = int(match.group(2))

    biomeID = int(biomes_by_position[(x, y)])

    fout.write('data/images/%s\t%d\n' % (image, biomeID))
