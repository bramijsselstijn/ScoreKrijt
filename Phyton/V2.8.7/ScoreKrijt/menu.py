# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 21:39:30 2026

@author: BramI
"""


import tkinter as tk
from tkinter import messagebox, PhotoImage, Menu
from .tk_adapter import resource_path as rp
from PIL import Image, ImageTk

from . import constants as c

class MainMenu(Menu):
    """The Application's main menu """
    def __init__(self, parent, settings, callbacks, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Ensure images are instance attributes so they aren't garbage collected
        # Note: If these paths are incorrect, PhotoImage will throw a TclError
        try:
            self.new_file_icon = PhotoImage(file=rp('ScoreKrijt/icons/new_file.gif'))
            self.open_file_icon = PhotoImage(file=rp('ScoreKrijt/icons/open_file.gif'))
            self.save_file_icon = PhotoImage(file=rp('ScoreKrijt/icons/save.gif'))
            self.undo_icon = PhotoImage(file=rp('ScoreKrijt/icons/undo.gif'))
            self.redo_icon = PhotoImage(file=rp('ScoreKrijt/icons/redo.gif'))
        except tk.TclError as e:
            print(f"Warning: Icon files not found. {e}")
            self.new_file_icon = self.open_file_icon = self.save_file_icon = None
            self.undo_icon = self.redo_icon = None

        # Data sources (assuming 'c' is your configuration module imported elsewhere)
        self.fonts = c.FontTypes.Fonts
        self.playColors = c.ColorValeus.PlayColors

        # --- File Menu ---
        file_menu = Menu(self, tearoff=False)
        file_menu.add_command(label="New", accelerator='Ctrl+N', compound='left', image=self.new_file_icon, underline=0, command=callbacks['file->new'])
        file_menu.add_command(label="Open", accelerator='Ctrl+O', compound='left', image=self.open_file_icon, underline=0, command=callbacks['file->open'])   
        # Fixed: Changed command to 'file->save' (was 'file->open' in your snippet)
        #file_menu.add_command(label="Save", accelerator='Ctrl+S', compound='left', image=self.save_file_icon, underline=0, command=callbacks['file->save'])
        #file_menu.add_command(label="Save as", accelerator='Shift+Ctrl+S', compound='left', underline=0, command=callbacks['file->save_as'])
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=callbacks['file->quit'])
        self.add_cascade(label='File', menu=file_menu)
        
        # --- Edit Menu ---
        edit_menu = Menu(self, tearoff=False)
        edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', compound='left', image=self.undo_icon, command=callbacks['return_and_prev_turn'])
        edit_menu.add_separator()
        edit_menu.add_command(label='Wedstrijd Info', command=callbacks['edit_match'])
        self.add_cascade(label='Edit', menu=edit_menu)
            
        # --- View Menu (Weergave) ---
        view_menu = Menu(self, tearoff=False)
        view_menu.add_checkbutton(label='Groot scherm', variable=settings['bigScreen'], command=callbacks['big_screen_toggle'])
        view_menu.add_checkbutton(label='Open Groot scherm in full screen', variable=settings['OpenBigScreenFullScreen'])
        view_menu.add_checkbutton(label='Geschiedenis', variable=settings['BS history'])
        
        view_menu.add_separator()
        # Submenu: Lettertype
        font_menu = Menu(view_menu, tearoff=0) 
        for font_name in sorted(self.fonts):     
            font_menu.add_radiobutton(label=font_name, variable=settings['font'], command=callbacks['change_font'])
        view_menu.add_cascade(label="Lettertype", menu=font_menu)
        
        # Submenu: Start kleur
        startingColor_menu = Menu(view_menu, tearoff=0) 
        for color_name in sorted(self.playColors):     
            startingColor_menu.add_radiobutton(label=color_name, variable=settings['start color'], command=callbacks['set_player_color'])
        view_menu.add_cascade(label="Start kleur", menu=startingColor_menu)
        
        view_menu.add_separator()
        view_menu.add_checkbutton(label='BlueTooth Mode', variable=settings['BlueTooth Mode'])
        view_menu.add_checkbutton(label='Wedstrijd overzicht', variable=settings['ShowGameSummery'])
        view_menu.add_checkbutton(label='Wedstrijd mailen', variable=settings['AskToMail'])
        view_menu.add_checkbutton(label='Wedstrijden controlleren', variable=settings['CheckPreviousMatches'])
        view_menu.add_checkbutton(label='Nieuw wedstrijd automatisch starten', variable=settings['StartNewMatchAutomatic'])
        view_menu.add_checkbutton(label='Wedstrijden verwijderen na (ingesteld) jaar', variable=settings['CleanupOldMatches'])
        view_menu.add_separator()
        view_menu.add_command(label='Instellingen', underline=0, command=callbacks['settings_menu'])
        self.add_cascade(label='Weergave', menu=view_menu)
        
        # --- Help Menu ---
        help_menu = Menu(self, tearoff=False)
        biljart_rules = Menu(help_menu, tearoff=0)
        biljart_rules.add_command(label='Het biljart', command=lambda: HetBiljart(self.master))
        biljart_rules.add_command(label='Acquitstoot en carambole', command=Acquitstoot)
        biljart_rules.add_command(label='Algemene spelers fouten', command=Spelersfouten)
        help_menu.add_cascade(label='Algemeen biljart regels', menu=biljart_rules)
        help_menu.add_separator()
        # --- Libre Help ---
        libre_help = Menu(help_menu, tearoff=0)
        libre_help.add_command(label='Het libre-spel', command=HetLibreSpel)
        libre_help.add_command(label='Uitspringen', command=UitspringenLibre)
        libre_help.add_command(label='Vastliggen', command=VastliggenLibre)
        help_menu.add_cascade(label='Libre help', menu=libre_help)
        help_menu.add_separator()
        # --- coushen ---
        coushen_help = Menu(help_menu, tearoff=0)
        coushen_help.add_command(label='Het bandstoten-spel', command=HetBandstotenSpel)
        coushen_help.add_command(label='Uitspringen', command=UitspringenLibre)
        coushen_help.add_command(label='Vastliggen', command=VastliggenLibre)
        help_menu.add_cascade(label='Bandstoten help', menu=coushen_help)
        help_menu.add_separator()
        # --- 3 Coushens ---
        three_coushen_help = Menu(help_menu, tearoff=0)
        three_coushen_help.add_command(label='Het 3 banden-spel', command=Het3bandenSpel)
        three_coushen_help.add_command(label='Uitspringen', command=Het3bandenUitspringen)
        three_coushen_help.add_command(label='Vastliggen', command=Het3bandenVastliggen)
        help_menu.add_cascade(label='Driebanden help', menu=three_coushen_help)
                
        # --- Common info
        help_menu.add_separator()
        help_menu.add_separator()
        help_menu.add_command(label='Help', command=self.show_help)
        help_menu.add_command(label='About...', command=self.show_about)
        self.add_cascade(label='Help', menu=help_menu)
    
    def show_about(self):
        messagebox.showinfo(
            title='About', 
            message='Score Krijt', 
            detail='by Bram IJsselstijn\nFor more info read the manual.\nNote: there is no manual.\n\nDeze software is gemaakt met behulp van AI (Claude van Anthropic).\nThis software was made with the help of AI (Claude by Anthropic).'
        )

    def show_help(self):
        messagebox.showinfo(
            title='Help', 
            message='Score Krijt Help', 
            detail=
            'Contact support if you cannot find the manual.\n'+
            'Also do not connact the writer of this program.\n'+
            'He is a noob at this stupid game ;).\n\n'+
            'Special thanks to "Biljartvereniging de Musketier",\n'+
            'and "Het gebouw, Ammerstol" for testing\n\n'+
            'Rules found on: \n'+
            'https://www.bcraalte.nl/informatie/biljart-regels \n'+
            '1-2025'
        )

class HelpWindow(tk.Toplevel):
    def __init__(self, title, content, image_path=None, master=None):
        super().__init__(master)
        self.title(title)
        self.geometry("700x600")

        if image_path:
            self._create_image(image_path)

        self._create_text(content)

    def _create_image(self, path):
        self.original_image = Image.open(path)

        self.img_label = tk.Label(self)
        self.img_label.pack(fill="x")

        self.bind("<Configure>", self._resize_image)
        self._resize_image()

    def _resize_image(self, event=None):
        width = self.winfo_width()
        if width < 10:
            return

        w, h = self.original_image.size
        new_h = int(h * (width / w))
        resized = self.original_image.resize((width, new_h), Image.LANCZOS)

        self.photo = ImageTk.PhotoImage(resized)
        self.img_label.config(image=self.photo)

    def _create_text(self, content):
        frame = tk.Frame(self)
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text = tk.Text(
            frame,
            wrap="word",
            yscrollcommand=scrollbar.set,
            font=("Courier New", 11)
        )
        text.pack(fill="both", expand=True)

        scrollbar.config(command=text.yview)

        text.insert("1.0", content)
        text.config(state="disabled")

class HetBiljart(HelpWindow):
    def __init__(self, master=None):
        super().__init__(
            title="Het biljart",
            image_path=rp("ScoreKrijt/icons/biljart.png"),
            content=self._inhoud(),
            master=master
        )

    def _inhoud(self):
        return """Het biljart

De korte banden van het biljart worden de bovenband (het verst van de afstootlijn af)
en de benedenband (het dichtst bij de afstootlijn) genoemd.

Op het biljart staan over het algemeen 5 acquits (stippen waar de bal behoort te liggen).

- het bovenacquit (het dichtst bij de bovenband op de lengteaslijn)
- het middenacquit (het middelste acquit op de lengteaslijn)
- het benedenacquit (het middelste acquit op de afstootlijn)
- het rechteracquit (rechts van het benedenacquit)
- het linkeracquit (links van het benedenacquit)
"""

class Acquitstoot(HelpWindow):
    def __init__(self, master=None):
        super().__init__(
            title="Acquitstoot en carambole",
            content=self._inhoud(),
            master=master
        )

    def _inhoud(self):
        return """De acquitstoot

Voor de beginstoot (acquitstoot) worden de ballen als volgt in de beginpositie geplaatst:

De rode bal vanaf de bovenband op het bovenste acquit (ga daarbij midden voor de bovenband staan) 
en de witte ballen vanaf de benedenband (midden voor). Eerst de aanspeelbal op het benedenacquit 
en daarna de speelbal op het rechter acquit tenzij een speler aangeeft vanaf het linker acquit 
willen spelen, dan wordt de speelbal op het linker acquit geplaatst.

Als een gemerkte bal (aanspeelbal) op een acquit wordt geplaatst, dan moet die bal zo worden 
geplaatst, dat de speler het merkteken kan zien. Het beste is de bal zo neer te leggen, dat het 
merkteken boven op de bal komt te liggen.

De beginstoot vindt altijd plaats rechtstreeks via de rode bal. Elke ander manier is fout 
en moet direct worden afgeteld.

Er is altijd sprake van een beginstoot, als de ballen in de beginpositie moeten worden geplaatst. 
Dus ook als tijdens de wedstrijd de ballen vastliggen en deze op verzoek van de speler worden 
opgezet of als een van de ballen is uitgesprongen. Het opzetten gaat weer op dezelfde manier zoals 
hierboven beschreven is.

 

De carambole

Een carambole is gemaakt als de speelbal, nadat deze in beweging is gebracht door een éénmalig 
toegepaste stoot door de pomerans van de keu, de beide andere ballen raakt en is pas geldig nadat 
alle ballen tot stilstand zijn gekomen en er volgens de arbiter geen fouten zijn gemaakt door de 
speler (als de speler geen fouten heeft gemaakt en de ballen nog rollen mag de carambole al vast 
geteld worden).

Alléén de arbiter beslist of een carambole geldig is of niet en niemand anders.


"""        

class Spelersfouten(HelpWindow):
    def __init__(self, master=None):
        super().__init__(
            title="Spelersfouten",
            content=self._inhoud(),
            master=master
        )

    def _inhoud(self):
        return """Spelersfouten

Fouten die een speler kan maken, zijn:

1. uitgesprongen bal (buiten de omlijsting of op de omlijsting);
2. touché (een van de ballen wordt aangeraakt, op welke wijze dan ook);
3. indirect touché (opzettelijk zo handelen, dat, zonder dat de ballen 
   worden aangeraakt, de positie van de ballen wordt, gewijzigd; bijv. 
   hard tegen het biljart stoten of het laken optrekken met een nagel 
   of tegen een bal blazen);
4. biljardé (doordrukken of een bal stoten die vastligt anders dan d.m.v.
   een massé of piqué);
5. voeten los (op het moment van de stoot niet met tenminste 
   één voet de grond raken);
6. merkteken (als naar oordeel van de arbiter een speler afstoot, en die 
   speler voordien een zichtbaar merkteken heeft aangebracht en dit 
   merkteken als hulpmiddel gebruikt om een carambole te maken);
7. verkeerde bal (spelen met een andere bal dan de speelbal);
   bewegende bal(len) (bij het afstoten liggen de ballen of ligt één bal 
   nog niet stil na de vorige stoot).
   
Wat is een biljardé?

- Wanneer de keu nog in contact is met de speelbal op het moment dat die 
  speelbal een andere bal of een band raakt 
  (het zgn. doordrukken. Dit is moeilijk te constateren);
- Het spelen via de vastliggende bal of band nadat door de arbiter 
  was aangekondigd dat de speelbal vast lag, anders dan via een kopstoot.
"""

class HetLibreSpel(HelpWindow):
    def __init__(self, master=None):
        super().__init__(
            title="Het libre-spel",
            content=self._inhoud(),
            master=master
        )

    def _inhoud(self):
        return """Het libre

Bij het libre (vrije spel) maakt het in principe niet uit hoe 
de caramboles gemaakt worden, mits daarbij maar geen speelfouten 
worden gemaakt. Bij dit spel hebben we wel te maken met verboden 
zones.

De verboden zones bij libre klein bevinden zich in de hoeken van 
het biljart. De grootte van deze zones zijn als volgt:

Tòt de overgangsklasse 17 X 17 cm. (op de banden)
Vanaf de overgangsklasse en hoger 28,75 X 57,5 cm. 
(op de banden en de grootste maat op de lange band)
Voor de verboden zones gelden de volgende annonces:

à cheval
entrée
dedans
resté dedans (is een fout, dus: noteren enz.)

"A cheval" moet worden geannonceerd als een van de aanspeelballen 
in een verboden zone ligt en de andere bal (niet de speelbal) tegen
diezelfde zone aanligt, dus voor de lijn.

"Entrée" moet worden geannonceerd als beide ballen voor de eerste keer 
in één verboden zone liggen. Ligt een van de aanspeelballen half op de 
lijn, dan wordt geacht, dat die bal in de zone ligt. De speler mag in 
die zone dan een carambole maken. Blijven de ballen vervolgens in die 
zone liggen, dan volgt de positie "Dedans". Wordt echter één van de 
ballen uit die zone gespeeld en keert er daarna weer in terug, dan 
ontstaat opnieuw de positie "Entree".

"Dedans" moet ook door de arbiter worden geannonceerd. Het is de positie 
ná entrée als beide aan te spelen ballen in de verboden zone zijn blijven 
liggen. De speler mag nu nog één carambole in die verboden zone maken. 
Bij het maken van die carambole moét een van de aanspeelballen uit die 
verboden zone gespeeld worden.
(NB. Uiteraard mag de bal daarna wel weer in die verboden zone terugkeren 
 en ontstaat de positie "Entree" weer).

"Resté dedans" is de positie ná dedans. De beide aanspeelballen zijn ná 
de carambole bij de "Dedans"-positie in de verboden zone blijven liggen.
Dit is een speelfout en de arbiter moet de speler dus aftellen. 
Hij annonceert:" Noteren 2, de heer/mevrouw X, 2".
De laatste carambole telt niet mee.
"""

class UitspringenLibre(HelpWindow):
    def __init__(self, master=None):
        super().__init__(
            title="Uitspringen libre",
            content=self._inhoud(),
            master=master
        )

    def _inhoud(self):
        return """Uitspringen bij libre en bandstoten

Dit is een speelfout, dus de desbetreffende speler wordt afgeteld 
met de annonce: "Noteren enz." Vervolgens worden de ballen nadat ze 
schoongemaakt zijn in de beginpositie gelegd, waarbij de speelbal 
van de volgende speler op het rechter of op verzoek van de speler 
op het linker acquit wordt gelegd.
"""

class VastliggenLibre(HelpWindow):
    def __init__(self, master=None):
        super().__init__(
            title="Vastliggende ballen libre",
            content=self._inhoud(),
            master=master
        )

    def _inhoud(self):
        return """Vastliggende ballen bij libre en bandstoten

Vastliggende bal(len) bij libre-klein
De arbiter zal "Vast" annonceren en de speler heeft de volgende 
keuzemogelijkheden:

1. De ballen in de beginpositie laten leggen door de arbiter;
2. Spelen via de niet vastliggende bal of via een of meer andere 
   banden dan de vastliggende band;
3. Losspelen van zijn speelbal via een "kopstoot".
"""

class HetBandstotenSpel(HelpWindow):
    def __init__(self, master=None):
        super().__init__(
            title="Het Bandstoten-spel",
            content=self._inhoud(),
            master=master
        )

    def _inhoud(self):
        return """Het bandstoten

Bij het bandstoten is een carambole geldig, als voldaan is aan 
de regels voor het libre en als de speelbal, voordat de 3e bal 
is geraakt, tenminste één band heeft geraakt.

Er zijn geen verboden zones bij het bandstoten.

Een uitspringende bal (is een speelfout) en vastliggende 
bal(len) worden op dezelfde manier afgewikkeld als bij
het libre.
"""

class Het3bandenSpel(HelpWindow):
    def __init__(self, master=None):
        super().__init__(
            title="Het driebanden-spel",
            content=self._inhoud(),
            master=master
        )

    def _inhoud(self):
        return """Het driebanden
    
Bij het driebanden is een carambole geldig, als voldaan is aan 
de regels voor het libre en als de speelbal, en voordat de 3e 
bal is geraakt, de speelbal tenminste drie maal een band heeft 
geraakt. Het mag meerdere malen dezelfde band zijn.

Er zijn geen verboden zones bij het driebanden.
"""

class Het3bandenUitspringen(HelpWindow):
    def __init__(self, master=None):
        super().__init__(
            title="Uitspringen driebanden",
            content=self._inhoud(),
            master=master
        )

    def _inhoud(self):
        return """Uitspringen bij driebanden
    
Als bij het driebanden een bal uitspringt wordt de speler afgeteld 
en de uitgesprongen bal, nadat deze is schoongemaakt, geplaatst op 
het voor die bal geldende acquit en wel als volgt:

a. de rode bal op het bovenacquit;
b. de oude speelbal op het middenacquit;
c. de nieuwe speelbal op het benedenacquit.

Indien het voor de uitgesprongen bal aangewezen acquit bezet is of 
versperd wordt, dan wordt die bal geplaatst op het acquit van de bal 
welke het acquit verspert.
"""

class Het3bandenVastliggen(HelpWindow):
    def __init__(self, master=None):
        super().__init__(
            title="Vastliggen driebanden",
            content=self._inhoud(),
            master=master
        )

    def _inhoud(self):
        return """Vastliggen met driebanden
    
Bij driebanden heeft de speler bij vastliggende ballen de volgende 
keuze mogelijkheden:

1. Spelen via de niet vastliggende bal of via een of meer andere banden 
   dan de vastliggende band;
2. Losspelen van zijn speelbal via een "kopstoot";
3. Het op de acquits laten leggen van de speelbal en de vastliggende bal. 
   Eventueel alle ballen, als de speelbal tegen beide andere ballen 
   vastligt en wel als volgt:
      a. de rode bal op het bovenacquit
      b. de speelbal op het benedenacquit
      c. de andere bal op het middenacquit

Indien het voor de vastliggende bal aangewezen acquit bezet is of 
versperd wordt, dan wordt die bal geplaatst op het acquit van de 
bal die het acquit verspert.
"""
