---
layout: default
title: Proposal
---
	
## Summary

Our project will focus on applying deep learning models so that it can be used for classification task. Our main idea for this project is to generate many random maps and take screenshots from random points in that map and try and identify what biome or naturally generated structure is within that specific picture. 

Our project will take in a screenshot of a map as input and return one or more names of the biomes or structures that are shown in that picture. The primary types of biomes and structures that will be highly considered in this project will mostly be part of the Overworld of Minecraft, which means anything underground, The Nether, and The End will not be included in our project as of now. Aside from detecting biomes, most generated structures, including small and large ones, above ground will be detected as well. 

Other examples of uses of our project could be for detecting what kind of environment is in a regular picture, like a picture at the beach, and finding what objects or structures are within that picture as well. 

## AI/ML Algorithms Used

The AI/ML algorithms that we are planning on using are deep learning models applied with classification task and reinforcement learning. 

## Evaluation Plan

We will evaluate our project quantitatively by measuring the success rate for correctly identifying biomes and features.
We will build an evaluation set the same way we build our training set:
we will generate a default Minecraft world and render images from many points and angles on the surface.
While rendering these images, we will also record the biome tag. The baseline will be always picking whichever biome is most common,
which will be very poor. We hope our project will have a much higher success rate,
because a large portion of images seem “easy” to predict.
Our moonshot case would be correctly predicting the biome for almost all cases.
If we reach this, we will need to add more features, or more specific biome types.
We could add elevation, structures (villages, etc).

We will evaluate our project qualitatively with some very obvious images.
For example, we can take a picture of pure snow, and confirm our project predicts a snowy biome.
It could also be interesting to run our project in reverse, to generate exaggerated biomes, similar to DeepDream.

Appointment Time: Tuesday, April 25, 2017