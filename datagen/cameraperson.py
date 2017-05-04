#!/usr/bin/python

import MalmoPython
import logging
import random
import time
import json
import sys

from PIL import Image

# replace this with the path on your system
map_file_path = '/Users/cory/Library/Application Support/minecraft/saves/Seed1Size100x100'

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


# start at y = 64 as guess for floor level
y = 64

# main loop
while world_state.is_mission_running:

    # teleport to column
    teleportAndWait(x, y, z)

    # move to surface
    column = observation['column']
    newY = 256
    while newY > 0 and column[newY - y + 256] == 'air':
        newY -= 1
    y = newY + 1
    teleportAndWait(x, y, z)

    if z == minz:
        # new row (huge teleport from previous location)
        # wait for terrain to load before taking picture
        time.sleep(10.0)
    
    frame = None
    while frame == None:
        waitForNextVideoFrame()
        frame = video_frame

        if int(frame.xPos) != int(x) or int(frame.yPos) != int(y) or int(frame.zPos) != int(z):
            frame = None

    image = Image.frombytes('RGBA', (frame.width, frame.height), str(frame.pixels))
    imgname = 'images/horizon_%d_%d.png' % (x, z)
    image.save(imgname)
    logger.info('saved "%s"' % imgname)

    z = z + 16
    if z > maxz:
        # make sure the terrain loads
        z = minz
        x = x + 16
        if x > maxx:
            break

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
