# MCEdit filter
# Saves the biome ID for each xz coordinate
#
# Output file format:
#   tab separated
#   first line header
#   x   y   biomeID

from mcplatform import askSaveFile
from directories import getDocumentsFolder

displayName = "SaveBiomes"

def perform(level, box, options):
    fname = askSaveFile(getDocumentsFolder(), 'Save to file...', 'biomes.txt', '*', '.txt')
    fout = open(fname, "w+")
    fout.write('x\ty\tbiomeID\n')

    for x in xrange(box.minx, box.maxx):
        chunkx = x // 16
        for z in xrange(box.minz, box.maxz):
            chunkz = z // 16
            biome = level.getChunk(chunkx, chunkz).Biomes[x % 15, z % 15]
            fout.write(str(x) + '\t' + str(z) + '\t' + str(biome) + '\n')
