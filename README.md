# **OT_Projekt_Oswald - Game Design Document - SK**

Na danom repozitáre sa nachádza implementácia prototypu hry v Pygame, ktorá je záverečným projektom predmetu Objektové Technológie.

**Autor**: Adrián Oswald

**Vybraná téma**: Four elements (štyri elementy)

---
## **1. Úvod**
Navrhnutá hra je vytvorená pre predmet Objektové technológie, s cieľom vytvorenia funkčného prototypu hry ako projektu ku skúške.  Vytvorená hra spĺňa požiadavky zadanej témy Four elements (štyri elementy). Hra má charakter hráč proti celému svetu, kde na hráča útočia príšery a jeho cieľom je prepracovať sa k cieľu a počas toho prežiť vlny nepriateľov.
### **1.1 Inšpirácia**

Hra má inšpiráciu v starých 8 bitových retro hrách, ako boli na konzoliach NES, s jednoduchým cieľom zabiť všetkých nepriateľov nachádzajúcich sa v jednom leveli.

### **1.2 Herný zážitok**
Cieľom hry je, aby sa hráč dostal na koniec levelu. K tomu potrebuje zabiť všetky vlny rôznych typov nepriateľov patriacich pod element zo spawnerov. Hráč v hre otvára truhly, v ktorých sa nachádza 1 typ elementárneho meča. Hráč zo začiatku nemá ihneď meč s elementom.
### **1.3 Vývojový softvér**
- **Pygame-CE**: zvolený programovací jazyk.
- **PyCharm 2024.3.2**: vybrané IDE.
- **Tiled 1.11.2**: grafický nástroj na vytváranie levelov.
- **Itch.io**: zdroj grafických assetov a zvukov do hry.

---
## **2. Koncept**

### **2.1 Prehľad hry**
Hráč ovláda svoju postavu a snaží sa dostať na koniec hry. Počas toho je jeho cesta zablokovaná a odomýka sa každým prežitím vĺn nepriateľov. Hráč pre zľahčenie postupu má po mape umiestnené truhly, v ktorých sa nachádza 1 meč s elementom. Na každého nepriateľa pôsobia elementy inak, napríklad ohnivý meč nepoškodzuje ohnivého slime.
### **2.2 Interpretácia témy (Four elements (štyri elementy))**
**"Four elements (štyri elementy)"** - Hráč bojuje proti 5 typov slimov, 4 typy majú element( Červený - Oheň, Modrý - Voda, Sivý/Biely - Vzduch, Zelený - Zem ) a 5 je slime bez elementu, taktiež má hráč k dispozícii 5 typov mečov. 4 typy mečov sú elementy a 1 je bez elementu.
### **2.3 Základné mechaniky**
- **Prekážky**: na mape sa nachádzajú objekty, ktoré tvoria aktívnu prekážku ako pre hráča, ak aj pre nepriateľov.
- **Healing potion**: hráč má určitú šancu na drop healing potionu z nepriateľa,
- **Pevne stanovené miesta generovania nepriateľov**: nepriateľia sa generujú na stanovených mestiach, pretože to patrí to gameplay loopu.
- **Hráč musí likvidovať nepriateľov**: hráč má k dispozícii 5 typov mečov. 1 základny bez elementu dostane na začiatku hry, a zvyšne 4 s elementami nájde v dalších truhlách rozmiestnených po mape.

### **2.4 Návrh tried**

#### **Herná logika a cyklus**
- **Game**: Riadi hlavnú hernú logiku, vykresľovanie, kolízie, nepriateľov, interakcie hráča, mapu, GUI, inventár a herný cyklus.
- **MainMenu**: Spravuje hlavnú ponuku, zobrazuje pozadie, tlačidlá a reaguje na vstupy.
- **TileMap**: Načítava a vykresľuje hernú mapu, vrátane terénu, objektov, nepriateľov, spawnerov a interaktívnych prvkov.
- **SlimeSpawner**: Spravuje spawnovanie Slimov v rôznych vlnách a oblastiach na základe časových intervalov.

#### **Postavy a nepriatelia**
- **Player**: Spravuje hráčovu postavu, pohyb, animácie, útoky a interakcie s predmetmi.
- **Entity**: Základná trieda pre všetky pohybujúce sa objekty v hre, vrátane nepriateľov.
- **Enemy**: Reprezentuje nepriateľa, zahŕňa jeho správanie, pohyb a vykreslenie.
- **Slime**: Základná trieda pre Slimov, definuje ich pohyb, hernú logiku a vykreslenie.
- **WaterSlime, FireSlime, EarthSlime, AirSlime**: Podtriedy Slime s vlastnosťami príslušného elementu.

#### **Predmety**
- **Item**: Základná trieda pre predmety, ktoré môže hráč zbierať a používať.
- **HealingPotion**: Liečivý predmet obnovujúci zdravie hráča.
- **Chest**: Predstavuje truhlu, ktorá po interakcii otvorí, priradí predmet hráčovi a prehrá zvuk.

#### **Meče**
- **Sword**: Základná trieda pre všetky typy mečov, ich hernú logiku a schopnosti.
- **BasicSword**: Základný meč bez špeciálnych efektov.
- **FireSword, WaterSword, EarthSword, AirSword**: Meče so špecifickými vlastnosťami a efektmi podľa elementu (poškodenie, špeciálne schopnosti).

#### **Grafika a vykresľovanie**
- **AllSprites**: Spravuje vykresľovanie všetkých herných objektov s dynamickým posunom kamery.
- **Sprite**: Trieda pre zobrazenie a umiestnenie objektu na obrazovke.
- **CollisionSprite**: Trieda pre objekt s kolíziou a umiestnením na obrazovke.
- **Slash**: Trieda pre animáciu a pohyb švihnutia meča.

#### **GUI a inventár**
- **GUI**: Zobrazuje herné rozhranie, zdravie, FPS a správu o predmetoch.
- **InventoryGUI**: Spravuje a vykresľuje inventár hráča s možnosťou výberu a vybavenia predmetov.

---

## **3. Grafika**

### **3.1 Interpretácia témy (Štyri elementy)**
Hra využíva vizuálne atraktívne assety z itch.io, kde nepriatelia sú reprezentovaní rôznymi typmi slimov, pričom každý typ má svoj element: Červený (Oheň), Modrý (Voda), Sivý/Biely (Vzduch), Zelený (Zem) a jeden bez elementu. Zameranie je na 2D sprite objekty s minimalistickými animáciami pohybu.

<p align="center">
  <img src="https://github.com/AdrianOswaldUKF/OT_Projekt_Adrian_Oswald/blob/main/slime.png?raw=true" alt="slime">
  <img src="https://github.com/AdrianOswaldUKF/OT_Projekt_Adrian_Oswald/blob/main/fire.png?raw=true" alt="fire slime">
  <img src="https://github.com/AdrianOswaldUKF/OT_Projekt_Adrian_Oswald/blob/main/water.png?raw=true" alt="water slime">
  <img src="https://github.com/AdrianOswaldUKF/OT_Projekt_Adrian_Oswald/blob/main/air.png?raw=true" alt="air slime">
  <img src="https://github.com/AdrianOswaldUKF/OT_Projekt_Adrian_Oswald/blob/main/earth.png?raw=true" alt="earth slime">
  <br>
  <em>Obrázok 3 Ukážka sprite-ov nepriateľov</em>
</p>

### **3.2 Dizajn**
V hre sú použité assety z itch.io, konkrétne z balíka *Peaceful Pixels: The Grassland, Tileset and Asset Pack 16x16* (https://schwarnhild.itch.io/peacefulpixels00) pre nepriateľov, a *Free RPG Tileset* (https://pixel-poem.itch.io/free-rpg-tileset) a *Volcanoe Tileset and Asset Pack 32x32 Pixels* (https://schwarnhild.itch.io/volcanoe-tileset-and-asset-pack-32x32-pixels) pre mapu. Cieľom bolo vytvoriť príjemný a vizuálne harmonický dizajn s rôznymi prostrediami, ktoré sa postupne kombinujú.

<p align="center">
  <img src="https://github.com/AdrianOswaldUKF/OT_Projekt_Adrian_Oswald/blob/main/level1.png?raw=true" alt="Level dizajn">
  <br>
  <em>Obrázok 4 Ukážka dizajnu levelu</em>
</p>

---

## **4. Zvuk**

### **4.1 Hudba**
Hudba v hlavnom menu a hre je od xDeviruchi: [16-Bit Fantasy & Adventure Music (2025)](https://xdeviruchi.itch.io/16-bit-fantasy-adventure-music-pack)
### **4.2 Zvuky**
Zvukové efekty v hre sú zamerané na 8 - 16 bitovú tému a pochádzajú z rôznych free zdrojov, najmä itch.io.
## **5. Herný zážitok**

### **5.1 Používateľské rozhranie**
Používateľské rozhranie je základne a obsahuje hlavné menu, inventár, HP bar a pause menu počas hry.

### **5.2 Ovládanie**
<ins>**Klávesnica**</ins>
- **WASD**: pohyb hráča po mape.
- **Klávesy šípok**: alternatívne ovládanie pohybu hráča po mape.
- **Space**: útok s mečom.
- **E**: otvoriť truhlu ( Hráč musí byť otočený správnym smerom k truhle ).
- **ESC**: pauza / menu.
- **F11**: fullscreen / windowed ( 800x600 ).
- **1, 2, 3, 4, 5**: výber mečov v inventári/toolbare.

<ins>**Myš**</ins> 
- **Ľavé tlačidlo**: výber meča v inventári/toolbare.


---
