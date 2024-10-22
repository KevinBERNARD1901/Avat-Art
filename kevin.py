# Ceci est la page de Kévin le boss

from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import pygame

# Initialisation de la kinect
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Color)

# Initialisation de pygame
pygame.init()
ecran_width, ecran_height = 960, 540
ecran = pygame.display.set_mode((ecran_width, ecran_height))

# Fonction pour dessiner un squelette
def draw_body(ecran, joints):
    for joint in joints:
        position = joints[joint].Position
        x, y, z = position.x, position.y, position.z
        if z > 0:
            x, y = int(x * 100 + ecran_width // 2), int(-y * 100 + ecran_height // 2)
            pygame.draw.circle(ecran, (255, 0, 0), (x, y), 5)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Récupération des données de la kinect
    if kinect.has_new_body_frame():
        bodies = kinect.get_last_body_frame()
        if bodies != None:
            for i in range(0, kinect.max_body_count):
                body = bodies.bodies[i]
                if not body.is_tracked:
                    continue
                joints = body.joints
                # Récupération de la position du poignet gauche
                joint = joints[PyKinectV2.JointType_WristLeft]
                position = joint.Position
                x, y, z = position.x, position.y, position.z
                print(x, y, z)
                draw_body(ecran, joints)