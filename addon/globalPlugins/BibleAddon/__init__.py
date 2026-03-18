# BibleAddon - Un complemento que te permite  leer la Biblia.  
# Copyright (C) 2025 Carlos  A. Pacheco Uribe <carcheco@outlook.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# Importamos los modulos relacionados con NVDA.
import globalPluginHandler #Modulo necesario cuando se hace un plugin global.
import addonHandler # Para usar la función initTranslation
import globalVars # Si falta este Modulo, entre otras cosas, no aparece el addon en Preferencias > Gestos de entrada.
import ui # Modulo que nos permite mostrar mensaje sin interfaz  grafica.
from scriptHandler import script # Modulo que contiene el decorador script Necesario para ejecutar el dialogo BibleAddon
from logHandler import log # Para enviar mensajes al registro de NVDA. 
import gui # Paquete  con modulos para interfaz gráfica de NVDA
# Importamos los modulos de python. 
import wx  # Paquete para desarrollo de interfaz grafica.
from . striprtf.striprtf import rtf_to_text # Modulo para convertir de formato RTF a texto.
import os # Modulo que contiene entre otras cosas, funciones que permite establecer una ruta de carpetas.
import json # modulo para gestionar  el archivo settings.json. 
# Importamos los modulos propios del Add-on.
from .varsBible import * # Modulo que Contiene  como constantes   los libros de La Biblia.
from .daoBible import * # Modulo para implementar el patrón DAO.

addonHandler.initTranslation() # Inicializa la traducción de este complemento ya que tiene texto apto para traducir.

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self, *args, **kwds):
        super(GlobalPlugin, self).__init__(*args, **kwds)
        self._createdMenu() # Función que crea el item Para llamar el adddon desde el menú herramientas de NVDA.
        self.dialogStarted= False # Variable que permite no volver a llamar al addon cuando este está ya abierto. 
        
    @script(description= _("Llama al complemento BibleAddon"), category= _("BibleAddon"))
    def script_Run(self, event):
        if self.dialogStarted == False:
            self.pathDb= self._getPathArchiveBbl()
            def _dialogRun():
                """Función para cargar la interfaz de usuario del BibleAddon en pantalla."""
                dialog= BibleDialog(gui.mainFrame, self)
                gui.mainFrame.prePopup() # Metodo necesario antes de mostrar cualquier dialogo o menú 
                dialog.Show()
            
            self.dialogStarted= True
            wx.CallAfter(_dialogRun) # Una manera de llamar al dialogo sin usar el modulo Thread directamente.
        else:
            ui.message(_("Ya hay una instancia de BibleAddon activa."))

    def _createdMenu(self):
        """Función privada para colocar el item del BibleAddon en el menú herramientas de NVDA"""
        self.menuTools= gui.mainFrame.sysTrayIcon.toolsMenu
        self.itemBibleAddon= self.menuTools.Append(wx.ID_ANY, _("&BibleAddon"))
        gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU,self.script_Run, self.itemBibleAddon)

    def _getPathArchiveBbl(self):
        """ Función privada para obtener  el nombre del archivo .bbl  para abrir."""
        folder= os.path.dirname(__file__)
        # Creamos una lista con los archivos .bbl que estén dentro de la carpeta BibleAddon para garantizar
        # que hay por lo menos una Biblia para cargar. 
        bblArchives= [database for database in os.listdir(folder) if database.endswith(".bbl")] 
        if bblArchives: # si hay aunque sea un archivo .bbl
            Bible= bblArchives[0] # Tomamos el primero de la lista.
            pathDb= os.path.join(folder, Bible) # Declaramos la ruta donde sqlite abrira la base de datos.
        else:
            pathDb= None 
        return pathDb
        
if globalVars.appArgs.secure:
    GlobalPlugin = globalPluginHandler.GlobalPlugin # noqa: F811 

class BibleDialog(wx.Dialog):
    """ Clase que extiende de wx.Dialog para mostrar la interfáz de usuario en pantalla."""
    def __init__(self, parent, selfGlobalPlugin):
        self.sgp= selfGlobalPlugin # Variable que me permite referenciar atributos y métodos en la instancia  de GlobalPlugin
        self.sgp.dialogStarted= True
        self.pathDb= self.sgp.pathDb
        folder= os.path.dirname(__file__) # obtenemos la ruta de la carpeta que contiene al BibleAddon.
        self.fileSettings= os.path.join(folder, "settings.json") # obtenemos ahora la ruta completa del archivo de configuración.
        self.idBook, self.chapter= self.loadSettings() # Obtenemos el libro y capítulo en donde quedó la lectura.
        # Obtenemos el testamento, nombre del libro y numeros de capitulos del libro en que quedo la lectura para colocarlo en la barra de búsqueda.
        self.idTestament, self.nameBook, self.numChapters= self.getInfoBook(self.idBook) 
        self.bible= None
        # Iniciamos la contrucción de la interfaz del usuario.
        super(BibleDialog, self).__init__(parent, wx.ID_ANY, size=(800, 600))
        # Declaramos el panel superior que será la  barra de  búsqueda
        panelTop= wx.Panel(self, -1)
        # declaramos el BoxSizer para el panel superior
        sizerTop= wx.BoxSizer(wx.HORIZONTAL)
        # declaración de los widgets del panel superior
        label1= wx.StaticText(panelTop, wx.ID_ANY, _("Elija un Testamento"))
        self.choiceTestament= wx.Choice(panelTop, wx.ID_ANY, choices=varsBible.testament)
        self.choiceTestament.SetSelection(self.idTestament)
        self.choiceTestament.Bind(wx.EVT_CHOICE, self.selectedTestament)
        label2= wx.StaticText(panelTop, wx.ID_ANY, _("Elija un Libro"))
        self.choiceBooks= wx.Choice(panelTop, wx.ID_ANY)
        # Creamos la lista   items de libros según  self.idTestament (0 antiguo  testamento, 1 nuevo testamento). 
        items= varsBible.booksOt if self.idTestament == 0 else varsBible.booksNt
        # Obtenemos el libro a mostrar a partir de self.idBook. Los libros del antiguo tienen idBook desde 1 al 39. Los del Nuevo van desde el 40 al 66.
        # Para el Antiguo el combo carga 39 libros (0 al 38) y si es el Nuevo, carga 27 libros (40 al 66).
        # Ej: Un idBook= 47 es del Nuevo  y ocupa la posición 7 en el combo (47 - 40) y un idBook= 18, del Antiguo, ocupa la posición 17 (18-1) en el combo. 
        indexSelection= self.idBook - 1 if self.idTestament == 0 else self.idBook - 40 
        self.choiceBooks.SetItems(items)
        self.choiceBooks.SetSelection(indexSelection)
        self.choiceBooks.Bind(wx.EVT_CHOICE, self.selectedBook)
        label3= wx.StaticText(panelTop, wx.ID_ANY, _("Elija un Capítulo"))
        self.comboChapters= wx.ComboBox(panelTop, wx.ID_ANY, style= wx.TE_PROCESS_ENTER)
        for i in range(self.numChapters):
            self.comboChapters.Append(str(i+1))
        self.comboChapters.Bind(wx.EVT_TEXT, self.onlyDigit)
        self.comboChapters.Bind(wx.EVT_COMBOBOX, self.selectedChapter)
        self.comboChapters.Bind(wx.EVT_TEXT_ENTER, self.inputChapter)
        self.buttonGo= wx.Button(panelTop,wx.ID_ANY, label= _("Ir"))
        self.buttonGo.Disable()
        self.buttonGo.Bind(wx.EVT_BUTTON, self.onGo)

        #Colocamos los widget creados dentro del BoxSizer
        sizerTop.Add(label1,0,wx.ALL,10)
        sizerTop.Add(self.choiceTestament,1,wx.EXPAND | wx.ALL,10)
        sizerTop.Add(label2,0,wx.ALL,10)
        sizerTop.Add(self.choiceBooks,1,wx.EXPAND | wx.ALL,10)
        sizerTop.Add(label3,0,wx.ALL,10)
        sizerTop.Add(self.comboChapters,1,wx.EXPAND | wx.ALL,10)
        sizerTop.Add(self.buttonGo,0,wx.ALL,10)

        #Aplicamos el sizer al panel superior
        panelTop.SetSizer(sizerTop)

        #Declaramos el panel central 
        panelCentral= wx.Panel(self, -1)
        # Declaramos el sizer del panel central
        sizerPc= wx.BoxSizer(wx.VERTICAL)
        # Declaramos el TextCtrl que contendra los versiculos biblicos
        self.verses= wx.TextCtrl(panelCentral, style= wx.EXPAND | wx.TE_MULTILINE | wx.TE_READONLY)
        # Lo agregamos al sizer        
        sizerPc.Add(self.verses, 1, wx.EXPAND | wx.ALL, 10) 
        # Agregamos el sizer al panel central
        panelCentral.SetSizer(sizerPc)
        
        # Declaramos el panel inferior
        panelBottom= wx.Panel(self, -1)
        # Declaramos el sizer del panel inferior
        sizerPb= wx.BoxSizer(wx.HORIZONTAL)
        # Declaramos los widget para este panel
        self.buttonNext= wx.Button(panelBottom, wx.ID_ANY, label= _("Siguiente"))
        self.buttonNext.Bind(wx.EVT_BUTTON, self.onNext)
        self.buttonBack= wx.Button(panelBottom, wx.ID_ANY, label= _("Anterior"))
        self.buttonBack.Bind(wx.EVT_BUTTON, self.onBack)
        self.buttonClose= wx.Button(panelBottom, wx.ID_CANCEL, label= _("Salir"))
        self.Bind(wx.EVT_BUTTON, self.onClose, id= wx.ID_CANCEL)
        self.Bind(wx.EVT_CLOSE, self.onClose)
        
        # agregamos los widget al sizer
        sizerPb.Add(self.buttonNext, 0, wx.ALL, 15)
        sizerPb.Add(self.buttonBack, 0, wx.ALL, 15)
        sizerPb.Add(self.buttonClose, 0, wx.ALL, 15)
        
        # Agregamos el sizer al panel inferior
        panelBottom.SetSizer(sizerPb)
        
        # Declaramos el sizer principal
        mainSizer= wx.BoxSizer(wx.VERTICAL)
        # Agregamos los paneles al sizer principal
        mainSizer.Add(panelTop, 0, wx.EXPAND | wx.ALL, 10)
        mainSizer.Add(panelCentral, 1, wx.EXPAND | wx.ALL, 10)
        mainSizer.Add(panelBottom, 0, wx.EXPAND | wx.ALL, 10)

        # Agregamos el sizer principal al dialogo
        self.SetSizer(mainSizer)
        self.verses.SetFocus() # Le damos el foco al texto Biblico
        
        # Declaramos atajos de teclado para una mejor navegación. 
        
        idShortcutTestament= wx.NewIdRef()  #ir a seleccionar un Testamento (Alt + 1)
        idShortcutBook= wx.NewIdRef()  #ir a seleccionar un Libro (Alt +2)
        idBack= wx.NewIdRef()  #Retroceder un capítulo (Alt +flecha izquierda)
        idNext= wx.NewIdRef()  #Avanzar un capítulo (Alt +flecha derecha)
        idNameBook= wx.NewIdRef()  #decir nombre del libro y capítulo actual. (Alt +i)
        accelerators= [
            wx.AcceleratorEntry(wx.ACCEL_ALT, ord('1'), idShortcutTestament),
            wx.AcceleratorEntry(wx.ACCEL_ALT, ord('2'), idShortcutBook),
            wx.AcceleratorEntry(wx.ACCEL_ALT, wx.WXK_LEFT, idBack),
            wx.AcceleratorEntry(wx.ACCEL_ALT, wx.WXK_RIGHT, idNext),
            wx.AcceleratorEntry(wx.ACCEL_ALT, ord('i'), idNameBook)
        ]
        tableAcelerators= wx.AcceleratorTable(accelerators)
        self.SetAcceleratorTable(tableAcelerators)
        self.Bind(wx.EVT_MENU, self.focusTestament, id=idShortcutTestament)
        self.Bind(wx.EVT_MENU, self.focusBook, id=idShortcutBook) 
        self.Bind(wx.EVT_MENU, self.onBack, id=idBack)
        self.Bind(wx.EVT_MENU, self.onNext, id=idNext)
        self.Bind(wx.EVT_MENU, self.sayNameBook, id=idNameBook)
        
        # Centramos el dialogo
        self.CenterOnScreen()

        # Cargamos en memoria La Biblia.
        ui.message(_("Cargando La Biblia..."))
        dao= daoBible.DaoBible(self.pathDb)
        if dao.existBible:
            info= dao.getInfoBible()
            self.nameBible= f"{info[0]}"
            title= "Biblia: " + self.nameBible + "- - " + self.nameBook + " capítulo " + str(self.chapter)
            self.SetTitle(_(title))
            self.bible= self.loadBible()
            self.verses.SetValue(self.getVerses())
            #SetPage(self.getVerses())
        else:
            wx.MessageBox(_("No existe una Biblia para abrir"), _("Atención"), wx.OK | wx.ICON_ERROR)

    # Definicion de  metodos de los widget que generan un evento.
    def selectedTestament(self, event):
        """ Método que llena el choiceBooks con los nombres de los libros según el testamento seleccionado en el choiceTestament """
        selection= self.choiceTestament.GetSelection()
        self.choiceBooks.Clear()
        self.comboChapters.Clear()
        if selection == 0:
            self.choiceBooks.SetItems(varsBible.booksOt)
        else:
            self.choiceBooks.SetItems(varsBible.booksNt)

    def selectedBook(self, event):
        """ Método que llena el ComboBox de capítulos  con el número de estos cuando se selecciona un libro en el choiceBooks """
        selection= self.choiceBooks.GetStringSelection()
        selectedBook= next(book for book in varsBible.bibleBooks if book['LIBRO'] == selection)
        self.idBook= int(selectedBook['ID'])
        self.nameBook= selectedBook['LIBRO']
        self.numChapters= int(selectedBook['NUM_CAP'])
        self.comboChapters.Clear()
        for i in range(self.numChapters):
            self.comboChapters.Append(str(i+1))

    def selectedChapter(self, event):
        """ Método que asigna  un número de     capítulo a self.chapter cuando se selecciona  un item del comboChapters """ 
        numChapter= self.comboChapters.GetValue() 
        self.chapter=  int(numChapter)
        self.buttonGo.Enable()

    def inputChapter(self, event):
        """ Metodo que muestra  el texto biblico seleccionado cuando se presiona enter  en el ComboBox de capítulo """
        chapter= self.comboChapters.GetValue() 
        if int(chapter) > self.numChapters or chapter == " " or chapter == "0":
            wx.MessageBox(_("Este libro va del capítulo 1 al ") + str(self.numChapters) +_(". Ingrese un capítulo valido"), _("Atención"), wx.OK | wx.ICON_WARNING)
            self.comboChapters.SetValue('1')
            self.comboChapters.SetFocus()
        else:
            self.chapter= int(chapter)
            text= self.getVerses()
            self.verses.SetValue(text)
            self.buttonGo.Disable()
            self.verses.SetFocus()

    def onGo(self, event):
        """ Metodo que muestra el texto biblico seleccionado al presionar el botón Ir """
        text= self.getVerses()
        self.verses.SetValue(text)
        self.buttonGo.Disable()
        self.verses.SetFocus()

    def onBack(self, event):
        """ Metodo que retrocede un capítulo para el libro seleccionado cuando se presiona el botón Anterior" """
        if self.chapter > 1:
            self.chapter -= 1
            text= self.getVerses()
            self.verses.SetValue(text)
            self.verses.SetFocus()

    def onNext(self, event):
        """ Metodo que adelanta  un capítulo para el libro seleccionado cuando se presiona el botón Siguiente " """
        if self.chapter < self.numChapters:
            self.chapter += 1
            text= self.getVerses()
            self.verses.SetValue(text)
            self.verses.SetFocus()

    def onlyDigit(self, event):
        """ Metodo que valida que el valor escrito en el comboChapters sea un digito """
        text= self.comboChapters.GetValue()
        if text:
            if not text.isdigit(): 
                wx.MessageBox(_("Ingrese un valor de capitulo valido"), _("Error"), wx.OK | wx.ICON_ERROR )
                self.comboChapters.SetValue("")
            event.Skip()

    def onClose(self, event):
        """ Metodo que cierra el addon """
        self.saveSettings(self.idBook, self.chapter)
        self.sgp.dialogStarted= False
        self.Close(True)
        self.Destroy()
        gui.mainFrame.postPopup()

    # Definicion de otros metodos
    def focusTestament(self, event):
        """ Metodo que le da el foco al choiceTestament al pulsar la tecla alt mas 1 """
        self.choiceTestament.SetFocus()

    def focusBook(self, event):
        """ Metodo que le da el foco al choiceBook al pulsar la tecla alt mas 2 """
        self.choiceBooks        .SetFocus()

    def sayNameBook(self, event):
        """ Metodo que verbaliza el nombre y capítulo del libro actual. """
        msg= self.nameBook + " " +_("Capítulo ") + str(self.chapter)
        ui.message(msg)

    def getVerses(self):
        """ 
        Método que busca en self.bible los versículos según self.idBook y self.chapter y a medida que obtiene los versículos, 
        elimina el formato RTF retornando el texto en formato txt.
        """
        title= "Biblia: " + self.nameBible + " - " + self.nameBook + " capítulo " + str(self.chapter)
        self.SetTitle(_(title))
        text= _(self.nameBook) + _(" - Capítulo ") + str(self.chapter) +"."
        for bible in self.bible:
            if bible[0] == self.idBook and bible[1] == self.chapter: # Si estoy en el libro y capítulo buscado... 
                if bible[2] == 1 and bible[3].find('\par') != -1: # Si hay un título en el primer versículo, se elimina el valor 1 ...
                    verse_aux= rtf_to_text(bible[3])  # y colocamos solo el título, damos un salto de línea  
                    idx= verse_aux.find('\n',3)  # para luego escribir el valor 1 con el texto del versículo.
                    verse= verse_aux[:idx+1] + '1.' + verse_aux[idx+1:]
                else:
                    verse= "\n" + str(bible[2]) + ". " + rtf_to_text(bible[3]) # Se elimina el formato RTF  
                text+= verse
        return text

    def loadBible(self):
        """      Metodo que retorna una tupla con todos los versículos de La Biblia. """
        dao= daoBible.DaoBible(self.pathDb)
        if dao.conected is True:
            bible= dao.getBible()
            return bible
        else:
            wx.MessageBox(_("Error al conectar a la base de datos de La Biblia"), _("Error"), wx.OK | wx.ICON_ERROR)
            return None

    def loadSettings(self):
        """
        Metodo que recupera  del   archivo settings.json el id del libro y el capítulo, para así
        poder retomar la lectura donde quedo antes de cerrar el plugin.
        """
        defaultBook= 1
        defaultChapter= 1
        if os.path.exists(self.fileSettings):
            try:
                with open(self.fileSettings, "r", encoding="utf-8") as f:
                    settings= json.load(f)
                    idBook= settings.get("idBook", 1)
                    chapter= settings.get("chapter", 1)
                    return idBook, chapter
            except(IOError, json.JSONDecodeError) as e:
                log.error(_(f"error al cargar configuración guardada. {e}"))
                os.remove(self.fileSettings)
                self.saveSettings(defaultBook, defaultChapter)
                return defaultBook, defaultChapter
        else:
            self.saveSettings(defaultBook, defaultChapter)
            return defaultBook, defaultChapter

    def saveSettings(self, idBook, chapter):
        """
        Metodo que pasa por parámetros el id del libro y un número de capítulo para 
que sean guardados  en el archivo setting.json.
""" 
        settings= {
            "idBook": idBook,
            "chapter": chapter
        }
        try:
            with open(self.fileSettings, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)
                log.info(_("Archivo guardado."))
        except IOError as e:
            log.error(_(f"Error al guardar archivo. {e}"))

    def getInfoBook(self, idBook):
        """
        Metodo que pasa por parámetro el id de un libro y retorna el id del testamento para saber si es del antiguo o del nuevo, 
        el nombre del libro y el número de capítulos que contiene.
        """
        selection= None
        for book in varsBible.bibleBooks:
            if book['ID'] == str(idBook):
                selection= book
                break
        idTestament= 0 if selection['PACTO'] == "AT" else 1  
        return idTestament, selection['LIBRO'], int(selection['NUM_CAP'])
