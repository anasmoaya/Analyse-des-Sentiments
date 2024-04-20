import xml.etree.ElementTree as ET
import nltk
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize

# Téléchargement des ressources nécessaires de NLTK
nltk.download('sentiwordnet')
nltk.download('wordnet')
nltk.download('punkt')

def get_sentiwordnet_score(word):
    synsets = wn.synsets(word, pos=wn.ADJ)  # Focus sur les adjectifs
    if not synsets:
        return 0  # Retourne un score neutre si aucun synset trouvé

    synset = synsets[0]  # Utilisation du premier synset
    swn_synset = swn.senti_synset(synset.name())
    return swn_synset.pos_score() - swn_synset.neg_score()

def load_data_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []
    for sentence in root.findall('.//sentence'):
        text = sentence.find('text').text
        aspects = []
        for aspect_term in sentence.findall('.//aspectTerm'):
            aspects.append({
                'term': aspect_term.get('term'),
                'polarity': aspect_term.get('polarity'),
                'from': int(aspect_term.get('from')),
                'to': int(aspect_term.get('to'))
            })
        data.append({'text': text, 'aspects': aspects})
    return data

def evaluate_algorithm(file_path, senti_dict):
    data = load_data_from_xml(file_path)
    correct = 0
    total = 0
    for item in data:
        text = item['text']
        tokens = word_tokenize(text.lower())
        for aspect in item['aspects']:
            aspect_tokens = word_tokenize(aspect['term'].lower())
            if aspect_tokens[0] in tokens:
                aspect_index = tokens.index(aspect_tokens[0])
                start = max(0, aspect_index - 3)
                end = min(len(tokens), aspect_index + 3)
                context = tokens[start:end]
                score = sum(get_sentiwordnet_score(word) for word in context)
                predicted_polarity = 'neutral'
                if score > 0:
                    predicted_polarity = 'positive'
                elif score < 0:
                    predicted_polarity = 'negative'
                
                if predicted_polarity == aspect['polarity']:
                    correct += 1
                total += 1
    accuracy = (correct / total) * 100 if total > 0 else 0
    return accuracy
f
# Utilisation des fichiers Gold pour évaluation
accuracy = evaluate_algorithm('Laptop_Test_Gold.xml', get_sentiwordnet_score)
print(f"Accuracy: {accuracy:.2f}%")
