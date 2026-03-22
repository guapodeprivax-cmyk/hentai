import requests
import time
import random
import os

# 🔐 Secrets Replit
TOKEN = os.getenv("44d65a2b2fd2febf46c9062b48878f6b")
CHAT_ID = os.getenv("34851852")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=data)
    except:
        pass

def check_username(username):
    url = f"https://www.tiktok.com/@{username}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=5)

        if r.status_code == 200:
            return "❌ Pris"
        elif r.status_code == 404:
            return "✅ Disponible"
        else:
            return "⚠️ Erreur"
    except:
        return "⚠️ Erreur"

# 🔥 TA LISTE
words = [
"amour","passion","tendresse","attachement","desir","adoration","idylle","romantisme",
"seduction","flirt","emoi","ardeur","liaison","union","couple","relation","complicite",
"elan","devotion","coeur","sentiment","amitie","amant","amante","eros","romantique",
"epanouissement","fidelite","passionnel","jalousie","fusion","emotion","charme",
"attirance","romance","volupte",

"agression","abus","contrainte","coercition","viol","harcelement","assaut","trauma",
"agresseur","victime","penetration","violation","sexuel","delit","crime","intimite",
"honte","culpabilite","impuisance","peur","violence","crimes","attaque",

"sexualite","libido","orgasme","erection","excitation","erotisme","nudite","plaisir",
"sensualite","masturbation","rapport","coit","fellation","cunnilingus","sodomie",
"pratiques","sexe","erotique","fantasme","act","stimulation","jouissance","corps",

"emploi","metier","profession","carriere","fonction","poste","activite","tache",
"occupation","salaire","entreprise","responsabilite","performance","productivite",
"bureau","industrie","chantier","artisanat","competence","job","contrat","mission",

"organisme","physique","anatomie","chair","peau","muscles","os","squelette","organes",
"visage","mains","pieds","membres","posture","silhouette","forme","beaute","sante",
"souffle","respiration","toucher","sensations","douleur","cicatrices","mouvements",

"crime","delit","infraction","vol","cambriolage","meurtre","homicide","brigandage",
"banditisme","fraude","escroquerie","mafia","gang","criminel","justice","tribunal",
"policier","enquete","arrestation","prison","jugement","coupable",

"foi","croyance","spiritualite","divinite","dieu","culte","priere","eglise","mosquee",
"temple","synagogue","rituel","sacre","messe","doctrine","dogme","prophete",
"meditation","esprit","transcendance",

"damnation","souffrance","feu","tourment","torture","supplice","chatiment","tenebres",
"diable","satan","demon","desespoir","haine","colere","punition",

"bonheur","paix","joie","grace","harmonie","serenite","lumiere","eden",

"tristesse","melancolie","anxiete","solitude","detresse","pleurs","angoisse",

"mort","deces","cimetiere","funerailles","ame","extinction","tragedie",

"bondage","domination","soumission","sadisme","masochisme","fantasme",

"haine","discrimination","machisme","oppression","mepris"
]

# 🔥 Génération de usernames à partir de tes mots
def generate_usernames(words, n=4000):
    usernames = set()

    while len(usernames) < n:
        w1 = random.choice(words)
        w2 = random.choice(words)

        styles = [
            f"{w1}{w2}",
            f"{w1}_{w2}",
            f"{w1}{random.randint(10,9999)}",
            f"{w1}{w2}{random.randint(1,999)}",
        ]

        usernames.add(random.choice(styles))

    return list(usernames)

usernames = generate_usernames(words, 4000)

print(f"🚀 {len(usernames)} usernames générés\n")

# 🔁 Checker
for username in usernames:
    result = check_username(username)

    msg = f"{result} : {username}"
    print(msg)
    send_telegram(msg)

    time.sleep(random.uniform(0.9, 1.5))

print("\n✅ Terminé")
