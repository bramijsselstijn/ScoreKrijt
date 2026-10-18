# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 23:41:10 2026

@author: BramI
"""
import sys
import os

import tkinter as tk
from .constants import FieldTypes as FT

class TkModelAdapter:

    TYPE_MAP = {
        FT.string: tk.StringVar,
        FT.long_string: tk.StringVar,
        FT.string_list: tk.StringVar,   # opgeslagen als CSV string
        FT.iso_date_string: tk.StringVar,
        FT.decimal: tk.DoubleVar,
        FT.integer: tk.IntVar,
        FT.int_list: tk.StringVar,      # opgeslagen als CSV string
        FT.boolean: tk.BooleanVar
    }

    @classmethod
    def create_variables(cls, model, master=None):
        variables = {}

        for field, rules in model.fields.items():
            field_type = rules.get("type")
            default = rules.get("default", "")

            # int_list of string_list -> default als string
            if field_type in (FT.int_list, FT.string_list) and isinstance(default, list):
                default = list_to_string(default)

            tk_var_class = cls.TYPE_MAP.get(field_type, tk.StringVar)
            variables[field] = tk_var_class(master=master, value=default)

        return variables
    
def parse_list(var_value: str) -> list[int]:
    """Converteer comma-separated string naar list[int]."""
    if not var_value:
        return []
    return [int(x) for x in var_value.split(",") if x.strip().isdigit()]

def list_to_string(lst: list[int]) -> str:
    """Converteer list[int] naar comma-separated string."""
    return ",".join(str(x) for x in lst)

def format_time(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{h:02}:{m:02}:{s:02}"

def resource_path(relative_path):
    """Geeft correct pad voor dev en exe"""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)