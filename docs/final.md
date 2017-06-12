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
In order to generate all of the images for testing, we implemented basic data generation scripts to create thousands of images to test. In the first round of testing, we generated about 10,201 images in total to test. 
Most of these pictures were taken during daytime within the game. The data for all of this images can be accessed on our Github Page and is [Available Here](https://github.com/anahitab/A-Deep-Learning-Model-to-predict-frames-from-Malmo-Env-in-real-time/releases)

In the second round of testing, we tried a different approach by generating more images in different conditions such as weather and night. 
In our final data set, we generated more images with different times of day, yaw, and pitch. 
We captured a screenshot of each chunk at 4 different times: 0 (sunrise), 6000 (noon), 12000 (sunset), 18000 (night). 
The yaw and pitch are random (uniformly distributed) for each data point. 
We generated over 40,000 images in this last round of testing. 
This final data set can be accessed on our Github as well and is [Available Here](https://github.com/anahitab/Biome-Predictor/releases/tag/v1.0.0)

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

We used the [Minecraft Wiki Biomes Page](http://minecraft.gamepedia.com/Biome) as a reference for all of the possible biomes that can possibly be used in our program.
We stored all of the possible biomes into a dictionary called `biomeNameDict` so that it can be used for our prediction classes. 

Out of all of these biomes, these are the following biomes, with their respective ID's, that we chose to train our AI: 
 
* 0 : 'Ocean'
* 1 : 'Plains'
* 3 : 'Extreme Hills'
* 4 : 'Forest'
* 5 : 'Taiga'
* 6 : 'Swampland'
* 7 : 'River'
* 16 : 'Beach'
* 18 : 'ForestHills'
* 19 : 'TaigaHills'
* 21 : 'Jungle'
* 22 : 'JungleHills'
* 23 : 'JungleEdge'
* 24 : 'Deep Ocean'
* 25 : 'Stone Beach'
* 27 : 'Birch Forest'
* 28 : 'Birch Forest Hills'
* 29 :  'Roofed Forest'
* 34 : 'Extreme Hills+'
* 129 : 'Sunflower Plains'
* 131 : 'Extreme Hills M'
* 132 : 'Flower Forest'
* 155 : 'Birch Forest M'


We selected these biomes because they are the most common biomes that we will see in the Overworld, which will be the primary location for testing. 
We take the ID's of each of these biomes and stored them into a list called `biomeIdList` in order to convert between our prediction classes and Mincraft biome ID's


We used a Deep Learning approach for the classification of the biomes from the Malmo environment. Deep learning does the excellent work of feature extraction from any Object/Image or even the text.
There are many types of Neural Networks, but using a Convolutional Neural Network is so natural as they can be applied to whole image at a time. This means that they are good at extracting features at once.
 
In our model we used three layers of CNN:
The first layer has filter of shape 3X3 and the number of filters were 32. We also used max pooling layer using a window size of two get the maximum value.
1. ReLU was also used so that it can model to learn more complicated relations.
2. Our second layer has filter of shape 3X3 and the number of filters were 32. We also used max pooling layer of window size in two. ReLU was also used in this layer.
3. Our third layer has filter of shape 3X3 and the number of filters were 64. We also used max pooling layer using a window size of two get the maximum value. ReLU was also used in this layer.
4. We have to add fully-connected layers after the convolution layers, so we need to reduce the 4-dim tensor to 2-dim which can be used as input to the fully-connected layer. For this we need to flatten the output of the previous layer and we flatten the output from last layer.
5. Following the common saying in DL Deeper the better We used two fully connected layer to get the final output.
6. We used softmax layer on the output from second fully connected layer to get probability class. We used AdamOptimizer for optimization.



## Evaluation //todo: 2nd round of testing, and explain graphs 



We tested our model on the test dataset. Our model has a pretty good accuracy and it is around 94%. Following is the sample output with True label and predicted label.


![Graph 1](https://raw.githubusercontent.com/anahitab/Biome-Predictor/master/docs/img/fig_2-1.png)


Confusion matrix to describe the performance of our classification model on the test data. 


![Graph 2](https://raw.githubusercontent.com/anahitab/Biome-Predictor/master/docs/img/figure_2-1.png)

## References

- <https://github.com/dennybritz/reinforcement-learning>
- **MCEdit:** <https://github.com/Khroki/MCEdit-Unified>
- **Malmo:** <https://github.com/Microsoft/malmo>
- **Tensorflow** <https://github.com/tensorflow/tensorflow>
- **Minecraft Wiki** <http://minecraft.gamepedia.com/Minecraft_Wiki>