# RebornBy187bot

Un bot Telegram complet pentru marketplace cu selleri, produse și locații (sectoarele Bucureștiului), cu gamificare (XP, ranking, grade), sistem referral trackabil, clasament, suport, tutoriale și navigație cu butoane.

## Funcționalități

### Pentru Utilizatori
- **Marketplace**: Navigare după locații (sectoare) sau produse
- **Selleri**: Index complet cu filtrare și căutare
- **Referral**: Sistem de invitații cu link-uri trackabile
- **Gamificare**: XP, ranking-uri și grade
- **Clasament**: Leaderboard cu multiple perioade
- **Suport**: Contact direct cu staff-ul
- **Tutoriale**: Ghiduri complete pentru utilizare

### Pentru Selleri
- Apariție automată în toate listele relevante
- Chat direct cu clienții
- Sistem de reputație
- Mapare produse și locații

### Pentru Admini
- Gestionare completă selleri, produse, locații
- Acordare rank-uri și grade
- Confirmare comenzi
- Lansare giveaway-uri și lottery

## Instalare

1. Clonează repository-ul:
```bash
git clone <repository-url>
cd rebornby187bot
```

2. Instalează dependențele:
```bash
pip install -r requirements.txt
```

3. Configurează environment:
```bash
cp .env.example .env
# Editează .env cu datele tale
```

4. Rulează bot-ul:
```bash
python bot.py
```

## Configurare

Editează fișierul `.env`:

```
BOT_TOKEN=your_bot_token_here
OWNER_ID=your_telegram_user_id
GROUP_ID=your_group_chat_id
DB_URL=sqlite:///./data/reborn.db
```

## Structura Proiectului

```
rebornby187bot/
├── bot.py                 # Fișierul principal
├── config.py             # Configurări
├── requirements.txt      # Dependențe
├── handlers/            # Handler-e pentru comenzi
├── services/           # Servicii business logic
├── models/            # Modele bază de date
├── keyboards/         # Tastaturi inline
├── utils/            # Utilitare
└── data/            # Baza de date SQLite
```

## Comenzi Disponibile

### Utilizatori
- `/start` - Meniu principal
- `/help` - Ajutor pe roluri
- `/profil` - Vezi profilul tău
- `/info @user` - Vezi profilul unui user
- `/market` - Accesează marketplace-ul
- `/selleri` - Index selleri
- `/link` - Generează link referral
- `/clasament` - Leaderboard
- `/ranking` - Vezi progresul tău

### Admini
- `/add_seller @user` - Adaugă seller
- `/set_location @user <sector>` - Setează locația
- `/set_product @user <prod1,prod2>` - Setează produse
- `/give_rank @user <nivel>` - Acordă rank
- `/confirm_order <txn_id>` - Confirmă comandă

## Gamificare

### XP (Experience Points)
- +100 XP pentru fiecare referral calificat
- +10 XP săptămânal pentru vechime
- +25 XP pentru fiecare comandă confirmată
- +100 XP pentru verificare FULL

### Ranking-uri
- **Începător** (0 referali)
- **Inițiat** (15+ referali)
- **Aspirant** (20+ referali)
- **Support** (25+ referali)
- **Connector** (50+ referali)
- **Hustler (VIP)** (100+ referali)

### Grade (acordate manual)
- El Patron
- TheArchitect
- TrustSeller
- Runner (Droper)
- Admin
- Support
- Seller
- Staff

## Produse Disponibile

- Bob Marley
- Maroc
- Need For Speed
- Power Horse
- SnowMan
- Breaking Bag (2M, 3M, 4M)
- Berlin Calling
- Alice in Wonderland
- Albert Hoffman
- Big Pharma

## Locații

- Sector 1 - Sector 6 (București)

## Contribuții

Pentru contribuții, te rugăm să:
1. Faci fork la repository
2. Creezi o branch pentru feature-ul tău
3. Faci commit cu modificările
4. Deschizi un Pull Request

## Licență

Acest proiect este licențiat sub MIT License.

