# coding: utf-8
# BibleAddon - Un complemento que te permite  leer la Biblia.  
# Copyright (C) 2025 Carlos  A. Pacheco Uribe <carcheco@outlook.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

import sqlite3
from logHandler import log

class DaoBible():
    """ Clase para implementar el patrón Data Access Object (DAO) """ 
    def __init__(self, path):
        self.path= path 
        self.conex= None
        self.conected= False
        self.existBible= True

        if self.path is None:
            self.existBible= False
        else:
            try:
                self.conex= sqlite3.connect(self.path)
                self.conected= True
                log.info(_("Conectado a La Biblia."))
            except sqlite3.Error as e:
                log.error(_(f"Error al conectar a la base de datos {e}"))
                self.conected= False

    def getInfoBible(self):
        """ Metodo para obtener el nombre y la abreviatura de La Biblia cargada """ 
    
        try:
            cursor= self.conex.cursor()
            sql= "SELECT Description, Abbreviation FROM Details;"
            cursor.execute(sql)
            info= cursor.fetchall()
            return info
        except sqlite3.Error as e:
            log.error(_(f"Error al consultar info de La Biblia. {e}"))
        finally:
            if self.conex:
                self.conex.close()

    def getBible(self):
        """ Metodo que obtiene todos los versículos de La Biblia """
        if self.conex is None:
            return None
        try:
            cursor= self.conex.cursor()
            sql= "SELECT Book, Chapter, Verse, Scripture FROM Bible ORDER BY Book, Chapter, Verse;" 
            cursor.execute(sql)
            verses= cursor.fetchall()
            return verses
        except sqlite3.Error as e:
            log.error(_(f"Error al consultar La Biblia. {e}"))
        finally:
            if self.conex:
                self.conex.close()

    def getVersesBook(self, idBook):
        """
        Metodo que retorna todos los versículos de un libro de La Biblia 
        a partir del id de un libro el cual es pasado como parametro. 
        """
        if self.conex is None:
            return None
        try:
            cursor= self.conex.cursor()
            sql= "SELECT Chapter, Verse, Scripture FROM Bible WHERE Book= ? ORDER BY Book, Chapter, Verse;"
            cursor.execute(sql, (idBook))
            verses= cursor.fetchall()
            return verses
        except sqlite3.Error as e:
            log.error(_(f"Error al consultar La Biblia. {e}."))
        finally:
            if self.conex:
                self.conex.close()
