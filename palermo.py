from playsound import playsound
from gtts import gTTS
import platform
import random
import json
import os



data_file = "vocabulary.json"

def load_data():
    if os.path.exists(data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("błąd pliku. ładuję bazę domyślną.")

    """ w razie W jakby json padl """
    from vocabulary import last_words
    return last_words

def save_data(data):
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"\n postęp zapisany w {data_file} ")

def choose_mode():
    list_of_modes = ["PL_to_IT","IT_to_PL","gap_filling"]
    while True:
        mode = input("WYBIERZ TRYB: \n1 - z PL na IT, \n2 - z IT na PL, \n3 - Uzupełnianie zdań\n\n")
        if mode in ["1","2","3"]:
            return list_of_modes[int(mode) - 1]
        else:
            print("--- BŁĄD! ---")

def get_hint(word_dict, attempts, lang):
    word = word_dict[lang]

    reveal_max = (len(word) - 1) // 2
    reveal_count = min(attempts + 1, reveal_max)
    if reveal_count > 0:
        hint = f"{word[:reveal_count]}...{word[-reveal_count:]}"
    else:
        hint = f"{word[0]}..."

    print(f" Podpowiedź: {hint} ({len(word)} liter)")


def main():
    vocabulary = load_data()
    session_list = vocabulary.copy()
    random.shuffle(session_list)

    print("=== WŁOSKI NAUKA wersja 1.1 ===")
    mode = choose_mode()
    print("komendy: 'q' - wyjdź, 'h' - podpowiedź, 's' - pomiń")

    for entry in session_list:
        attempts = 0
        if mode == "PL_to_IT":
            print(f"\nsłowo po polsku: {entry['pl']}")
            question_word = entry["pl"]
            target_answer = entry["it"]
            lang_answer = "it"
            lang_tts = "pl"
            tts = gTTS(text=question_word, lang=lang_tts)
        elif mode == "IT_to_PL":
            print(f"\nsłowo po włosku: {entry['it']}")
            question_word = entry["it"]
            target_answer = entry["pl"]
            lang_answer = "pl"
            lang_tts = "it"
            tts = gTTS(text=question_word, lang=lang_tts)
        elif mode == "gap_filling":
            if "sentence_it" not in entry: continue

            target_answer = entry["it"]
            sentence_full = entry["sentence_it"]
            sentence_hidden = sentence_full.replace(target_answer, "____").replace(target_answer.capitalize(), "____")

            print(f"\nZdanie po polsku: {entry['sentence_pl']}")
            print(f"Uzupełnij lukę:   {sentence_hidden}")

            question_word = sentence_hidden
            lang_answer = "it"
            tts = gTTS(text=sentence_full, lang=lang_answer)

        tts.save("wymowa.mp3")

        # Sprawdzamy system operacyjny
        if platform.system() == "Linux":
            # Na Linuxie używamy sprawdzonego mpg123
            os.system("mpg123 -q wymowa.mp3 > /dev/null 2>&1")
        else:
            # Na Windowsie/reszcie używamy playsound
            from playsound import playsound
            playsound("wymowa.mp3")

        while attempts < 3:
            user_input = input("Oznacza to?: ").strip().lower()

            if user_input in ["q", "quit", "wyjdz"]:
                save_data(vocabulary)
                return

            if user_input == target_answer:
                entry["lvl"] += 1
                print(f" brawo! poziom słówka '{target_answer}': {entry['lvl']} ")
                break

            elif user_input in ["h", "hint"]:
                get_hint(entry, attempts, lang_answer)
                """ podpowiedz nie jest bledem jbc"""
                continue

            elif user_input in ["s", "skip", "nwm"]:
                print(f" prawidłowa odpowiedź: '{target_answer}' ")
                break

            else:
                attempts += 1
                if attempts < 3:
                    print(f" błąd ({attempts}/3). spróbuj ponownie! ")
                else:
                    print(f" koniec prób. '{question_word}' oznacza: '{target_answer}' ")

    save_data(vocabulary)
    print("gratulacje. przerobiłeś całą dzisiejszą listę.")

if __name__ == "__main__":
    main()