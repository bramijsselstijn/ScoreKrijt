# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 10:33:42 2024

@author: BramI


Create our model class and field definitions as follows:
    
"""

import csv
import os
import json
import tkinter as tk
from .constants import FieldTypes as FT
#from .constants import ColorValeus as CV

class SettingsModel:
    """A model for saving settings"""
    variables = {
        'font':                     {'type': 'str'  , 'value': 'Bodoni'         , 'default': 'Bodoni', 'menutype':'Listbox', 'selection':'FontTypes.Fonts'},
        'BlueTooth Mode':           {'type': 'bool' , 'value': False            , 'default': False   , 'menutype':'Checkbutton'},
        'bigScreen':                {'type': 'bool' , 'value': False            , 'default': False   , 'menutype':'Checkbutton'},
        'OpenBigScreenFullScreen':  {'type': 'bool' , 'value': False            , 'default': False   , 'menutype':'Checkbutton'},
        'start color':              {'type': 'str'  , 'value': 'Yellow'         , 'default': 'Yellow', 'menutype':'Listbox', 'selection':'ColorValeus.PlayColors'},
       #'add point to big screen':  {'type': 'bool' , 'value': False            , 'default': False   , 'menutype':'Checkbutton'},
        'BS history':               {'type': 'bool' , 'value': True             , 'default': True    , 'menutype':'Checkbutton'},
        'GameType':                 {'type': 'str'  , 'value': 'Vaste beurten'  , 'default': 'Vaste beurten','menutype':'Listbox', 'selection':'GameTypes.Games'},
        'GameTurns':                {'type': 'int'  , 'value': 30               , 'default': 30      , 'menutype':'Spinbox', 'SpinboxInterval': 5, 'Min':10, 'max':150},
        'ShowGameSummery':          {'type': 'bool' , 'value': False            , 'default': False   , 'menutype':'Checkbutton' , 'category': 'Einde wedstrijd'},
        'AskToMail':                {'type': 'bool' , 'value': False            , 'default': False   , 'menutype':'Checkbutton' , 'category': 'Einde wedstrijd'},
        'StartNewMatchAutomatic':   {'type': 'bool' , 'value': False            , 'default': False   , 'menutype':'Checkbutton' , 'category': 'Einde wedstrijd'},
        'ReceiverEmail':            {'type': 'str'  , 'value': ""               , 'default': ""      , 'menutype':'Entry', 'category': 'E-Mail'},
        'CheckPreviousMatches':     {'type': 'bool' , 'value': False            , 'default': False   , 'menutype':'Checkbutton'},
        'CleanupOldMatches':        {'type': 'bool' , 'value': True             , 'default': True    , 'menutype':'Checkbutton'},
        'YearOfOldMatchesDeleted':  {'type': 'int'  , 'value': 5                , 'default': 5       , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':1, 'max':100},
        'Maximum TMC Value':        {'type': 'int'  , 'value': 999              , 'default': 999     , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':'Minimum TMC Value', 'max':999},
        'Minimum TMC Value':        {'type': 'int'  , 'value': 6                , 'default': 6       , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':0,  'max':'Maximum TMC Value'},
        'Minimum Turns Value':      {'type': 'int'  , 'value': 10               , 'default': 10      , 'menutype':'Spinbox', 'SpinboxInterval': 5, 'Min':10, 'max':150},
        'BS Mid col. width divider':{'type': 'int'  , 'value': 5                , 'default': 5       , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':2,  'max':7    , 'category': 'Big Screen'},
        'BS PlayerName fs':         {'type': 'int'  , 'value': 70               , 'default': 70      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':20, 'max':120  , 'category': 'Big Screen'},
        'BS TMCText fs':            {'type': 'int'  , 'value': 28               , 'default': 28      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':10, 'max':60   , 'category': 'Big Screen'},
        'BS TMCValue fs':           {'type': 'int'  , 'value': 42               , 'default': 42      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':15, 'max':90   , 'category': 'Big Screen'},
        'BS TurnText font size':    {'type': 'int'  , 'value': 70               , 'default': 70      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':50, 'max':90   , 'category': 'Big Screen'},
        'BS TurnValue font size':   {'type': 'int'  , 'value': 100              , 'default': 100     , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':50, 'max':150  , 'category': 'Big Screen'},
        'BS CurrentCarText fs':     {'type': 'int'  , 'value': 50               , 'default': 50      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':20, 'max':80   , 'category': 'Big Screen'},
        'BS CurrentCarValue fs':    {'type': 'int'  , 'value': 60               , 'default': 60      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':40, 'max':80   , 'category': 'Big Screen'},
        'BS Number of history rows':{'type': 'int'  , 'value': 3                , 'default': 3       , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':1,  'max':10   , 'category': 'Big Screen'},
        'BS HistoryText fs':        {'type': 'int'  , 'value': 30               , 'default': 30      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':10, 'max':50   , 'category': 'Big Screen'},
        'BS HistoryValue fs':       {'type': 'int'  , 'value': 30               , 'default': 30      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':10, 'max':50   , 'category': 'Big Screen'},
        'BS InfoCarText fs':        {'type': 'int'  , 'value': 50               , 'default': 50      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':20, 'max':80   , 'category': 'Big Screen'},
        'BS InfoCarValue fs':       {'type': 'int'  , 'value': 200              , 'default': 200     , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':120, 'max':280 , 'category': 'Big Screen'},
        'BS StatsText fs':          {'type': 'int'  , 'value': 30               , 'default': 30      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':10, 'max':50   , 'category': 'Big Screen'},
        'BS StatsValue fs':         {'type': 'int'  , 'value': 50               , 'default': 50      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':20, 'max':80   , 'category': 'Big Screen'},
        'BS PointsText fs':         {'type': 'int'  , 'value': 30               , 'default': 30      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':10, 'max':50   , 'category': 'Big Screen'},
        'BS PointsValue fs':        {'type': 'int'  , 'value': 50               , 'default': 50      , 'menutype':'Spinbox', 'SpinboxInterval': 1, 'Min':20, 'max':80   , 'category': 'Big Screen'},
        'SenderMail':               {'type': 'str'  , 'value': '' , 'default': ''      , 'menutype':'Entry' , 'category': 'E-Mail'},
        'MailAppPassword':          {'type': 'str'  , 'value': ''  , 'default': ''      , 'menutype':'Entry' , 'category': 'E-Mail'},
        
        } #Setting variables, with its default settings
    
    def __init__(self, filename='ScoreKrijtSettings.json'): 
        # determine the file path 
        self.filename=filename
        self.load()
    
    def load(self):
        """Load the settings from the settigns file """
                
        # if the file doesn't exist, return
        if not os.path.exists(self.filename):
            return
        
        with open(self.filename, 'r') as fh:
            raw_values = json.loads(fh.read())
        
        # dont implicity trust the raw values, 
        # but only get known keys
        
        for key in self.variables:
            if key in raw_values and 'value' in raw_values[key]:
                raw_value = raw_values[key]['value']
                self.variables[key]['value'] = raw_value
    
    def save(self, settings=None):
        #json_string = json.dump(self.variables)
        with open(self.filename, 'w') as fh:
            json.dump(self.variables, fh) # Dump directly to the file handle
            
    def set(self, key, value):
        # 1. Controleer of de waarde een Tkinter variabele is
        # Zo ja, haal direct de echte inhoud op (bijv. "Bodoni")
        if isinstance(value, (tk.StringVar, tk.IntVar, tk.BooleanVar)):
            value = value.get()
    
        # 2. Nu is 'value' een gewone string, int of bool.
        # Controleer of de key bestaat en of het type overeenkomt.
        if key in self.variables:
            expected_type = self.variables[key]['type']
            actual_type = type(value).__name__ # 'str', 'int', 'bool'
            
            if actual_type == expected_type:
                self.variables[key]['value'] = value
            else:
                raise ValueError(f"Verkeerd type voor {key}. Verwacht: {expected_type}, gekregen: {actual_type}")
        else:
            raise ValueError(f"Key '{key}' bestaat niet in SettingsModel.")
    
    def get(self, key):
        if key not in self.variables:
            raise KeyError(f"Key '{key}' niet gevonden.")
        
        val = self.variables[key]['value']
        
        # 1. Probeer .get() als het een object is
        if hasattr(val, 'get'):
            return val.get()
        
        # 2. Los het "PY_VAR1" probleem op:
        # Als val een string is die begint met PY_VAR, halen we de waarde uit Tkinter
        if isinstance(val, str) and val.startswith("PY_VAR"):
            try:
                return tk._default_root.getvar(val)
            except:
                return val
                
        return val



class CSVGameModel:
    """CSV file storage"""
    fields = {
        # "Date": {'type': FT.iso_date_string},
        "Player1": {'type': FT.string, 'default': "Speler 1"},
        "Player2": {'type': FT.string, 'default': "Speler 2"},
        "Player1TMC": {'type': FT.integer, 'min':6, 'default': 6},
        "Player2TMC": {'type': FT.integer, 'min':6, 'default': 6},
        "Player1Car": {'type': FT.integer, 'min':0, 'default': 0},
        "Player2Car": {'type': FT.integer, 'min':0, 'default': 0},
        "Player1Points": {'type': FT.integer, 'min':0, 'default': 0},
        "Player2Points": {'type': FT.integer, 'min':0, 'default': 0},
        "Player1HighestSerie": {'type': FT.integer, 'min':0, 'default': 0},
        "Player2HighestSerie": {'type': FT.integer, 'min':0, 'default': 0},
        "Player1CarToNextPoint": {'type': FT.integer, 'min':0, 'default': 0},
        "Player2CarToNextPoint": {'type': FT.integer, 'min':0, 'default': 0},
        "Player1PlayTime": {'type': FT.integer, 'min': 0, 'default': 0}, #in seconds
        "Player2PlayTime": {'type': FT.integer, 'min': 0, 'default': 0}, #in seconds
        "Player1BackGroundColor": {'type': FT.string, 'default':'Yellow'},
        "Player2BackGroundColor": {'type': FT.string, 'default':'White'},
        "Turn": {'type': FT.integer, 'min':0, 'default': 0},
        "CurrentPlayerName": {'type': FT.string, 'default' : "Speler 1"},
        "CurrentCar": {'type': FT.integer,'min': 0, 'default': 0},
        "CurrentCarToNextPoint": {'type': FT.integer, 'min':0, 'default': 0},
        "CurrentCarToNextPointText": {'type': FT.string, 'default': 'nog ? voor volgend punt'}
        }
    
    def __init__(self, filename):
        self.filename = filename
    
    def save_record(self, data, rownum=None):
        """Save a dict of data to the CSV file"""
        newfile = not os.path.exists(self.filename)
        
        if rownum is not None:
            records = self.get_all_records()
            records[rownum] = data
            with open(self.filename, 'w') as fh:
                csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
                csvwriter.writeheader()
                csvwriter.writerow(records)
            
        else:
            with open(self.filename, 'a') as fh:
                csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())
                if newfile:
                    csvwriter.writeheader()
                csvwriter.writerow(data)
            
    def get_all_records(self):
        if not os.path.exists(self.filename):
            return[]
        with open(self.filename, 'r') as fh:
            csvreader = csv.DictReader(fh)
            records = list(csvreader)
        csvreader = csv.DictReader(fh)
        missing_fields = (set(self.fields.keys()) - set(csvreader.fieldnames))
        if len(missing_fields) > 0:
            raise Exception(
                "File is missing fields: {}".format(', '.join(missing_fields))
            )
        else:
            records = list(csvreader)
            
        trues = ('true', 'yes', '1')
        #falses = ('false', 'no', '0')
        
        bool_fields = [key for key, meta 
                       in self.fields.item()
                       if meta['type'] == FT.boolean]
    
        for record in records:
            for key in bool_fields:
                record[key] = record[key].lower() in trues
        
        return records
    
    def get_records(self, rownum):
        return self.get_all_records()[rownum]
    
