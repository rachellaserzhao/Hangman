#!/usr/local/bin/python

''' Project: Hangman
    Module myhangman.py - a hangman game in GUI

'''
import os
import sys
from Tkinter import*
import time
from random import randint
import argparse

def main():
    
    global options
    get_options()
    
    root = Tk()
    my_gui = HangmanGame(root)
    root.mainloop()


def get_options():
    
    parser = argparse.ArgumentParser(
            description='A hangman Game')
            
    options = parser.parse_args()


# All variables are instance variables 
class HangmanGame:

    
    def __init__(self, master):

        '''this is a construtor for variables and widgets in the GUI.'''
        
        self.word = StringVar()
        self.wrong_letter = IntVar()
        self.right_letter = IntVar()
        self.letter_used = StringVar()
        self.master = master
        master.title("Hangman")

        self.label = Label(master, text="This is a Hangman Game!")
        self.label.pack()

        self.graph = Canvas(master, width=800, height=400)
        self.graph.pack()
    
        self.get_word_button = Button(master, text="get new word", command=self.wordgen, height = 2, width = 9)
        self.get_word_button.pack()

        self.field_label = Label(master, text="Enter your guess in the field below")
        self.field_label.pack()
     
        self.text_field  = Entry(master, width=10)
        self.text_field.pack(ipady=3)
        #self.text_field.grid(row=1, column=1)
        self.text_field.focus_set()
        

        self.greet_button = Button(master, text="check letter", command=self.checkletter, height = 2, width = 9)
        self.greet_button.pack()
        
        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack(side=RIGHT)

        self.graph.create_text(400, 100, text= 'HANGMAN', fill="black", font = ("Times New Roman", 40), width=300)
        self.graph.create_text(400, 200, text= 'Press "get new word" to start', fill="blue", font = ("Comic Sans MS", 15, "bold"), width=300)
        
    
    def wordgen(self):
        '''select a random word from wordlist.txt file and set self.word, self.wrong_letter, self.right_letter, self.letter_used to 
        an initlal value'''
        self.word.set('')
        self.wrong_letter.set(0)
        self.right_letter.set(0)
        self.letter_used.set('')
    
        self.graph.delete('all')
        wordfile = open('wordlist.txt', 'r')
        wordlist = wordfile.readlines()
        total_words = len(wordlist)
        random_num = randint(0, total_words - 1)
        word = wordlist[random_num].replace('\n', '')
        self.word.set(word.lower())
        chosen_word = self.word.get()
        word_len = len(chosen_word)
        #print chosen_word
        
        [self.draw_line(i) for i in range(word_len)]
        self.draw_frame()
        
    
    def checkletter(self):
        '''check If character in self.text_field exists self.word and update values of self.right_letter, self.wrong_letter, self.letter_used '''
        self.graph.delete('letters')
        
        self.graph.delete('again')
        chosen_word = self.word.get()
        
        if self.wrong_letter.get() < 6:
            guess = self.text_field.get().lower()
            if guess == '' or len(guess) > 1:
                self.graph.create_text(400, 350, text= "Please enter one letter", fill="blue", font = ("Comic Sans MS", 15, "bold"), width=350, tag="again")

            elif guess in chosen_word and guess not in self.letter_used.get():
                self.letter_used.set(self.letter_used.get() + ' ' + guess)
                self.update(guess)

                if self.right_letter.get() == len(chosen_word):
                    
                    self.graph.create_text(400, 350, text= "You won! Get a new word or close", fill="dark green", font = ("Comic Sans MS", 15, "bold"))
                    self.graph.delete('man')
                    
            elif guess not in chosen_word and guess not in self.letter_used.get():
                print "wrong letter"
                self.wrong_letter.set(self.wrong_letter.get() + 1)
                self.letter_used.set(self.letter_used.get() + ' ' + guess)
                self.draw_person(self.wrong_letter.get())

                if self.wrong_letter.get() == 6:
                    self.graph.create_text(100, 230, text= chosen_word, fill="red", font = ("Comic Sans MS", 15, "bold"), tags = "again")
                    self.animation()
                else:
                    self.graph.create_text(170, 100, text= "Wrong letter, try again", fill="red", font = ("Comic Sans MS", 15, "bold"), width=300, tags = "again")
            else:
                self.graph.create_text(170, 100, text= "You have used this letter", fill="red", font = ("Comic Sans MS", 15, "bold"), width=300, tags = "again")
        else:
            self.graph.create_text(400, 350, text= "You lost! Get a new word or close", fill="blue", font = ("Comic Sans MS", 15, "bold"), width=300)
            self.graph.delete('all')

        self.text_field.delete(0, END)
        self.graph.create_text(500, 320, text= "letters used:" + self.letter_used.get(), fill="black", font = ("Arial", 15), width=300, tag="letters")

        

    def draw_line(self, num):

        '''update self.graph to draw line for word generated'''
        self.graph.create_line(20 + num*20, 200, 35 + num*20, 200, fill="black", width=3, tags='lines')
        

    def draw_frame(self):
        '''update self.graph to draw a frame for hangman'''
        self.graph.create_line(500 , 50, 500, 300, fill="black", width=6, tags='frame')
        self.graph.create_line(480 , 50, 600, 50, fill="black", width=6, tags='frame')
        self.graph.create_line(500 , 100, 550, 50, fill="black", width=6, tags='frame')
        self.graph.create_line(580 , 50, 580, 80, fill="black", width=6, tags='frame')
        

    def update(self, letter):
        '''update self.graph to draw display correct letter and update self.right_letter'''
        chosen_word = self.word.get()
        i = 0
        while i < len(chosen_word):
            if letter == chosen_word[i]:

                self.graph.create_text(26 + i*20, 190, text= chosen_word[i], font = ("Arial", 12, "bold"))
                i += 1
                self.right_letter.set(self.right_letter.get() + 1)
            else: 
                i += 1
          
        

    def draw_person(self, num):
        '''update self.graph to the person everytime a wrong guess was made'''
      
        if num == 1:
            self.graph.create_oval(560 , 80, 600, 120, width=3, tags='man')
        elif num == 2:
            self.graph.create_line(580 , 120, 580, 210, width=4, tags='man')
        elif num == 3:
            self.graph.create_line(580 , 160, 555, 125, width=3, tags='man')        
        elif num == 4:
            self.graph.create_line(580 , 160, 605, 125, width=3, tags='man')     
        elif num == 5:
            self.graph.create_line(580 , 210, 550, 240, width=3, tags='man')       
        elif num == 6:
            self.graph.create_line(580 , 210, 610, 240, width=3, tags='man')
        

    def animation(self):
        '''update self.graph to display an animation after a game is lost '''
        cap = self.graph.create_oval(35 ,10, 75, 35, width=1,fill='DeepSkyBlue2', tags='ufo')
        disk = self.graph.create_oval(10 ,20, 100, 40, width=1, fill='orange',tags='ufo')
        for x in range(0,105):
            self.graph.move(disk, 5, 0)
            self.graph.move(cap, 5, 0)
            time.sleep(0.025)
            self.graph.update()

        time.sleep(0.5)
        self.graph.create_line(550 ,30, 540, 260, fill='yellow', width=8, tags='ufo')
        self.graph.create_line(610, 30, 620, 260, fill='yellow', width=8, tags='ufo')
        self.graph.update()

        time.sleep(1)
        self.graph.delete('man')
        self.graph.delete('ufo')
        self.graph.create_text(400, 350, text= "You lost! Get a new word or close", fill="blue", font = ("Comic Sans MS", 15, "bold"), width=350)
        self.graph.update()
        


if __name__ == '__main__':
    main()

