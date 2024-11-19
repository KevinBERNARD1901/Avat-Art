from pykinect2 import PyKinectV2
from pykinect2 import PyKinectRuntime
import cv2
import pygame
import openpyxl
import time

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

# Ouverture du fichier (avec l'aide de monsieur GPT parceque vraiment trop à la bourre)
chemin_fichier_excel = "Acquisition_mouvement.xlsx" # A REMPLIR !!!
classeur = openpyxl.load_workbook(chemin_fichier_excel)
feuille = classeur["Acquisition"]
ligne_acquisiton = 3 # A implémenter de 3 à chaque acquisition
Nb_acquisition_faite = 0 # A implémenter de 1 à chaque acquisition
Nb_acquisition_a_faire = 100
Nb_joints = 25


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
                
                if (Nb_acquisition_faite < Nb_acquisition_a_faire):
                    # Récupération de la position de toutes les jointures
                    if body.hand_right_state == PyKinectV2.HandState_Closed and body.hand_left_state == PyKinectV2.HandState_Closed:
                        print("Mains fermées")
                        for i in range(Nb_joints):
                            x=joints[i].Position.x
                            y=joints[i].Position.y
                            z=joints[i].Position.z
                            # Print des coordonnées de la jointure
                            print("X=", x)
                            print("Y=", y)
                            print("Z=", z)

                            # Remplissage excel
                            feuille.cell(row=ligne_acquisiton,column=i+3, value=x)
                            feuille.cell(row=ligne_acquisiton+1,column=i+3, value=y)
                            feuille.cell(row=ligne_acquisiton+2,column=i+3, value=z)

                        #Mise à jour des variable de navigation dans l'excel
                        Nb_acquisition_faite += 1
                        print("Acquisition n°", Nb_acquisition_faite)
                        ligne_acquisiton += 3
                        
                        # Faire attendre pour éviter de prendre plusieurs fois la même acquisition
                        time.sleep(1)

                else:
                    running = False

                    # draw_body(screen, joints)
                    # pygame.display.flip()
                        
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

# Enregistrement
classeur.save(chemin_fichier_excel)
print("Modification enregistrée avec succès !")

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