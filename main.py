import cv2
import numpy as np
import pygetwindow
import pyautogui
import mss

#Put a title of Your window here
aimWindow = pygetwindow.getWindowsWithTitle('Counter-Strike 2')[0]

pyautogui.PAUSE = 0.01


with mss.mss() as sct:
    # Part of the screen to capture
    monitor = {"top": aimWindow.top, "left": aimWindow.left, "width": aimWindow.width, "height": aimWindow.height}

    #screen capturing process
    while "Screen capturing":
        img = np.array(sct.grab(monitor))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        #hsv
        lower = np.array([50, 150, 150])
        upper = np.array([70, 200, 200])

        mask = cv2.inRange(hsv, lower, upper)

        min_target_size = (100, 50)
        max_target_size = (500, 200)
        result = cv2.bitwise_and(img, img, mask=mask)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rectangles = []
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if (w >= min_target_size[0] and h >= min_target_size[1]) \
                    and (w <= max_target_size[0] and h <= max_target_size[1]):
                rectangles.append((int(x), int(y), int(w), int(h)))
                rectangles.append((int(x), int(y), int(w), int(h)))

        if len(rectangles):
            rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.5)

            for (x, y, w, h) in rectangles:
                pyautogui.moveTo(aimWindow.left + (x + (w / 2)), aimWindow.top + (y + (h / 2)), 0.02, pyautogui.easeOutQuad)
            pyautogui.leftClick()
        cv2.imshow('Computer Vision', img)

        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break