from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import cv2
import pygame
import openpyxl
import time
# import numpy as np

# Paramètres de l'animation
animation_path = "./Animations/Animation_vague_beta.mp4"
cap = cv2.VideoCapture(animation_path)
if not cap.isOpened():
    raise Exception("ERROR: Video could not be opened")

fps = 7 # J'ai 7 image par seconde dans l'animation
delay = int(1000/fps)

cv2.namedWindow("Frame", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Frame", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
screen_width = 1920
screen_height = 1080
# background_color = (241, 234, 206)
# canvas = np.full((screen_height, screen_width, 3), background_color, dtype=np.uint8)


# Initialisation de la kinect
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Body | PyKinectV2.FrameSourceTypes_Color)

# Initialisation de pygame
pygame.init()
width, height = 960, 540
screen = pygame.display.set_mode((width, height))

# Fonction pour dessiner un squelette
def draw_body(screen, joints):
    for joint in joints:
        print(type(joints))
        print("je suis là")
        position = joints[joint].Position
        x, y, z = position.x, position.y, position.z
        if z > 0:
            x, y = int(x * 100 + width // 2), int(-y * 100 + height // 2)
            pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)
      
# Fonction pour l'animation du coup de pied     
def animation_coup_de_pied():#path en argument
    running = True
    while running:
        success, frame = cap.read()

        if not success: #Si on arrive à la fin de la vidéo, on arrête la boucle while
            running = False
            continue

        screen = cv2.resize(frame, (screen_width, screen_height), interpolation=cv2.INTER_LINEAR)
        
        cv2.imshow("Frame", frame)

        if cv2.waitKey(delay) & 0xFF == ord('q'):
            running = False
            
    cap.release()
    cv2.destroyAllWindows() 

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
                
                # Indice des jointures à tester
                indice_pied_droit = 19
                indice_genoux_gauche = 13
                
                # Récupération des y
                y_pied_droit = joints[indice_pied_droit].Position.y
                y_genoux_gauche = joints[indice_genoux_gauche].Position.y
                
                # Test de comparaison
                if y_pied_droit > y_genoux_gauche : 
                    print("Pied droit plus haut que genou gauche")
                    animation_coup_de_pied()
                    running = False
                    

        if kinect.has_new_color_frame():
            frame = kinect.get_last_color_frame()
            
            if frame is not None:
                # Redimensionnement et transformation de l'image
                frame = frame.reshape((1080, 1920, 4))  # Reshape du frame pour 1080p
                frame = frame[:, :, :3]  # Supprimer le canal alpha
                frame = cv2.resize(frame, (width, height))  # Redimensionner avec OpenCV
                frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # Créer une surface Pygame
                
                # Afficher le frame redimensionné
                screen.blit(frame, (0, 0))
                pygame.display.flip()  # Mettre à jour l'affichage

# Nettoyer
pygame.quit()
kinect.close()


# # Test
# import sys
# from pykinect2 import PyKinectV2, PyKinectRuntime
# import pygame
# import cv2  # Nécessaire pour redimensionner l'image
# import pandas as pd

# # Initialisation de Pygame
# pygame.init()

# # Dimensions de la fenêtre réduite (par exemple, moitié de la résolution native du Kinect)
# width, height = 960, 540
# screen = pygame.display.set_mode((width, height))

# # Stockage des données
# hand_left_positions = []

# # Initialisation du Kinect
# kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

# print("Initialisation du Kinect...")

# # Boucle principale
# running = True
# print("Début de la boucle principale...")
# while running:
#     # Gestion des événements Pygame
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
    
#     # Afficher le squelette bâton
#     if kinect.has_new_body_frame():
#         bodies = kinect.get_last_body_frame()
        
#         if bodies is not None:
#             for i in range(0, kinect.max_body_count):
#                 body = bodies.bodies[i]
#                 if not body.is_tracked:
#                     continue
                
#                 joints = body.joints
#                 # Récupération des données seulement si la main est fermée
#                 if (body.hand_right_state == PyKinectV2.HandState_Closed & body.hand_left_state == PyKinectV2.HandState_Closed):
#                     x=joints[PyKinectV2.JointType_HandLeft].Position.x,
#                     y=joints[PyKinectV2.JointType_HandLeft].Position.y,
#                     z=joints[PyKinectV2.JointType_HandLeft].Position.z
#                     # Print des coordonnées de la main gauche
#                     print("Main gauche: x={}, y={}, z={}".format(x, y, z))
#                     # Écriture des coordonnées dans le fichier CSV
#                     hand_left_positions.append([x, y, z])
    
#     # Afficher la vidéo du Kinect
#     if kinect.has_new_color_frame():
#         frame = kinect.get_last_color_frame()
        
#         if frame is not None:
#             # Redimensionnement et transformation de l'image
#             frame = frame.reshape((1080, 1920, 4))  # Reshape du frame pour 1080p
#             frame = frame[:, :, :3]  # Supprimer le canal alpha
#             frame = cv2.resize(frame, (width, height))  # Redimensionner avec OpenCV
#             frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # Créer une surface Pygame
            
#             # Afficher le frame redimensionné
#             screen.blit(frame, (0, 0))
#             pygame.display.flip()  # Mettre à jour l'affichage

# # Nettoyer
# pygame.quit()
# kinect.close()
# sys.exit()

# # Créer un DataFrame à partir des données de la main gauche
# df = pd.DataFrame(hand_left_positions, columns=["x", "y", "z"])

# # Exporter le DataFrame en excel
# df.to_excel("hand_left_positions.xlsx", index=False)

# print("Coordonnées de la main gauche exportées avec succès !")


# # Connaître la position de toutes les articulations à importer en excel ou en csv
# # JointType_SpineBase = 0
# # JointType_SpineMid = 1
# # JointType_Neck = 2
# # JointType_Head = 3
# # JointType_ShoulderLeft = 4
# # JointType_ElbowLeft = 5
# # JointType_WristLeft = 6
# # JointType_HandLeft = 7
# # JointType_ShoulderRight = 8
# # JointType_ElbowRight = 9
# # JointType_WristRight = 10
# # JointType_HandRight = 11
# # JointType_HipLeft = 12
# # JointType_KneeLeft = 13
# # JointType_AnkleLeft = 14
# # JointType_FootLeft = 15
# # JointType_HipRight = 16
# # JointType_KneeRight = 17
# # JointType_AnkleRight = 18
# # JointType_FootRight = 19
# # JointType_SpineShoulder = 20
# # JointType_HandTipLeft = 21
# # JointType_ThumbLeft = 22
# # JointType_HandTipRight = 23
# # JointType_ThumbRight = 24
# # JointType_Count = 25