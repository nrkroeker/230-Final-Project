"""
    Nathalie Kroeker
    CSCI 230 Final Project (Attempt Number 2)
"""
# One of these works in atom, the other works in IDLE so this checks for the right one
try:
    from Tkinter import *
except ImportError:
    from tkinter import *


# Import the required modules
import pickle
import os
import random

##=======================================================================================================================##

# Some global variables
currentState = "A"
headerFont = ("courier", "25")
noteCards = []
practiceFromLoad = True

##=======================================================================================================================##
# Class to organize our card data
class Card(object):
    def __init__(self, thisPrompt = "word", thisResponse = "definition"):
        self.setPrompt(thisPrompt)
        self.setResponse(thisResponse)

    # Setters
    def setPrompt(self, P):
        self.__thisPrompt = P

    def setResponse(self, R):
        self.__thisResponse = R

    # Getters
    def getPrompt(self):
        return self.__thisPrompt

    def getResponse(self):
        return self.__thisResponse

##=======================================================================================================================##
# Frame with the main menu buttons
class MainMenu(Frame):
    def __init__(self):
        Frame.__init__(self)
        # Header label
        Label(self, text = "EasyNote", font = headerFont, relief = "groove", bg = "#8595A5").grid(row = 0, column = 3)

        # Buttons to go to more windows
        Button(self, text = "New", command = lambda: switch(1), highlightbackground = "#BBCCDE").grid(row = 1, column = 3, ipadx = 50, pady = 5, padx = 50)
        Button(self, text = "Load", command = lambda: switch(2), highlightbackground = "#BBCCDE").grid(row = 2, column = 3, ipadx = 50, pady = 5, padx = 50)
        Button(self, text = "Quit", command = quitProgram, highlightbackground = "#BBCCDE").grid(row = 3, column = 3, ipadx = 50, pady = 5, padx = 50)

##=======================================================================================================================##
# Frame to create your new set
class NewSet(Frame):
    def __init__(self):
        Frame.__init__(self)
        # Properties
        self.allCards = []
        self.cardFileName = ""

        # Make the first set of stuff that doesn't change
        Button(self, text = "Back", command = lambda: switch(0), highlightbackground = "#BBCCDE").grid(row = 0, column = 0)
        Label(self, text = "CREATE NEW SET", font = headerFont, bg = "#8595A5").grid(row = 1, column = 1, columnspan = 2)
        Label(self, text = "Prompt", bg = "#BBCCDE").grid(row = 2, column = 1)
        Label(self, text = "Response", bg = "#BBCCDE").grid(row = 2, column = 2)
        self.createEntries()

    # Function to create the blank entries
    def createEntries(self):
        global noteCards
        entryIndex = range(0,10)
        editedCards = []
        # Use a for loop to create entries for each card
        for card in entryIndex:
            # Create the entries with default values as the original values
            Label(self, text = str(card + 1) + ".", bg = "#BBCCDE").grid(row = (card + 3), column = 0)
            cardP = Entry(self, bg = "#EACECA", fg = "#4a3736", highlightbackground = "#BBCCDE")
            cardP.grid(row = (card + 3), column = 1)

            cardR = Entry(self, bg = "#EACECA", fg = "#4a3736", highlightbackground = "#BBCCDE")
            cardR.grid(row = (card + 3), column = 2)

            cardParts = Card()
            # Append each entry so we can retrieve the values later
            cardParts.setPrompt(cardP)
            cardParts.setResponse(cardR)
            noteCards.append(cardParts)

        # Button to save
        Button(self, text = "Save", command = self.save, highlightbackground = "#BBCCDE").grid(column = 1, columnspan = 2, ipadx = 50)

    # This function saves the edited version
    def save(self):
        global noteCards, top
        for card in noteCards:
            # Retrieve the entry, get the value out of it, and replace the prompt/response in the object with that value
            editP = card.getPrompt()
            editP = editP.get()
            card.setPrompt(editP)

            editR = card.getResponse()
            editR = editR.get()
            card.setResponse(editR)

            cardLoc = noteCards.index(card)
            noteCards[cardLoc] = card

        # Save popup
        top = self.top = Toplevel()
        top["bg"] = "#BBCCDE"
        top.title("Save Set")
        Button(top, text = "Cancel", command = lambda: top.destroy(), highlightbackground = "#BBCCDE").grid()
        Label(top, text = "Name your Set: ", bg = "#BBCCDE").grid(row = 1, column = 0)

        # Populate the popup box
        self.setName = Entry(top, bg = "#EACECA", fg = "#4A3736", highlightbackground = "#BBCCDE")
        self.setName.grid(row = 1, column = 1)
        enterButton = Button(top, text = "Enter", command = self.saving, highlightbackground = "#BBCCDE").grid(row = 2, column = 2)

    # Actually save the set
    def saving(self):
        global practiceFromLoad, noteCards
        nameForFile = self.setName.get()
        self.cardFileName = str(nameForFile + ".dat")
        self.cardFile = open(self.cardFileName, "wb")
        pickle.dump(noteCards, self.cardFile)

        # Close up the saving stuff and go to the necessary place
        self.cardFile.close()
        self.top.destroy()
        practiceFromLoad = False
        switch(3)

#========================================================================================================================##
# Class to load a past set
class LoadSet(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.cardFileName = ""

        # Some buttons and labels get gridded
        Button(self, text = "Back", command = lambda: switch(0), highlightbackground = "#BBCCDE").grid(row = 0, column = 0)

        Label(self, text = "Name of set: ", bg = "#BBCCDE").grid(row = 1, column = 0)
        self.fileSearch = Entry(self, highlightbackground = "#BBCCDE", bg = "#EACECA", fg = "#4a3736")
        self.fileSearch.grid(row = 1, column = 1)

        doTheSearch = Button(self, text = "Enter", command = self.searchForFile, highlightbackground = "#BBCCDE")
        doTheSearch.grid(columnspan = 2, ipadx = 50)

    # Function to pickle load the file
    def searchForFile(self):
        thisFile = self.fileSearch.get()
        self.cardFileName = (thisFile + ".dat")

        # Check if there's anything inside the file and only load if there is no exception
        try:
            if (os.path.getsize(self.cardFileName) >= 0):
                practiceFromLoad = True
                switch(3)
        except OSError:
            top = self.top = Toplevel()
            top.title("File Not Found")
            # Can't be referenced before assignment
            def close():
                top.destroy()
                switch(2)

            Label(top, text = "File not found. Try a different name.").grid()
            Button(top, text = "Ok", command = close).grid()

##=======================================================================================================================##
# Frame for the set menu
class SetMenu(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.fileName = ""
        self.cardFile = ""

        # Check whether we're coming from the load screen or new screen
        if practiceFromLoad == True:
            self.fileName = loadScreen.cardFileName
        elif practiceFromLoad == False:
            self.fileName = newScreen.cardFileName
        self.cardFile = open(self.fileName, "rb")

        loc = self.fileName.index(".")
        fileTitle = self.fileName[0:loc]
        Label(self, text = fileTitle.upper(), font = headerFont, bg = "#8595A5").grid()
        Button(self, text = "Generate Review Cards", command = lambda: switch(4), highlightbackground = "#BBCCDE").grid(ipadx = 50, padx = 50, pady = 5)
        Button(self, text = "View/Edit Set", command = lambda: switch(5), highlightbackground = "#BBCCDE").grid(ipadx = 50, padx = 50, pady = 5)
        Button(self, text = "Return to Main Menu", command = lambda: switch(0), highlightbackground = "#BBCCDE").grid(ipadx = 50, padx = 50, pady = 5)

##=======================================================================================================================##
# Frame for practicing with your cards
class Practice(Frame):
    def __init__(self):
        global noteCards
        Frame.__init__(self)
        self.intRand = IntVar()
        Checkbutton(self, text = "Random Order", variable = self.intRand, bg = "#BBCCDE").grid(row = 0, column = 0)

        # Index must start 0, prompt must come first
        self.index = 0
        self.isPrompt = True
        self.actualCard = ""

        # Pickle load with whichever file name it is
        noteCards = pickle.load(setScreen.cardFile)
        setScreen.cardFile.close()

        self.thisCard = noteCards[self.index]
        usePrompt = self.thisCard.getPrompt()
        counterLbl = Label(self, text = (self.index + 1), bg = "#BBCCDE").grid(row = 2, column = 1)

        Label(self, text = "", bg = "#FFFFFF", relief = "groove").grid(row = 1, column = 1, ipadx = 200, ipady = 100)
        # Set up the button
        self.actualCard = Button(self, text = usePrompt, command = self.buttonSwitch)
        self.actualCard.grid(row = 1, column = 1) # MAKE PADDING SO IT IS A LARGE CARD SORTA DEAL

        # Make the previous button
        Button(self, text = "Previous", command = lambda: self.checkRand(1), highlightbackground = "#BBCCDE").grid(row = 2, column = 0)
        # Make the next button
        Button(self, text = "Next", command = lambda: self.checkRand(2), highlightbackground = "#BBCCDE").grid(row = 2, column = 2)
        # Make a back button
        Button(self, text = "Back to Set Menu", command = lambda: switch(3), highlightbackground = "#BBCCDE").grid(row = 3, columnspan = 3)

##=======================================================================================================================##
    # This function checks if we need to make it random or not
    def checkRand(self, nextPrev):
        # If 1, it comes from the previous button
        if nextPrev == 1:
            if self.intRand.get() == 1:
                self.randomOrder()
            elif self.intRand.get() == 0:
                self.previous()
            else:
                print("Oops it broke")
        elif nextPrev == 2:      # If 2, it comes from the next button
            if self.intRand.get() == 1:
                self.randomOrder()
            elif self.intRand.get() == 0:
                self.next()
            else:
                print("Oops it broke")

    # Function to change
    def randomOrder(self):
        global noteCards
        # Set up the first integer for the random index
        noteList = len(noteCards) - 1
        self.index = random.randint(0, noteList)

        # Does all the card resetup stuff
        self.thisCard = noteCards[self.index]
        self.isPrompt = False
        self.buttonSwitch()

##=======================================================================================================================##
    # Function to switch whether prompt or response is displayed
    def buttonSwitch(self):
        # Change the counter value each time this button function is run
        Label(self, text = " " + str(self.index + 1) + " ", bg = "#BBCCDE").grid(row = 2, column = 1)
        # Switch this little checker thing
        self.isPrompt = not self.isPrompt
        # Retrieve the
        usePrompt = self.thisCard.getPrompt()
        useResponse = self.thisCard.getResponse()

        if self.isPrompt == True:
            self.actualCard["text"] = usePrompt
        elif self.isPrompt == False:
            self.actualCard["text"] = useResponse

##=======================================================================================================================##
    # Function to go to the previous card in the set
    def previous(self):
        global noteCards
        # Checks if it is the first card, it needs to go back to the last
        if self.index == 0:
            self.index = len(noteCards) - 1
        else:
            self.index -= 1
        # Then reset the current card to be prompt first
        self.thisCard = noteCards[self.index]
        self.isPrompt = False
        self.buttonSwitch()

    # This function goes to the next card in the set
    def next(self):
        global noteCards
        # If it reaches the last card, go back to the first
        if self.index == len(noteCards) - 1:
            self.index = 0
        else:
            self.index += 1
        # Then reset the current card to be prompt first
        self.thisCard = noteCards[self.index]
        self.isPrompt = False
        # Calls the function to update the text
        self.buttonSwitch()

##=======================================================================================================================##
# Frame to edit the set already created
class ViewEdit(Frame):
    def __init__(self):
        Frame.__init__(self)
        global noteCards

        Label(self, text = "Edit Set", font = headerFont, bg = "#8595A5").grid(row = 0, columnspan = 3)
        Label(self, text = "Prompt", bg = "#BBCCDE", fg = "#4a3736").grid(row = 1, column = 1)
        Label(self, text = "Response", bg = "#BBCCDE", fg = "#4a3736").grid(row = 1, column = 2)
        noteCards = pickle.load(setScreen.cardFile)
        setScreen.cardFile.close()
        self.editedCards = []

        # Use a for loop to create entries for each card
        for card in noteCards:
            # Set the card locations to use for rows
            cardLoc = noteCards.index(card)
            # Set cardEdit = to each object
            cardEdit = card
            # Retrieve the values from the card object
            promptEdit = cardEdit.getPrompt()
            responseEdit = cardEdit.getResponse()

            # Create the entries with default values as the original values
            Label(self, text = str(cardLoc + 1) + ".", bg = "#BBCCDE").grid(row = (cardLoc + 2), column = 0)
            editP = Entry(self, bg = "#EACECA", fg = "#4a3736", highlightbackground = "#BBCCDE")
            editP.insert(END, promptEdit)
            editP.grid(row = (cardLoc + 2), column = 1)

            editR = Entry(self, bg = "#EACECA", fg = "#4a3736", highlightbackground = "#BBCCDE")
            editR.insert(END, responseEdit)
            editR.grid(row = (cardLoc + 2), column = 2)

            parts = Card()
            # Append each entry so we can retrieve the values later
            parts.setPrompt(editP)
            parts.setResponse(editR)
            self.editedCards.append(parts)

        # Buttons to do all the things
        Button(self, text = "Save Changes", command = self.saveEdits, highlightbackground = "#BBCCDE").grid()
        Button(self, text = "Cancel", command = lambda: switch(3), highlightbackground = "#BBCCDE").grid()

    # This function saves the edited version
    def saveEdits(self):
        for card in self.editedCards:
            editP = card.getPrompt()
            editP = editP.get()
            card.setPrompt(editP)

            editR = card.getResponse()
            editR = editR.get()
            card.setResponse(editR)

            cardLoc = self.editedCards.index(card)
            self.editedCards[cardLoc] = card

        editFile = open(setScreen.fileName, "wb")
        pickle.dump(self.editedCards, editFile)
        editFile.close()
        switch(3)

##=======================================================================================================================##

# Set up the function to quit, global since it is accessed multiple times
def quitProgram():
    root.destroy()

# Needed to create these variables so they can be accessed in the classes used later
mainScreen = None
newScreen = None
loadScreen = None
setScreen = None
practiceScreen = None
editScreen = None

# Function to switch screens
def switch(state):
    global mainScreen, newScreen, loadScreen, setScreen, practiceScreen, editScreen
    # Remove whatever screen isn't none, so if it's already been created
    if mainScreen != None:
        mainScreen.grid_remove()
    if newScreen != None:
        newScreen.grid_remove()
    if loadScreen != None:
        loadScreen.grid_remove()
    if setScreen != None:
        setScreen.grid_remove()
    if practiceScreen != None:
        practiceScreen.grid_remove()
    if editScreen != None:
        editScreen.grid_remove()

    # Then check what value is being sent here, and that value determines which screen to switch to, and we grid it
    if state == 0:
        mainScreen = MainMenu()
        mainScreen.grid(row = 0, column = 0)
        mainScreen["bg"] = "#BBCCDE"
    elif state == 1:
        newScreen = NewSet()
        newScreen.grid(row = 0, column = 0)
        newScreen["bg"] = "#BBCCDE"
    elif state == 2:
        loadScreen = LoadSet()
        loadScreen.grid(row = 0, column = 0)
        loadScreen["bg"] = "#BBCCDE"
    elif state == 3:
        setScreen = SetMenu()
        setScreen.grid(row = 0, column = 0)
        setScreen["bg"] = "#BBCCDE"
    elif state == 4:
        practiceScreen = Practice()
        practiceScreen.grid(row = 0, column = 0)
        practiceScreen["bg"] = "#BBCCDE"
    elif state == 5:
        editScreen = ViewEdit()
        editScreen.grid(row = 0, column = 0)
        editScreen["bg"] = "#BBCCDE"
    else:
        print("no")

# Make an instance of the Tk class
root = Tk()
# Insert the main screen
switch(0)
# Give it a title
root.title("EasyNote 3.0")
# Run the Tk main loop
root.mainloop()
