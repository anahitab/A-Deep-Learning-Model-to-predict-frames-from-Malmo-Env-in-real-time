---
layout: default
title:  Final Report
---

## Video //todo: need to add description to video

<iframe width="560" height="315" src="https://www.youtube.com/embed/iJBFe0ALHdc" frameborder="0" allowfullscreen></iframe>

## Project Summary

Our project focuses on applying deep learning models so that it can be used for classification task. The main premise of this project is to generate many random maps with the help of Malmo and take screenshots from random points in that map and identify what biome or naturally generated stucture is within that specific picture.

Our project will take in a screenshot of a map as input and return one or more names of the biomes or structures that are shown in that picture. The main focus of this project will be towards the detection of biomes and structures primarily in the Overworld of Minecraft. 

The final product of this task should be able to return the name of a predicted biome while controlling a character within a Malmo generated world.

Other examples of uses of our project could be for detecting what kind of environment is in a regular picture, like a picture at the beach, and finding what objects or structures are within that picture as well.


## Approaches

### Image/Data Generation
In order to generate all of the images for testing, we implemented basic data generation scripts to create thousands of images to test. In the first round of testing, we generated about 10,201 images in total to test. The data for all of this images can be accessed on our Github Page and is [Available Here](https://github.com/anahitab/A-Deep-Learning-Model-to-predict-frames-from-Malmo-Env-in-real-time/releases)

In the second round of testing, our final data set, we generated more images with different times of day, yaw, and pitch. We captured a screenshot of each chunk at 4 different times: 0 (sunrise), 6000 (noon), 12000 (sunset), 18000 (night). The yaw and pitch are random (uniformly distributed) for each data point. We generated over 40,000 images in this last round of testing. This final data set can be accessed on our Github as well and is [Available Here](https://github.com/anahitab/A-Deep-Learning-Model-to-predict-frames-from-Malmo-Env-in-real-time/releases/tag/v1.0.0)

We used the original map, so the biomeID -> class can stay the same (no new biomes). This will make it easier to compare performance of the old model and new model.

The tools used in generating these images are the following: 

* [MCEdit Unified](https://github.com/Khroki/MCEdit-Unified): To help generate the map and extract biome information
* [Minecraft 1.8 server jar](https://s3.amazonaws.com/Minecraft.Download/versions/1.8/minecraft_server.1.8.jar): This jar is added to MCEdit to help generate the maps
* [Malmo](https://github.com/Microsoft/malmo): Used to generate the screenshots

### Process
There are 3 steps to how we generated the data: 

1. **Generate the map.** To pregenerate a map, we create a new world in MCEdit. We use the seed "1".
2. **Extract biome information.** We use a custom MCEdit filter `savebiomes.py`. Select all the chunks and run the filter.
3. **Capture screenshots.** We use a Malmo, to load the pregenerated map and capture screenshots from various positions, directions, and conditions. Run the Malmo agent `cameraperson.py`. Make sure you update the map path first.

### Approach for Biome Classification

Before classifying our biomes, we had to choose what biomes that we want our AI to train. Within the game of Minecraft, there is a total of 63 distinct biomes: 38 in the Overworld, one in The Nether, and one in The End.

Here is a table on all the possible biomes with their respective ID's that can possibly be used in our program:

ID | Biome
0 | 'Ocean'
1 | 'Plains'
129 | 'Sunflower Plains'
2 | 'Desert'
130 | 'Desert M'
3 | 'Extreme Hills'
131 | 'Extreme Hills M'
4 | 'Forest'
132 | 'Flower Forest'
5 | 'Taiga'
133 | 'Taiga M'
6 | 'Swampland'
134 | 'Swampland M'
7 | 'River'
8 | 'Hell'
9 | 'The End (Sky)'
10 | 'FrozenOcean'
11 | 'FrozenRiver'
12 | 'Ice Plains'
140 | 'Ice Plains Spikes'
13 | 'Ice Mountains'
14 | 'MushroomIsland'
15 | 'MushroomIslandShore'
16 | 'Beach'
17 | 'DesertHills'
18 | 'ForestHills'
19 | 'TaigaHills'
20 | 'Extreme Hills Edge'
21 | 'Jungle'
149 | 'Jungle M'
22 | 'JungleHills'
23 | 'JungleEdge'
151 | 'JungleEdge M'
24 | 'Deep Ocean'
25 | 'Stone Beach'
26 | 'Cold Beach'
27 | 'Birch Forest'
155 | 'Birch Forest M'
28 | 'Birch Forest Hills'
156 | 'Birch Forest Hills M'
29 | 'Roofed Forest'
157 | 'Roofed Forest M'
30 | 'Cold Taiga'
158 | 'Cold Taiga M'
31 | 'Cold Taiga Hills'
32 | 'Mega Taiga'
160 | 'Mega Spruce Taiga'
33 | 'Mega Taiga Hills'
161 | 'Redwood Taiga Hills M'
34 | 'Extreme Hills+'
162 | 'Extreme Hills+ M'
35 | 'Savanna'
163 | 'Savanna M'
36 | 'Savanna Plateau'
164 | 'Savanna Plateau M'
37 | 'Mesa'
165 | 'Mesa (Bryce)'
38 | 'Mesa Plateau F'
166 | 'Mesa Plateau F M'
39 | 'Mesa Plateau'
167 | 'Mesa Plateau M'

Out of all of these biomes, these are the following biomes that we chose to train our AI: 

ID | Biome
0 | 'Ocean'
24 | 'Deep Ocean'
16 | 'Beach'
4 | 'Forest'
18 | 'ForestHills'
7 | 'River'
6 | 'Swampland'
1 | 'Plains'
129 | 'Sunflower Plains'
27 | 'Birch Forest'
28 | 'Birch Forest Hills'
155 | 'Birch Forest M'
5 | 'Taiga'
29 |  'Roofed Forest'
132 | 'Flower Forest'
3 | 'Extreme Hills'
34 | 'Extreme Hills+'
25 | 'Stone Beach'
131 | 'Extreme Hills M'
21 | 'Jungle'
19 | 'TaigaHills'
23 | 'JungleEdge'
22 | 'JungleHills'
22 | 'JungleHills'

We selected these biomes becuase they are the most common biomes that we will see in the Overworld, which will be the primary location for testing. 



We used Deep Learning approach for the classification of the biomes from the Malmo environment. Deep learning does the excellent work of feature extraction from any Object/Image or even the text.
There are many types of Neural Networks, but using a Convolutional Neural Network is so natural as they can be applied to whole image at a time. This means that they are good at extracting features at once.
 
In our model we used three layers of CNN:
The first layer has filter of shape 3X3 and the number of filters were 32. We also used max pooling layer using a window size of two get the maximum value.<br>
1. ReLU was also used so that it can model to learn more complicated relations.<br>
2. Our second layer has filter of shape 3X3 and the number of filters were 32. We also used max pooling layer of window size in two. ReLU was also used in this layer.
3. Our third layer has filter of shape 3X3 and the number of filters were 64. We also used max pooling layer using a window size of two get the maximum value. ReLU was also used in this layer.
4. We have to add fully-connected layers after the convolution layers, so we need to reduce the 4-dim tensor to 2-dim which can be used as input to the fully-connected layer. For this we need to flatten the output of the previous layer and we flatten the output from last layer.
5. Following the common saying in DL Deeper the better We used two fully connected layer to get the final output.
6. We used softmax layer on the output from second fully connected layer to get probability class. We used AdamOptimizer for optimization.



## Evaluation //todo: 2nd round of testing, and explain graphs 



We tested our model on the test dataset. Our model has a pretty good accuracy and it is around 94%. Following is the sampel output with True label and predicted label.


![Graph 1](https://raw.githubusercontent.com/anahitab/A-Deep-Learning-Model-to-predict-frames-from-Malmo-Env-in-real-time/master/docs/img/fig_2-1.png)


Confusion matrix to describe the performance of our classification model on the test data. 


![Graph 2](https://raw.githubusercontent.com/anahitab/A-Deep-Learning-Model-to-predict-frames-from-Malmo-Env-in-real-time/master/docs/img/fig_2-1.png)

## References

- <https://github.com/dennybritz/reinforcement-learning>
- **MCEdit:** <https://github.com/Khroki/MCEdit-Unified>
- **Malmo:** <https://github.com/Microsoft/malmo>
- **Tensorflow** <https://github.com/tensorflow/tensorflow>
- **Minecraft Wiki** <http://minecraft.gamepedia.com/Minecraft_Wiki>