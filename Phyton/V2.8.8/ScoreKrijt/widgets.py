# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 10:33:42 2024

@author: BramI
"""

import math
import tkinter as tk
import tkinter.font as tkfont

from .constants import FontTypes
from .constants import ColorValeus as CV


#Top Row of main App and Big Screen

class NameLabel(tk.Frame):
   """Een label widget waarvan de tekst meeschaalt met de breedte."""
   def __init__(self, parent, name=None, field_color=None, font=None, app_service=None, font_size=None, **kwargs):
       super().__init__(parent, **kwargs)
       
       self.columnconfigure(0, weight=1)
       self.rowconfigure(0, weight=1)
       self.pack_propagate(False)
       
       # -----------------------------
       # Font state
       # -----------------------------
       self.current_font_key = "Clear"
       self.fixed_font_size = font_size
       if font:
           self.current_font_key = font.get() if hasattr(font, "get") else font

       actual_font = self._get_actual_font(self.current_font_key)

       # Eén font object dat we dynamisch aanpassen
       self.scaled_font = tkfont.Font(
           family=actual_font,
           size=12,
           weight="bold",
       )

       # -----------------------------
       # Label
       # -----------------------------
       self.label_widget = tk.Label(
           self,
           textvariable=name,
           font=self.scaled_font,
           borderwidth=5,
           relief="sunken",
           padx=5,
       )
       self.label_widget.grid(row=0, column=0, sticky="nsew")

       # Init styling
       if field_color:
           self.update_colors(field_color)

       # Resize binding
       self.bind("<Configure>", self._rescale_text)

       # Eerste schaal
       self.after(10, self._trigger_rescale)

       # Registreer bij AppService
       if app_service:
           app_service.register_widget_for_font(self)
          
    

   # -------------------------------------------------
   # Helpers
   # -------------------------------------------------

   def _get_actual_font(self, font_key):
       return FontTypes.Fonts.get(font_key, "Arial")

   def _trigger_rescale(self):
       """Forceer een herschaling bij init."""
       width = self.winfo_width()
       if width > 1:
           self._apply_font_size(width)

   def _apply_font_size(self, width):
       """Pas alleen de fontgrootte aan."""
       #new_size = max(8, int(width / 8))
       #self.scaled_font.configure(size=new_size)
       text = self.label_widget.cget("text")

       if not text:
            try:
                text = self.label_widget.getvar(
                    self.label_widget.cget("textvariable")
                )
            except:
                text = ""
    
       size = self.fixed_font_size.get() if hasattr(self.fixed_font_size, "get") else (self.fixed_font_size or max(8, int(width / 8)))
    
       self.scaled_font.configure(size=size)
    
       while size > 8 and self.scaled_font.measure(text) > width - 20:
            size -= 1
            self.scaled_font.configure(size=size)


   # -------------------------------------------------
   # Events
   # -------------------------------------------------

   def _rescale_text(self, event):
       self._apply_font_size(event.width)

   # -------------------------------------------------
   # Public API
   # -------------------------------------------------

   def update_colors(self, field_color):
       if not field_color:
           return

       color_key = (
           field_color.get("default")
           if isinstance(field_color, dict)
           else field_color.get() if hasattr(field_color, "get")
           else field_color
       )

       actual_color = CV.Colors.get(color_key)
       if actual_color:
           self.label_widget.configure(background=actual_color)

   def update_font(self, font):
       """Update alleen de fontfamilie en herschaal opnieuw."""
       if not font:
           return

       font_key = font.get() if hasattr(font, "get") else font
       self.current_font_key = font_key

       actual_font = self._get_actual_font(font_key)
       self.scaled_font.configure(family=actual_font)

       # Forceer herschaling met huidige breedte
       self._trigger_rescale()



#To show turn number in the BS Screen
class BSTurnAndHistory(tk.Frame):
    """Toont de huidige beurt op het scherm"""

    def __init__(self, parent, variables, settings=None, app_service=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.settings = settings
        self.v = variables
        # Huidige font-familie
        font = self.settings['font']
        self.current_font_family = "Arial"
        if font:
            self.current_font_family = font.get() if hasattr(font, 'get') else font

        # Fonts
        actual_font = FontTypes.Fonts.get(self.current_font_family, "Arial")
        self.fonts = {
            "TurnText": tkfont.Font(family=actual_font, size=self.settings['BS TurnText font size'].get(), weight="bold"),
            "TurnInt": tkfont.Font(family=actual_font, size=self.settings['BS TurnValue font size'].get(), weight="bold"),
            "CurrentCarText": tkfont.Font(family=actual_font, size=self.settings['BS CurrentCarText fs'].get(), weight="bold"),
            "CurrentCarVar": tkfont.Font(family=actual_font, size=self.settings['BS CurrentCarValue fs'].get(), weight="bold")            
        }

        # Labels
        self.info = {}
        self.info['TurnText'] = tk.Label(self, text="Beurt", font=self.fonts["TurnText"])
        self.info['TurnText'].grid(row=0, column=0, sticky='new')
        
        turn = self.v['Turn']
        
        self.info['TurnInt'] = tk.Label(self, textvariable=turn, font=self.fonts["TurnInt"])
        self.info['TurnInt'].grid(row=1, column=0, sticky='nesw')

        self.info['CurrentCarText'] = tk.Label(self, text="Caramboles", font=self.fonts["CurrentCarText"])
        self.info['CurrentCarText'].grid(row=2, column=0, sticky='nesw')
        
        currentCar = self.v['CurrentCar']
        
        self.info['CurrentCarVar'] = tk.Label(self, textvariable=currentCar, font=self.fonts["CurrentCarVar"])
        self.info['CurrentCarVar'].grid(row=3, column=0, sticky='nesw')
        
        if self.settings['BS history'].get():
            self.info['last_turns'] = BSLastTurnsFrame(
                self,
                variables=self.v,
                settings=self.settings,
                app_service=app_service,
                font=font
            )
            self.info['last_turns'].grid(row=4, column=0, sticky="sew", pady=20)



        # Registreer bij AppService
        if app_service:
            app_service.register_widget_for_font(self)

    def update_font(self, font):
        """Update alleen de font-family, behoud grootte en stijl"""
        self.current_font_family = font if isinstance(font, str) else font.get()
        for f in self.fonts.values():
            f.configure(family=FontTypes.Fonts.get(self.current_font_family, "Arial"))
    
    def updateLastTurns(self):
        try: 
            self.info['last_turns'].update_turns()
        except:
            return
        
class BSLastTurnsFrame(tk.Frame):
    """Toont de laatste x beurten voor beide spelers."""

    def __init__(self, parent, variables, settings, font=None, app_service=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.variables = variables
        self.settings = settings
        self.app_service = app_service
        self.show_turns = self.settings['BS Number of history rows'].get()

        # Font instellen
        self.current_font_family = font
        if font:
            self.current_font_family = font.get() if hasattr(font, 'get') else font

        actual_font = FontTypes.Fonts.get(self.current_font_family, "Arial")
        
        self.label_font = tkfont.Font(family=actual_font, size=self.settings['BS HistoryText fs'].get(), weight="bold")
        self.value_font = tkfont.Font(family=actual_font, size=self.settings['BS HistoryValue fs'].get(), weight="bold")

        # Kolommen configureren
        self.columnconfigure(0, weight=1, uniform="A")
        self.columnconfigure(1, weight=1, uniform="A")
        self.columnconfigure(2, weight=2)
        self.columnconfigure(3, weight=1, uniform="A")
        self.columnconfigure(4, weight=1, uniform="A")
        
        self.label = {}
        
        self.label['car1Text'] = tk.Label(self, text="car", font=self.label_font)
        self.label['tot1Text'] = tk.Label(self, text="tot", font=self.label_font)
        self.label['tunrText'] = tk.Label(self, text="beurt", font=self.label_font)
        self.label['car2Text'] = tk.Label(self, text="car", font=self.label_font)
        self.label['tot2Text'] = tk.Label(self, text="tot", font=self.label_font)
        
        self.label['car1Text'].grid(row=0, column=0, sticky="nsew", padx=5)
        self.label['tot1Text'].grid(row=0, column=1, sticky="nsew", padx=5)
        self.label['tunrText'].grid(row=0, column=2, sticky="nsew", padx=5)
        self.label['car2Text'].grid(row=0, column=3, sticky="nsew", padx=5)
        self.label['tot2Text'].grid(row=0, column=4, sticky="nsew", padx=5)
        
        # Labels opslaan
        self.labels = []
        # Maak lege labels
        for i in range(self.show_turns):
            
            p1_car_label = tk.Label(self, text="-", font=self.value_font)
            p1_tot_label = tk.Label(self, text="-", font=self.value_font)
            turn_label = tk.Label(self, text=f"{i+1}", font=self.value_font)
            p2_car_label = tk.Label(self, text="-", font=self.value_font)
            p2_tot_label = tk.Label(self, text="-", font=self.value_font)

            p1_car_label.grid(row=i+1, column=0, sticky="ew", padx=5)
            p1_tot_label.grid(row=i+1, column=1, sticky="ew", padx=5)
            turn_label.grid(row=i+1, column=2, sticky="ew", padx=5)
            p2_car_label.grid(row=i+1, column=3, sticky="ew", padx=5)
            p2_tot_label.grid(row=i+1, column=4, sticky="ew", padx=5)

            self.labels.append((p1_car_label, p1_tot_label, turn_label, p2_car_label, p2_tot_label))

        # Registreer bij AppService
        if app_service:
            app_service.register_widget_for_font(self)

        # Eerste update
        self.update_turns()
        self.update_font(font)
        
    def update_turns(self):
        """Update de labels met de laatste beurten (nieuwste bovenaan)."""
        points_and_turns = self.variables.get('points_and_turns', [])
    
        # Laatste show_turns beurten
        recent_turns = points_and_turns[-self.show_turns:]
    
        # Draai de volgorde om: nieuwste eerst
        recent_turns = list(reversed(recent_turns))
    
        for i in range(self.show_turns):
            if i < len(recent_turns):
                turn_data = recent_turns[i]
    
                p1_car_turn = turn_data[0]    # Player1 turn car
                p1_car_tot  = turn_data[1]    # Player1 totaal
                turn_num    = turn_data[2]    # Turn
                p2_car_turn = turn_data[3] if len(turn_data) > 4 else 0
                p2_car_tot  = turn_data[4] if len(turn_data) > 4 else 0
    
                self.labels[i][0].config(text=str(p1_car_turn))
                self.labels[i][1].config(text=str(p1_car_tot))
                self.labels[i][2].config(text=str(turn_num))
                self.labels[i][3].config(text=str(p2_car_turn))
                self.labels[i][4].config(text=str(p2_car_tot))
            else:
                # Lege labels als er minder beurten zijn
                for col in range(5):
                    self.labels[i][col].config(text="-")

    def update_font(self, font):
        """Update de font-family van de labels."""
        self.current_font_family = font if isinstance(font, str) else font.get()
        actual_font = FontTypes.Fonts.get(self.current_font_family, "Arial")
        self.label_font.configure(family=actual_font)
        self.value_font.configure(family=actual_font)





#BS Top Row Center    
class TMCFrame(tk.Frame):
    """Widget die TMC-waarden toont voor twee spelers, schaalbaar en met centrale font updates."""

    def __init__(self, parent, tmcP1=None, colorP1=None, tmcP2=None, colorP2=None, font=None, app_service=None, settings=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure(0, weight=1, uniform="A")
        self.columnconfigure(1, weight=1, uniform="A")
        self.rowconfigure(0, weight=1)
        self.configure(padx=5)

        # -----------------------------
        # Font state
        # -----------------------------
        self.current_font_key = "Clear"
        if font:
            self.current_font_key = font.get() if hasattr(font, "get") else font
        actual_font = FontTypes.Fonts.get(self.current_font_key, "Arial")
        self.text_font = tkfont.Font(family=actual_font, size=settings['BS TMCText fs'].get(), weight="bold")
        self.value_font = tkfont.Font(family=actual_font, size=settings['BS TMCValue fs'].get(), weight="bold")

        # -----------------------------
        # Frames en Labels
        # -----------------------------
        self.colorP1 = colorP1
        self.colorP2 = colorP2
        self.info = {}

        # Speler 1
        self.info["tmc1Frame"] = tk.Frame(self, borderwidth=5, relief="sunken", padx=5)
        self.info["tmc1Frame"].columnconfigure(0, weight=1)
        self.info["tmc1Frame"].grid(row=0, column=0, sticky="nsew")

        self.info["tmc1Text"] = tk.Label(self.info["tmc1Frame"], text="TMC", font=self.text_font)
        self.info["tmc1Text"].grid(row=0, column=0, sticky="nsew")
        self.info["tmc1Int"] = tk.Label(self.info["tmc1Frame"], textvariable=tmcP1, font=self.value_font)
        self.info["tmc1Int"].grid(row=1, column=0, sticky="nsew")

        # Speler 2
        self.info["tmc2Frame"] = tk.Frame(self, borderwidth=5, relief="sunken", padx=5)
        self.info["tmc2Frame"].columnconfigure(0, weight=1)
        self.info["tmc2Frame"].grid(row=0, column=1, sticky="nsew")

        self.info["tmc2Text"] = tk.Label(self.info["tmc2Frame"], text="TMC", font=self.text_font)
        self.info["tmc2Text"].grid(row=0, column=0, sticky="nsew")
        self.info["tmc2Int"] = tk.Label(self.info["tmc2Frame"], textvariable=tmcP2, font=self.value_font)
        self.info["tmc2Int"].grid(row=1, column=0, sticky="nsew")

        # Initial styling
        self.update_colors()

        # Font-schaal bij resize

        # Registratie bij AppService
        if app_service:
            app_service.register_widget_for_font(self)

    # -----------------------------
    # Helpers
    # -----------------------------
    def _apply_font_size(self, width):
        """Berekent grootte op basis van framebreedte en past toe."""
        new_size = max(11, int(width / 7))
        return

    def _rescale_text(self, event):
        self._apply_font_size(event.width)

    def _trigger_rescale(self):
        """Forceer initiale schaal bij init."""
        width = self.winfo_width()
        if width > 1:
            self._apply_font_size(width)

    # -----------------------------
    # Public API
    # -----------------------------
    def update_font(self, font):
        """Update de font-family en forceer herschaling."""
        if not font:
            return
        font_key = font.get() if hasattr(font, "get") else font
        self.current_font_key = font_key
        actual_font = FontTypes.Fonts.get(font_key, "Arial")
        self.text_font.configure(family=actual_font)
        self.value_font.configure(family=actual_font)
        self._trigger_rescale()

    def update_colors(self):
        """Update de achtergrondkleur van beide spelers."""
        if self.colorP1:
            actual_colorP1 = CV.Colors.get(self.colorP1.get())
            if actual_colorP1:
                for key in ["tmc1Frame", "tmc1Text", "tmc1Int"]:
                    self.info[key].configure(background=actual_colorP1)
        if self.colorP2:
            actual_colorP2 = CV.Colors.get(self.colorP2.get())
            if actual_colorP2:
                for key in ["tmc2Frame", "tmc2Text", "tmc2Int"]:
                    self.info[key].configure(background=actual_colorP2)
        
    
class BSInfoFrame(tk.Frame):
    """Widget met caramboles en spelerstats, volledig font-updatebaar."""

    def __init__(self, parent, playerName, variables=None, settings=None, app_service=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.playerName = playerName
        self.variables = variables
        self.settings = settings

        # -----------------------------
        # Font state
        # -----------------------------
        
        self.current_font_key = self.settings['font'].get()

        actual_font = self._get_actual_font(self.current_font_key)

        # Fonts
        self.fonts = {
            "car_text": tkfont.Font(family=actual_font, size=self.settings['BS InfoCarText fs'].get(), weight="bold"),
            "car_int": tkfont.Font(family=actual_font, size=self.settings['BS InfoCarValue fs'].get(), weight="bold"),
            "stats_text": tkfont.Font(family=actual_font, size=self.settings['BS StatsText fs'].get(), weight="bold"),
            "stats_var": tkfont.Font(family=actual_font, size=self.settings['BS StatsValue fs'].get(), weight="bold"),
            "points_text": tkfont.Font(family=actual_font, size=self.settings['BS PointsText fs'].get(), weight="bold"),
            "points_var": tkfont.Font(family=actual_font, size=self.settings['BS PointsValue fs'].get(), weight="bold")
        }

        self.infoFrame = {}
        self.info = {}

        # -----------------------------
        # Caramboles frame
        # -----------------------------
        self.infoFrame["Caramboles"] = tk.Frame(self, borderwidth=5, relief="sunken", padx=5)
        self.infoFrame["Caramboles"].grid(row=0, column=0, sticky="nsew")

        self.info["CarambolesText"] = tk.Label(self.infoFrame["Caramboles"], text="Caramboles", font=self.fonts["car_text"])
        self.info["CarambolesText"].grid(row=0, column=0, sticky="nsew")

        if self.playerName == self.variables["Player1"].get():
            self.info["CarambolesInt"] = tk.Label(self.infoFrame["Caramboles"], textvariable=self.variables["Player1Car"])
        else:
            self.info["CarambolesInt"] = tk.Label(self.infoFrame["Caramboles"], textvariable=self.variables["Player2Car"])

        self.info["CarambolesInt"].configure(font=self.fonts["car_int"])
        self.info["CarambolesInt"].grid(row=1, column=0, sticky="nsew")
        
        

        # -----------------------------
        # Player stats frame
        # -----------------------------
        self.infoFrame["PlayerStats"] = tk.Frame(self, borderwidth=5, relief="sunken")
        self.infoFrame["PlayerStats"].grid(row=1, column=0, sticky="nsew")
        self.infoFrame["PlayerStats"].columnconfigure(0, weight=1, uniform="B")
        self.infoFrame["PlayerStats"].columnconfigure(1, weight=1, uniform="B")
        self.infoFrame["PlayerStats"].columnconfigure(2, weight=1, uniform="B")

        # Static labels
        self.info["HighStreakText"] = tk.Label(self.infoFrame["PlayerStats"], text="Hoogste Serie", font=self.fonts["stats_text"], highlightbackground=CV.Colors.get("Black"), highlightthickness=2)
        self.info["HighStreakText"].grid(row=0, column=0, sticky="nsew")

        self.info["PointsText"] = tk.Label(self.infoFrame["PlayerStats"], text="Punten", font=self.fonts["points_text"], highlightbackground=CV.Colors.get("Black"), highlightthickness=2)
        self.info["PointsText"].grid(row=0, column=1, sticky="nsew")

        self.info["CarToPointText"] = tk.Label(self.infoFrame["PlayerStats"], text="Car. tot punt", font=self.fonts["stats_text"], highlightbackground=CV.Colors.get("Black"), highlightthickness=2)
        self.info["CarToPointText"].grid(row=0, column=2, sticky="nsew")

        # Dynamic labels
        self._prefix = "Player1" if self.playerName == self.variables["Player1"].get() else "Player2"

        # Punten en caramboles tot het volgende punt hangen af van de wedstrijdvorm
        # (bij Uit is uit worden het procenten en caramboles tot uit); zie _refresh_progress.
        self._points_var = tk.StringVar(self)
        self._to_go_var = tk.StringVar(self)

        self.info["HighStreakInt"] = tk.Label(self.infoFrame["PlayerStats"], textvariable=self.variables[f"{self._prefix}HighestSerie"])
        self.info["PointsInt"] = tk.Label(self.infoFrame["PlayerStats"], textvariable=self._points_var)
        self.info["CarToPointInt"] = tk.Label(self.infoFrame["PlayerStats"], textvariable=self._to_go_var)

        self.info["HighStreakInt"].configure(font=self.fonts["stats_var"], highlightbackground=CV.Colors.get("Black"), highlightthickness=2)
        self.info["HighStreakInt"].grid(row=1, column=0, sticky="nsew")

        self.info["PointsInt"].configure(font=self.fonts["points_var"], highlightbackground=CV.Colors.get("Black"), highlightthickness=2)
        self.info["PointsInt"].grid(row=1, column=1, sticky="nsew")

        self.info["CarToPointInt"].configure(font=self.fonts["stats_var"], highlightbackground=CV.Colors.get("Black"), highlightthickness=2)
        self.info["CarToPointInt"].grid(row=1, column=2, sticky="nsew")

        # General frame setup
        for frame in self.infoFrame.values():
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(1, weight=1)

        # Registreer bij AppService
        if app_service:
            app_service.register_widget_for_font(self)

        self._watch_progress()


    # -------------------------------------------------
    # Punten of procenten
    # -------------------------------------------------
    def _watch_progress(self):
        p = self._prefix
        watched = [self.variables[name] for name in (
            f"{p}Car", f"{p}TMC", f"{p}Points", f"{p}CarToNextPoint", "CurrentCar", "CurrentPlayerName"
        )]
        watched.append(self.settings["GameType"])

        self._traces = [(var, var.trace_add("write", self._refresh_progress)) for var in watched]
        self.bind("<Destroy>", self._stop_watching, add="+")
        self._refresh_progress()

    def _stop_watching(self, event):
        if event.widget is not self:
            return
        for var, trace_id in getattr(self, "_traces", []):
            try:
                var.trace_remove("write", trace_id)
            except Exception:
                pass
        self._traces = []

    def _refresh_progress(self, *_):
        """Bij vaste beurten: punten en caramboles tot het volgende punt.
        Bij Uit is uit: percentage van het te maken aantal en caramboles tot uit."""
        try:
            if not self.winfo_exists():
                return
            p = self._prefix
            if str(self.settings["GameType"].get()).strip().lower() == "uit is uit":
                tmc = float(self.variables[f"{p}TMC"].get())
                car = int(self.variables[f"{p}Car"].get())
                if self.variables["CurrentPlayerName"].get() == self.variables[p].get():
                    car += int(self.variables["CurrentCar"].get())   # lopende beurt telt direct mee
                percentage = int(car * 100 / tmc) if tmc > 0 else 0
                self._points_var.set(str(percentage))   # het kopje zegt al "Procent"
                self._to_go_var.set(str(max(0, math.ceil(tmc - car))))
                self.info["PointsText"].config(text="Procent")
                self.info["CarToPointText"].config(text="Car. tot uit")
            else:
                self._points_var.set(str(self.variables[f"{p}Points"].get()))
                self._to_go_var.set(str(self.variables[f"{p}CarToNextPoint"].get()))
                self.info["PointsText"].config(text="Punten")
                self.info["CarToPointText"].config(text="Car. tot punt")
        except (tk.TclError, ValueError):
            pass   # een variabele is tijdelijk leeg of het venster wordt net verwijderd
        except Exception:
            # Onverwachte fout: in het logboek zetten (scorekrijt-autostart.log) in plaats van stil te falen.
            import traceback
            traceback.print_exc()

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------
    def _get_actual_font(self, font_key):
        return FontTypes.Fonts.get(font_key, "Arial")

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------
    def update_font(self, font):
        """Update de fontfamilie en behoud grootte & stijl."""
        if not font:
            return

        font_key = font.get() if hasattr(font, "get") else font
        self.current_font_key = font_key

        actual_font = self._get_actual_font(font_key)
        for f in self.fonts.values():
            f.configure(family=actual_font)




#App Turn Info          
class TurnInfo(tk.Frame):
    """Widget die de huidige beurt toont."""

    def __init__(self, parent, turn=None, font=None, app_service=None, **kwargs):
        super().__init__(parent, **kwargs)

        # Layout & styling
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.configure(
            background=CV.Colors.get("DarkGray"),
            borderwidth=5,
            relief="sunken",
            padx=5,
        )

        self.labels = {}

        # -----------------------------
        # Font state
        # -----------------------------
        self.current_font_key = "Clear"
        if font:
            self.current_font_key = font.get() if hasattr(font, "get") else font

        actual_font = self._get_actual_font(self.current_font_key)

        self.fonts = {
            "turnText": tkfont.Font(
                family=actual_font,
                size=16,
                weight="bold",
            ),
            "turnNumber": tkfont.Font(
                family=actual_font,
                size=20,
                weight="bold",
            ),
        }

        # -----------------------------
        # Widgets
        # -----------------------------
        self.labels["turnText"] = tk.Label(
            self,
            text="Beurt",
            font=self.fonts["turnText"],
            background=CV.Colors.get("DarkGray"),
        )
        self.labels["turnText"].grid(row=0, column=0, sticky="n")

        self.labels["turnNumber"] = tk.Label(
            self,
            textvariable=turn,
            font=self.fonts["turnNumber"],
            background=CV.Colors.get("DarkGray"),
        )
        self.labels["turnNumber"].grid(row=1, column=0, sticky="nsew")

        # Init font
        self.update_font(font)

        # Registreer bij AppService
        if app_service:
            app_service.register_widget_for_font(self)

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def _get_actual_font(self, font_key):
        """Vertaal font-key naar echte systeemfont."""
        return FontTypes.Fonts.get(font_key, "Arial")

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------

    def update_font(self, font):
        """Update alleen de fontfamilie, behoud grootte & stijl."""
        if not font:
            return

        font_key = font.get() if hasattr(font, "get") else font
        self.current_font_key = font_key

        actual_font = self._get_actual_font(font_key)

        for f in self.fonts.values():
            f.configure(family=actual_font)
        
#App MatchInfo           
class MatchInfo(tk.Frame):
    """Widget met caramboles, TMC en punten, met dynamische font-updates."""

    def __init__(self, parent, tmc=None, car=None, points=None, field_color=None, font=None, app_service=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(background=CV.Colors.get("Black"))
        self.columnconfigure(0, weight=1)

        self.labels = {}

        # -----------------------------
        # Font state
        # -----------------------------
        self.current_font_key = "Clear"
        if font:
            self.current_font_key = font.get() if hasattr(font, "get") else font

        actual_font = self._get_actual_font(self.current_font_key)

        # Maak font objects voor de verschillende labels
        self.fonts = {
            "carText": tkfont.Font(family=actual_font, size=20, weight="bold"),
            "carNumber": tkfont.Font(family=actual_font, size=16, weight="bold"),
            "smallText": tkfont.Font(family=actual_font, size=12),
            "number": tkfont.Font(family=actual_font, size=14, weight="bold"),
        }

        # -----------------------------
        # Caramboles
        # -----------------------------
        self.labels["carText"] = tk.Label(
            self,
            text="Caramboles",
            font=self.fonts["carText"],
            foreground=CV.Colors.get("White"),
            background=CV.Colors.get("Black"),
        )
        self.labels["carText"].grid(row=0, column=0, sticky="nsew")

        self.labels["carNumber"] = tk.Label(
            self,
            textvariable=car,
            font=self.fonts["carNumber"],
            foreground=CV.Colors.get("White"),
            background=CV.Colors.get("Black"),
        )
        self.labels["carNumber"].grid(row=1, column=0, sticky="nsew")

        # -----------------------------
        # Info Frame (TMC / Points)
        # -----------------------------
        infoFrame = tk.Frame(self, background=CV.Colors.get("Black"))
        infoFrame.columnconfigure(0, weight=1, uniform="info")
        infoFrame.columnconfigure(1, weight=1, uniform="info")

        # TMC
        self.labels["tmcText"] = tk.Label(
            infoFrame,
            text="TMC",
            font=self.fonts["smallText"],
            background=CV.Colors.get("Gray"),
            highlightbackground=CV.Colors.get("Black"),
            highlightthickness=1,
        )
        self.labels["tmcText"].grid(row=0, column=0, sticky="nsew")

        self.labels["tmcNumber"] = tk.Label(
            infoFrame,
            textvariable=tmc,
            font=self.fonts["number"],
            background=CV.Colors.get("Gray"),
            highlightbackground=CV.Colors.get("Black"),
            highlightthickness=1,
        )
        self.labels["tmcNumber"].grid(row=1, column=0, sticky="nsew")

        # Points
        self.labels["pointsText"] = tk.Label(
            infoFrame,
            text="Punten",
            font=self.fonts["smallText"],
            background=CV.Colors.get("Gray"),
            highlightbackground=CV.Colors.get("Black"),
            highlightthickness=1,
        )
        self.labels["pointsText"].grid(row=0, column=1, sticky="nsew")

        self.labels["pointsNumber"] = tk.Label(
            infoFrame,
            textvariable=points,
            font=self.fonts["number"],
            background=CV.Colors.get("Green"),
            highlightbackground=CV.Colors.get("Black"),
            highlightthickness=1,
        )
        self.labels["pointsNumber"].grid(row=1, column=1, sticky="nsew")

        infoFrame.grid(row=2, column=0, sticky="nsew")

        # Init styling
        if field_color:
            self.update_colors(field_color)
        self.update_font(font)

        # Registreer bij AppService
        if app_service:
            app_service.register_widget_for_font(self)

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------
    def _get_actual_font(self, font_key):
        """Haal de echte font-familie op uit FontTypes."""
        return FontTypes.Fonts.get(font_key, "Arial")

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------
    def update_colors(self, field_color):
        """Update kleuren van labels op basis van field_color."""
        if not field_color:
            return

        color_key = field_color.get() if hasattr(field_color, "get") else field_color
        actual_color = CV.Colors.get(color_key)

        if actual_color:
            self.labels["tmcNumber"].configure(background=actual_color)

    def update_font(self, font):
        """Update font-family van alle labels, behoud grootte en gewicht."""
        if not font:
            return

        font_key = font.get() if hasattr(font, "get") else font
        self.current_font_key = font_key
        actual_font = self._get_actual_font(font_key)

        for f in self.fonts.values():
            f.configure(family=actual_font)


#App
class CurrentTurnInfo(tk.Frame):
    """Widget met info over de huidige beurt."""

    def __init__(self, parent, variables=None, font=None, app_service=None, **kwargs):
        super().__init__(parent, **kwargs)

        self.columnconfigure(0, weight=1)
        self.configure(borderwidth=5, relief="sunken", padx=5)

        self.labels = {}

        # -----------------------------
        # Font state
        # -----------------------------
        self.current_font_key = "Clear"
        if font:
            self.current_font_key = font.get() if hasattr(font, "get") else font

        actual_font = self._get_actual_font(self.current_font_key)

        # Fonts voor de labels
        self.fonts = {
            "playerName": tkfont.Font(family=actual_font, size=18, weight="bold"),
            "text": tkfont.Font(family=actual_font, size=12),
            "number": tkfont.Font(family=actual_font, size=20, weight="bold"),
        }

        # -----------------------------
        # Labels
        # -----------------------------
        self.labels["currentPlayerName"] = tk.Label(
            self,
            textvariable=variables["CurrentPlayerName"],
            font=self.fonts["playerName"]
        )
        self.labels["currentPlayerName"].grid(row=0, column=0, sticky="nsew")
        
        self.labels["carText"] = tk.Label(
            self,
            text="Caramboles deze beurt",
            font=self.fonts["text"]
        )
        self.labels["carText"].grid(row=1, column=0, sticky="nsew")

        self.labels["currentCar"] = tk.Label(
            self,
            textvariable=variables["CurrentCar"],
            font=self.fonts["number"]
        )
        self.labels["currentCar"].grid(row=2, column=0, sticky="nsew")

        self.labels["carToGo"] = tk.Label(
            self,
            textvariable=variables["CurrentCarToNextPointText"],
            font=self.fonts["text"]
        )
        self.labels["carToGo"].grid(row=3, column=0, sticky="nsew")

        # Forceer init font update
        self.update_font(font)

        # Registreer bij AppService
        if app_service:
            app_service.register_widget_for_font(self)

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------
    def _get_actual_font(self, font_key):
        """Vertaal font-key naar een echte systeemfont."""
        return FontTypes.Fonts.get(font_key, "Arial")

    # -------------------------------------------------
    # Public API
    # -------------------------------------------------
    def update_font(self, font):
        """Update alleen de fontfamilie, behoud grootte en stijl."""
        if not font:
            return

        font_key = font.get() if hasattr(font, "get") else font
        self.current_font_key = font_key

        actual_font = self._get_actual_font(font_key)

        for f in self.fonts.values():
            f.configure(family=actual_font)
