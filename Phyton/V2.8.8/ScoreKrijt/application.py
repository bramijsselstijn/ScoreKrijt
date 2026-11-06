# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 10:33:42 2024

@author: BramI
"""

import os
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

from . import views as v
from . import models as m
from . import service
from . import menu as mainmenu
from .bluetooth_service import BluetoothService
from .bluetooth_protocol import BluetoothProtocol
from .constants import APP_VERSION


class Application(tk.Tk):
    """Aplication root window"""
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        
        self.big_screen = None
               
        self.title("Score Krijt") #Main app name
        
                
        self.app_service = service.AppService()
        self.variables = self.app_service.create_tk_variables(master=self)
        self.variables['points_and_turns'] = []
        #Settings
        self.settings_model = m.SettingsModel()
        self._remote_display_preview = False
        self.load_settings()
        
        self.appInfoScreen = v.AppInfoScreen(
            self,
            settings=self.settings,
            variables=self.variables
        )
        
        
        self.logica = service.AppLogica(self.variables, self.settings, master=self)
        
        # Injecteer view in service
        self.app_service.app_info_screen = self.appInfoScreen
        
        self.callbacks = { 
            'file->open': self.on_file_open,
            'file->quit': self.destroy,
            'file->new': self.new_match,
            'edit_match': self.edit_match,
            'file->save': self.on_save,
            'file->save_as': self.save_as,
            'change_font': self.change_font,
            'set_player_color': self.set_player_color,
            'return_and_prev_turn': self.return_and_prev_turn,
            'note_and_next_turn': self.note_and_next_turn,
            'decrement_score':  self.decrement_current_car,
            'increment_score': self.increment_current_car,
            'big_screen_toggle': self.toggle_big_screen,
            'settings_menu': self.settings_menu,
        }
        
        menu = mainmenu.MainMenu(self, self.settings, self.callbacks)
        self.config(menu=menu)
        
        self.appInfoScreen = v.AppInfoScreen(self, settings=self.settings, variables=self.variables, app_service=self.app_service)
        self.appInfoScreen.columnconfigure(0, weight = 1)
        self.appInfoScreen.grid(row=0, sticky= 'nesw')
        
        self.buttons = v.ButtonGroup(self, self.callbacks)
        self.buttons.grid(row=1, sticky= 'nesw')
        
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 0)
        self.rowconfigure(1, weight = 1)
        
        #set settings
        self.set_player_color()
        self.change_font()
        self.calcNextPoint()
        
        #Key Bindings
        
        self.bind('<Control-n>', self.new_match)
        self.bind('<Control-N>', self.new_match)
        
        self.bind('<Return>', self.note_and_next_turn)
        # bind_all: F12 werkt in elk ScoreKrijt-venster (hoofdvenster, groot scherm, dialogen),
        # ook als het toetsenbord na het sluiten van het grote scherm in een ander venster staat.
        self.bind_all('<F12>', lambda event: self.toggle_taskbar())
        self.bind('p', self.increment_current_car)
        self.bind('+', self.increment_current_car)
        self.bind('-', self.decrement_current_car)
        self.bind('m', self.decrement_current_car)
        self.bind('<BackSpace>',self.return_and_prev_turn)
        self.bind('<Control-z>',self.return_and_prev_turn)
        
        self.bluetooth = BluetoothService(message_callback=self.process_bluetooth_command)
        
        if self.settings["BlueTooth Mode"].get():
            self.settings['bigScreen'].set(True)    
            self.settings['OpenBigScreenFullScreen'].set(True)
            self.settings['ShowGameSummery'].set(False)
            self.settings['AskToMail'].set(False)
            self.settings['StartNewMatchAutomatic'].set(False)
            
            self.after(500, self.start_bluetooth_safe)
        
        #Set BigScreen
        if self.settings["bigScreen"].get():
            if self.settings["OpenBigScreenFullScreen"].get():
                # Verberg het normale ScoreKrijt-venster.
                self.withdraw()
        
            self.toggle_big_screen()
        
        # Laat de launcher weten dat het scorebord klaar is, zodat het opstartscherm sluit.
        # Dit staat vóór de controles hieronder: die kunnen een vraagvenster tonen.
        ready_file = os.environ.get("SCOREKRIJT_READY_FILE")
        if ready_file:
            self.after(2000, lambda: self._signal_ready(ready_file))

        # Check previous matches
        if self.settings['CleanupOldMatches'].get():
            self.logica.cleanup_old_matches(years=int(self.settings['YearOfOldMatchesDeleted'].get()))
        
        if self.settings['CheckPreviousMatches'].get():
            self.logica.check_open_matches()

    def _signal_ready(self, path):
        try:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write("ready")
        except OSError:
            pass
        
        
        

    def load_settings(self):
        """Load settings into our self.settings dict"""
        vartypes = {
            'bool': tk.BooleanVar,
            'str': tk.StringVar,
            'int': tk.IntVar,
            'float': tk.DoubleVar
        }
        self.settings = {}
        for key, data in self.settings_model.variables.items():
            vartype = vartypes.get(data['type'], tk.StringVar)
            self.settings[key] = vartype(value=data['value'])
            
        for var in self.settings.values():
            var.trace('w', self.save_settings)

    def save_settings(self, *args):
        
        """Save the current settings to a preferance file"""
        if self._remote_display_preview:
            return
        
        for key, variable in self.settings.items():
            meta = self.settings_model.variables[key]
            value = variable.get()

            if meta["type"] == "int":
                if value == "":
                    value = meta["default"]
                    variable.set(value)
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        value = meta["default"]
                        variable.set(value)
    
            elif meta["type"] == "float":
                if value == "":
                    value = meta["default"]
                    variable.set(value)
                else:
                    try:
                        value = float(value)
                    except ValueError:
                        value = meta["default"]
                        variable.set(value)
    
            elif meta["type"] == "bool":
                value = bool(value)
    
            self.settings_model.set(key, value)
        self.settings_model.save()
             

    def increment_current_car(self, event=None):
        if self.variables['Turn'].get() == 0:
            messagebox.showerror(
                "Wedstijd afgerond",
                "Start een nieuw wedstrijd."
            )
            return
        self.logica.increment_current_car()
        self.update_player_turn_color()
        self.logica.cal_car_to_next_point()
        self.calcPoints()
        self.send_game_state_to_phone()
        
    def decrement_current_car(self, event=None):
        if self.variables['Turn'].get() == 0:
            messagebox.showerror(
                "Wedstijd afgerond",
                "Start een nieuw wedstrijd."
            )
            return
        self.logica.decrement_current_car()
        self.logica.cal_car_to_next_point()
        self.calcPoints()
        self.send_game_state_to_phone()
        
    def save_as(self):
        path = self.logica.save_match()
        print(f"Wedstrijd opgeslagen: {path}")
    
    def on_save(self):
        path = self.logica.save_match()
        print(f"Wedstrijd opgeslagen: {path}")
        return
    
    def on_file_open(self):
        file_path = filedialog.askopenfilename(
            title="Open wedstrijd",
            filetypes=[("CSV bestanden", "*.csv")]
        )
    
        if not file_path:
            return
    
        try:
            self.logica.load_match_file(file_path)
    
            # UI herberekenen
            self.logica.cal_both_points()
            self.update_player_turn_color()
            self.logica.cal_car_to_next_point()
            self.update_big_screen_turns()
    
        except Exception as e:
            messagebox.showerror(
                "Fout bij openen",
                f"Wedstrijd kon niet worden geopend:\n{e}"
            )
    
    def edit_match(self):
        self.set_player_color()
        v.EditMatchInfo(self, self.variables, self.settings , self.logica)
    
    def calcNextPoint(self):
        self.logica.cal_car_to_next_point()
    
    def calcPoints(self):
        self.logica.cal_points()
    
    def return_and_prev_turn(self, event=None):
        if self.variables['Turn'].get() == 0:
            self.variables['Turn'].set(self.settings['GameTurns'].get() + 1)
        self.logica.return_and_prev_turn()
        self.logica.cal_points()
        self.update_player_turn_color()
        self.logica.cal_car_to_next_point()

        self.update_big_screen_turns()
        self.send_game_state_to_phone()
        
    def note_and_next_turn(self, event=None):
        if self.variables['Turn'].get() == 0:
            messagebox.showerror(
                "Wedstijd afgerond",
                "Start een nieuw wedstrijd."
            )
            return
        self.logica.add_time_to_current_player()
        endGame = self.logica.note_and_next_turn()
        self.update_big_screen_turns()
        self.logica.update_match_file()
                
        if endGame: self.end_of_match()
            
        else:
            self.logica.cal_both_points()
            self.update_player_turn_color()    
            self.logica.cal_car_to_next_point()
 
        self.send_game_state_to_phone()
        #print(self.variables['points_and_turns'])
        
    def end_of_match(self):
        self.variables['Turn'].set(int(self.variables['Turn'].get())-1) #self.settings['GameTurns'].get() instead of 0
        self.set_player_color()
        self.logica.stop_timer()
        
        summary = self.logica.get_match_summary()
        
        self.variables['Turn'].set(0) #self.settings['GameTurns'].get() instead of 0
        
        self.send_bluetooth_event("match_finished", {
            "winner": self.logica.winner,
            "reason": self.logica.match_end_reason,
        })
        
        
        if self.settings['ShowGameSummery'].get():
            summary_window = v.MatchSummaryWindow(self, summary)
            self.wait_window(summary_window)
        
        if self.settings['AskToMail'].get():
            self.logica.ask_send_match_email()
        
        if self.settings['StartNewMatchAutomatic'].get():
            self.new_match()
    
    def set_player_color(self):
        self.logica.set_player_color(self.settings)
        self.appInfoScreen.update_full_player_color(self.variables)
        if self.big_screen:
            self.big_screen.update_full_player_color(self.variables)
    
    def update_player_turn_color(self):
        self.appInfoScreen.update_player_turn_color(self.variables)
        if self.big_screen:
            self.big_screen.update_player_turn_color(self.variables)
            
    def change_font(self):
        font_name = self.settings['font'].get()  # lees de actuele waarde
        self.app_service.update_all_fonts(font_name)  # stuur direct de string door
  
    def new_match(self, event=None):
        self.set_player_color()
        v.NewMatch(self, self.variables, self.settings, self.logica)
    
    def update_big_screen_turns(self):
        if self.big_screen:
            self.big_screen.update_turns()
        
    def _keep_big_screen_fullscreen(self, delays_ms=(300, 1500, 3000, 5500, 7000)):
        """Vraag volledig scherm na het opstarten een paar keer opnieuw aan.

        Een verzoek op het moment dat het venster net is gemaakt wordt op de
        SK-Box (Wayland/labwc) soms genegeerd, zeker als het hoofdvenster
        verborgen is en het opstartscherm van de launcher er nog overheen ligt.
        """
        def apply():
            screen = self.big_screen
            if screen is None or not screen.winfo_exists():
                return
            if self.settings['OpenBigScreenFullScreen'].get():
                screen.attributes("-fullscreen", True)

        for delay in delays_ms:
            self.after(delay, apply)

    def toggle_taskbar(self):
        """F12 op de SK-Box: taakbalk tonen of verbergen (Raspberry Pi OS, labwc).

        Werkt met het grote scherm open (F12 in dat scherm) en zonder groot scherm (F12 in het
        gewone venster). Tonen: een groot scherm gaat uit volledig scherm en de taakbalk wordt
        gestart. Verbergen: de taakbalk stopt en een groot scherm vult weer het scherm.
        """
        panel = shutil.which("wf-panel-pi")
        if not panel:
            return
        screen = self.big_screen
        if screen is not None and not screen.winfo_exists():
            screen = None
        proc = getattr(self, "_panel_process", None)
        if self._panel_running():
            subprocess.run(["pkill", "-x", "wf-panel-pi"])
            # Ruim het gestopte proces op. Een afgesloten maar niet opgeruimd proces
            # (zombie) blijft voor pgrep "draaiend", waardoor de volgende F12 de taakbalk
            # niet meer zou tonen.
            if proc is not None:
                try:
                    proc.wait(timeout=2)
                except Exception:
                    pass
                self._panel_process = None
            if screen is not None and self.settings['OpenBigScreenFullScreen'].get():
                screen.attributes("-fullscreen", True)
                self._keep_big_screen_fullscreen()
        else:
            if proc is not None:
                try:
                    proc.wait(timeout=0.2)
                except Exception:
                    pass
            if screen is not None:
                screen.attributes("-fullscreen", False)
            self._panel_process = subprocess.Popen(
                [panel], start_new_session=True,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    @staticmethod
    def _panel_running():
        """True als wf-panel-pi echt draait (een zombie telt niet mee)."""
        try:
            result = subprocess.run(["ps", "-C", "wf-panel-pi", "-o", "stat="],
                                    capture_output=True, text=True)
            return any(line.strip() and not line.strip().startswith("Z")
                       for line in result.stdout.splitlines())
        except (OSError, ValueError):
            return subprocess.run(["pgrep", "-x", "wf-panel-pi"],
                                  stdout=subprocess.DEVNULL).returncode == 0

    def toggle_big_screen(self, event=None):

        # AAN â†’ openen
        if (self.big_screen is None or not self.big_screen.winfo_exists()) and self.settings['bigScreen'].get():
            self.big_screen = v.BigScreenView(parent=self, variables=self.variables, settings=self.settings, app_service=self.app_service)
                        
            if self.settings['OpenBigScreenFullScreen'].get():
                self.big_screen.update_idletasks()
                self.big_screen.attributes("-fullscreen", True)
                self._keep_big_screen_fullscreen()

        # UIT â†’ sluiten
        else:
            try:
                self.big_screen.close()
                self.big_screen = None
                self.settings['bigScreen'].set(False)
            except:
                return
            
    def settings_menu(self, event = None):
        v.SettingsMenu(self, settings = self.settings, settings_model=self.settings_model)
        return
    
    def process_bluetooth_command(self, msg):
        # Bluetooth gebruikt een achtergrondthread.
        # Tkinter moet op de hoofdthread blijven draaien.
        self.after(0, lambda: self._execute_bluetooth_command(msg))
    
    
    def _execute_bluetooth_command(self, msg):
        cmd = msg.get("cmd")
    
        try:
            if cmd == "hello":
                self.handle_bluetooth_hello(msg)

            elif cmd == "status":
                self.send_game_state_to_phone()
    
            elif cmd == "ping":
                self.send_bluetooth_event("pong")
    
            elif cmd == "prepare_match":
                self.prepare_match_from_phone(msg)

            elif cmd == "start_new_match":
                self.start_match_from_phone(msg)
    
            elif cmd == "score_plus":
                self.increment_current_car()
    
            elif cmd == "score_minus":
                self.decrement_current_car()
    
            elif cmd == "next_turn":
                self.note_and_next_turn()
    
            elif cmd == "undo":
                self.return_and_prev_turn()
            
            elif cmd == "match_finished":
                self.finish_match_from_phone(msg)
            
            elif cmd == "update_match":
                self.update_match_from_phone(msg)

            elif cmd == "get_display_settings":
                self.send_display_settings_to_phone()

            elif cmd == "preview_display_settings":
                self.apply_display_settings(msg.get("settings", {}), save=False)

            elif cmd == "save_display_settings":
                self.apply_display_settings(msg.get("settings", {}), save=True)

            elif cmd == "reset_display_settings":
                self.reset_display_settings()
    
        except Exception as e:
            self.bluetooth.send({
                "status": "error",
                "message": f"Commando '{cmd}' mislukt: {e}",
            })

    DISPLAY_SETTING_KEYS = {
        "show_history": "BS history",
        "history_rows": "BS Number of history rows",
        "middle_width_percent": "BS Mid col. width percent",
        "player_name_size": "BS PlayerName fs",
        "score_text_size": "BS InfoCarText fs",
        "score_value_size": "BS InfoCarValue fs",
        "turn_text_size": "BS TurnText font size",
        "turn_value_size": "BS TurnValue font size",
        "current_car_text_size": "BS CurrentCarText fs",
        "current_car_value_size": "BS CurrentCarValue fs",
        "tmc_text_size": "BS TMCText fs",
        "tmc_value_size": "BS TMCValue fs",
        "points_text_size": "BS PointsText fs",
        "points_value_size": "BS PointsValue fs",
        "stats_text_size": "BS StatsText fs",
        "stats_value_size": "BS StatsValue fs",
        "history_text_size": "BS HistoryText fs",
        "history_value_size": "BS HistoryValue fs",
    }

    def build_display_settings(self):
        return {wire: self.settings[key].get() for wire, key in self.DISPLAY_SETTING_KEYS.items()}

    def send_display_settings_to_phone(self, saved=False):
        self.bluetooth.send({"event": "display_settings", "status": "ok",
                             "saved": saved, "settings": self.build_display_settings()})

    def apply_display_settings(self, values, save=False):
        if not isinstance(values, dict):
            raise ValueError("Instellingen moeten een object zijn")
        self._remote_display_preview = not save
        try:
            for wire, raw_value in values.items():
                key = self.DISPLAY_SETTING_KEYS.get(wire)
                if not key:
                    continue
                meta = self.settings_model.variables[key]
                if meta["type"] == "bool":
                    value = bool(raw_value)
                else:
                    value = int(raw_value)
                    minimum, maximum = int(meta.get("Min", value)), int(meta.get("max", value))
                    if not minimum <= value <= maximum:
                        raise ValueError(f"{wire} moet tussen {minimum} en {maximum} liggen")
                self.settings[key].set(value)
        finally:
            self._remote_display_preview = False
        if save:
            self.save_settings()
        self.refresh_big_screen_layout()
        self.send_display_settings_to_phone(saved=save)

    def reset_display_settings(self):
        defaults = {wire: self.settings_model.variables[key]["default"]
                    for wire, key in self.DISPLAY_SETTING_KEYS.items()}
        self.apply_display_settings(defaults, save=True)

    def refresh_big_screen_layout(self):
        if self.big_screen is None or not self.big_screen.winfo_exists():
            return
        for child in self.big_screen.winfo_children():
            child.destroy()
        self.big_screen._build_ui()
        self.big_screen.update_full_player_color(self.variables)
            
            
    def build_game_state(self):
        turn = self.variables["Turn"].get()
    
        if turn == 0:
            match_state = "finished"
            suggested_action = "new_match_allowed"
        elif self.logica.match_file_path and not self.logica.match_finished:
            match_state = "running"
            suggested_action = "ask_continue_match"
        else:
            match_state = "not_started"
            suggested_action = "new_match_allowed"
    
        return {
            "event": "game_state",
            "protocol": "scorekrijt-bt",
            "version": "1.0",
            "match_state": match_state,
            "suggested_action": suggested_action,
            "game": {
                "player1": self.variables["Player1"].get(),
                "player2": self.variables["Player2"].get(),
                "player1_tmc": self.variables["Player1TMC"].get(),
                "player2_tmc": self.variables["Player2TMC"].get(),
                "player1_car": self.variables["Player1Car"].get(),
                "player2_car": self.variables["Player2Car"].get(),
                "player1_points": self.variables["Player1Points"].get(),
                "player2_points": self.variables["Player2Points"].get(),
                "current_player": self.variables["CurrentPlayerName"].get(),
                "active_player": 1 if self.variables["CurrentPlayerName"].get() == self.variables["Player1"].get() else 2,
                "current_car": self.variables["CurrentCar"].get(),
                "turn": self.variables["Turn"].get(),
                "game_type": self.settings["GameType"].get(),
                "game_turns": self.settings["GameTurns"].get(),
                "start_color": self.settings["start color"].get(),
                "player1_highest_serie": self.variables["Player1HighestSerie"].get(),
                "player2_highest_serie": self.variables["Player2HighestSerie"].get(),
                "player1_play_time": self.variables["Player1PlayTime"].get(),
                "player2_play_time": self.variables["Player2PlayTime"].get(),
                "turn_history": [
                    {
                        "turn": row[2],
                        "p1_score": row[0],
                        "p1_total": row[1],
                        "p2_score": row[3] if len(row) > 3 else None,
                        "p2_total": row[4] if len(row) > 4 else None,
                    }
                    for row in self.variables["points_and_turns"]
                ],
            }
        }
    
    
    def send_game_state_to_phone(self):
        if hasattr(self, "bluetooth") and self.bluetooth:
            self.bluetooth.send(self.build_game_state())

    def send_connection_match_status(self):
        """Eenmalige wedstrijdcontrole als antwoord op een nieuwe telefoonverbinding."""
        if not hasattr(self, "bluetooth") or not self.bluetooth:
            return
        state = self.build_game_state()
        state["event"] = "connection_match_status"
        state["protocol_version"] = BluetoothProtocol.PROTOCOL_VERSION
        state["app_version"] = APP_VERSION
        state["match_active"] = self.variables["Turn"].get() != 0
        self.bluetooth.send(state)

    def handle_bluetooth_hello(self, msg):
        phone_version = int(msg.get("protocol_version", 1))
        box_version = BluetoothProtocol.PROTOCOL_VERSION
        if phone_version != box_version:
            self.bluetooth.send({
                "event": "protocol_incompatible",
                "status": "error",
                "phone_protocol_version": phone_version,
                "box_protocol_version": box_version,
                "update_component": "sk_box" if phone_version > box_version else "phone_app",
                "message": "Telefoonapp en SK-Box gebruiken verschillende communicatieprotocollen",
            })
            return
        self.send_connection_match_status()
    
    def prepare_match_from_phone(self, msg):
        """Toon namen en TMC op de SK-Box terwijl de telefoon de aanvang van de wedstrijd bepaalt.

        Er wordt geen wedstrijd gestart (geen timer, geen wedstrijdbestand). Een wedstrijd die
        loopt (Turn > 0) wordt nooit aangeraakt."""
        v = self.variables
        if v["Turn"].get() > 0:
            self.send_bluetooth_event("match_prepare_ignored", {"reason": "match_running"})
            return

        player1 = str(msg["player1"]).strip()
        player2 = str(msg["player2"]).strip()
        player1_tmc = int(msg["player1_tmc"])
        player2_tmc = int(msg["player2_tmc"])
        if not player1 or not player2:
            raise ValueError("Beide spelersnamen zijn verplicht")
        if player1_tmc <= 0 or player2_tmc <= 0:
            raise ValueError("TMC moet groter dan nul zijn")

        v["Player1"].set(player1[:14])
        v["Player2"].set(player2[:14])
        v["Player1TMC"].set(player1_tmc)
        v["Player2TMC"].set(player2_tmc)

        if "game_type" in msg:
            self.settings["GameType"].set(msg["game_type"])
        if "game_turns" in msg and int(msg["game_turns"]) > 0:
            self.settings["GameTurns"].set(int(msg["game_turns"]))

        # Een leeg bord laten zien, ook als er nog een afgeronde wedstrijd stond.
        for name in ("Player1Car", "Player2Car", "CurrentCar", "Player1Points", "Player2Points",
                     "Player1HighestSerie", "Player2HighestSerie"):
            v[name].set(0)
        v["CurrentPlayerName"].set(v["Player1"].get())
        v["points_and_turns"].clear()

        # Nog niet bepaald wie begint: alle bovenste vakken wit. De kleuren en de actieve speler
        # komen pas bij het starten van de wedstrijd (start_match_from_phone).
        v["Player1BackGroundColor"].set("White")
        v["Player2BackGroundColor"].set("White")
        self.appInfoScreen.update_full_player_color(v)
        if self.big_screen:
            self.big_screen.update_full_player_color(v)
        self.logica.cal_both_points()
        self.logica.cal_car_to_next_point()
        self.update_big_screen_turns()
        self.send_bluetooth_event("match_prepared")

    def start_match_from_phone(self, msg):
        try:
            player1 = str(msg["player1"]).strip()
            player2 = str(msg["player2"]).strip()
            player1_tmc = int(msg["player1_tmc"])
            player2_tmc = int(msg["player2_tmc"])
            game_turns = int(msg.get("game_turns", 30))
    
            if not player1 or not player2:
                raise ValueError("Beide spelersnamen zijn verplicht")
    
            if player1_tmc <= 0 or player2_tmc <= 0:
                raise ValueError("TMC moet groter dan nul zijn")
    
            if game_turns <= 0:
                raise ValueError("Aantal beurten moet groter dan nul zijn")
    
            self.variables["Player1"].set(player1[:14])
            self.variables["Player2"].set(player2[:14])
            self.variables["Player1TMC"].set(player1_tmc)
            self.variables["Player2TMC"].set(player2_tmc)
    
            self.settings["GameType"].set(
                msg.get("game_type", "Vaste beurten")
            )
            self.settings["GameTurns"].set(game_turns)
            self.settings["start color"].set(
                msg.get("start_color", "Geel")
            )
    
            self.logica.stop_timer()
            self.logica.reset_new_game()
            self.set_player_color()
            self.logica.cal_points()
            self.logica.cal_car_to_next_point()
            self.logica.start_timer_if_needed()
    
            self.update_player_turn_color()
            self.update_big_screen_turns()
    
            self.send_match_started_to_phone()
    
        except Exception as e:
            if hasattr(self, "bluetooth") and self.bluetooth:
                self.bluetooth.send({
                    "status": "error",
                    "message": f"Nieuwe wedstrijd starten mislukt: {e}"
                })

    def finish_match_from_phone(self, msg):
        self._sync_match_from_phone(msg, notify_phone=False, allow_finished_turn=True)
        self.variables["Turn"].set(0)
        self.variables["CurrentCar"].set(0)
        self.logica.stop_timer()
        self.logica.match_finished = True
        self.set_player_color()
        self.logica.cal_both_points()
        self.logica.cal_car_to_next_point()
        self.update_big_screen_turns()
        self.logica.update_match_file()
        self.send_bluetooth_event("match_finished")
        self.send_game_state_to_phone()

    def send_bluetooth_event(self, event_name, extra=None):
        if not hasattr(self, "bluetooth") or not self.bluetooth:
            return
    
        data = {
            "event": event_name,
            "status": "ok"
        }
    
        if extra:
            data.update(extra)
    
        self.bluetooth.send(data)
    
    
    def send_match_started_to_phone(self):
        self.send_bluetooth_event("match_started")
        self.send_game_state_to_phone()
    
    def start_bluetooth_safe(self):
        try:
            self.bluetooth.start()
            print("Bluetooth service gestart")
        except Exception as e:
            messagebox.showerror(
                "Bluetooth fout",
                f"Bluetooth kon niet worden gestart:\n\n{e}"
            )
            self.settings["BlueTooth Mode"].set(False)
    
    def update_match_from_phone(self, msg):
        self._sync_match_from_phone(msg, notify_phone=True, allow_finished_turn=False)

    def _sync_match_from_phone(self, msg, notify_phone=True, allow_finished_turn=False):
        if "player1" in msg:
            name = str(msg["player1"]).strip()
            if not name:
                raise ValueError("Naam speler 1 mag niet leeg zijn")
            self.variables["Player1"].set(name[:14])

        if "player2" in msg:
            name = str(msg["player2"]).strip()
            if not name:
                raise ValueError("Naam speler 2 mag niet leeg zijn")
            self.variables["Player2"].set(name[:14])

        if "player1_tmc" in msg:
            value = int(msg["player1_tmc"])
            if value <= 0:
                raise ValueError("TMC speler 1 moet groter dan nul zijn")
            self.variables["Player1TMC"].set(value)

        if "player2_tmc" in msg:
            value = int(msg["player2_tmc"])
            if value <= 0:
                raise ValueError("TMC speler 2 moet groter dan nul zijn")
            self.variables["Player2TMC"].set(value)

        if "player1_car" in msg:
            self.variables["Player1Car"].set(int(msg["player1_car"]))

        if "player2_car" in msg:
            self.variables["Player2Car"].set(int(msg["player2_car"]))

        if "current_car" in msg:
            self.variables["CurrentCar"].set(int(msg["current_car"]))
        elif "current_turn_car" in msg:
            self.variables["CurrentCar"].set(int(msg["current_turn_car"]))

        if "turn" in msg:
            turn = int(msg["turn"])
            if turn < 0 or (turn == 0 and not allow_finished_turn):
                raise ValueError("Beurt moet groter dan nul zijn")
            self.variables["Turn"].set(turn)

        if "turn_history" in msg:
            history = msg["turn_history"]
            if not isinstance(history, list):
                raise ValueError("Beurtgeschiedenis moet een lijst zijn")

            restored_history = []
            for index, record in enumerate(history):
                if not isinstance(record, dict):
                    raise ValueError("Ongeldige regel in beurtgeschiedenis")

                turn_number = int(record.get("turn", index + 1))
                if turn_number != index + 1:
                    raise ValueError("Beurtnummers in geschiedenis zijn niet opeenvolgend")

                def history_value(name, default=0):
                    value = record.get(name)
                    return default if value is None else int(value)

                restored_history.append([
                    history_value("p1_score"),
                    history_value("p1_total"),
                    turn_number,
                    history_value("p2_score"),
                    history_value("p2_total"),
                ])

            self.variables["points_and_turns"].clear()
            self.variables["points_and_turns"].extend(restored_history)

        if "active_player" in msg:
            active_player = int(msg["active_player"])
            if active_player == 1:
                self.variables["CurrentPlayerName"].set(self.variables["Player1"].get())
            elif active_player == 2:
                self.variables["CurrentPlayerName"].set(self.variables["Player2"].get())
            else:
                raise ValueError("Actieve speler moet 1 of 2 zijn")
        elif "current_player" in msg:
            current_player = str(msg["current_player"]).strip()
            if current_player:
                self.variables["CurrentPlayerName"].set(current_player[:14])

        if "game_type" in msg:
            self.settings["GameType"].set(msg["game_type"])

        if "game_turns" in msg:
            self.settings["GameTurns"].set(int(msg["game_turns"]))
        elif "max_turns" in msg:
            self.settings["GameTurns"].set(int(msg["max_turns"]))

        if "start_color" in msg:
            color = msg["start_color"]

            if color not in ("Geel", "Wit"):
                raise ValueError("Startkleur moet 'Geel' of 'Wit' zijn")

            self.settings["start color"].set(color)

        self.set_player_color()
        self.logica.cal_both_points()
        self.logica.cal_car_to_next_point()
        self.update_player_turn_color()
        self.update_big_screen_turns()
        self.logica.update_match_file()

        if notify_phone:
            self.send_bluetooth_event("match_updated")
            self.send_game_state_to_phone()



