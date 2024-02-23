from pyautogui import *
import pyautogui
import time
import keyboard
from numpy import random
import win32api, win32con


#click function will ckick at the given coordonates
def click(x,y):
    win32api.SetCursorPos((x,y))     #moves the cursor to the given coordonates
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)      #left click press
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)        #left click release
    time.sleep(0.1)
    

#locateOnScreen function will search for the given image/object in the given areea
#and return the x, y coordonates if found
def locateOnScreen(img, x1, y1, width, height):
    locatie = pyautogui.locateOnScreen(img, confidence = 0.98, region = (x1, y1, width, height))   #checks if the object is visible in the given area and saves the details
    if locatie != None:    #checks if the object is visible in the given area
        x, y = (pyautogui.center(locatie))      #gets the center coordonates of the object detected
        return x, y                             #returns the x and y coordonates
    else:
        return -1, -1                           #else, returns -1, a value that cant be mistaken with a good value


#refresh funtion will refresh the pagi and wait for it to load
def refresh(x,y):
    stopped_refreshing = 0    #will be 1 when refreshing is done
    pyautogui.press('f5')     #press f5 to refresh the page
    time.sleep(0.4)
    while stopped_refreshing != 1:     #while its still frefreshing
        time.sleep(0.2)
        x_ref, y_ref = locateOnScreen('tab.jpg', x-15,y-15,40,40)      #checks if the curent tab icon is visible, if not, the tab
        if x_ref != -1:                                                    #is still refreshing and it will return the value -1, the icon
            stopped_refreshing = 1                                         #is visible, the stopped_refreshing will be 1 and stop the loop
    

#tab_detector function will search for all the steam tabs oppened, and save the coordonates of eatch of them in a list
def tab_detector():
    
    orizontal = 0      #the distance from where it starts searching for the tabs
    repetari = 0       #tells the loop if its the first time running or not
    coordonate_taburi = []    #here the tabs coordonates will be stored

    while orizontal < 1920:      #checks to not go beyond my display resolution
        x, y = locateOnScreen('tab.jpg', orizontal,0,1920,100)     #stores the x, y coordonates of the tab
        
        if x != -1:        #if there is a tab visible
            if repetari == 0:       #checks if this is the first time running the loop
                coordonate_taburi = coordonate_taburi + [[x,y]]       #stores the first tab coordonates
                click(x, y)      #clicks on the tab
                repetari = 1     #memorise that is not the first time running the loop
                print ('tab detected', x, y)    #prints the tab position
                
            else:
                if [x, y] != coordonate_taburi[-1]:    #checks if the curent tab coordonates detected is not already stored
                    coordonate_taburi = coordonate_taburi + [[x,y]]    #adds the current tab coordonates to the stored ones
                    print ('tab detected', x, y)      #prints the tab position
                    click(x, y)     #clicks on the tab
        
        else:
            print('No other tab detected')   #if there are no tabs detected
            break                            #stop the loop
        
        orizontal = orizontal+40       #the distance from where it starts searching for the tabs
    
    return coordonate_taburi         #returns all the tabs detected


#sort_and_scroll function will scroll the page until it finds the sort button, then will press the button
def scroll_and_sort(x,y):
    sort_button = 0       #gets the value 1 if the sort button was found
    scroll_tryes = 0      #counts how many times it scrolled
    x_sort, y_sort = locateOnScreen('sort_by_float.jpg', 200,50,900,300)        #searches for the sort button
    
    if x_sort != -1:    #checks if the sort button was found
        click(x_sort,y_sort)     #clicks the button
        x_sorted, y_sorted = locateOnScreen('sorted.jpg', x_sort-200, y_sort-50, 400, 100)    #checks if the button was registred as pressed
        waiting = 0   #will count the waiting loop
        while x_sorted == -1 and waiting < 20:      #if the button wasnt registred, and the loop count is < 20
            x_sorted, y_sorted = locateOnScreen('sorted.jpg', x_sort-200, y_sort-50, 400, 100)        #checks if the button was registred
            time.sleep(0.2)
            waiting = waiting + 1     #adds 1 to the loop count

    else:                 #if the button could't be pressed
        print('Sort Button Not Found\nRETRYING...')
        win32api.SetCursorPos((400,400))  #moves cursor on the page to be able to scroll
        pyautogui.scroll(20000)      #scrolls to the top of the page
        time.sleep(0.1)
    
        while sort_button != 1:       #while sort button is not found
            scroll_tryes = scroll_tryes + 1   #counts how many times it scrolled
            pyautogui.scroll(-100)     #scrolls down
            time.sleep(0.1)
            x_sort, y_sort = locateOnScreen('sort_by_float.jpg', 200,50,900,300)       #searches for the sort button
            
            if x_sort != -1:     #checks if the sort button was found
                click(x_sort, y_sort)    #clicks the button
                sort_button = 1          #counts the button as found
            
            if scroll_tryes > 20:         #if it scrolled > 30 times
                refresh(x,y)                 #will call the refresh function
                time.sleep(0.2)
                pyautogui.scroll(20000)   #will scroll to the top of the page
                scroll_tryes = 0          #will reset the scroll counter and try again on the refreshed page
            
    time.sleep(0.2)


#when called, buy function will check if there are any items that match the filter and buys them
def buy():
    buy_buttons = 1   #marks the buy button as existent (since the sort button was pressed, the buy buttons are visible)
    last_seen = 200   #marks the starting point, and then save the last y coordonate where a button was found
    
    while buy_buttons != 0:     #while there are buy buttons unchecked
        x_buy, y_buy = locateOnScreen('buy.jpg', 800, last_seen, 1600, 1000)   #will get the coordonates of the first buy button
        
        if x_buy != -1:     #if there is a buy button
            last_seen = y_buy    #save the y coordonate of the button found
            screenshot = pyautogui.screenshot()     #takes a screenshot
            r,g,b = screenshot.getpixel((x_buy, y_buy+20))    #saves the rgb values (the color) of the pixel below the button
            
            if r == 53 and g == 73 and b == 8:     #if the pixel below the button is green
                buy_buttons = 0        #marks that there will be no other buy buttons on the page
                click(x_buy, y_buy)    #clicks the buy button
                time.sleep(0.2)
                
                x_check, y_check = locateOnScreen('check_box.jpg', 0, 500, 800, 1040)      #gets the x and y coordonates of the terms and conditions box
                click(x_check, y_check)      #clicks on the terms and conditions check box
                time.sleep(0.2)
                
                x_purchase, y_purchase = locateOnScreen('purchase.jpg', 800, 500, 1920, 1040)     #gets the x and y coordonates of the purchase button
                click(x_purchase,y_purchase)     #clicks the purchase button
                time.sleep(1)
                return 1     #returns 1 to add to the buy_counter
                
        else:
            buy_buttons = 0    #marks that there are no buttons left
            return 0      #return 0 since there was no item bought
        



#here the program will start with eatch function on the necessary order
time.sleep(4)
coordonate_taburi = tab_detector()                #calls the tab_detector function and saves the tabs coordonates
print(coordonate_taburi)                          #prints the coordonates of the found tabs
sleeping_time = len(coordonate_taburi) * 2.5      #calculates the sleeping time based on the number of tabs
buy_counter = 0                                   #here will be stored the the number of items bought
loop = 0                                          #will store how many times the loop runned

while True:
    print('______________________________\n\nloop nr', loop, ':')       #marks a new loop start and prints the loop count
    
    for coordonate_tab in coordonate_taburi:        #runs through eatch tab coordonates
        x, y = coordonate_tab          #gets the current tab coordonates
        click(x,y)                 #clicks on the tab
        
        refresh(x,y)                  #calls the refresh function on the curent tab
        time.sleep(1)
        
        scroll_and_sort(x,y)       #calls the sort function
        
        bought = buy()             #calls the buy function and saves if a item was bought
        time.sleep(1)
        
        if bought != 0:          #if a item was bought
            buy_counter = buy_counter + bought          #adds 1 to the buy_counter if an item was bought
            print('item bought on tab ', coordonate_tab, ' total bought items: ', buy_counter)     #prints on what tab was the
                                                                                                   #item bought and the total number of items   
    
        if keyboard.is_pressed("q"):    #checks if the 'q' key is pressed
            break                       #will stop the loop

    print('total bought items: ', buy_counter)
    if keyboard.is_pressed("q"):    #checks if the 'q' key is pressed
            break                   #will stop the loop
        
    loop = loop + 1                 #will add 1 to the loop count
    time.sleep(random.uniform(sleeping_time, sleeping_time * 1.4))      #will pause for a randomaside time based on the number of tabs
