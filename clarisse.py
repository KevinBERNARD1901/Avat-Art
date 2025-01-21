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

def max_liste(L):
    res=0
    for x in l:
        if x> res :
            res = X
    return res
      
# Fonction pour l'animation du coup de pied donne vague   
def animation_coup(animation_path):#path en argument
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
                                        
                    print("coup de poing feu")
                    temps_boucle = 0.3
                    X = []
                    Y = []
                    D = [] # Distance
                    V = [] # Vitesse
                    A = [] # Accélération
                    
                    delta_X = []
                    delta_Y = []
                    delta_V = []
                    
                    t_vitesse = 0
                    compteur_frame = 0
                    
                    t1 = time.time()
                    t2 = time.time()
                    
                    while t2-t1 < temps_boucle:
                        compteur_frame+=1
                        t2=time.time()
                        
                        if compteur_frame == 4:
                            t_vitesse = t2-t1                            
                            
                        bodies_int = kinect.get_last_body_frame()
                        if bodies_int != None:
                            for i in range(0, kinect.max_body_count):
                                body_int = bodies_int.bodies[i]
                                if not body_int.is_tracked:
                                    continue
                                joints_int = body_int.joints
                        X += [joints_int[indice_poing_droit].Position.x]
                        Y += [joints_int[indice_poing_droit].Position.y]
                    l = len(X) # Longueur de la liste
                    
                    for i in range(3,l,4):
                        delta_X+=[abs(X[i]-X[i-3])]
                        delta_Y+=[abs(Y[i]-Y[i-3])]
                    
                    for i in len(delta_X) :
                        D.append(math.sqrt(delta_X[i]**2 + delat_Y[i]**2))
                    
                    for i in D:
                        i = i/t_vitesse
                    
                    for i in range(1,len(V),2):
                        delta_V.append(abs(V[i]-V[i-1]))
                    
                    for v in delta_V:
                        A.append(v/(2*t_vitesse))
                    
                    print(max_liste(A))
                    
                    
                    
                    
                    # Détection de l'intensité
                        # Nouvelle frame
                    
                    
                    
                    
                    
                    
                    
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
            
            # if frame is not None:
            #     # Redimensionnement et transformation de l'image
            #     frame = frame.reshape((1080, 1920, 4))  # Reshape du frame pour 1080p
            #     frame = frame[:, :, :3]  # Supprimer le canal alpha
            #     frame = cv2.resize(frame, (width, height))  # Redimensionner avec OpenCV
            #     frame = pygame.surfarray.make_surface(frame.swapaxes(0, 1))  # Créer une surface Pygame
                
            #     # Afficher le frame redimensionné
            #     screen.blit(frame, (0, 0))
            #     pygame.display.flip()  # Mettre à jour l'affichage

# Nettoyer
pygame.quit()
kinect.close()