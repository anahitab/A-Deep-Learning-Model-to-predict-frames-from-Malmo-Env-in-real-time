import MalmoPython
import logging
import random
import time
import json
import sys
from real_time_pre import predict_
import numpy as np
from main import FLAGS
from scipy import misc

#from PIL import Image

import tensorflow as tf

# replace this with the path on your system
#map_file_path = '/Users/cory/Library/Application Support/minecraft/saves/Seed1Size100x100'
map_file_path = '/home/prayalankar/Downloads/Malmo/Minecraft/saves/Seed1Size100x100'


minx = -800
maxx = 800
minz = -800
maxz = 800

video_width = 128
video_height = 128

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # set to INFO if you want fewer messages

   
missionXML = '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    
      <About>
        <Summary>Save screenshots all around the map</Summary>
      </About>
      
     <ServerSection>
        <ServerInitialConditions>
            <Time>
                <StartTime>6000</StartTime>
                <AllowPassageOfTime>false</AllowPassageOfTime>
            </Time>
        </ServerInitialConditions>
        <ServerHandlers>
            <FileWorldGenerator src="''' + map_file_path + '''"/>
            <ServerQuitWhenAnyAgentFinishes />
        </ServerHandlers>
    </ServerSection>
    <AgentSection mode="Spectator">
        <Name>Cameraperson</Name>
        <AgentStart>
            <Placement x="0" y="127.0" z="0"/>
        </AgentStart>
        <AgentHandlers>
            <ObservationFromFullStats />
            <ObservationFromGrid>
                <Grid name="column">
                    <min x="0" y="-256" z="0" />
                    <max x="0" y="256" z="0" />
                </Grid>
            </ObservationFromGrid>
            <VideoProducer want_depth="true">
                <Width>''' + str(video_width) + '''</Width>
                <Height>''' + str(video_height) + '''</Height>
            </VideoProducer>
            <AbsoluteMovementCommands />
        </AgentHandlers>
    </AgentSection>
  </Mission>'''

validate = True
my_mission = MalmoPython.MissionSpec( missionXML, validate )

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

agent_host.setObservationsPolicy(MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY)
agent_host.setVideoPolicy(MalmoPython.VideoPolicy.LATEST_FRAME_ONLY)

if agent_host.receivedArgument("test"):
    num_reps = 1
else:
    num_reps = 10

my_mission_record_spec = MalmoPython.MissionRecordSpec()


max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record_spec )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            logger.error("Error starting mission: %s" % e)
            exit(1)
        else:
            time.sleep(2)

logger.info("Waiting for the mission to start")
world_state = agent_host.getWorldState()
observation = None
while not world_state.has_mission_begun:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()

logger.info('Mission started')

x = minx
z = minz

def waitForNextObservation():
    global world_state
    global observation

    while world_state.is_mission_running:
        world_state = agent_host.getWorldState()
        if world_state.number_of_observations_since_last_state > 0:
            observation = json.loads(world_state.observations[-1].text)
            return
        time.sleep(0.1)

def waitForNextVideoFrame():
    global world_state
    global video_frame

    while world_state.is_mission_running:
        world_state = agent_host.getWorldState()
        if world_state.number_of_video_frames_since_last_state > 0:
            video_frame = world_state.video_frames[-1]
            return
        time.sleep(0.5)


# waits for an observation where position = xyz
def teleportAndWait(x, y, z, yaw='', pitch=''):
    agent_host.sendCommand('tp %s %s %s %s %s' % (x, y, z, yaw, pitch))

    def hasCorrectPosition():
        return (int(observation['XPos']), int(observation['YPos']), int(observation['ZPos'])) == (int(x), int(y), int(z))

    def hasCorrectRotation():
        correctYaw = yaw == '' or int(observation['Yaw']) == int(yaw)
        correctPitch = pitch == '' or int(observation['Pitch']) == int(pitch)
        return correctYaw and correctPitch

    while observation == None or not (hasCorrectPosition() and hasCorrectRotation()):
        waitForNextObservation()


def getBiomeIdFromPrediction(prediction):
    '''
        Gets the corresponding Minecraft Biome ID from a class ID.
        @param  prediction  class ID [0, len(biomeIdList) )
        @return             Biome ID used by Minecraft
    '''

    biomeIdList = [0, 24, 16, 4, 18, 7, 6, 1, 129, 27, 28, 155, 5, 29, 132, 3, 34, 25, 131, 21, 19, 23, 22]

    if 0 <= prediction < len(biomeIdList):
        return biomeIdList[prediction]
    else:
        return None

def getBiomeName(biomeId):
    '''
        Gets the English name of a biome from a Minecraft Biome ID
        @param  biomeId Minecraft Biome ID int, or None
        @return         English name string
    '''

    
    # source: http://minecraft.gamepedia.com/Biome/ID
    biomeNameDict = {
        0: 'Ocean',
        1: 'Plains',
        129: 'Sunflower Plains',
        2: 'Desert',
        130: 'Desert M',
        3: 'Extreme Hills',
        131: 'Extreme Hills M',
        4: 'Forest',
        132: 'Flower Forest',
        5: 'Taiga',
        133: 'Taiga M',
        6: 'Swampland',
        134: 'Swampland M',
        7: 'River',
        8: 'Hell',
        9: 'The End (Sky)',
        10: 'FrozenOcean',
        11: 'FrozenRiver',
        12: 'Ice Plains',
        140: 'Ice Plains Spikes',
        13: 'Ice Mountains',
        14: 'MushroomIsland',
        15: 'MushroomIslandShore',
        16: 'Beach',
        17: 'DesertHills',
        18: 'ForestHills',
        19: 'TaigaHills',
        20: 'Extreme Hills Edge',
        21: 'Jungle',
        149: 'Jungle M',
        22: 'JungleHills',
        23: 'JungleEdge',
        151: 'JungleEdge M',
        24: 'Deep Ocean',
        25: 'Stone Beach',
        26: 'Cold Beach',
        27: 'Birch Forest',
        155: 'Birch Forest M',
        28: 'Birch Forest Hills',
        156: 'Birch Forest Hills M',
        29: 'Roofed Forest',
        157: 'Roofed Forest M',
        30: 'Cold Taiga',
        158: 'Cold Taiga M',
        31: 'Cold Taiga Hills',
        32: 'Mega Taiga',
        160: 'Mega Spruce Taiga',
        33: 'Mega Taiga Hills',
        161: 'Redwood Taiga Hills M',
        34: 'Extreme Hills+',
        162: 'Extreme Hills+ M',
        35: 'Savanna',
        163: 'Savanna M',
        36: 'Savanna Plateau',
        164: 'Savanna Plateau M',
        37: 'Mesa',
        165: 'Mesa (Bryce)',
        38: 'Mesa Plateau F',
        166: 'Mesa Plateau F M',
        39: 'Mesa Plateau',
        167: 'Mesa Plateau M'
    }

    return biomeNameDict.get(biomeId, 'Biome %d' % biomeId)

# start at y = 64 as guess for floor level
y = 64




def predict(frameInput):
    
    #print(type(frameInput))
    arr = np.array(frameInput)
    #print(arr)
    #print(len(arr))
    #print("-"*50)
    '''
        Predicts the most likely class from an input image content.
        
        @param  frameInput  pixel data? how does TF need it formatted?
        @return class ID prediction (0-22)
    '''
    rt = [ 0 for i in range(23)]
    res = predict_(rt,arr,FLAGS)

    # TODO @anahta
    return res


# TODO @anahita load TensorFlow model

# main loop
while world_state.is_mission_running:

#    # teleport to column
#    teleportAndWait(x, y, z)
#
#    # move to surface
#    column = observation['column']
#    newY = 256
#    while newY > 0 and column[newY - y + 256] == 'air':
#        newY -= 1
#    y = newY + 1
#    teleportAndWait(x, y, z)
#
#    if z == minz:
#        # new row (huge teleport from previous location)
#        # wait for terrain to load before taking picture
#        time.sleep(10.0)
    
    frame = None
    while frame == None:
        waitForNextVideoFrame()
        frame = video_frame

#        if int(frame.xPos) != int(x) or int(frame.yPos) != int(y) or int(frame.zPos) != int(z):
#            frame = None

#    image = Image.frombytes('RGBA', (frame.width, frame.height), str(frame.pixels))
#    imgname = 'data/temp.png'
#    image.save(imgname)

    # TODO @anahita check format
    # I am not sure how to format the pixels, to use as input for our model.
    # This might be correct?
    frameTfInput = frame.pixels

    # prediction is an ID, 0-22
    prediction = predict(frameTfInput)

    # uses the mapping from new labels to old labels
    biomeId = getBiomeIdFromPrediction(prediction)

    # uses a mapping I found on the Minecraft wiki
    biomeName = getBiomeName(biomeId)

    print 'Predicted biome: ' + biomeName # or say in Malmo chat

#    z = z + 16
#    if z > maxz:
#        # make sure the terrain loads
#        z = minz
#        x = x + 16
#        if x > maxx:
#            break

# end main loop

## main loop:
#while world_state.is_mission_running:
#    world_state = agent_host.getWorldState()
#    while world_state.number_of_video_frames_since_last_state < 1 and world_state.is_mission_running:
#        logger.info("Waiting for frames...")
#        time.sleep(0.05)
#        world_state = agent_host.getWorldState()
#
#    logger.info("Got frame!")
#
#    
#    msg = world_state.observations[-1].text
#    observations = json.loads(msg)
#    grid = observations.get(u'column', 0)
#
#    print grid
#
#    # frame_info = { "pixels": world_state.video_frames[0].pixels, "biome": world_state.
#
#    # print world_state.video_frames[0].pixels
#
logger.info("Mission has stopped.")
#time.sleep(1) # let the Mod recover
