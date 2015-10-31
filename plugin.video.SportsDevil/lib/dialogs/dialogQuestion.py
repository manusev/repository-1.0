# -*- coding: utf-8 -*-

import xbmcgui

class DialogQuestion:

    def __init__(self):
        self.dlg = xbmcgui.Dialog()
        self.head = '[COLOR blue][B]SportsDevil [COLOR white]Pregunta[/B][/COLOR]'

    def ask(self, question):
        return self.dlg.yesno(self.head, question)
    
    def close(self):
        self.dlg.close()