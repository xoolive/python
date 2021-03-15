import cv2
import matplotlib.pyplot as plt

img = cv2.imread("amsterdam.jpg", cv2.IMREAD_COLOR)
print(f"{img.shape = }")

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

# -- Rotation --

(h, w) = img.shape[:2]
# calculate the center of the image
center = (w / 2, h / 2)
scale = 1.0

# Perform the counter clockwise rotation holding at the center 45 degrees
M = cv2.getRotationMatrix2D(center, 45, scale)
rotated45 = cv2.warpAffine(img, M, (h, w))

plt.imshow(cv2.cvtColor(rotated45, cv2.COLOR_BGR2RGB))
plt.show()


# -- CLAHE --

# conversion RGB vers LAB
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
l, a, b = cv2.split(lab)
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
# Fusion du canal L amélioré avec les autres canaux A et B
merged = cv2.merge((clahe.apply(l), a, b))
# conversion LAB vers RGB
clahe = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

plt.imshow(cv2.cvtColor(clahe, cv2.COLOR_BGR2RGB))
plt.show()

# -- Edges --

edges = cv2.Canny(img, 100, 100, True)

plt.imshow(cv2.cvtColor(255 - edges, cv2.COLOR_BGR2RGB))
plt.show()
