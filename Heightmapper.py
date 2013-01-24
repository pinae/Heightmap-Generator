#! /usr/bin/env python
# coding=utf-8

import cv
from random import randint
from Watermapper import createWatermap
from Config import mapdimensions, slope, slopediag


def updateMaxmap(maxmap, watermap_dir, pix, height):
    maxmap[pix[0], pix[1]] = height
    neighborheight = height
    if watermap_dir[pix[0], pix[1]] != 0: neighborheight = height + slope
    testpix = (pix[0] - 1, pix[1])
    if testpix[0] >= 0:
        if maxmap[testpix[0], testpix[1]] > neighborheight:
            updateMaxmap(maxmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    if watermap_dir[pix[0], pix[1]] != 1: neighborheight = height + slopediag
    testpix = (pix[0] - 1, pix[1] - 1)
    if testpix[0] >= 0 and testpix[1] >= 0:
        if maxmap[testpix[0], testpix[1]] > neighborheight:
            updateMaxmap(maxmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    if watermap_dir[pix[0], pix[1]] != 2: neighborheight = height + slope
    testpix = (pix[0], pix[1] - 1)
    if testpix[1] >= 0:
        if maxmap[testpix[0], testpix[1]] > neighborheight:
            updateMaxmap(maxmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    if watermap_dir[pix[0], pix[1]] != 3: neighborheight = height + slopediag
    testpix = (pix[0] + 1, pix[1] - 1)
    if testpix[0] < maxmap.height and testpix[1] >= 0:
        if maxmap[testpix[0], testpix[1]] > neighborheight:
            updateMaxmap(maxmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    if watermap_dir[pix[0], pix[1]] != 4: neighborheight = height + slope
    testpix = (pix[0] + 1, pix[1])
    if testpix[0] < maxmap.height:
        if maxmap[testpix[0], testpix[1]] > neighborheight:
            updateMaxmap(maxmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    if watermap_dir[pix[0], pix[1]] != 5: neighborheight = height + slopediag
    testpix = (pix[0] + 1, pix[1] + 1)
    if testpix[0] < maxmap.height and testpix[1] < maxmap.width:
        if maxmap[testpix[0], testpix[1]] > neighborheight:
            updateMaxmap(maxmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    if watermap_dir[pix[0], pix[1]] != 6: neighborheight = height + slope
    testpix = (pix[0], pix[1] + 1)
    if testpix[1] < maxmap.width:
        if maxmap[testpix[0], testpix[1]] > neighborheight:
            updateMaxmap(maxmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    if watermap_dir[pix[0], pix[1]] != 7: neighborheight = height + slopediag
    testpix = (pix[0] - 1, pix[1] + 1)
    if testpix[0] >= 0 and testpix[1] < maxmap.width:
        if maxmap[testpix[0], testpix[1]] > neighborheight:
            updateMaxmap(maxmap, watermap_dir, testpix, neighborheight)


def updateMinmap(minmap, watermap_dir, pix, height):
    #print "Pos: "+str(pix[0])+","+str(pix[1])
    minmap[pix[0], pix[1]] = height
    neighborheight = height
    testpix = (pix[0] - 1, pix[1])
    if testpix[0] >= 0:
        #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
        #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
        if watermap_dir[testpix[0], testpix[1]] != 4: neighborheight = height - slope
        if minmap[testpix[0], testpix[1]] < neighborheight:
            updateMinmap(minmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    testpix = (pix[0] - 1, pix[1] - 1)
    if testpix[0] >= 0 and testpix[1] >= 0:
        #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
        #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
        if watermap_dir[testpix[0], testpix[1]] != 5: neighborheight = height - slopediag
        if minmap[testpix[0], testpix[1]] < neighborheight:
            updateMinmap(minmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    testpix = (pix[0], pix[1] - 1)
    if testpix[1] >= 0:
        #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
        #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
        if watermap_dir[testpix[0], testpix[1]] != 6: neighborheight = height - slope
        if minmap[testpix[0], testpix[1]] < neighborheight:
            updateMinmap(minmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    testpix = (pix[0] + 1, pix[1] - 1)
    if testpix[0] < minmap.height and testpix[1] >= 0:
        #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
        #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
        if watermap_dir[testpix[0], testpix[1]] != 7: neighborheight = height - slopediag
        if minmap[testpix[0], testpix[1]] < neighborheight:
            updateMinmap(minmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    testpix = (pix[0] + 1, pix[1])
    if testpix[0] < minmap.height:
        #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
        #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
        if watermap_dir[testpix[0], testpix[1]] != 0: neighborheight = height - slope
        if minmap[testpix[0], testpix[1]] < neighborheight:
            updateMinmap(minmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    testpix = (pix[0] + 1, pix[1] + 1)
    if testpix[0] < minmap.height and testpix[1] < minmap.width:
        #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
        #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
        if watermap_dir[testpix[0], testpix[1]] != 1: neighborheight = height - slopediag
        if minmap[testpix[0], testpix[1]] < neighborheight:
            updateMinmap(minmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    testpix = (pix[0], pix[1] + 1)
    if testpix[1] < minmap.width:
        #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
        #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
        if watermap_dir[testpix[0], testpix[1]] != 2: neighborheight = height - slope
        if minmap[testpix[0], testpix[1]] < neighborheight:
            updateMinmap(minmap, watermap_dir, testpix, neighborheight)
    neighborheight = height
    testpix = (pix[0] - 1, pix[1] + 1)
    if testpix[0] >= 0 and testpix[1] < minmap.width:
        #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
        #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
        if watermap_dir[testpix[0], testpix[1]] != 3: neighborheight = height - slopediag
        if minmap[testpix[0], testpix[1]] < neighborheight:
            updateMinmap(minmap, watermap_dir, testpix, neighborheight)


def updateMaxmapStack(maxmap, watermap_dir, startpix, startheight):
    maxmapStack = [[startpix,startheight]]

    def insertMaxmapStack(pix, height):
        for i in range(0, len(maxmapStack)):
            if maxmapStack[i][1] <= height:
                maxmapStack.insert(i, [pix, height])
                break
        maxmapStack.append([pix,height])

    while len(maxmapStack):
        data = maxmapStack.pop(0)
        pix = data[0]
        height = data[1]
        maxmap[pix[0], pix[1]] = height
        neighborheight = height
        if watermap_dir[pix[0], pix[1]] != 0: neighborheight = height + slope
        testpix = (pix[0] - 1, pix[1])
        if testpix[0] >= 0:
            if maxmap[testpix[0], testpix[1]] > neighborheight:
                insertMaxmapStack(testpix, neighborheight)
        neighborheight = height
        if watermap_dir[pix[0], pix[1]] != 1: neighborheight = height + slopediag
        testpix = (pix[0] - 1, pix[1] - 1)
        if testpix[0] >= 0 and testpix[1] >= 0:
            if maxmap[testpix[0], testpix[1]] > neighborheight:
                insertMaxmapStack(testpix, neighborheight)
        neighborheight = height
        if watermap_dir[pix[0], pix[1]] != 2: neighborheight = height + slope
        testpix = (pix[0], pix[1] - 1)
        if testpix[1] >= 0:
            if maxmap[testpix[0], testpix[1]] > neighborheight:
                insertMaxmapStack(testpix, neighborheight)
        neighborheight = height
        if watermap_dir[pix[0], pix[1]] != 3: neighborheight = height + slopediag
        testpix = (pix[0] + 1, pix[1] - 1)
        if testpix[0] < maxmap.height and testpix[1] >= 0:
            if maxmap[testpix[0], testpix[1]] > neighborheight:
                insertMaxmapStack(testpix, neighborheight)
        neighborheight = height
        if watermap_dir[pix[0], pix[1]] != 4: neighborheight = height + slope
        testpix = (pix[0] + 1, pix[1])
        if testpix[0] < maxmap.height:
            if maxmap[testpix[0], testpix[1]] > neighborheight:
                insertMaxmapStack(testpix, neighborheight)
        neighborheight = height
        if watermap_dir[pix[0], pix[1]] != 5: neighborheight = height + slopediag
        testpix = (pix[0] + 1, pix[1] + 1)
        if testpix[0] < maxmap.height and testpix[1] < maxmap.width:
            if maxmap[testpix[0], testpix[1]] > neighborheight:
                insertMaxmapStack(testpix, neighborheight)
        neighborheight = height
        if watermap_dir[pix[0], pix[1]] != 6: neighborheight = height + slope
        testpix = (pix[0], pix[1] + 1)
        if testpix[1] < maxmap.width:
            if maxmap[testpix[0], testpix[1]] > neighborheight:
                insertMaxmapStack(testpix, neighborheight)
        neighborheight = height
        if watermap_dir[pix[0], pix[1]] != 7: neighborheight = height + slopediag
        testpix = (pix[0] - 1, pix[1] + 1)
        if testpix[0] >= 0 and testpix[1] < maxmap.width:
            if maxmap[testpix[0], testpix[1]] > neighborheight:
                insertMaxmapStack(testpix, neighborheight)


def updateMinmapStack(minmap, watermap_dir, startpix, startheight):
    minmapStack = [[startpix,startheight]]

    def insertMinmapStack(pix, height):
        for i in range(0, len(minmapStack)):
            if minmapStack[i][1] >= height:
                minmapStack.insert(i, [pix, height])
                break
        minmapStack.append([pix, height])

    while len(minmapStack):
        data = minmapStack.pop(0)
        pix = data[0]
        height = data[1]
        #print "Pos: "+str(pix[0])+","+str(pix[1])
        minmap[pix[0], pix[1]] = height
        neighborheight = height
        testpix = (pix[0] - 1, pix[1])
        if testpix[0] >= 0:
            #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
            #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
            if watermap_dir[testpix[0], testpix[1]] != 4: neighborheight = height - slope
            if minmap[testpix[0], testpix[1]] < neighborheight:
                insertMinmapStack(testpix,neighborheight)
        neighborheight = height
        testpix = (pix[0] - 1, pix[1] - 1)
        if testpix[0] >= 0 and testpix[1] >= 0:
            #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
            #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
            if watermap_dir[testpix[0], testpix[1]] != 5: neighborheight = height - slopediag
            if minmap[testpix[0], testpix[1]] < neighborheight:
                insertMinmapStack(testpix,neighborheight)
        neighborheight = height
        testpix = (pix[0], pix[1] - 1)
        if testpix[1] >= 0:
            #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
            #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
            if watermap_dir[testpix[0], testpix[1]] != 6: neighborheight = height - slope
            if minmap[testpix[0], testpix[1]] < neighborheight:
                insertMinmapStack(testpix,neighborheight)
        neighborheight = height
        testpix = (pix[0] + 1, pix[1] - 1)
        if testpix[0] < minmap.height and testpix[1] >= 0:
            #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
            #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
            if watermap_dir[testpix[0], testpix[1]] != 7: neighborheight = height - slopediag
            if minmap[testpix[0], testpix[1]] < neighborheight:
                insertMinmapStack(testpix,neighborheight)
        neighborheight = height
        testpix = (pix[0] + 1, pix[1])
        if testpix[0] < minmap.height:
            #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
            #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
            if watermap_dir[testpix[0], testpix[1]] != 0: neighborheight = height - slope
            if minmap[testpix[0], testpix[1]] < neighborheight:
                insertMinmapStack(testpix,neighborheight)
        neighborheight = height
        testpix = (pix[0] + 1, pix[1] + 1)
        if testpix[0] < minmap.height and testpix[1] < minmap.width:
            #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
            #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
            if watermap_dir[testpix[0], testpix[1]] != 1: neighborheight = height - slopediag
            if minmap[testpix[0], testpix[1]] < neighborheight:
                insertMinmapStack(testpix,neighborheight)
        neighborheight = height
        testpix = (pix[0], pix[1] + 1)
        if testpix[1] < minmap.width:
            #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
            #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
            if watermap_dir[testpix[0], testpix[1]] != 2: neighborheight = height - slope
            if minmap[testpix[0], testpix[1]] < neighborheight:
                insertMinmapStack(testpix,neighborheight)
        neighborheight = height
        testpix = (pix[0] - 1, pix[1] + 1)
        if testpix[0] >= 0 and testpix[1] < minmap.width:
            #print "Watermap x|y: "+str(testpix[0])+"|"+str(testpix[1])
            #print " :: "+str(watermap[testpix[0]][testpix[1]].dir)
            if watermap_dir[testpix[0], testpix[1]] != 3: neighborheight = height - slopediag
            if minmap[testpix[0], testpix[1]] < neighborheight:
                insertMinmapStack(testpix,neighborheight)


def createHightmap(watermap_dir):
    cv.NamedWindow("heightmap", cv.CV_WINDOW_AUTOSIZE)
    cv.NamedWindow("minmap", cv.CV_WINDOW_AUTOSIZE)
    cv.NamedWindow("maxmap", cv.CV_WINDOW_AUTOSIZE)
    cv.MoveWindow("heightmap", 10, 10)
    cv.MoveWindow("minmap", 10 + mapdimensions[0] + 10, 10)
    cv.MoveWindow("maxmap", 10 + 2 * mapdimensions[0] + 20, 10)
    heightmap = cv.CreateImage((mapdimensions[0], mapdimensions[1]), 8, 1)
    minmap = cv.CreateImage((mapdimensions[0], mapdimensions[1]), 8, 1)
    maxmap = cv.CreateImage((mapdimensions[0], mapdimensions[1]), 8, 1)
    for x in range(0, mapdimensions[0]):
        for y in range(0, mapdimensions[1]):
            maxmap[y, x] = 255
            minmap[y, x] = 0
            heightmap[y, x] = 0
            watermap_dir[y, x] = watermap_dir[y, x] / 30
    fails = 0
    update = 0
    startphase = 400
    while fails < 10:
        pix = (randint(0, mapdimensions[1] - 1), randint(0, mapdimensions[0] - 1))
        if heightmap[pix[0], pix[1]] > 0:
            fails += 1
            #print "Fails erhöht auf "+str(fails)
        else:
            fails = 0
            #print "Fails auf 0 gesetzt"
            height = randint(minmap[pix[0], pix[1]], maxmap[pix[0], pix[1]])
            heightmap[pix[0], pix[1]] = height
            #min- und maxmap updaten
            updateMaxmap(maxmap, watermap_dir, pix, height)
            updateMinmap(minmap, watermap_dir, pix, height)
            #Anzeige
            if update == 0:
                if startphase > 0:
                    update = 1
                else:
                    update = 75 + 10 * (fails + 1) * (fails + 1)
                cv.ShowImage("heightmap", heightmap)
                cv.ShowImage("minmap", minmap)
                cv.ShowImage("maxmap", maxmap)
                if cv.WaitKey(1) == 27:
                    break
            update -= 1
            startphase -= 1
            #cv.WaitKey(0)
    print "Zufälliges setzen der Pixel beendet. Jetzt systematisch."
    for y in range(0, mapdimensions[1]):
        for x in range(0, mapdimensions[0]):
            pix = (y, x)
            height = randint(minmap[pix[0], pix[1]], maxmap[pix[0], pix[1]])
            heightmap[pix[0], pix[1]] = height
            #min- und maxmap updaten
            updateMaxmap(maxmap, watermap_dir, pix, height)
            updateMinmap(minmap, watermap_dir, pix, height)
            #Anzeige
        cv.ShowImage("heightmap", heightmap)
        cv.ShowImage("minmap", minmap)
        cv.ShowImage("maxmap", maxmap)
        if cv.WaitKey(1) == 27:
            break
    cv.ShowImage("heightmap", heightmap)
    cv.ShowImage("minmap", minmap)
    cv.ShowImage("maxmap", maxmap)
    cv.SaveImage("heightmap.png", heightmap)
    cv.WaitKey(0)


def main():
    watermap = createWatermap()
    createHightmap(watermap[0])


if __name__ == "__main__":
    main()