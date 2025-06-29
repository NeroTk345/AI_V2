import random

# --- Pas dit getal aan naar het gewenste aantal regels ---
# 500.000 regels = 250.000 'user'/'AI' paren
target_lines = 500000 

# --- Voeg hier meer templates toe voor meer variatie ---

# Templates voor vragen en opmerkingen van de gebruiker
user_templates = [
    "hoe gaat het?",
    "wat is je naam?",
    "wie ben jij?",
    "wat kun je allemaal?",
    "vertel me een grap over {subject}",
    "kun je me helpen met {topic}?",
    "wat is de hoofdstad van {country}?",
    "ik voel me {emotion}",
    "wat weet je over {concept}?",
    "leg uit wat {term} is",
    "heb je hobby's?",
    "wat is je favoriete {thing}?",
    "ik heb een vraag",
    "kun je een rijmwoord voor {word} vinden?",
    "wat is de zin van het leven?",
    "vertel iets interessants",
    "ik verveel me",
    "hoe werkt {technology}?",
]

# Templates voor antwoorden van de AI
ai_templates = [
    "Met mij gaat het goed, dank je wel. Hoe kan ik je van dienst zijn?",
    "Ik ben een behulpzame AI-assistent.",
    "Mijn doel is om je te helpen met informatie en gesprekken.",
    "Ik kan vragen beantwoorden, grappen vertellen en nog veel meer. Wat wil je proberen?",
    "Zeker! Hier is een grap over {subject}: {joke}",
    "Natuurlijk kan ik je helpen met {topic}. Wat is je specifieke vraag?",
    "De hoofdstad van {country} is {capital}.",
    "Het spijt me te horen dat je je {emotion} voelt. Kan ik iets doen om je op te vrolijken?",
    "{concept} is een fascinerend onderwerp. Het omvat {explanation}.",
    "{term} kan worden omschreven als {definition}.",
    "Als AI heb ik geen hobby's zoals mensen, maar ik geniet ervan om te leren en te helpen!",
    "Ik heb geen persoonlijke voorkeuren, maar ik kan je wel vertellen wat populair is op het gebied van {thing}.",
    "Stel je vraag gerust, ik zal mijn best doen om een antwoord te vinden.",
    "Een woord dat rijmt op {word} is {rhyme}.",
    "Dat is een diepe vraag. Velen geloven dat het doel is om gelukkig en betekenisvol te zijn.",
    "Wist je dat octopussen drie harten hebben?",
    "Laten we een spelletje doen! Denk aan een getal tussen 1 en 100.",
    "{technology} is gebaseerd op het principe van {tech_principle}.",
]

# Woorden om in de templates te vullen voor variatie
subjects = {
    "subject": ["computers", "dieren", "eten", "wetenschap"],
    "topic": ["huiswerk", "programmeren", "koken", "reizen"],
    "country": ["Nederland", "België", "Duitsland", "Frankrijk", "Spanje"],
    "emotion": ["blij", "verdrietig", "boos", "verveeld"],
    "concept": ["zwaartekracht", "fotosynthese", "kunstmatige intelligentie"],
    "term": ["een variabele", "een algoritme", "de cloud"],
    "thing": ["kleur", "eten", "film", "boek"],
    "word": ["huis", "muis", "kat", "hond"],
    "technology": ["het internet", "bluetooth", "GPS"]
}

# Specifieke data voor de templates
jokes_map = {
    "computers": "Waarom was de computer koud? Hij had zijn Windows open laten staan!",
    "dieren": "Wat zegt de ene vis tegen de andere? 'Haai!'",
    "eten": "Wat is geel en hangt achter een auto? Een banaanhangwagen.",
    "wetenschap": "Twee atomen lopen op straat. Zegt de een: 'Ik ben mijn elektron kwijt!' Vraagt de ander: 'Weet je het zeker?' 'Ja,' zegt de eerste, 'ik ben positief geladen!'"
}

capitals_map = {
    "Nederland": "Amsterdam",
    "België": "Brussel",
    "Duitsland": "Berlijn",
    "Frankrijk": "Parijs",
    "Spanje": "Madrid"
}

explanations_map = {
    "zwaartekracht": "de aantrekkingskracht die objecten met massa op elkaar uitoefenen.",
    "fotosynthese": "het proces waarbij planten lichtenergie gebruiken om kooldioxide en water om te zetten in zuurstof en glucose.",
    "kunstmatige intelligentie": "het vermogen van een machine om mensachtige intelligentie te vertonen, zoals leren en problemen oplossen."
}

definitions_map = {
    "een variabele": "een container in code om data tijdelijk op te slaan.",
    "een algoritme": "een stapsgewijze procedure om een probleem op te lossen.",
    "de cloud": "een netwerk van servers die diensten via het internet aanbieden."
}

rhymes_map = {
    "huis": "pluis",
    "muis": "buis",
    "kat": "mat",
    "hond": "mond"
}

tech_principles_map = {
    "het internet": "het wereldwijd verbinden van computernetwerken.",
    "bluetooth": "draadloze communicatie over korte afstanden.",
    "GPS": "het bepalen van een positie op aarde met behulp van satellieten."
}

def generate_line(template, fillers):
    """Vult een template met willekeurige woorden."""
    line = template
    for key, values in fillers.items():
        placeholder = "{" + key + "}"
        if placeholder in line:
            # Specifieke data maps gebruiken indien beschikbaar
            if key == 'country':
                country = random.choice(values)
                line = line.replace(placeholder, country).replace("{capital}", capitals_map[country])
            elif key == 'subject':
                subject = random.choice(values)
                line = line.replace(placeholder, subject).replace("{joke}", jokes_map[subject])
            elif key == 'concept':
                concept = random.choice(values)
                line = line.replace(placeholder, concept).replace("{explanation}", explanations_map[concept])
            elif key == 'term':
                term = random.choice(values)
                line = line.replace(placeholder, term).replace("{definition}", definitions_map[term])
            elif key == 'word':
                word = random.choice(values)
                line = line.replace(placeholder, word).replace("{rhyme}", rhymes_map[word])
            elif key == 'technology':
                tech = random.choice(values)
                line = line.replace(placeholder, tech).replace("{tech_principle}", tech_principles_map[tech])
            else:
                line = line.replace(placeholder, random.choice(values))
    return line

# --- Hoofdlogica om het bestand te schrijven ---
print(f"Dataset genereren met {target_lines} regels...")

with open("input.txt", "w", encoding="utf-8") as f:
    for i in range(target_lines // 2):
        # Kies een willekeurig paar templates
        user_template = random.choice(user_templates)
        ai_template = random.choice(ai_templates)

        # Genereer de user- en AI-regels
        user_line = generate_line(user_template, subjects)
        ai_line = generate_line(ai_template, subjects)

        # Schrijf naar het bestand, zorg ervoor dat het logisch is (niet alle combinaties zijn perfect)
        f.write(f"user: {user_line}\n")
        f.write(f"AI: {ai_line}\n")
        
        # Voortgangsindicator
        if (i + 1) % 10000 == 0:
            print(f"{(i + 1) * 2} regels geschreven...")

print("Dataset genereren voltooid! Het bestand 'input.txt' is aangemaakt.")