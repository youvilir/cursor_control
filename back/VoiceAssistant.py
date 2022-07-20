import pyautogui 
import speech_recognition
import autopy
from PyQt5 import QtCore 

class VoiceControl():
    start = True

    def __init__(self, LeftCkick=None, RightClick=None,
                 DoubleLeftClick=None, ScrollUp=None,
                 ScrollDown=None, ScrollLeft=None,
                 ScrollRight=None, DragAndDrop=None):

        self.LeftCkick=LeftCkick
        self.RightClick=RightClick
        self.DoubleLeftClick=DoubleLeftClick
        self.ScrollUp=ScrollUp
        self.ScrollDown=ScrollDown
        self.ScrollLeft=ScrollLeft
        self.ScrollRight=ScrollRight
        self.DragAndDrop=DragAndDrop

        self.sr = speech_recognition.Recognizer()
        self.Microphone = speech_recognition.Microphone()

        self.sr.pause_threshold = 0.5

        self.listOfCommands = [self.LeftCkick, self.RightClick, 
                        self.DoubleLeftClick, self.ScrollUp, 
                        self.ScrollDown, self.ScrollLeft, 
                        self.ScrollRight, self.DragAndDrop]

    def select_microphone(self, mic):
        mics = self.Microphone.list_microphone_names()
        try:
            index_mic = mics.index(mic)
            self.Microphone = speech_recognition.Microphone(device_index=index_mic)
        except:
            pass

    def show_microphone(self):
        try:
            mics = self.Microphone.list_microphone_names()
            current_mic = mics[self.Microphone.device_index]
            return current_mic
        except:
            pass


    def DoLeftCkick(self):
        autopy.mouse.click()
        
    def DoRightClick(self):
        autopy.mouse.toggle(autopy.mouse.Button.RIGHT, False)
        
    def DoDoubleLeftClick(self):
        autopy.mouse.click()
        autopy.mouse.click()
        
    def DoScrollUp(self):
        pyautogui.scroll(200)

    def DoScrollDown(self):
        pyautogui.scroll(-200)

    def DoScrollLeft(self):
        pyautogui.hscroll(-200)

    def DoScrollRight(self):
        pyautogui.hscroll(200)

    def DoDragAndDrop(self):
        autopy.mouse.toggle(autopy.mouse.Button.LEFT, True)
  
    def MouseAction(self, argument):
        switcher = {
            self.LeftCkick: self.DoLeftCkick,
            self.RightClick: self.DoRightClick,
            self.DoubleLeftClick: self.DoDoubleLeftClick,
            self.ScrollUp: self.DoScrollUp,
            self.ScrollDown: self.DoScrollDown,
            self.ScrollLeft: self.DoScrollLeft,
            self.ScrollRight: self.DoScrollRight,
            self.DragAndDrop: self.DoDragAndDrop
        }

        func = switcher.get(argument)

        func()

    def Start(self):

        with self.Microphone as mic:

            while True:
                if not self.start:
                    break

                self.sr.adjust_for_ambient_noise(source=mic, duration=0.5)
                audio=self.sr.listen(mic)

                try:
                    command = self.sr.recognize_google(audio_data=audio, language='ru-RU').lower()

                    for com in self.listOfCommands:
                        if com in command:
                            self.MouseAction(com)

                except:
                    pass

