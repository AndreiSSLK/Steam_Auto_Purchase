# Steam Auto Purchase

A program that will automatically find the steam tabs opened, and constantly go through eatch of them to find items that match the filters aplied.
The main tool used is the locateOnScreen function from pyautogui library.


## How it works
- When starting, the program will look for all the steam tabs opened in browser and save the location of eatch of them.

![Screenshot (121)](https://github.com/AndreiSSLK/Steam_Auto_Purchase/assets/160149891/9c7f1648-f6e3-4fc9-ae6f-b884bc4141d5)


- After that, it will go through eatch tab, refresh and wait for the page to stop refreshing. After that it will look for the sort button, if not found after some tryes, it means the page got an error and needs to be refreshed again. When the sort button is found and pressed, it will check if there are any items matching the filters aplied and buy them. When done, it will stop for some time and start again.

  ![Screenshot (122)](https://github.com/AndreiSSLK/Steam_Auto_Purchase/assets/160149891/ed3ec8d5-e52c-49c9-8ea0-9958e2829b66)

- To quit the program hold down "Q" key


## Why i made it

Sometimes when I'm doing some tasks that are somewhat boring, or encounter a challange I'm curious if I could make a program that can solve that challenge. 
I do this to evolve my programming skills and to learn something from it.
