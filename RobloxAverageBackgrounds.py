import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

directory = "./RobloxHome"
loadDir = "/RobloxImages/"
saveDir = "/RobloxColors/"
colorAverages = []
fileNames = []
for filename in os.listdir(directory + loadDir):
    fileNames.append(filename[5:-4].replace("_", "-") + "\n" + filename[:4])
    print(filename)
    arr = cv2.imread(directory+ loadDir + filename)
    newArr = arr[0]
    for y in range(1, np.shape(arr)[0]):
        newArr = np.concatenate((newArr, arr[y]))

    vals, counts = np.unique(newArr, return_counts=True, axis=0)
    vals = list(vals)
    counts = list(counts)

    colors = {}
    sum = 0
    averageColor = [0, 0, 0]
    for i in range(len(counts)):
        colors[counts[i]] = vals[i]
        averageOfColor = 0
        sum += counts[i]
        for j in range(3):
            averageColor[j] += counts[i]*vals[i][j]
    for i in range(3):
        averageColor[i] /= sum
        averageColor[i] = round(averageColor[i])
    colors = dict(reversed(sorted(colors.items())))

    width, height = 300, 100
    blankimage = np.zeros((height, width, 3), np.uint8)
    amount, offset = 15, 0

    blankimage[int(height*5/6):, :] = averageColor
    for i in range(width):
        blankimage[:int(height*5/6), i] = colors[list(colors)[int(i/width*amount+offset)]]
    cv2.imwrite(directory + saveDir + "C_" + filename, blankimage)
    colorAverages.append(averageColor)
    print(averageColor)

x = np.array(range(len(colorAverages)))
y = np.array(colorAverages)

yav = (y[:, 0] + y[:, 1] + y[:, 2])/3

plt.plot(x, y[:, 0], color="blue")
plt.plot(x, y[:, 1], color="green")
plt.plot(x, y[:, 2], color="red")
plt.plot(x, yav, color="black")
index = 0
for xp,yp in zip(x,y[:, 0]):
    plt.annotate(fileNames[index], (xp, yp), textcoords="offset points", xytext=(0,10), ha='center')
    index += 1
plt.ylim(0, 255)
plt.title("Average Colors")
plt.xlabel("Date")
plt.ylabel("Colors")
ax = plt.gca()
ax.axes.xaxis.set_ticklabels([])
plt.show()