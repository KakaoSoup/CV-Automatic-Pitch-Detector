import cv2
import platform

src = 0

if(platform.system() == 'Windows'):
      capture = cv2.VideoCapture(src, cv2.CAP_DSHOW)
else:
      capture = cv2.VideoCapture(src)
      
      