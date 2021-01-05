import sys, pygame
from djitellopy import Tello
import cv2
import numpy
import Controller


def start_drone():
    drone = TelloDrone()
    drone.change_video_settings(720, 600)
    controller = Controller()

    pygame.init()
    size = width, height = 720, 600
    screen = pygame.display.set_mode(size)
    img = pygame.Surface((width, height))

    #drone.drone.takeoff()
    print(drone.drone.query_battery())

    flying = True
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while flying:
        for event in pygame.event.get():
            drone.reset_speed()
            if event.type == pygame.QUIT:
                flying = False
                drone.turn_off()
                break

            if event.type == pygame.KEYDOWN:
                # emergency landing
                if event.key == pygame.K_ESCAPE:
                    print('turning off')
                    flying = False
                    drone.turn_off()
                    break
                # check for key down using dictionary to tuple
                controller.key_down(event.key)
            elif event.type == pygame.KEYUP:
                # check for key up using dictionary to tuple
                controller.key_up(event.key)
            # move the drone according to the movement vector (x,y,z)
            # x = forward/backwards, y = left/right, z = up/down
        drone.move_drone(controller)
        drone_frame = drone.get_frame()
        if drone_frame is not None:
            img = cv2.resize(drone_frame, (width, height))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame', frame)
    drone.turn_off()


if __name__ == "__main__":
    start_drone()
