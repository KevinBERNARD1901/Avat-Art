########################################################################################
########################################################################################

###########################    Caractérisation des mouvements    #######################
def import_donnees_csv() :
    import sys
    from pykinect2 import PyKinectV2, PyKinectRuntime
    import pygame
    import cv2  # Nécessaire pour redimensionner l'image
    import pandas as pd

    # Initialisation de Pygame
    pygame.init()

    # Dimensions de la fenêtre réduite (par exemple, moitié de la résolution native du Kinect)
    width, height = 960, 540
    screen = pygame.display.set_mode((width, height))

    # Stockage des données
    hand_left_positions = []

    # Initialisation du Kinect
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)

    print("Initialisation du Kinect...")

    # Boucle principale
    running = True
    print("Début de la boucle principale...")
    while running:
        # Gestion des événements Pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Afficher le squelette bâton
        if kinect.has_new_body_frame():
            bodies = kinect.get_last_body_frame()
            
            if bodies is not None:
                for i in range(0, kinect.max_body_count):
                    body = bodies.bodies[i]
                    if not body.is_tracked:
                        continue
                    
                    joints = body.joints
                    # Récupération des données seulement si la main est fermée
                    if (body.hand_right_state == PyKinectV2.HandState_Closed & body.hand_left_state == PyKinectV2.HandState_Closed):
                        x=joints[PyKinectV2.JointType_HandLeft].Position.x,
                        y=joints[PyKinectV2.JointType_HandLeft].Position.y,
                        z=joints[PyKinectV2.JointType_HandLeft].Position.z
                        # Print des coordonnées de la main gauche
                        print("Main gauche: x={}, y={}, z={}".format(x, y, z))
                        # Écriture des coordonnées dans le fichier CSV
                        hand_left_positions.append([x, y, z])
        
        # Afficher la vidéo du Kinect
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
    sys.exit()

    # Créer un DataFrame à partir des données de la main gauche
    df = pd.DataFrame(hand_left_positions, columns=["x", "y", "z"])

    # Exporter le DataFrame en excel
    df.to_excel("hand_left_positions.xlsx", index=False)

    print("Coordonnées de la main gauche exportées avec succès !")



########################################################################################
########################################################################################

###########################    Détection de l'accélération    ##########################

def detection_par_acceleration() :
    from pykinect2 import PyKinectV2
    from pykinect2 import PyKinectRuntime
    import cv2
    import pygame
    import openpyxl
    import time
    import math
    # import numpy as np

    # Paramètres des animations
    animation_path_wave = "./Animations/Animation_vague_gauche.mp4"
    animation_path_wave_right = "./Animations/Animation_vague_droite.mp4"
    animation_path_aura = "./Animations/aura 2.mp4"
    animation_path_rocher = "./Animations/Rocher.mp4"
    animation_path_soulevement = ".\Animations\Animation_soulevement.mp4"
    animation_path_feu = ".\Animations\Animation_feu.mp4"

    fps = 16 # J'ai 10 images par seconde dans l'animation
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
    # screen = pygame.display.set_mode((width, height))

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

    # Fonction max
    def max(x,y):
        if x>y :
            return x
        else :
            return y

    def min(x,y):
        if x<y :
            return x
        else :
            return y  
        
    # Fonction pour l'animation du coup de pied donne vague   
    def animation_coup(animation_path) :#path en argument
        cap = cv2.VideoCapture(animation_path)
        if not cap.isOpened():
            raise Exception("ERROR: Video could not be opened")
        running = True
        while running:
            success, frame = cap.read()

            if not success: #Si on arrive à la fin de la vidéo, on arrête la boucle while
                running = False
                continue

            screen = cv2.resize(frame, (screen_width, screen_height), interpolation=cv2.INTER_LINEAR)
            
            cv2.imshow("Frame", frame)

            if cv2.waitKey(delay) & 0xFF == ord('q'):#
                running = False
                
        cap.release()

    # Boucle principale
    running_loop = True
    running_animation = False
    liste_position=[]
    attente = False

    while running_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_loop = False
        
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
                    indice_pied_gauche = 15
                    indice_genou_gauche = 13
                    indice_genou_droit = 17
                    indice_epaule_droite = 8
                    indice_coude_droit = 9
                    indice_tete = 3
                    indice_poing_droit = 11
                    indice_poing_gauche = 7
                    indice_hanche_droite = 16
                    indice_hanche_gauche = 12
                    indice_milieu_colonne = 1
                    indice_hanche = 0
                    
                    liste_position=[]
                    
                    # Récupération des positions
                    for i in range(25):
                        liste_position.append([joints[i].Position.x, joints[i].Position.y, joints[i].Position.z])
                    
                    # Test de comparaison coup de pied droit
                    if attente != True and liste_position[indice_pied_droit][1] > liste_position[indice_genou_gauche][1] : 
                        print("Pied droit plus haut que genou gauche")
                        animation_coup(animation_path_wave)
                        # running_loop = False
                        
                    # Test de comparaison coup de pied gauche 
                    if attente != True and liste_position[indice_pied_gauche][1]> liste_position[indice_genou_droit][1] : 
                        print("Pied gauche plus haut que genou droit")
                        animation_coup(animation_path_wave_right)
                        # running_loop = False
                    
                    #Test coup de poing droit
                    if attente != True and liste_position[indice_epaule_droite][1] < liste_position[indice_poing_droit][1] < liste_position[indice_tete][1]  and liste_position[indice_coude_droit][1] > liste_position[indice_epaule_droite][1] and liste_position[indice_poing_droit][0] > liste_position[indice_coude_droit][0]:
                        t1=time.time()                    
                        print("coup de poing feu")
                        attente = 0.1
                        # Détection de l'intensité
                            # Nouvelle frame
                        time.sleep(attente)
                        bodies_2 = kinect.get_last_body_frame()
                        if bodies_2 != None:
                            for i in range(0, kinect.max_body_count):
                                body_2 = bodies_2.bodies[i]
                                if not body_2.is_tracked:
                                    continue
                                joints_2 = body_2.joints
                        t2 = time.time()

                        bodies_3 = kinect.get_last_body_frame()
                        if bodies_3 != None:
                            for i in range(0, kinect.max_body_count):
                                body_3 = bodies_3.bodies[i]
                                if not body_3.is_tracked:
                                    continue
                                joints_3 = body_3.joints
                        t3=time.time()
                        
                        time.sleep(attente)
                        bodies_4 = kinect.get_last_body_frame()
                        if bodies_4 != None:
                            for i in range(0, kinect.max_body_count):
                                body_4 = bodies_4.bodies[i]
                                if not body_4.is_tracked:
                                    continue
                                joints_4 = body_4.joints
                        t4=time.time()
                        
                            # Position main droite
                        delta_x_1 = abs(joints[indice_poing_droit].Position.x - joints_2[indice_poing_droit].Position.x)
                        delta_y_1 = abs(joints[indice_poing_droit].Position.y - joints_2[indice_poing_droit].Position.y)
                        distance_1 = math.sqrt(delta_x_1**2 + delta_y_1**2)
                        vitesse_1 = distance_1 / (t2-t1)
                        print("vitesse 1: ", vitesse_1)
                        delta_x_2 = abs(joints_3[indice_poing_droit].Position.x - joints_4[indice_poing_droit].Position.x)
                        delta_y_2 = abs(joints_3[indice_poing_droit].Position.y - joints_4[indice_poing_droit].Position.y)
                        distance_2 = math.sqrt(delta_x_2**2 + delta_y_2**2)
                        vitesse_2 = distance_2 / (t4-t3)
                        
                        print("vitesse 2 : ", vitesse_2)
                        acceleration = abs(vitesse_2-vitesse_1)/(t4-t1)
                        print("accélération :", acceleration)
                                
                        
                        # Lancement de l'animation                    
                        animation_coup(animation_path_feu)
                        # running_loop = False
                    
                    #Test soulèvement
                    if attente != True and liste_position[indice_poing_droit][1] < max(liste_position[indice_genou_droit][1],liste_position[indice_genou_gauche][1]) and liste_position[indice_poing_gauche][1] > liste_position[indice_tete][1]:
                        print("Soulèvement")
                        animation_coup(animation_path_soulevement)
                        attente = True
                            
                    #Test coup de poing terre
                    if attente == True and liste_position[indice_epaule_droite][1] < liste_position[indice_poing_droit][1] < liste_position[indice_tete][1]  and liste_position[indice_coude_droit][1] > liste_position[indice_epaule_droite][1] and liste_position[indice_poing_droit][0] > liste_position[indice_coude_droit][0]:
                        print("tete vers droite")
                        animation_coup(animation_path_rocher)
                        attente = False
                    
                    #Test aura + fin
                    if attente != True and body.hand_right_state == PyKinectV2.HandState_Closed and body.hand_left_state == PyKinectV2.HandState_Closed and min(liste_position[indice_poing_droit][1],liste_position[indice_poing_gauche][1])>liste_position[indice_tete][1]:
                        print("aura + fin")
                        animation_coup(animation_path_aura)
                        running_loop=False
                        input() #Faire alt+échap puis entrer quelque chose dans le terminal

            if kinect.has_new_color_frame():
                frame = kinect.get_last_color_frame()

    # Nettoyer
    pygame.quit()
    kinect.close()