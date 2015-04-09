import time
import win32api
import multiprocessing as mp

import Image
import ImageGrab
import win32con
import numpy


# Globals
x_pad = 252
y_pad = 156
purple2 = Image.open('purple2.png')
purple3 = Image.open('purple3.png')
carrierGreen = Image.open('carrierGreen.png')
carrierGreenFlipped = Image.open('carrierGreen.png').transpose(Image.FLIP_LEFT_RIGHT)
motherShip = Image.open('motherShip.png')
motherShipCheck = Image.open('motherShipCheck.png')

alienVarieties = [Image.open('yellow1.png'), Image.open('yellow3.png'), Image.open('yellow4.png'),
                  Image.open('yellow5.png'), Image.open('blue3.png'), Image.open('blue5.png'), Image.open('blue6.png'),
                  Image.open('purple2.png'), Image.open('purple3.png')]

# Define an output queue
output = mp.Queue(maxsize=0)


def screenGrabToRam():
    box = (x_pad, y_pad, x_pad + 1129, y_pad + 348)
    return ImageGrab.grab(box)


def screenGrabToRamMotherShipCheck():
    box = (12, 114, 14, 116)
    return ImageGrab.grab(box)


def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def mousePos(cord):
    win32api.SetCursorPos((x_pad + cord[0], y_pad + cord[1]))
    time.sleep(.02)


def subImg(img1, img2, returnFirstMatch):
    img1 = numpy.asarray(img1)
    img2 = numpy.asarray(img2)

    img1y = img1.shape[0]
    img1x = img1.shape[1]

    img2y = img2.shape[0]
    img2x = img2.shape[1]

    stopy = img2y - img1y + 1
    stopx = img2x - img1x + 1

    # Setup a list of processes that we want to run
    processes = 4
    yStartAndEnds = []

    chunkSize = stopy / 4

    if chunkSize > 1:
        for x in range(processes):
            start = (chunkSize * x) + x
            stop = (chunkSize * (x + 1)) + x
            if stop > stopy:
                stop = stopy
            yStartAndEnds.append((start, stop))
    else:
        processes = 1
        yStartAndEnds.append((0, stopy))

    processes = [mp.Process(target=subImageWorker, args=(img1, img2, img1x, img1y, stopx, yStartAndEnds[x][0], yStartAndEnds[x][1], output, returnFirstMatch)) for x in range(processes)]

    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    # Get process results from the output queue
    results = []
    for p in processes:
        while not output.empty():
            results.append(output.get())

    return results


# define a example function
def subImageWorker(img1, img2, img1x, img1y, stopx, starty, stopy, output, returnFirstMatch):
    for x1 in range(0, stopx):
        for y1 in range(starty, stopy):
            x2 = x1 + img1x
            y2 = y1 + img1y

            pic = img2[y1:y2, x1:x2]
            test = pic == img1

            if test.all():
                output.put((x1, y1))
                if returnFirstMatch:
                    return

    return


def isMotherShipHere():
    motherShipMatches = subImg(motherShipCheck, screenGrabToRamMotherShipCheck(), True)
    return len(motherShipMatches) > 0


def main():

    currentAlienVariety = 0
    timesNotFound = 0

    while True:
        # carrierMatches = subImg(carrierGreen, screenGrabToRam(), True)
        # for match in carrierMatches:
        #     mousePos(match)
        #
        #     for x in range(0, 6):
        #         leftClick()
        #         time.sleep(.01)

        if isMotherShipHere():
            print('Mothership is here!')
            motherShipMatches = subImg(motherShip, screenGrabToRam(), True)
            for match in motherShipMatches:
                modifiedPos = (match[0], match[1])
                mousePos(modifiedPos)

                for x in range(0, 200):
                    leftClick()
                    time.sleep(.005)

        print('currently searching for variety index:' + str(currentAlienVariety))
        matches = subImg(alienVarieties[currentAlienVariety], screenGrabToRam(), False)
        for match in matches:
            mousePos(match)

        if len(matches) == 0:
            timesNotFound += 1

        if timesNotFound > 2:
            currentAlienVariety += 1

            if currentAlienVariety >= len(alienVarieties):
                currentAlienVariety = 0

            timesNotFound = 0



if __name__ == '__main__':
    main()