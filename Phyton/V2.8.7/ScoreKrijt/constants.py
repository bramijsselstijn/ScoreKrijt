# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 10:33:42 2024

@author: BramI
"""

APP_VERSION = "2.8.7.1"

class FieldTypes:
    string = 1
    string_list = 2
    iso_date_string = 3
    long_string = 4
    decimal = 5
    integer = 6
    boolean = 7
    int_list = 8
    
class FontTypes:
    Fonts = {
        "Bodoni": "Bodoni MT",
        "Clear": "Helvetica",
        "Type Writer": "Times New Roman",
#        "Clean": "Consolas",
#        "Clean 2": "Courier New"
    }
   
class ColorValeus:
    Colors = { 
        'White' : '#fff',
        'Gray' : '#afabab',
        'DarkGray' : '#7f7f7f',
        'Black' : '#000',
        'Yellow' : '#ffc000',
        'Green' : '#548235',
        'Wit':'#fff',
        'Geel':'#ffc000'
    }
    PlayColors = {
        'Wit' : 'ColorWhite',
        'Geel' : 'ColorYellow'
        }

class GameTypes:
    Games = {
        'Vaste beurten' : 'fixed turns',
        'Uit is uit' : 'Out is out',
        #'Tien over rood' : 'Ten along red',
        #'Honderden' : 'Hundreds',
        }