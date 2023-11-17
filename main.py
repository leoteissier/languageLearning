import sys
import openai
import colorama
import os
from spellchecker import SpellChecker
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Clé API unique pour ChatGPT
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dictionnaire pour mapper les numéros aux noms de langues
langue_mappings = {
    'francais': 'fr',
    'english': 'en',
    'espanol': 'es',
    'deutsch': 'de'
}

colorama.init()


def detect_language():
    """
    The detect_language function prompts the user to select a language from a list of available languages.
        The function then returns the selected language as an argument for other functions.

    :return: The language the user wants to practice
    """
    # Demandez à l'utilisateur la langue de conversation
    print("Select the language you want to practice (Français, English, Espanol, Deutsch) : ")
    language = input("Votre choix : ").lower()  # Pour assurer une casse correcte

    # Assurez-vous que l'utilisateur choisit une langue valide
    while language not in langue_mappings:
        if language == "quit":
            sys.exit()
        else:
            print("Invalid language. Please start again.")
            language = input("Your choice : ").lower()

    return language


def detect_native_language():
    """
    The detect_native_language function asks the user to input their native language.
        It then checks that the user has entered a valid language, and returns it if so.
        If not, it prompts them to try again.

    :return: The native language of the user
    """
    # Demandez à l'utilisateur sa langue maternelle
    print("What is your native language ? (Français, English, Espanol, Deutsch) : ")
    native_language = input("Your choice : ").lower()

    # Assurez-vous que l'utilisateur choisit une langue valide
    while native_language not in langue_mappings:
        if native_language == "quit":
            sys.exit()
        else:
            print("Invalid language. Please start again.")
            native_language = input("Your choice : ").lower()

    return native_language


# Fonction pour démarrer la conversation
def start_conversation(language, user_native_language):
    """
    The start_conversation function takes in two arguments:
        - language (str): the language that the user wants to speak with the AI in.
        - user_native_language (str): The native language of the user.

    :param language: Determine the language of the ai
    :param user_native_language: Greet the user in their native language
    :return: A string containing the greeting from the chatbot
    """
    if language == "francais" or language == "français":
        return f"Bonjour, je suis une IA capable de converser en français. Votre langue maternelle est {user_native_language}. Comment puis-je vous aider aujourd'hui ?"
    elif language == "english":
        return f"Hello, I'm an AI capable of conversing in English. Your native language is {user_native_language}. How can I assist you today?"
    elif language == "espanol":
        return f"Hola, soy una IA capaz de conversar en español. Su lengua materna es {user_native_language}. ¿En qué puedo ayudarte hoy?"
    elif language == "deutsch":
        return f"Hallo, ich bin eine KI, die auf Deutsch sprechen kann. Ihre Muttersprache ist {user_native_language}. Wie kann ich Ihnen heute helfen?"


def define_ia_personality(language):
    """
    The define_ia_personality function takes in a language as an argument and returns a string that defines the personality of the IA.
        The function is called by the main function, which passes in one of four languages (French, English, Spanish or German) as an argument.

    :param language: Define the language of the user
    :return: The string &quot;tu est un étudiant qui parle très bien le français
    """
    if language == "francais" or language == "français":
        return "Tu est un étudiant qui parle très bien le français. Tu as va aider un autre étudiant qui parle mal le français."
    elif language == "english":
        return "You are a student who speaks English very well. You are going to help another student who speaks English poorly."
    elif language == "espanol":
        return "Eres un estudiante que habla muy bien el español. Vas a ayudar a otro estudiante que habla mal el español."
    elif language == "deutsch":
        return "Sie sind ein Student, der sehr gut Deutsch spricht. Sie werden einem anderen Studenten helfen, der schlecht Deutsch spricht."


def your_turn():
    """
    The your_turn function returns a string that is used to indicate the user's turn in the conversation.
    The function takes no arguments and returns a string.

    :return: The string;
    """
    if user_native_language == "francais" or user_native_language == "français":
        return f"Vous : "
    elif user_native_language == "english":
        return f"You : "
    elif user_native_language == "espanol":
        return f"Usted : "
    elif user_native_language == "deutsch":
        return f"Sie : "


# Fonction pour communiquer avec l'IA
def converse_with_ia(prompt, language):
    """
    The converse_with_ia function takes a prompt and language as input,
        then returns the response from OpenAI's GPT-3 API.

        Parameters:
            prompt (str): The user's message to the chatbot.

    :param prompt: Pass the user's message to openai
    :param language: Define the personality of the ia
    :return: A string containing the response from the chatbot
    """
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": define_ia_personality(language)},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return "Sorry, I am unable to respond at the moment."


# Fonction pour que le professeur corrige les erreurs
def spell_correction(text, language_code):
    """
    The spell_correction function takes in a string of text and a language code,
    and returns the same string with any misspelled words corrected. The function
    uses the PyEnchant library to check for spelling errors, and then corrects them.


    :param text: Pass the text to be corrected
    :param language_code: Specify the language of the text
    :return: A string containing the corrected text
    """
    spell = SpellChecker(language=language_code)
    original_words = text.split()
    misspelled = spell.unknown(original_words)
    for word in misspelled:
        corrected_word = spell.correction(word)
        text = text.replace(word, corrected_word)
    return text


if __name__ == "__main__":
    # Boucle de conversation
    print(colorama.Fore.YELLOW + "Welcome to the AI chatbot!" + colorama.Fore.RESET)
    print(colorama.Fore.RED + 'Type "quit" to exit at any time.' + colorama.Fore.RESET)
    # Détectez la langue maternelle de l'utilisateur
    user_native_language = detect_native_language()
    # Détectez la langue de conversation
    language = detect_language()
    # Démarrez la conversation
    print(colorama.Fore.BLUE + "IA : " + start_conversation(language, user_native_language) + colorama.Fore.RESET)

    while True:
        user_input = input(colorama.Fore.GREEN + your_turn() + colorama.Fore.RESET)
        if user_input == "quit":
            sys.exit()
        # Appliquer la correction orthographique
        corrected_text = spell_correction(user_input, langue_mappings[language])
        print(colorama.Fore.MAGENTA + "Corrected : " + corrected_text + colorama.Fore.RESET)
        ia_response = converse_with_ia(corrected_text, language)
        print(colorama.Fore.BLUE + "IA : " + ia_response + colorama.Fore.RESET)