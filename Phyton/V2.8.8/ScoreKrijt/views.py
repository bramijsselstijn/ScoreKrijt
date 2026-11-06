# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 10:33:42 2024

@author: BramI
"""

import tkinter as tk
from tkinter import messagebox, Frame, Label, Button, Scrollbar, LabelFrame, Checkbutton, Entry, Spinbox, PhotoImage
from tkinter.ttk import Treeview, Notebook, Combobox
from .constants import GameTypes
from .tk_adapter import format_time, resource_path as rp
from . import widgets as w 
import os

class AppInfoScreen(Frame):
    """The input form for our widgets"""               
    def __init__(self, parent, settings=None, variables=None, app_service=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # A dict to keep track of info field widgets
        self.info = {} 
        
        
        #row 1 - Consists out playernames
        
        playerNameFrame = Frame(self) 
        playerNameFrame.columnconfigure(0, weight=1, uniform='Player')
        playerNameFrame.columnconfigure(1, weight=1, uniform='Player')
        
        self.info['Player1Name'] = w.NameLabel(playerNameFrame, name=variables['Player1'], field_color=variables['Player1BackGroundColor'], font=settings["font"], app_service=app_service)
        self.info['Player1Name'].grid(row=0, column=0, sticky='nesw')
        
        self.info['Player2Name'] = w.NameLabel(playerNameFrame, name=variables['Player2'], field_color=variables['Player2BackGroundColor'], font=settings["font"], app_service=app_service)
        self.info['Player2Name'].grid(row=0, column=1, sticky='nesw')
        
        playerNameFrame.grid(row=0, column=0, sticky=(tk.E + tk.W))
        
        
        #row 2 - Consists of match info, left and right sides are for the players, middle is the turn counter.
        
        matchInfoFrame = Frame(self)
        matchInfoFrame.columnconfigure(0, weight=2, uniform='MatchInfo')
        matchInfoFrame.columnconfigure(1, weight=0)
        matchInfoFrame.columnconfigure(2, weight=2, uniform='MatchInfo')
        
        self.info['MatchInfoPlayer1'] = w.MatchInfo(matchInfoFrame,
            tmc=variables['Player1TMC'], 
            car=variables['Player1Car'], 
            points=variables['Player1Points'], 
            field_color=variables['Player1BackGroundColor'], 
            font=settings['font'], 
            app_service=app_service
            ) 
        self.info['MatchInfoPlayer1'].grid(row=0, column=0, sticky='nesw')
        
        self.info['Turns'] = w.TurnInfo(matchInfoFrame,
            turn=variables['Turn'],
            font=settings['font'], 
            app_service=app_service
            )
        self.info['Turns'].grid(row=0, column=1, sticky='nesw')
        
        self.info['MatchInfoPlayer2'] = w.MatchInfo(matchInfoFrame,
            tmc=variables['Player2TMC'], 
            car=variables['Player2Car'], 
            points=variables['Player2Points'], 
            field_color=variables['Player2BackGroundColor'], 
            font=settings['font'], 
            app_service=app_service
            ) 
        self.info['MatchInfoPlayer2'].grid(row=0, column=2, sticky='nesw')
        
        matchInfoFrame.grid(row=1,column=0, sticky='nesw')
        
        
        #row 3 - Consists of current turn info.
        
       # currentTurnFrame = Frame(self)
        self.info['CurrentTurnInfo'] = w.CurrentTurnInfo(self,
            variables=variables,
            font=settings['font'],
            app_service=app_service
            )
        
        self.info['CurrentTurnInfo'].grid(row=2, column=0, sticky='nesw')
        
       # currentTurnFrame.grid(row=2,column=0, sticky='nesw')
        
        
    def update_new_font(self, font):
        for key in self.info:
            self.info[key].update_font(font)
            
    def update_full_player_color(self, variables):
        self.info['Player1Name'].update_colors(variables['Player1BackGroundColor'].get())
        self.info['Player2Name'].update_colors(variables['Player2BackGroundColor'].get())
        self.info['MatchInfoPlayer1'].update_colors(variables['Player1BackGroundColor'].get())
        self.info['MatchInfoPlayer2'].update_colors(variables['Player2BackGroundColor'].get())
        return
    
    def update_player_turn_color(self, variables):
        if variables["CurrentPlayerName"].get() == variables["Player1"].get():
            self.info['Player1Name'].update_colors(variables['Player1BackGroundColor'].get())
            self.info['Player2Name'].update_colors('DarkGray')
        else:
            self.info['Player1Name'].update_colors('DarkGray')
            self.info['Player2Name'].update_colors(variables['Player2BackGroundColor'].get())

class ButtonGroup(Frame):
    def __init__(self, parent, callbacks, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.callbacks = callbacks
        self.button = {}
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self._load_icons()
        self._create_buttons()

    def _load_icons(self):
        try:
            self.icons = {
                "minus": PhotoImage(file=rp('ScoreKrijt/icons/Minus.png')),
                "plus": PhotoImage(file=rp('ScoreKrijt/icons/Plus.png')),
                "note": PhotoImage(file=rp('ScoreKrijt/icons/Noteer.png')),
                "return": PhotoImage(file=rp('ScoreKrijt/icons/Return.png')),
            }
        except tk.TclError as e:
            print(f"Warning: Icon files not found. {e}")
            self.icons = {}

    def _run_callback(self, key):
        callback = self.callbacks.get(key)
        if callback:
            callback()
        else:
            print(f"⚠️ Geen callback voor '{key}'")

    def _create_buttons(self):
        config = [
            ("ReturnButton", "#cc0505", "return", "return_and_prev_turn", 0, 0),
            ("MinusButton",  "#898989", "minus",  "decrement_score",      0, 1),
            ("NoteButton",   "#3f5f29", "note",   "note_and_next_turn",   1, 0),
            ("PlusButton",   "#898989", "plus",   "increment_score",      1, 1),
        ]

        for name, bg, icon, cb_key, ry, cx in config:
            btn = Button(
                self,
                background=bg,
                borderwidth=5,
                relief='raised',
                image=self.icons.get(icon),
                command=lambda k=cb_key: self._run_callback(k)
            )
            btn.grid(row=ry, column=cx, sticky='nesw')
            self.button[name] = btn

class NewMatch(tk.Toplevel):
    def __init__(self,parent, variables, settings, logic,*args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Nieuwe wedstrijd")
        self.logic = logic
        self.settings = settings
        self.switch_icon = PhotoImage(file=rp('ScoreKrijt/icons/Switch.png'))
        
        def validate_int(P):
            if P == "":
                return True
            if P.isdigit():
                waarde = int(P)
                if waarde <= self.settings['Maximum TMC Value'].get():
                    return True
            return False
        
        def switch_players():
            p1n = new_player1Name.get()
            p1g = new_player1TMC.get()
            p2n = new_player2Name.get()
            p2g = new_player2TMC.get()
             
            # Wis oude tekst
            new_player1Name.delete(0, 'end')
            new_player1TMC.delete(0, 'end')
            new_player2Name.delete(0, 'end')
            new_player2TMC.delete(0, 'end')
            
            # Voeg gewisselde tekst in
            new_player1Name.insert(0, p2n)
            new_player2Name.insert(0, p1n)
            new_player1TMC.insert(0, p2g)
            new_player2TMC.insert(0, p1g)
    
        def update_turns_visibility(*args):
            if not self.winfo_exists():
                return
            if game_type_var.get() == 'Vaste beurten':
                self.turns_label.grid()
                self.max_turns_entry.grid()
            else:
                self.turns_label.grid_remove()
                self.max_turns_entry.grid_remove()
    
        def apply_changes(window):
            # Controleer op lege velden
            if (new_player1Name.get().strip() == "" or new_player2Name.get().strip() == "" or new_player1TMC.get() == "" or new_player2TMC.get() == ""):
                messagebox.showwarning(title="Invoerfout", message="Alle velden moeten ingevuld zijn.")
                return 
            if (int(new_player1TMC.get()) < self.settings['Minimum TMC Value'].get() or int(new_player2TMC.get()) < self.settings['Minimum TMC Value'].get()):
                messagebox.showwarning(title="Invoerfout", message="De te maken caramboles moet hoger zijn als 6.")
                return
            if game_type_var.get() == 'Vaste beurten':
                if (int(self.max_turns_entry.get()) <= self.settings['Minimum Turns Value'].get()):
                    messagebox.showwarning(
                        title="Invoerfout",
                        message="Geef een geldig aantal beurten op.\nMet minimaal 10 beurten"
                    )
                    return
            # Update de hoofdvariabelen
            variables['Player1'].set(new_player1Name.get())
            variables['Player2'].set(new_player2Name.get())
            variables['Player1TMC'].set(new_player1TMC.get())
            variables['Player2TMC'].set(new_player2TMC.get())
            
            self.settings['GameTurns'].set(self.max_turns_entry.get())
            
            self.logic.stop_timer()
            self.logic.reset_new_game()
            self.logic.cal_points()
            self.logic.cal_car_to_next_point()
            self.logic.start_timer_if_needed()
            
            parent.update_big_screen_turns()
          
            window.destroy()            
        
        vcmd_int = (self.register(validate_int), '%P')
        
        # --- UI ---
        Label(self, text='Speler 1: ').grid(row=0, column=0,sticky='e')
        new_player1Name = tk.Entry(self, width=25)
        new_player1Name.grid(row=0, column=1,padx=2,pady=2,sticky='we')
        new_player1Name.insert(0, variables['Player1'].get())
    
        Label(self, text='Te maken caramboles: ').grid(row=0, column=2,sticky='e')
        new_player1TMC = tk.Entry(self, width=5, validate='key', validatecommand=vcmd_int)
        new_player1TMC.grid(row=0, column=3,padx=2,pady=2,sticky='we')
        new_player1TMC.insert(0, variables['Player1TMC'].get())
            
        Label(self, text='Speler 2: ').grid(row=1, column=0,sticky='e')
        new_player2Name = tk.Entry(self, width=25)    
        new_player2Name.grid(row=1, column=1,padx=2,pady=2,sticky='we')
        new_player2Name.insert(0, variables['Player2'].get())
    
        Label(self, text='Te maken caramboles: ').grid(row=1, column=2,sticky='e')
        new_player2TMC = tk.Entry(self, width=5, validate='key', validatecommand=vcmd_int)
        new_player2TMC.grid(row=1, column=3,padx=2,pady=2,sticky='we')
        new_player2TMC.insert(0, variables['Player2TMC'].get())
        
        Label(self, text='Wedstrijdvorm: ').grid(row=2, column=0, sticky='e')
        game_type_var = self.settings['GameType']
        game_type_menu = tk.OptionMenu(
            self,
            game_type_var,
            *GameTypes.Games.keys()
        )
        game_type_menu.grid(row=2, column=1, sticky='w')
        
        # --- Aantal beurten ---
        self.turns_label = Label(self, text='Wedstrijd beurten: ')
        self.turns_label.grid(row=2, column=2, sticky='e')
        
        self.max_turns_entry = tk.Entry(
            self,
            width=5,
            validate='key',
            validatecommand=vcmd_int
        )
        self.max_turns_entry.insert(0, self.settings['GameTurns'].get())
        self.max_turns_entry.grid(row=2, column=3, sticky='w')
        
        
        game_type_var = self.settings['GameType']
        game_type_var.trace_add("write", update_turns_visibility)
        
        update_turns_visibility()
        new_player1Name.focus_set()
    
        Button(self, image=self.switch_icon, command=switch_players).grid(row=1, column=4, padx=3, pady=2, sticky='swe')
        Button(self, text="Start Wedstrijd", command=lambda: apply_changes(self)).grid(row=2, column=4, columnspan=5, pady=10, sticky='e')

        self.bind('<Return>', lambda e: apply_changes(self))
        #self.grab_set()
        
class EditMatchInfo(tk.Toplevel):
    def __init__(self, parent, variables, settings ,logic, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.title("Speler info aanpassen")
        self.logic = logic
        self.v = variables
        self.settings = settings

        def validate_int(P):
            return P == "" or (P.isdigit() and int(P) <= self.settings['Maximum TMC Value'].get())

        vcmd = (self.register(validate_int), '%P')

        Label(
            self,
            text="Let op: alleen namen en te maken caramboles wijzigen.\nScores blijven behouden."
        ).grid(row=0, column=0, columnspan=4, pady=5)

        # --- Player 1 ---
        Label(self, text="Speler 1").grid(row=1, column=0, sticky="w")
        p1_name = tk.Entry(self, width=25)
        p1_name.grid(row=1, column=1)
        p1_name.insert(0, self.v["Player1"].get())

        Label(self, text="TMC").grid(row=1, column=2)
        p1_tmc = tk.Entry(self, width=5, validate="key", validatecommand=vcmd)
        p1_tmc.grid(row=1, column=3)
        p1_tmc.insert(0, self.v["Player1TMC"].get())

        # --- Player 2 ---
        Label(self, text="Speler 2").grid(row=2, column=0, sticky="w")
        p2_name = tk.Entry(self, width=25)
        p2_name.grid(row=2, column=1)
        p2_name.insert(0, self.v["Player2"].get())

        Label(self, text="TMC").grid(row=2, column=2)
        p2_tmc = tk.Entry(self, width=5, validate="key", validatecommand=vcmd)
        p2_tmc.grid(row=2, column=3)
        p2_tmc.insert(0, self.v["Player2TMC"].get())

        def apply():
            if not all([
                p1_name.get().strip(),
                p2_name.get().strip(),
                p1_tmc.get(),
                p2_tmc.get()
            ]):
                messagebox.showwarning("Invoerfout", "Alle velden moeten ingevuld zijn.")
                return

            if int(p1_tmc.get()) < self.settings['Minimum TMC Value'].get() or int(p2_tmc.get()) < self.settings['Minimum TMC Value'].get():
                messagebox.showwarning("Invoerfout", "Te maken caremboles moet\nmoet minimaal 6 zijn.")
                return

            self.logic.update_player_info(
                p1_name.get(),
                p1_tmc.get(),
                p2_name.get(),
                p2_tmc.get()
            )
            self.destroy()

        Button(
            self,
            text="Update wedstrijd",
            command=apply
        ).grid(row=3, column=0, columnspan=4, pady=10, sticky="e")

        p1_name.focus_set()
        self.bind("<Return>", lambda e: apply())
        self.grab_set()
        

class BigScreenView(tk.Toplevel):

    def __init__(self, parent, variables, settings, app_service=None):
        super().__init__(parent)

        self.v = variables
        self.settings = settings
        self.app_service = app_service
        self.title("Score Krijt – Groot Scherm")

        self.bind("<F11>", self.toggle_fullscreen)
        # F12 (taakbalk) is aan het hele programma gebonden (bind_all in application.py).
        self.bind("<Escape>", lambda e: self.close())
        self.protocol("WM_DELETE_WINDOW", self.close)

        self._build_ui()
        font = self.settings['font']
        self.update_new_font(font)
        self.config(cursor="none")

    def _middle_percent(self):
        """Breedte van de middelste kolom in procenten van het scherm (10-60)."""
        try:
            percent = int(self.settings['BS Mid col. width percent'].get())
        except (tk.TclError, ValueError):
            percent = 20
        return max(10, min(60, percent))

    # -------------------------------------------------
    # UI
    # -------------------------------------------------
    def _build_ui(self):
        # De kolombreedtes volgen de verhouding van de gewichten (uniform-groep):
        # het middelste gewicht is het ingestelde percentage, de zijkanten delen de rest.
        mid_percent = self._middle_percent()
        self.columnconfigure(0, weight=100 - mid_percent, uniform="BSColumns")
        self.columnconfigure(1, weight=2 * mid_percent, uniform="BSColumns")
        self.columnconfigure(2, weight=100 - mid_percent, uniform="BSColumns")
        
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
      
        self.info = {}
                
        self.info['Player1Name'] = w.NameLabel(self, name=self.v['Player1'], field_color=self.v['Player1BackGroundColor'], font=self.settings["font"], font_size=self.settings['BS PlayerName fs'], app_service=self.app_service)
        self.info['Player1Name'].grid(row=0, column=0, sticky='nsew')
        
        self.info['TMCs'] = w.TMCFrame(self,
            tmcP1 = self.v['Player1TMC'], 
            colorP1 = self.v['Player1BackGroundColor'],
            tmcP2 = self.v['Player2TMC'], 
            colorP2 = self.v['Player2BackGroundColor'], 
            font=self.settings['font'], 
            app_service=self.app_service,
            settings=self.settings
            )
        self.info['TMCs'].grid(row=0, column=1,sticky='nsew')
        
        self.info['Player2Name'] = w.NameLabel(self, name=self.v['Player2'], field_color=self.v['Player2BackGroundColor'], font=self.settings["font"], font_size=self.settings['BS PlayerName fs'], app_service=self.app_service)
        self.info['Player2Name'].grid(row=0, column=2, sticky='nsew')
        
        self.info['Player1Stats'] = w.BSInfoFrame(self, self.v['Player1'].get(), variables=self.v,settings=self.settings, app_service=self.app_service)
        self.info['Player1Stats'].grid(row=1, column=0, sticky='nsew')
        
        self.info['TurnCount'] = w.BSTurnAndHistory(self, variables = self.v, settings=self.settings, app_service=self.app_service)
        self.info['TurnCount'].grid(row=1, column=1, sticky='nsew')        
                
        self.info['Player2Stats'] = w.BSInfoFrame(self, self.v['Player2'].get(), variables=self.v,settings=self.settings, app_service=self.app_service)
        self.info['Player2Stats'].grid(row=1, column=2, sticky='nsew')        
        
    def update_full_player_color(self, variables):
        self.info['Player1Name'].update_colors(variables['Player1BackGroundColor'].get())
        self.info['Player2Name'].update_colors(variables['Player2BackGroundColor'].get())
        self.info['TMCs'].update_colors() #colorP1=variables['Player1BackGroundColor'].get(), colorP2=variables['Player2BackGroundColor'].get()
    
    def update_player_turn_color(self, variables):
        if variables["CurrentPlayerName"].get() == variables["Player1"].get():
            self.info['Player1Name'].update_colors(variables['Player1BackGroundColor'].get())
            self.info['Player2Name'].update_colors('DarkGray')
        else:
            self.info['Player1Name'].update_colors('DarkGray')
            self.info['Player2Name'].update_colors(variables['Player2BackGroundColor'].get())

    def update_new_font(self, font):
        for key in self.info:
            self.info[key].update_font(font)
            
    def update_turns(self):
        self.info['TurnCount'].updateLastTurns()
    
    def toggle_fullscreen(self, event=None):
       # if not self.attributes("-fullscreen"):
        self.attributes("-fullscreen", not self.attributes("-fullscreen"))

    def close(self):
        master = self.master
        self.attributes("-fullscreen", False)
        self.destroy()

        # Toon het normale ScoreKrijt-venster opnieuw en geef het het toetsenbord, zodat
        # F12 (taakbalk) en de andere toetsen meteen werken. Op de SK-Box (Wayland/labwc)
        # gaat het focussen vlak na het sluiten van een volledig scherm soms mis; daarom
        # wordt het kort daarna nog een paar keer herhaald.
        def show_main():
            try:
                if master and master.winfo_exists():
                    master.deiconify()
                    master.lift()
                    master.focus_force()
            except tk.TclError:
                pass

        if master:
            show_main()
            for delay in (150, 600):
                try:
                    master.after(delay, show_main)
                except tk.TclError:
                    break

class MatchSummaryWindow(tk.Toplevel):
    def __init__(self, master, summary):
        super().__init__(master)
        self.title("Wedstrijd samenvatting")
        self.geometry("600x700")

        Label(self, text=f"Spelvorm: {summary['game_type']}").pack()
        Label(self, text=f"Beurten: {summary['turns_played']}").pack()
        Label(self, text=f"Einde: {summary['end_reason']}").pack(pady=5)

        for p in summary["players"]:
            frame = LabelFrame(self, text=p["name"])
            frame.pack(fill="x", padx=10, pady=5)

            Label(frame, text=f"Te maken caramboles: {p['tmc']}").pack(anchor="w")
            Label(frame, text=f"Caramboles: {p['car']}").pack(anchor="w")
            Label(frame, text=f"Punten: {p['points']}").pack(anchor="w")
            Label(frame, text=f"Hoogste serie: {p['highest']}").pack(anchor="w")
            Label(frame, text=f"Tijd gespeeld: {format_time(p['playtime'])}").pack(anchor="w")

        # ---- TABEL PER BEURT ----
        frame = Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = (
            "Beurt",
            "P1 Car", "P1 Totaal",
            "P2 Car", "P2 Totaal"
        )

        tree = Treeview(frame, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=100)

        scrollbar = Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for t in summary["turn_details"]:
            tree.insert(
                "",
                "end",
                values=(
                    t["turn"],
                    t["player1"]["car"], t["player1"]["total"],
                    t["player2"]["car"], t["player2"]["total"]
                )
            )
        
        Label(
            self,
            text=f"Winnaar: {summary['winner']}",
            font=("Arial", 12, "bold")
        ).pack(pady=10)

        Button(self, text="Sluiten", command=self.destroy).pack(pady=10)
    
class SendMatchEmailWindow(tk.Toplevel):
    
    
    def __init__(self, master, send_callback):
        super().__init__(master)
        self.master = master
        self.title("Wedstrijd versturen")
        #self.geometry("350x150")
        self.resizable(False, False)

        self.send_callback = send_callback

        tk.Label(self, text="E-mailadres ontvanger:").pack(pady=5)

        self.email_var = tk.StringVar()
        
        if (self.master.settings['ReceiverEmail'].get()):
            self.email_var.set(self.master.settings['ReceiverEmail'].get())
        
        tk.Entry(self, textvariable=self.email_var, width=40).pack(padx=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="Versturen", command=self._send).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Annuleren", command=self.destroy).pack(side="left", padx=5)
        
        self.status_var = tk.StringVar()
        tk.Label(self, textvariable=self.status_var, fg="blue").pack(pady=(0, 5))
                
        self.bind('<Return>', self._send)
        self.bind('<Escape>', self._close)

    def _send(self, event=None):
        email = self.email_var.get().strip()

        if "@" not in email:
            messagebox.showerror("Fout", "Voer een geldig e-mailadres in")
            return
    
        self.master.settings['ReceiverEmail'].set(email)
    
        self.status_var.set("Wedstrijd wordt verzonden...")
        self.update_idletasks()
    
        try:
            self.send_callback(email)
    
        except Exception as e:
            self.status_var.set("Verzenden mislukt")
            messagebox.showerror(
                "Verzenden mislukt",
                f"De wedstrijd kon niet worden verstuurd:\n\n{e}"
            )
            return
        """
        self.status_var.set("Wedstrijd succesvol verzonden")
        messagebox.showinfo(
            "Verzonden",
            "De wedstrijd is succesvol per e-mail verstuurd."
        )"""
        
        self.destroy()
    
    def _close(self, event=None):
        self.destroy()

class OpenMatchesWindow(tk.Toplevel):
    def __init__(self, master, open_matches, load_callback):
        super().__init__(master)
        self.title("Openstaande wedstrijden")
        self.geometry("500x300")
        self.resizable(False, False)

        self.open_matches = open_matches
        self.load_callback = load_callback

        tk.Label(self, text="Openstaande wedstrijden:").pack(pady=10)

        # Listbox met scrollbar
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True, padx=10, pady=5)
        self.listbox = tk.Listbox(frame, selectmode=tk.SINGLE)
        self.listbox.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame, command=self.listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # Voeg wedstrijden toe
        for f in open_matches:
            self.listbox.insert(tk.END, os.path.basename(f))

        # Standaard selectie: laatste wedstrijd
        self.listbox.selection_set(tk.END)

        # Knoppen
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Laden", command=self.load_selected).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Verwijderen", command=self.delete_selected).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Negeren", command=self.destroy).pack(side="left", padx=5)

    def get_selected_path(self):
        idx = self.listbox.curselection()
        if not idx:
            return None
        return self.open_matches[idx[0]]

    def load_selected(self):
        path = self.get_selected_path()
        if path:
            self.load_callback(path)
        self.destroy()

    def delete_selected(self):
        path = self.get_selected_path()
        if path:
            if messagebox.askyesno("Verwijderen", f"Weet je zeker dat je '{os.path.basename(path)}' wilt verwijderen?"):
                try:
                    os.remove(path)
                    messagebox.showinfo("Verwijderd", f"{os.path.basename(path)} is verwijderd.")
                    self.listbox.delete(self.listbox.curselection())
                    self.open_matches.remove(path)
                except Exception as e:
                    messagebox.showerror("Fout", f"Kan bestand niet verwijderen:\n{e}")
        if not self.open_matches:
            self.destroy()
            
            
class SettingsMenu(tk.Toplevel):

    def __init__(self, master, settings, settings_model):
        super().__init__(master)
        self.title("Instellingen")
        self.resizable(True, True)
        self.geometry("700x500")

        self.settings = settings
        self.model = settings_model

        self._build_ui()

        self.bind("<Escape>", lambda e: self.destroy())
        
        btns = Frame(self)
        btns.pack(fill="x", pady=10)
        
        Button(btns, text="Sluiten", command=self.destroy).pack(side="right", padx=5)
        Button(btns, text="Reset defaults", command=self._reset_defaults).pack(side="left")
        
    def _build_ui(self):
        notebook = Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
    
        self.tabs = {}
    
        for key, meta in self.model.variables.items():
            category = meta.get("category", "Algemeen")
    
            if category not in self.tabs:
                scroll = ScrollableFrame(notebook)
                notebook.add(scroll, text=category)
                self.tabs[category] = scroll.scrollable_frame
    
            self._add_setting_row(self.tabs[category], key, meta)
    
    def _add_setting_row(self, parent, key, meta):
        row = Frame(parent)
        row.pack(fill="x", pady=3, padx=5)
    
        label_text = meta.get("label", key)
        Label(row, text=label_text, width=30, anchor="w").pack(side="left")
    
        var = self.settings[key]
        widget = self._create_widget(row, key, meta, var)
    
        widget.pack(side="right", fill="x", expand=True)
        
        
    def _create_widget(self, parent, key, meta, var):
        t = meta["menutype"]
    
        if t == "Checkbutton":
            return Checkbutton(parent, variable=var)
    
        if t == "Entry":
            show = "*" if meta.get("password") else None
            return Entry(parent, textvariable=var, show=show)
    
        if t == "Spinbox":
            min_val = self._resolve_bound(meta.get("Min", 0))
            max_val = self._resolve_bound(meta.get("max", 999))
        
            spin = Spinbox(
                parent,
                from_=min_val,
                to=max_val,
                increment=meta.get("SpinboxInterval", 1),
                textvariable=var,
                width=10
            )

            # Focus-out event: corrigeer lege of foutieve waarden
            spin.bind("<FocusOut>", lambda e, v=var, m=meta: self._validate_spinbox(v, m))
            return spin
    
        if t == "Listbox":
            values = self._resolve_selection(meta)
            cb = Combobox(parent, values=values, textvariable=var, state="readonly")
            return cb

        raise ValueError(f"Onbekend menutype: {t}")
        
    def _validate_spinbox(self, var, meta):
        """Zet een lege of ongeldig ingevulde Spinbox terug naar default of geldig int."""
        try:
            value = var.get()
            if value == "":
                var.set(meta["default"])
            else:
                var.set(int(value))
        except Exception:
            var.set(meta["default"])
            
    def _resolve_bound(self, value):
        if isinstance(value, str):
            if value in self.settings:
                return self.settings[value].get()
            return 0
        return value
    
    def _resolve_selection(self, meta):
        path = meta.get("selection")
        if not path:
            return []
    
        module, attr = path.split(".")
        source = globals().get(module)
    
        if source and hasattr(source, attr):
            return getattr(source, attr)
    
        return []
       
       
    def _reset_defaults(self):
        if not messagebox.askyesno("Reset", "Alle instellingen terugzetten?"):
            return
    
        for key, meta in self.model.variables.items():
            self.settings[key].set(meta["default"])

class ScrollableFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0)
        scrollbar = Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel support (Windows)
        self.scrollable_frame.bind(
            "<Enter>", lambda e: canvas.bind_all("<MouseWheel>",
                                                 lambda ev: canvas.yview_scroll(int(-1 * (ev.delta / 120)), "units"))
        )
        self.scrollable_frame.bind(
            "<Leave>", lambda e: canvas.unbind_all("<MouseWheel>")
        )
