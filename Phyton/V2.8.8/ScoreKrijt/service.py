# -*- coding: utf-8 -*-
"""
Created on Fri Jan  9 23:43:04 2026
file name, service.py
@author: BramI
"""
import os
from tkinter import messagebox
from datetime import datetime
from .constants import FieldTypes as FT, FontTypes
from .models import CSVGameModel
from .tk_adapter import TkModelAdapter, format_time
from .Internet import has_internet, send_csv_via_email
from .views import SendMatchEmailWindow, OpenMatchesWindow
import math
import time

CSV_DELIMITER = ";"

class AppLogica:
    """Beheer van scores en wedstrijdlogica."""

    def __init__(self, variables, settings, master=None):
        self.v = variables  # gedeelde TkVariables van AppService
        self.settings = settings
        self.master = master
        
        self.match_dir = "matches"
        os.makedirs(self.match_dir, exist_ok=True)  
        
        self.match_file_path = None
        self.match_finished = False
        self.match_end_reason = None  # "Vaste beurten" | "Uit is uit"
        self.winner = None            # "Player1" | "Player2" | "Gelijk"
        
        self.match_start_time = None
        self.last_turn_start_time = None

        self.match_start_time = None
        self.last_turn_start_time = None
        self.timer_running = False
        
        self.match_start_datetime = None

    
    def ask_send_match_email(self):
        if not has_internet():
            messagebox.showwarning(
                "Geen internetverbinding",
                "Er is geen internetverbinding.\nDe wedstrijd kan niet per e-mail worden verstuurd."
            )
            
            return
    
        result = messagebox.askyesno(
            "Wedstrijd versturen",
            "Wil je de wedstrijd per e-mail versturen?"
            )
    
        if not result:
            return
    
        mail_window = SendMatchEmailWindow(
            self.master,
            send_callback=lambda email: send_csv_via_email(
                self.match_file_path,
                email,
                self.master.settings
            )
        )
    
        self.master.wait_window(mail_window)
    
    def add_time_to_current_player(self):
        if not self.timer_running:
            return
    
        now = time.time()
        elapsed = int(now - self.last_turn_start_time)
        
        if elapsed == 0: 
            elapsed = 1
        
        if self.v["CurrentPlayerName"].get() == self.v["Player1"].get():
            self.v["Player1PlayTime"].set(
                self.v["Player1PlayTime"].get() + elapsed
            )
        else:
            self.v["Player2PlayTime"].set(
                self.v["Player2PlayTime"].get() + elapsed
            )
    
        self.last_turn_start_time = now
            
    def start_timer_if_needed(self):
        if not self.timer_running:
            now = time.time()
            self.match_start_time = now
            self.last_turn_start_time = now
            self.timer_running = True
    
    def stop_timer(self):
        self.timer_running = False
    
    def check_open_matches(self):
        open_matches = self.find_open_matches()
        
        if open_matches:
            # Sorteer op bestandsnaam
            open_matches.sort()
            OpenMatchesWindow(self.master, open_matches, load_callback=self.load_match_file)
                
    def get_match_summary(self):
        v = self.v
        s = self.settings
    
        turns = []
        for row in v["points_and_turns"]:
            turns.append({
                "turn": row[2],
                "player1": {
                    "car": row[0],
                    "total": row[1]
                },
                "player2": {
                    "car": row[3],
                    "total": row[4]
                }
            })
    
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "players": [
                {
                    "name": v["Player1"].get(),
                    "tmc": v["Player1TMC"].get(),
                    "car": v["Player1Car"].get(),
                    "points": v["Player1Points"].get(),
                    "highest": v["Player1HighestSerie"].get(),
                    "playtime": v["Player1PlayTime"].get()
                },
                {
                    "name": v["Player2"].get(),
                    "tmc": v["Player2TMC"].get(),
                    "car": v["Player2Car"].get(),
                    "points": v["Player2Points"].get(),
                    "highest": v["Player2HighestSerie"].get(),
                    "playtime": v["Player2PlayTime"].get()
                }
            ],
            "game_type": s["GameType"].get(),
            "turns_played": v["Turn"].get(),
            "end_reason": self.match_end_reason,
            "winner": self.winner,
            "turn_details": turns
        }
                
    def cleanup_old_matches(self, years=5):
        now = datetime.now()
        for filename in os.listdir(self.match_dir):
            if filename.endswith(".csv"):
                # Veronderstel bestandsnaam: YYYY-MM-DD_HH-MM_Player1_Player2_STATUS.csv
                date_part = filename.split("_")[0]  # 'YYYY-MM-DD'
                try:
                    file_date = datetime.strptime(date_part, "%Y-%m-%d")
                    age_years = (now - file_date).days / 365
                    if age_years > years:
                        os.remove(os.path.join(self.match_dir, filename))
                        print(f"Verwijderd oud wedstrijdbestand: {filename}")
                except Exception as e:
                    print(f"Kan datum niet lezen van bestand {filename}: {e}")
        
    def reset_new_game(self):

        v = self.v
        # Reset match overall  settings 
        self.match_end_reason = None
        self.winner = None
        
        # Reset  variablen        
        v["CurrentPlayerName"].set(v["Player1"].get())
        
        v["Turn"].set(1)
        v["CurrentCar"].set(0)

        v["Player1Car"].set(0)
        v["Player2Car"].set(0)

        v["Player1Points"].set(0)
        v["Player2Points"].set(0)

        v["Player1HighestSerie"].set(0)
        v["Player2HighestSerie"].set(0)
        
        v["Player1PlayTime"].set(0)
        v["Player2PlayTime"].set(0)

        # Reset Match List
        v["points_and_turns"].clear()
        self.match_finished = False
        
        # New match file
        self.start_match_file()
        
    
    def update_player_info(self, p1_name, p1_tmc, p2_name, p2_tmc):
        # Bepaal wie nu actief is (naam-based)
        current_player_name = self.v["CurrentPlayerName"].get()

        # Update namen & te maken caramboles
        self.v["Player1"].set(p1_name)
        self.v["Player2"].set(p2_name)
        self.v["Player1TMC"].set(int(p1_tmc))
        self.v["Player2TMC"].set(int(p2_tmc))

        # Zorg dat CurrentPlayer dezelfde speler blijft
        if current_player_name == p1_name or current_player_name == self.v["Player1"].get():
            self.v["CurrentPlayerName"].set(self.v["Player1"].get())
        else:
            self.v["CurrentPlayerName"].set(self.v["Player2"].get())
 
        self.cal_points()
        self.cal_car_to_next_point()
    
    def note_and_next_turn(self):
        v = self.v  # shortcut
                
        currentTurn = v["Turn"].get()
               
        turn_idx = currentTurn - 1

        # Een telefoon kan een wedstrijd hervatten nadat de SK-Box opnieuw is
        # gestart. Oudere appversies stuurden daarbij geen beurtgeschiedenis.
        # Vul ontbrekende regels aan zodat de eerstvolgende wissel altijd veilig is.
        while len(v['points_and_turns']) <= turn_idx:
            turn_number = len(v['points_and_turns']) + 1
            v['points_and_turns'].append([0, v["Player1Car"].get(), turn_number])
    
        # Wie is de huidige speler?
        if v["CurrentPlayerName"].get() == v["Player1"].get():
            
            #add currentCar to player car if not done before!
            v["Player1Car"].set(v["CurrentCar"].get()+v["Player1Car"].get())
            
            # Update hoogste serie speler 1
            if v["CurrentCar"].get() > v["Player1HighestSerie"].get():
                v["Player1HighestSerie"].set(v["CurrentCar"].get())
            # Wissel speler
            v["CurrentPlayerName"].set(v["Player2"].get())
    
            # Update PointsAndTurns
            if len(v['points_and_turns']) < v["Turn"].get():
                v['points_and_turns'].append([
                    v["CurrentCar"].get(),
                    v["Player1Car"].get(),
                    v["Turn"].get()
                ])
            else:
                v['points_and_turns'][turn_idx][0] = v["CurrentCar"].get()
                v['points_and_turns'][turn_idx][1] = v["Player1Car"].get()
            
            try:
                v['CurrentCar'].set(v['points_and_turns'][turn_idx][3])
                #print("Teruggehaald van p2")
            except:
                v['CurrentCar'].set(0)
                #print("Reset voor p2")
        else:
         
            #add currentCar to player car if not done before!
            v["Player2Car"].set(v["CurrentCar"].get()+v["Player2Car"].get())
            
            # Update hoogste serie speler 2
            if v["CurrentCar"].get() > v["Player2HighestSerie"].get():
                v["Player2HighestSerie"].set(v["CurrentCar"].get())
            # Wissel speler
            v["CurrentPlayerName"].set(v["Player1"].get())
            v["Turn"].set(v["Turn"].get() + 1)
    
            # Update PointsAndTurns
            if len(v['points_and_turns'][turn_idx]) < 4:
                v['points_and_turns'][turn_idx].extend([
                    v["CurrentCar"].get(),
                    v["Player2Car"].get()
                ])
            else:
                v['points_and_turns'][turn_idx][3] = v["CurrentCar"].get()
                v['points_and_turns'][turn_idx][4] = v["Player2Car"].get()
            
            try:
                v['CurrentCar'].set(v['points_and_turns'][turn_idx + 1][0])
                #print("Teruggehaald van p1")
            except:
                v['CurrentCar'].set(0)
                #print("Reset voor p1")
                
            if (v["Turn"].get() > int(self.settings['GameTurns'].get()) and self.settings['GameType'].get() == 'Vaste beurten'):
                self.finish_match(reason="Vaste beurten")
                return True
        
        game_type = self.settings['GameType'].get()
        
        if game_type == 'Uit is uit':
            if (v["CurrentPlayerName"].get() == v["Player1"].get()):
                
                p1_points = self.v["Player1Points"].get()
                p2_points = self.v["Player2Points"].get()
                
                # --- GELIJK â†’ VERLENGING ---
                if (p1_points == 10 and p2_points == 10):
            
                    self.v["Player1TMC"].set(math.ceil(float(self.v["Player1TMC"].get()) * 1.3))
                    self.v["Player2TMC"].set(math.ceil(float(self.v["Player2TMC"].get()) * 1.3))
                
                elif (p1_points == 10 or p2_points == 10):
                    self.finish_match(reason="Uit is uit")
                    return True  # winnaar bekend
         
        
        return False
        # Optioneel: debug
        #print(v['points_and_turns'])
 
    
       
    def return_and_prev_turn(self):
        v = self.v  # shortcut
        """Ga terug naar de vorige beurt en herstel waarden."""
        current_turn_idx = v["Turn"].get() - 1

        # Huidige speler ophalen
        current_player = v["CurrentPlayerName"].get()
        player1 = v["Player1"].get()
        player2 = v["Player2"].get()

        car_this_turn = v["CurrentCar"]
        player1_car = v["Player1Car"]
        player2_car = v["Player2Car"]
        turn_number = v["Turn"]

        # Als huidige speler Player1 is
        if current_player == player1:
            if turn_number.get() == 1:
                return  # Kan niet verder terug
            # Reset huidige beurt
            car_this_turn.set(0)
            # Herstel vorige beurt van Player2
            prev_idx = current_turn_idx - 1
            if prev_idx >= 0 and len(v['points_and_turns']) > prev_idx:
                car_this_turn.set(v['points_and_turns'][prev_idx][3])
                player2_car.set(v['points_and_turns'][prev_idx][4] - car_this_turn.get())
            # Zet huidige speler naar Player2
            v["CurrentPlayerName"].set(player2)
            turn_number.set(prev_idx + 1)  # Turn is 1-based
        else:
            # Als huidige speler Player2 is
            v["CurrentPlayerName"].set(player1)
            if len(v['points_and_turns']) > current_turn_idx:
                car_this_turn.set(v['points_and_turns'][current_turn_idx][0])
                player1_car.set(v['points_and_turns'][current_turn_idx][1] - car_this_turn.get())
            else:
                car_this_turn.set(0)  
        
       
        # Optioneel: debug
        #print(v['points_and_turns'])
                
    def cal_car_to_next_point(self):
        #Bereken caramboles nodig tot het volgende punt voor de huidige speler.

        current_player = self.v["CurrentPlayerName"].get()

        tmcP1 = float(self.v["Player1TMC"].get())
                
        carP1 = int(self.v["Player1Car"].get())
        target_varP1 = self.v["Player1CarToNextPoint"]
 
        tmcP2 = float(self.v["Player2TMC"].get())
        carP2 = int(self.v["Player2Car"].get())
        target_varP2 = self.v["Player2CarToNextPoint"]
            
        if current_player == self.v["Player1"].get():    
            carP1 = carP1 + self.v['CurrentCar'].get()     #Derect waarde meerekenen.!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        else:
            carP2 = carP2 + self.v['CurrentCar'].get()     #Derect waarde meerekenen.!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            
        waarde_car_per_puntP1 = tmcP1 / 10
        huidig_puntenP1 = int(carP1 / waarde_car_per_puntP1)
        volgend_puntP1 = huidig_puntenP1 + 1
        benodigde_carP1 = math.ceil(volgend_puntP1 * waarde_car_per_puntP1)
        resterendP1 = max(0, benodigde_carP1 - carP1)
        
        waarde_car_per_puntP2 = tmcP2 / 10
        huidig_puntenP2 = int(carP2 / waarde_car_per_puntP2)
        volgend_puntP2 = huidig_puntenP2 + 1
        benodigde_carP2 = math.ceil(volgend_puntP2 * waarde_car_per_puntP2)
        resterendP2 = max(0, benodigde_carP2 - carP2)

        if current_player == self.v["Player1"].get(): 
            # Algemene + speler-specifieke waarde
            self.v["CurrentCarToNextPoint"].set(resterendP1)    
            currentCarToNextPointText = f"nog {resterendP1} voor volgend punt"
        else:
            self.v["CurrentCarToNextPoint"].set(resterendP2)    
            currentCarToNextPointText = f"nog {resterendP2} voor volgend punt"
            
        self.v["CurrentCarToNextPointText"].set(currentCarToNextPointText)
            
        target_varP1.set(resterendP1)
        target_varP2.set(resterendP2)
       
    def cal_points(self):
        """Bereken punten voor beide spelers op basis van caramboles en gemiddelde."""
        
        current_player = self.v["CurrentPlayerName"].get()
        
        if current_player == self.v["Player1"].get():
            # Speler 1
            car = int(self.v["Player1Car"].get())
            p1_tmc = float(self.v["Player1TMC"].get())
            
            p1_car = car + self.v['CurrentCar'].get()     #Derect waarde meerekenen.!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            if p1_tmc > 0:
                val_point = p1_tmc / 10
                p1_points = int(p1_car / val_point)
            else:
                p1_points = 0
    
            self.v["Player1Points"].set(p1_points)
        else:
            # Speler 2
            car = int(self.v["Player2Car"].get())
            p2_tmc = float(self.v["Player2TMC"].get())
            
            p2_car = car + self.v['CurrentCar'].get()     #Derect waarde meerekenen.!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            
            if p2_tmc > 0:
                val_point = p2_tmc / 10
                p2_points = int(p2_car / val_point)
            else:
                p2_points = 0
    
            self.v["Player2Points"].set(p2_points)
      
    def cal_both_points(self):
        """Bereken punten voor beide spelers op basis van caramboles en TMC."""

        current_player = self.v["CurrentPlayerName"].get()
        current_car = int(self.v["CurrentCar"].get())

        p1_car = int(self.v["Player1Car"].get())
        p2_car = int(self.v["Player2Car"].get())

        if current_player == self.v["Player1"].get():
            p1_car += current_car
        elif current_player == self.v["Player2"].get():
            p2_car += current_car

        p1_tmc = float(self.v["Player1TMC"].get())
        p2_tmc = float(self.v["Player2TMC"].get())

        p1_points = int(p1_car / (p1_tmc / 10)) if p1_tmc > 0 else 0
        p2_points = int(p2_car / (p2_tmc / 10)) if p2_tmc > 0 else 0

        self.v["Player1Points"].set(p1_points)
        self.v["Player2Points"].set(p2_points)

    def increment_current_car(self):
        var = self.v["CurrentCar"]
        current_value = var.get()
        current_player = self.v["CurrentPlayerName"].get()
    
        # Haal speler-specifieke variabelen
        if current_player == self.v["Player1"].get():
            player_car = self.v["Player1Car"].get()
            player_tmc = float(self.v["Player1TMC"].get())
        else:
            player_car = self.v["Player2Car"].get()
            player_tmc = float(self.v["Player2TMC"].get())
    
        # Bereken max mogelijk voor deze beurt
        max_for_turn = player_tmc - player_car
    
        # Bij â€œUit is uitâ€ mag de speler niet meer caramboles nemen dan zijn gemiddelde
        if self.settings['GameType'].get() == 'Uit is uit':
            if current_value >= max_for_turn:
                return  # kan niet hoger
            var.set(current_value + 1)
        else:
            # Standaard gedrag voor andere speltypes
            var.set(current_value + 1)

    def decrement_current_car(self):
        var = self.v["CurrentCar"]
        value = var.get()
        min_val = CSVGameModel.fields["CurrentCar"]["min"]
        if value > min_val:
            var.set(value - 1)
    
    def set_player_color(self, settings):
        start_color = settings['start color'].get()  # 'Geel' of 'Wit'
        if start_color == 'Geel':
            self.v['Player1BackGroundColor'].set('Yellow')
            self.v['Player2BackGroundColor'].set('White')
        else:
            self.v['Player1BackGroundColor'].set('White')
            self.v['Player2BackGroundColor'].set('Yellow')
            
    def finish_match(self, reason):
        v = self.v
    
        self.match_finished = True
        self.match_end_reason = reason
    
        if reason == "Vaste beurten":
            p1_points = v["Player1Points"].get()
            p2_points = v["Player2Points"].get()
    
            if p1_points > p2_points:
                self.winner = v["Player1"].get()
            elif p2_points > p1_points:
                self.winner = v["Player2"].get()
            else:
                self.winner = "Gelijk"
    
        elif reason == "Uit is uit":
            if v["Player1Points"].get() >= 10:
                self.winner = v["Player1"].get()
            elif v["Player2Points"].get() >= 10:
                self.winner = v["Player2"].get()
        
        self.update_match_file()
        self.finish_match_file()      
    
    def _build_match_filename(self, finished=False):
        status = "AFGEROND" if finished else "LOPEND"

        if not self.match_start_datetime:
            self.match_start_datetime = datetime.now()  # fallback
    
        date_str = self.match_start_datetime.strftime("%Y-%m-%d")
        time_str = self.match_start_datetime.strftime("%H-%M")
    
        p1 = self.v["Player1"].get().replace(" ", "_")
        p2 = self.v["Player2"].get().replace(" ", "_")
    
        return f"{date_str}_{time_str}_{p1}_{p2}_{status}.csv"
        
    def update_match_file(self):
        if not self.match_file_path:
            return
    
        v = self.v
        s = self.settings
        d = CSV_DELIMITER
    
        with open(self.match_file_path, "w", encoding="utf-8", newline="") as f:
            
            f.write("sep=;\n")
            # ===== HEADER =====
            f.write(f"Datum{d}{datetime.now().strftime('%Y-%m-%d')}\n")
            f.write(f"Tijd{d}{datetime.now().strftime('%H:%M')}\n\n")
        
            f.write(f"Speler 1{d}{v['Player1'].get()}{d}TMC{d}{v['Player1TMC'].get()}\n")
            f.write(f"Speler 2{d}{v['Player2'].get()}{d}TMC{d}{v['Player2TMC'].get()}\n\n")
        
            f.write(f"Wedstrijdvorm{d}{s['GameType'].get()}\n")
            f.write(f"Aantal beurten{d}{s['GameTurns'].get()}\n\n")
        
            # ===== TABEL =====
            f.write(
                f"{v['Player1'].get()}{d}{d}{d}{d}{v['Player2'].get()}\n"
                f"Beurt{d}Car{d}Tot{d}{d}Beurt{d}Car{d}Tot\n"
            )
        
            for row in v["points_and_turns"]:
                beurt = row[2]
        
                p1_car = row[0] if len(row) > 0 else ""
                p1_tot = row[1] if len(row) > 1 else ""
        
                p2_car = row[3] if len(row) > 3 else ""
                p2_tot = row[4] if len(row) > 4 else ""
        
                f.write(
                    f"{beurt}{d}{p1_car}{d}{p1_tot}{d}{d}"
                    f"{beurt}{d}{p2_car}{d}{p2_tot}\n"
                )
    
            f.write("\n")
    
            # ===== TOTALEN =====
            f.write(f"{v['Player1'].get()} totaal caramboles{d}{v['Player1Car'].get()}\n")
            f.write(f"{v['Player2'].get()} totaal caramboles{d}{v['Player2Car'].get()}\n\n")
            
            
            f.write(f"{v['Player1'].get()} speeltijd{d}{format_time(v['Player1PlayTime'].get())}\n")
            f.write(f"{v['Player2'].get()} speeltijd{d}{format_time(v['Player2PlayTime'].get())}\n")
    
            # ===== GAMESTATUS =====
            f.write("'==============================\n")
            f.write("WEDSTRIJDSTATUS\n")
            f.write("'==============================\n")
    
            if not self.match_finished:
                f.write(f"Eindstatus{d}LOPEND\n")
            else:
                f.write(f"Eindstatus{d}AFGEROND\n")
                f.write(f"Reden einde{d}{self.match_end_reason}\n\n")
            
                if self.match_end_reason == "Vaste beurten":
                    f.write(f"Speler 1 punten{d}{v['Player1Points'].get()}\n")
                    f.write(f"Speler 2 punten{d}{v['Player2Points'].get()}\n\n")
            
                f.write(f"Winnaar{d}{self.winner}\n")
    
    def start_match_file(self):
        self.match_start_datetime = datetime.now()

        filename = self._build_match_filename(finished=False)
        self.match_file_path = os.path.join(self.match_dir, filename)
    
        self.match_finished = False
        self.update_match_file()
        
    def finish_match_file(self):
        if not self.match_file_path:
            return
    
        new_name = self._build_match_filename(finished=True)
        new_path = os.path.join(self.match_dir, new_name)
    
        try:
            os.rename(self.match_file_path, new_path)
            self.match_file_path = new_path
            self.match_finished = True
        except Exception as e:
            print("Kon wedstrijd bestand niet hernoemen:", e)
    
    def load_match_file(self, file_path):
        self.match_file_path = file_path
    
        with open(file_path, encoding="utf-8") as f:
            lines = [
                line.strip()
                for line in f
                if line.strip() and not line.startswith("sep=")
            ]
    
        self._parse_header(lines)
        self._parse_turns(lines)
        self._restore_state()

    def _parse_header(self, lines):
        s = self.settings
        player1_set = False
        player2_set = False
    
        for line in lines:
            parts = line.split(";")
            
            if parts[0] == "Speler 1" and not player1_set:
                name = parts[1].strip() if len(parts) > 1 else "Player1"
                tmc_str = parts[3].strip() if len(parts) > 3 else "0"
                try:
                    tmc = int(tmc_str)
                except ValueError:
                    tmc = 0
                self.v["Player1"].set(name)
                self.v["Player1TMC"].set(tmc)
                player1_set = True
            
            elif parts[0] == "Speler 2" and not player2_set:
                name = parts[1].strip() if len(parts) > 1 else "Player2"
                tmc_str = parts[3].strip() if len(parts) > 3 else "0"
                try:
                    tmc = int(tmc_str)
                except ValueError:
                    tmc = 0
                self.v["Player2"].set(name)
                self.v["Player2TMC"].set(tmc)
                player2_set = True
            
            elif parts[0] == "Wedstrijdvorm" and len(parts) > 1:
                s["GameType"].set(parts[1])
            
            elif parts[0] == "Aantal beurten":
                try:
                    s["GameTurns"].set(int(parts[1]))
                except (IndexError, ValueError):
                    s["GameTurns"].set(10)  # default aantal beurten
            
            elif parts[0] == "Eindstatus" and len(parts) > 1:
                self.match_finished = (parts[1] == "AFGEROND")
            
            elif parts[0] == "Reden einde" and len(parts) > 1:
                self.match_end_reason = parts[1]
                    
    def _parse_turns(self, lines):
        v = self.v
        v["points_and_turns"].clear()
    
        start = False
        for line in lines:
            if line.startswith("Beurt;Car"):
                start = True
                continue
    
            if start:
                parts = line.split(";")
                if len(parts) < 7:
                    break
    
                beurt = int(parts[0])
                p1_car = int(parts[1]) if parts[1] else 0
                p1_tot = int(parts[2]) if parts[2] else 0
                p2_car = int(parts[5]) if parts[5] else 0
                p2_tot = int(parts[6]) if parts[6] else 0
    
                v["points_and_turns"].append([
                    p1_car, p1_tot, beurt,
                    p2_car, p2_tot
            ])
    def _restore_state(self):
        v = self.v
    
        if not v["points_and_turns"]:
            return
    
        last = v["points_and_turns"][-1]
    
        v["Player1Car"].set(last[1])
        v["Player2Car"].set(last[4])
    
        v["Turn"].set(last[2])
        v["CurrentCar"].set(0)
    
        # bepaal actieve speler
        if v["Turn"].get() == len(v["points_and_turns"]):
            v["CurrentPlayerName"].set(v["Player2"].get())
        else:
            v["CurrentPlayerName"].set(v["Player1"].get())
            
    def find_open_matches(self):
        """Return een lijst van bestandsnamen van openstaande wedstrijden (LOPEND in bestandsnaam)."""
        match_dir = self.match_dir  # gebruik bestaande map
        open_matches = []

        if not os.path.exists(match_dir):
            return open_matches

        for filename in os.listdir(match_dir):
            if filename.endswith(".csv") and "_LOPEND" in filename:
                open_matches.append(os.path.join(match_dir, filename))

        return open_matches
    

class AppService:
    def __init__(self, font_var=None):
        # Lijst van widgets die hun font moeten updaten
        self._registered_widgets = []
        self._font_var = font_var

        if font_var:
            # Trace op StringVar zodat veranderingen live worden doorgegeven
            font_var.trace_add("write", self._on_font_change)

    def create_tk_variables(self, master=None):
        """Maak alle TkVariables op basis van CSVGameModel en FieldTypes."""
        return TkModelAdapter.create_variables(CSVGameModel, master)

    def get_ui_value(self, variable, field_type):
        """Converteer TkVar naar python waarde, inclusief int_list."""
        value = variable.get()
        if field_type == FT.integer:
            return int(value)
        if field_type == FT.int_list:
            from .utils import parse_list
            return parse_list(value)
        if field_type == FT.boolean:
            return bool(value)
        return value

    def register_widget_for_font(self, widget):
        """Registreer een widget die update_font(font) ondersteunt."""
        if widget not in self._registered_widgets:
            self._registered_widgets.append(widget)
            # Forceer meteen update bij registratie als font al bekend is
            if self._font_var:
                widget.update_font(self._get_actual_font_family())

    def _on_font_change(self, *args):
        """Wordt aangeroepen als de font StringVar verandert."""
        new_family = self._get_actual_font_family()
        for widget in self._registered_widgets:
            try:
                widget.update_font(new_family)
            except Exception as e:
                print(f"Fout bij font update van {widget}: {e}")

    def _get_actual_font_family(self):
        """Haal de echte font-family op uit FontTypes."""
        key = self._font_var.get() if hasattr(self._font_var, "get") else self._font_var
        return FontTypes.Fonts.get(key, "Arial")

    def update_all_fonts(self, font_name):
        """Update het font voor alle geregistreerde widgets."""
        for widget in self._registered_widgets:
            try:
                widget.update_font(font_name)
            except Exception as e:
                print(f"Fout bij font update van {widget}: {e}")

