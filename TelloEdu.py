import sys, pygame
import cv2
import numpy
import TelloDrone
from Controller import Controller
from DroneState import States, StateMachine
from Face import Face

def detecting_face(frame, classifier):
        I = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = classifier.detectMultiScale(I, 1.3, 5)
        # return the first face that occures else return failure
        for (x, y, w, h) in faces:
            return (True, Face(x, y, w, h))
        return (False, None)


def start_drone():
    drone = TelloDrone()
    drone.change_video_settings(720, 600)

    controller = Controller()

    state_machine = StateMachine()

    pygame.init()
    size = width, height = 720, 600
    screen = pygame.display.set_mode(size)
    img = pygame.Surface((width, height))

    features = dict(maxCorners=500,
                    qualityLevel=0.3,
                    minDistance=7,
                    blockSize=7)

    lk = dict(winSize=(15, 15),
            maxLevel=2,
            criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 100, 0.3))

    
    print(drone.drone.query_battery())

    drone_active = True
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    myFace = None
    last_I = None

    while state_machine.state != States.EXIT:
        try:
            # check for pygame events
            for event in pygame.event.get():
                drone.reset_speed()
                if event.type == pygame.QUIT:
                    state_machine.state_change(3)
                    drone.turn_off()
                    break

                if event.type == pygame.KEYDOWN:
                    # emergency landing
                    if event.key == pygame.K_ESCAPE:
                        print('turning off')
                        state_machine.state_change(3)
                        drone.turn_off()
                        break
                    elif event.key == pygame.K_ENTER:
                        drone.drone.takeoff()
                        state_machine.state_change(0)
                    else:
                        controller.key_down(event.key)

                elif event.type == pygame.KEYUP:
                    controller.key_up(event.key)
        
            # deal with states
            if (state_machine.state == States.Waiting):
                print('waiting for takeoff')
        
            elif (state_machine.state == States.USER_CONTROL):
                drone.move_drone(controller)
                drone_frame = drone.get_frame()
                if drone_frame is not None:
                    img = cv2.resize(drone_frame, (width, height))
                    cv2.imshow('Camera', img)
            
            elif (state_machine.state == States.SEARCHING):
                try:
                    drone.move_drone(controller)
                    drone_frame = drone.get_frame()
                    if drone_frame is not None:
                        img = cv2.resize(drone_frame, (width, height))
                        ret, myFace = detecting_face(img, face_cascade)
                        if ret:
                            ret, last_I = myFace.prepare_tracker(img, features)
                            if ret:
                                state_machine.state_change(0)
                        cv2.imshow('Camera', img)
                except:
                    print('-- SEARCHING FAILED --')
                    state_machine.state_change(3)
            elif (state_machine.state == States.TRACKING):
                try:
                    drone.move_drone(controller)
                    drone_frame = drone.get_frame()
                    if drone_frame is not None:
                        img = cv2.resize(drone_frame, (width, height))
                        last_I = myFace.tracking_face(last_I, img, lk)
                        img = cv2.circle(img, ( int(myFace.x + myFace.w / 2), int(myFace.y + myFace.h / 2)), myFace.colors[0].tolist(), -1)
                        if not ret:
                            state_machine.state_change(0)
                        cv2.imshow('Camera', img)
                except:
                    print('-- SEARCHING FAILED --')
                    state_machine.state_change(3)
        except:
            print('Drone Failed ')
    drone.turn_off()


if __name__ == "__main__":
    start_drone()
