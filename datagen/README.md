# Scripts for generating training and validation data

## Tools

We use [MCEdit Unified](https://github.com/Khroki/MCEdit-Unified) to help generate the map and extract biome information.

We add the [Minecraft 1.8 server jar](https://s3.amazonaws.com/Minecraft.Download/versions/1.8/minecraft_server.1.8.jar) to MCEdit, to generate the maps.

We use [Malmo](https://github.com/Microsoft/malmo) to generate screenshots.

## Process

There are three steps to generating data.

1. **Generate the map.** To pregenerate a map, we create a new world in MCEdit. We use the seed "1".
2. **Extract biome information.** We use a custom MCEdit filter `savebiomes.py`. Select all the chunks and run the filter.
3. **Capture screenshots.** We use a Malmo, to load the pregenerated map and capture screenshots from various positions, directions, and conditions. Run the Malmo agent `cameraperson.py`. Make sure you update the map path first.
