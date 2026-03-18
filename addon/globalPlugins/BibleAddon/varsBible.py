# coding: utf-8
# BibleAddon - Un complemento que te permite  leer la Biblia.  
# Copyright (C) 2025 Carlos  A. Pacheco Uribe <carcheco@outlook.com>
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

""" Modulo  que contiene estructuras de datos utilizadas por el addon. """

# Declaramos una lista para el pacto 
testament= ("Antiguo Testamento", "Nuevo Testamento")

# Declaramos una lista de diccionarios, un diccionario contiene los datos para cada libro
bibleBooks= (
    {"ID": "1", "LIBRO": _("Génesis"), "NUM_CAP": "50", "PACTO": "AT"},
    {"ID": "2", "LIBRO": _("Éxodo"), "NUM_CAP": "40", "PACTO": "AT"},
    {"ID": "3", "LIBRO": _("Levítico"), "NUM_CAP": "27", "PACTO": "AT"},
    {"ID": "4", "LIBRO": _("Números"), "NUM_CAP": "36", "PACTO": "AT"},
    {"ID": "5", "LIBRO": _("Deuteronomio"), "NUM_CAP": "34", "PACTO": "AT"},
    {"ID": "6", "LIBRO": _("Josué"), "NUM_CAP": "24", "PACTO": "AT"},
    {"ID": "7", "LIBRO": _("Jueces"), "NUM_CAP": "21", "PACTO": "AT"},
    {"ID": "8", "LIBRO": _("Rut"), "NUM_CAP": "4", "PACTO": "AT"},
    {"ID": "9", "LIBRO": _("1 Samuel"), "NUM_CAP": "31", "PACTO": "AT"},
    {"ID": "10", "LIBRO": _("2 Samuel"), "NUM_CAP": "24", "PACTO": "AT"},
    {"ID": "11", "LIBRO": _("1 Reyes"), "NUM_CAP": "22", "PACTO": "AT"},
    {"ID": "12", "LIBRO": _("2 Reyes"), "NUM_CAP": "25", "PACTO": "AT"},
    {"ID": "13", "LIBRO": _("1 Crónicas"), "NUM_CAP": "29", "PACTO": "AT"},
    {"ID": "14", "LIBRO": _("2 Crónicas"), "NUM_CAP": "36", "PACTO": "AT"},
    {"ID": "15", "LIBRO": _("Esdras"), "NUM_CAP": "10", "PACTO": "AT"},
    {"ID": "16", "LIBRO": _("Nehemías"), "NUM_CAP": "13", "PACTO": "AT"},
    {"ID": "17", "LIBRO": _("Ester"), "NUM_CAP": "10", "PACTO": "AT"},
    {"ID": "18", "LIBRO": _("Job"), "NUM_CAP": "42", "PACTO": "AT"},
    {"ID": "19", "LIBRO": _("Salmos"), "NUM_CAP": "150", "PACTO": "AT"},
    {"ID": "20", "LIBRO": _("Proverbios"), "NUM_CAP": "31", "PACTO": "AT"},
    {"ID": "21", "LIBRO": _("Eclesiastés"), "NUM_CAP": "12", "PACTO": "AT"},
    {"ID": "22", "LIBRO": _("Cantares"), "NUM_CAP": "8", "PACTO": "AT"},
    {"ID": "23", "LIBRO": _("Isaías"), "NUM_CAP": "66", "PACTO": "AT"},
    {"ID": "24", "LIBRO": _("Jeremías"), "NUM_CAP": "52", "PACTO": "AT"},
    {"ID": "25", "LIBRO": _("Lamentaciones"), "NUM_CAP": "5", "PACTO": "AT"},
    {"ID": "26", "LIBRO": _("Ezequiel"), "NUM_CAP": "48", "PACTO": "AT"},
    {"ID": "27", "LIBRO": _("Daniel"), "NUM_CAP": "12", "PACTO": "AT"},
    {"ID": "28", "LIBRO": _("Oseas"), "NUM_CAP": "14", "PACTO": "AT"},
    {"ID": "29", "LIBRO": _("Joel"), "NUM_CAP": "3", "PACTO": "AT"},
    {"ID": "30", "LIBRO": _("Amós"), "NUM_CAP": "9", "PACTO": "AT"},
    {"ID": "31", "LIBRO": _("Abdías"), "NUM_CAP": "1", "PACTO": "AT"},
    {"ID": "32", "LIBRO": _("Jonás"), "NUM_CAP": "4", "PACTO": "AT"},
    {"ID": "33", "LIBRO": _("Miqueas"), "NUM_CAP": "7", "PACTO": "AT"},
    {"ID": "34", "LIBRO": _("Nahúm"), "NUM_CAP": "3", "PACTO": "AT"},
    {"ID": "35", "LIBRO": _("Habacuc"), "NUM_CAP": "3", "PACTO": "AT"},
    {"ID": "36", "LIBRO": _("Sofonías"), "NUM_CAP": "3", "PACTO": "AT"},
    {"ID": "37", "LIBRO": _("Hageo"), "NUM_CAP": "2", "PACTO": "AT"},
    {"ID": "38", "LIBRO": _("Zacarías"), "NUM_CAP": "14", "PACTO": "AT"},
    {"ID": "39", "LIBRO": _("Malaquías"), "NUM_CAP": "4", "PACTO": "AT"},
    {"ID": "40", "LIBRO": _("Mateo"), "NUM_CAP": "28", "PACTO": "NT"},
    {"ID": "41", "LIBRO": _("Marcos"), "NUM_CAP": "16", "PACTO": "NT"},
    {"ID": "42", "LIBRO": _("Lucas"), "NUM_CAP": "24", "PACTO": "NT"},
    {"ID": "43", "LIBRO": _("Juan"), "NUM_CAP": "21", "PACTO": "NT"},
    {"ID": "44", "LIBRO": _("Hechos"), "NUM_CAP": "28", "PACTO": "NT"},
    {"ID": "45", "LIBRO": _("Romanos"), "NUM_CAP": "16", "PACTO": "NT"},
    {"ID": "46", "LIBRO": _("1 Corintios"), "NUM_CAP": "16", "PACTO": "NT"},
    {"ID": "47", "LIBRO": _("2 Corintios"), "NUM_CAP": "13", "PACTO": "NT"},
    {"ID": "48", "LIBRO": _("Gálatas"), "NUM_CAP": "6", "PACTO": "NT"},
    {"ID": "49", "LIBRO": _("Efesios"), "NUM_CAP": "6", "PACTO": "NT"},
    {"ID": "50", "LIBRO": _("Filipenses"), "NUM_CAP": "4", "PACTO": "NT"},
    {"ID": "51", "LIBRO": _("Colosenses"), "NUM_CAP": "4", "PACTO": "NT"},
    {"ID": "52", "LIBRO": _("1 Tesalonicenses"), "NUM_CAP": "5", "PACTO": "NT"},
    {"ID": "53", "LIBRO": _("2 Tesalonicenses"), "NUM_CAP": "3", "PACTO": "NT"},
    {"ID": "54", "LIBRO": _("1 Timoteo"), "NUM_CAP": "6", "PACTO": "NT"},
    {"ID": "55", "LIBRO": _("2 Timoteo"), "NUM_CAP": "4", "PACTO": "NT"},
    {"ID": "56", "LIBRO": _("Tito"), "NUM_CAP": "3", "PACTO": "NT"},
    {"ID": "57", "LIBRO": _("Filemón"), "NUM_CAP": "1", "PACTO": "NT"},
    {"ID": "58", "LIBRO": _("Hebreos"), "NUM_CAP": "13", "PACTO": "NT"},
    {"ID": "59", "LIBRO": _("Santiago"), "NUM_CAP": "5", "PACTO": "NT"},
    {"ID": "60", "LIBRO": _("1 Pedro"), "NUM_CAP": "5", "PACTO": "NT"},
    {"ID": "61", "LIBRO": _("2 Pedro"), "NUM_CAP": "3", "PACTO": "NT"},
    {"ID": "62", "LIBRO": _("1 Juan"), "NUM_CAP": "5", "PACTO": "NT"},
    {"ID": "63", "LIBRO": _("2 Juan"), "NUM_CAP": "1", "PACTO": "NT"},
    {"ID": "64", "LIBRO": _("3 Juan"), "NUM_CAP": "1", "PACTO": "NT"},
    {"ID": "65", "LIBRO": _("Judas"), "NUM_CAP": "1", "PACTO": "NT"},
    {"ID": "66", "LIBRO": _("Apocalipsis"), "NUM_CAP": "22", "PACTO": "NT"}
)

# A partir de la lista de libros de la Biblia declaramos una lista para los libros del antiguo testamento y otra lista para los libros del nuevo testamento.
booksOt= []
for i in  range(0, 39): 
    book= bibleBooks[i]
    booksOt.append(book['LIBRO']) 

booksNt= []
for i in  range(39,66): 
    book= bibleBooks[i]
    booksNt.append(book['LIBRO']) 
