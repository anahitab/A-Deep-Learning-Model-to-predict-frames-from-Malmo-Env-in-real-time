

## Project Summary

As stated in our proposal, our project focuses on applying deep learning models so that it can be used for classification task. The main premise of this project is to generate many random maps with the help of Malmo and take screenshots from random points in that map and identify what biome or naturally generated stucture is within that specific picture.

Our project will take in a screenshot of a map as input and return one or more names of the biomes or structures that are shown in that picture. The main focus of this project will be towards the detection of biomes and structures primarily in the Overworld of Minecraft. 

Other examples of uses of our project could be for detecting what kind of environment is in a regular picture, like a picture at the beach, and finding what objects or structures are within that picture as well.


## Approach


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

### Testing 

## Evaluation

## Demo Video

Watch our program predict biomes in real time, as a player explores the world.

<iframe width="560" height="315" src="https://www.youtube.com/embed/iJBFe0ALHdc" frameborder="0" allowfullscreen></iframe>

## Remaining Goals and Challenges

One of our remaining goals for the project is to generate more images for testing. Since we have only done one round of data generation for one world seed in Minecraft, creating images within different worlds can help train our program to better predict biomes. 

One challenge that we face is generating images that contain structures and less common biomes. Because the world and photos are randomly generated, it may prove to be difficult to find any sort of structures throughout the map because those places have a very low spawn/appearance rate on any map. In order to find as many of these rare biomes and structures as we can, we'll need to generate more data sets using different random worlds with the help of our [data generation scripts](https://github.com/anahitab/PROJECT/tree/master/datagen).

