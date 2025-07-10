import random
import matplotlib.pyplot as plt

k = int(input("Please, provide number of clusters: "))
observationFile = input("Please, provide path to the file: ")
print("------------------------------------------")
valuesList = []
with open(observationFile, "r") as file:
    fileLines = file.readlines()
    fileLines.remove(fileLines[0])
    tempList = []
    for list in fileLines:
        tempList = list.split(',')
        tempList[len(tempList)-1] = tempList[len(tempList)-1].replace('\n', '')
        for index in range(len(tempList)-1):
            tempList[index] = float(tempList[index])
        valuesList.append(tempList)

amountOfAttributes = len(valuesList[0])-1

clusters = []
centroidList = []

for i in range(0, k):
    clusters.append([])

for observation in valuesList:
    clusters[random.randint(0,k-1)].append(observation)


def getCluster(observation):
    for cluster in clusters:
        if(observation in cluster):
            return clusters.index(cluster)

def getPurity():
    print("Purity:")
    for clusterIndex in range(len(clusters)):
        classes = {}
        for observation in clusters[clusterIndex]:
            if observation[len(observation)-1] not in classes:
                classes[observation[len(observation) - 1]] = 0
            classes[observation[len(observation)-1]] += 1
        print(f"\tCluster {clusterIndex+1}:")
        for key in classes:
            print(f"\t\t{key}: {classes[key]/len(clusters[clusterIndex])*100}%")


def calculateCentroids():
    global centroidList

    centroidList = []

    for _ in range(k):
        centroidList.append([0 for _ in range(amountOfAttributes)])

    for clusterIndex in range(len(clusters)):
        try:
            for observationIndex in range(len(clusters[clusterIndex])):
                for index in range(len(clusters[clusterIndex][observationIndex]) - 1):
                    centroidList[clusterIndex][index] += clusters[clusterIndex][observationIndex][index]


            for index in range(len(centroidList[clusterIndex])):
                centroidList[clusterIndex][index] /= len(clusters[clusterIndex])


        except ZeroDivisionError:
            pass
    

changed = True

def assignClusters():
    global clusters
    global changed

    changed = False

    tempClusters = []
    for i in range(0, k):
        tempClusters.append([])


    sumDistances = 0
    for observation in valuesList:
        resultList = []
        previousCluster = getCluster(observation)
        for centroid in centroidList:
            result = 0
            for index in range(len(centroid)):
                result += (centroid[index] - observation[index])**2
            resultList.append(result)
        minDistance = min(resultList)
        sumDistances += minDistance
        nearestCluster = resultList.index(minDistance)
        tempClusters[nearestCluster].append(observation)
        if(previousCluster != nearestCluster):
            changed = True
    clusters = tempClusters

    print(f"Sum of distances: {sumDistances}")
    getPurity()
    print("------------------------------------------")


def draw_clusters(clusters, centroidList):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'black', 'brown']

    for i, cluster in enumerate(clusters):
        x = [point[0] for point in cluster]
        y = [point[1] for point in cluster]
        plt.scatter(x, y, color=colors[i % len(colors)], label=f'Cluster {i + 1}')

    for i, centroid in enumerate(centroidList):
        plt.scatter(centroid[0], centroid[1], color='black', marker='x', s=100, label=f'Centroid {i + 1}')

    plt.title("K-means Cluster Visualization")
    plt.legend()
    plt.grid(True)
    plt.show()


while(changed):
    calculateCentroids()
    assignClusters()

draw_clusters(clusters, centroidList)
