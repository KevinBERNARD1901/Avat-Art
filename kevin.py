# Test
import sys
from pykinect2 import PyKinectV2, PyKinectRuntime
import pygame
import cv2  # Nécessaire pour redimensionner l'image

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre réduite (par exemple, moitié de la résolution native du Kinect)
width, height = 960, 540
screen = pygame.display.set_mode((width, height))

# Initialisation du Kinect
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)

print("Initialisation du Kinect...")

# Boucle principale
running = True
print("Début de la boucle principale...")
while running:
    # Gestion des événements Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
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