#Created by: Justin Bronson
#Created on: Nov 2017
#Created for ICS3U
#This program is a virtual game of 21


#from PIL import Image
import ui
import os
import random
import time

cardsFlipped = []
selectedCards = []
dealtCards = []

positionDict = {}

cardFlipCount = 0
totalMoves = 0
locked = 0

#initalize arrays
deck = (os.listdir('./assets/deck'))

def card_dealer():
    cardDealt = random.randint(0,51)
    while cardDealt in dealtCards:
        cardDealt = random.randint(0,51)
    dealtCards.append(cardDealt)
    return cardDealt
    
def flip_cards():
    global locked
    view[cardsFlipped[0]].image = ui.Image('./assets/image.jpeg').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
    view[cardsFlipped[1]].image = ui.Image('./assets/image.jpeg').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
    view[cardsFlipped[0]].enabled = True
    view[cardsFlipped[1]].enabled = True
    del cardsFlipped[0:len(cardsFlipped)]
    view['result_label'].text = ''
    locked = 0

def select_position():
    cardPosition = random.randint(1,12)
    while cardPosition in selectedCards:
        cardPosition = random.randint(1,12)
    selectedCards.append(cardPosition)
    return cardPosition

def cardSelected(sender):
    global cardFlipCount
    global locked
    global totalMoves
    
    if locked == 1:
       return
    
    totalMoves = totalMoves + 1
    view['moves_label'].text = 'Moves: ' + str(totalMoves)
    view['result_label'].text = ''
    cardsFlipped.append(str(sender.name))
    sender.image = ui.Image('./assets/deck/' + positionDict[sender.name]).with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
    sender.enabled = False
    	
    if len(cardsFlipped) == 2:
        locked = 1
        if positionDict[cardsFlipped[0]] == positionDict[cardsFlipped[1]]:
            locked = 0
            cardFlipCount = cardFlipCount + 2
            view['result_label'].text = 'You found a match !!'
            if cardFlipCount == 12:
                view['result_label'].text = 'Congrats, you won in ' + str(totalMoves) + ' moves.'
                view['play_again_button'].enabled = True
            else:
                del cardsFlipped[0:len(cardsFlipped)]
        else:
            view['result_label'].text = 'Not a match, try again'
            ui.delay(flip_cards,1)

def start_game():
    del selectedCards[0:len(selectedCards)]
    del cardsFlipped[0:len(cardsFlipped)]
    
    global cardFlipCount
    global totalMoves
    global locked
    cardFlipCount = 0
    totalMoves = 0
    
    positionDict.clear()
    
    for counter in range(1, 13):
        view['cardButton' + str(counter)].image = ui.Image('./assets/image.jpeg').with_rendering_mode(ui.RENDERING_MODE_ORIGINAL)
        view['cardButton' + str(counter)].enabled = True
    
    view['moves_label'].text = 'Moves: 0'
    view['result_label'].text = ' '
    
    for counter in range(1, 7):
        cardSelected = card_dealer()
        cardPos1 = select_position()
        cardPos2 = select_position()
        
        positionDict['cardButton' + str(cardPos1)] = deck[cardSelected]
        positionDict['cardButton' + str(cardPos2)] = deck[cardSelected]
    
    view['play_again_button'].enabled = False
    locked = 0
	
def play_again_button_touch_up_inside(sender):
    start_game()

view = ui.load_view()
start_game()
view.present('sheet')
