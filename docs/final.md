---
layout: default
title:  Final Report
---

## Video

[![Description of the Video](https://img.youtube.com/vi/FI3aW0RabBg/0.jpg)](https://www.youtube.com/watch?v=FI3aW0RabBg)

## Project Summary

//todo

## Approaches

###Image/Data Generation
In order to generate all of the images for testing, we implemented basic data generation scripts to create thousands of images to test. We have generated about 10,201 images in total to test. The data for all of this images can be accessed on our Github Page and is [Available Here](https://github.com/anahitab/PROJECT/releases)

The tools used in generating these images are the following: 

* [MCEdit Unified](https://github.com/Khroki/MCEdit-Unified): To help generate the map and extract biome information
* [Minecraft 1.8 server jar](https://s3.amazonaws.com/Minecraft.Download/versions/1.8/minecraft_server.1.8.jar): This jar is added to MCEdit to help generate the maps
* [Malmo](https://github.com/Microsoft/malmo): Used to generate the screenshots

### Process
There are 3 steps to how we generated the data: 

1. **Generate the map.** To pregenerate a map, we create a new world in MCEdit. We use the seed "1".
2. **Extract biome information.** We use a custom MCEdit filter `savebiomes.py`. Select all the chunks and run the filter.
3. **Capture screenshots.** We use a Malmo, to load the pregenerated map and capture screenshots from various positions, directions, and conditions. Run the Malmo agent `cameraperson.py`. Make sure you update the map path first.

//todo


## Evaluation

//todo

## References

- <https://github.com/dennybritz/reinforcement-learning>
- **MCEdit:** <https://github.com/Khroki/MCEdit-Unified>
- **Malmo:** <https://github.com/Microsoft/malmo>
- **Tensorflow** <https://github.com/tensorflow/tensorflow>