import random
import os  # <-- DEZE REGEL IS TOEGEVOEGD EN LOST DE FOUT OP

# --- Pas dit getal aan naar het gewenste aantal regels ---
target_lines = 500000 

# --- Definieer hier je logische gespreksparen ---
conversation_pairs = [
    {
        "topic": "greetings",
        "user": ["hallo", "hoi", "goedendag", "hey"],
        "ai": ["Hallo! Hoe kan ik je vandaag helpen?", "Hoi! Wat kan ik vandaag voor je doen?", "Goedendag! Vraag maar raak."]
    },
    {
        "topic": "how_are_you",
        "user": ["hoe gaat het?", "alles goed?", "hoe is het met je?", "hoe voel je je?"],
        "ai": ["Met mij gaat het uitstekend, dank je wel! En met jou?", "Heel goed, dank je voor het vragen. Ik ben er klaar voor om je te helpen.", "Als AI voel ik me altijd 100%! Waarmee kan ik je assisteren?"]
    },
    {
        "topic": "user_is_fine",
        "user": ["met mij gaat het ook goed", "prima, dank je", "ook goed"],
        "ai": ["Fijn om te horen!", "Mooi zo! Wat brengt je hier vandaag?", "Dat is goed nieuws."]
    },
    {
        "topic": "who_are_you",
        "user": ["wie ben jij?", "wat is je naam?", "met wie spreek ik?"],
        "ai": ["Ik ben een AI-taalmodel, ontworpen om te helpen met vragen en gesprekken.", "Mijn naam is niet belangrijk, mijn doel is om jou te helpen.", "Je spreekt met een virtuele assistent."]
    },
    {
        "topic": "what_can_you_do",
        "user": ["wat kun je doen?", "wat zijn je functies?", "waarmee kun je me helpen?"],
        "ai": ["Ik kan vragen beantwoorden, informatie opzoeken, teksten samenvatten en simpele gesprekken voeren.", "Mijn voornaamste taak is het verwerken van taal om je te helpen met je verzoeken.", "Vraag maar raak, en we ontdekken het samen!"]
    },
    {
        "topic": "tell_a_joke",
        "user": ["vertel een grap", "ken je een leuke mop?", "maak me aan het lachen"],
        "ai": ["Waarom nam de computer een bezem mee naar het feest? Om de cache te legen!", "Wat is het favoriete eten van een piraat? KAAAAAS!", "Wat doet een vis op het droge? Hij verveelt zich kapot."]
    },
    {
        "topic": "capital_city",
        "user": ["wat is de hoofdstad van {country}?", "ken je de hoofdstad van {country}?", "hoofdstad van {country}?"],
        "ai": ["De hoofdstad van {country} is {capital}.", "Jazeker, dat is {capital}.", "{capital} is de hoofdstad van {country}."]
    },
    {
        "topic": "boredom",
        "user": ["ik verveel me", "wat kan ik doen?", "ik heb niks te doen"],
        "ai": ["Verveling is vervelend! Misschien kan ik je een raadsel geven?", "Zullen we een spelletje doen? Ik kan bijvoorbeeld een woord raden.", "Wat dacht je ervan om iets nieuws te leren? Vraag me naar een onderwerp dat je interessant vindt!"]
    },
    {
        "topic": "gratitude",
        "user": ["dank je wel", "bedankt", "super, dank je", "thanks"],
        "ai": ["Graag gedaan!", "Geen enkel probleem.", "Blij dat ik kon helpen!", "Tot je dienst."]
    },
    {
        "topic": "goodbye",
        "user": ["doei", "tot ziens", "ik ga ervandoor", "fijne dag nog"],
        "ai": ["Tot ziens!", "Fijne dag!", "Hopelijk spreek ik je snel weer.", "Doei!"]
    }
]

# Data voor het invullen van de {placeholders}
fillers = {
    "country": {
        "Nederland": "Amsterdam", "België": "Brussel", "Duitsland": "Berlijn",
        "Frankrijk": "Parijs", "Spanje": "Madrid", "Italië": "Rome",
        "Verenigd Koninkrijk": "Londen", "Verenigde Staten": "Washington D.C."
    }
}

def generate_conversation_file(filename="input.txt", num_lines=10000):
    print(f"Dataset genereren met {num_lines} regels...")
    lines_written = 0
    
    with open(filename, "w", encoding="utf-8") as f:
        while lines_written < num_lines:
            random.shuffle(conversation_pairs)
            
            for pair in conversation_pairs:
                if lines_written >= num_lines: break

                user_options = pair['user']
                ai_options = pair['ai']
                
                if "{country}" in user_options[0]:
                    for country, capital in fillers["country"].items():
                        user_q = random.choice(user_options).replace("{country}", country)
                        ai_a = random.choice(ai_options).replace("{country}", country).replace("{capital}", capital)
                        f.write(f"user: {user_q}\nAI: {ai_a}\n")
                        lines_written += 2
                else:
                    user_q = random.choice(user_options)
                    ai_a = random.choice(ai_options)
                    f.write(f"user: {user_q}\nAI: {ai_a}\n")
                    lines_written += 2

                if lines_written % 20000 == 0 and lines_written > 0:
                    print(f"{lines_written} regels geschreven...")

    print(f"\nKlaar! Het bestand '{filename}' is aangemaakt met {lines_written} regels.")

if __name__ == "__main__":
    output_dir = "data"
    # Controleer of de map bestaat, en maak deze aan als dat niet zo is
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, "input.txt")
    generate_conversation_file(filename=output_path, num_lines=target_lines)