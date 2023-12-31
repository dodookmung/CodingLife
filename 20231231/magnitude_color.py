import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image


def magnitude_color_show(img):
  img1, img2, img3 = img[:,:, 0], img[:,:, 1], img[:,:, 2]

  dft = cv2.dft(np.float32(img1),flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)
  magnitude_spectrum1 = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
  plt.subplot(121),plt.imshow(img1, cmap='gray')
  plt.title('R Image'), plt.xticks([]), plt.yticks([])
  plt.subplot(122),plt.imshow(magnitude_spectrum1, cmap='gray')
  plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
  plt.show()

  dft = cv2.dft(np.float32(img2),flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)
  magnitude_spectrum2 = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
  plt.subplot(121),plt.imshow(img2, cmap='gray')
  plt.title('G Image'), plt.xticks([]), plt.yticks([])
  plt.subplot(122),plt.imshow(magnitude_spectrum2, cmap='gray')
  plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
  plt.show()

  dft = cv2.dft(np.float32(img3),flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)
  magnitude_spectrum3 = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
  plt.subplot(121),plt.imshow(img3, cmap='gray')
  plt.title('B Image'), plt.xticks([]), plt.yticks([])
  plt.subplot(122),plt.imshow(magnitude_spectrum3, cmap='gray')
  plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
  plt.show()

  magnitude_spectrum1 = Image.fromarray(magnitude_spectrum1).convert('L')
  magnitude_spectrum2 = Image.fromarray(magnitude_spectrum2).convert('L')
  magnitude_spectrum3 = Image.fromarray(magnitude_spectrum3).convert('L')

  return magnitude_spectrum1, magnitude_spectrum2, magnitude_spectrum3

def magnitude_color(img):
  img1, img2, img3 = img[:,:, 0], img[:,:, 1], img[:,:, 2] 

  dft = cv2.dft(np.float32(img1),flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)
  magnitude_spectrum1 = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

  dft = cv2.dft(np.float32(img2),flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)
  magnitude_spectrum2 = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

  dft = cv2.dft(np.float32(img3),flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)
  magnitude_spectrum3 = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

  magnitude_spectrum1 = Image.fromarray(magnitude_spectrum1).convert('L')
  magnitude_spectrum2 = Image.fromarray(magnitude_spectrum2).convert('L')
  magnitude_spectrum3 = Image.fromarray(magnitude_spectrum3).convert('L')

  return magnitude_spectrum1, magnitude_spectrum2, magnitude_spectrum3



img = cv2.imread(fake_path+fake[3])
magnitude_spectrum1, magnitude_spectrum2, magnitude_spectrum3 = magnitude_color_show(img)

img = Image.open(fake_path+fake[3])

merged=Image.merge("RGB",(magnitude_spectrum1, magnitude_spectrum2, magnitude_spectrum3))
plt.subplot(121), plt.imshow(img)
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(merged)
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.show()