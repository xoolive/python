import matplotlib.pyplot as plt
import freetype

fig, ax = plt.subplots(1, 3, figsize=(15, 4))

face = freetype.Face(
    "LibertinusSerif-Regular.otf", size=48 * 64, resolution=300
)
res = face.load_char("g")
ax[0].imshow(res, cmap="gray_r")

face = freetype.Face(
    "MathJax_Fraktur-Regular.otf", size=48 * 64, resolution=300
)

res = face.load_char("F")
ax[1].imshow(res, cmap="gray_r")

face = freetype.Face("NotoSansCJK-Medium.ttc", size=48 * 64, resolution=300)
res = face.load_char("滋")

ax[2].imshow(res, cmap="gray_r")
plt.show()
