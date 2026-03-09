import random
import json
import os

data_file = "../vocabulary.json"

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

def get_hint(word_dict, attempts):
    pl_word = word_dict["pl"]

    if attempts == 0:
        hint = f"{pl_word[0]}...{pl_word[-1]}"
        print(f" podpowiedź: {hint} ({len(pl_word)} liter)")

    elif attempts == 1 and len(pl_word) > 4:
        hint = f"{pl_word[0]}{pl_word[1]}...{pl_word[-2]}{pl_word[-1]}"
        print(f" podpowiedź: {hint} ({len(pl_word)} liter)")

    elif attempts == 2 and len(pl_word) > 6:
        hint = f"{pl_word[0]}{pl_word[1]}{pl_word[2]}...{pl_word[-3]}{pl_word[-2]}{pl_word[-1]}"
        print(f" podpowiedź: {hint} ({len(pl_word)} liter)")


def main():
    vocabulary = load_data()
    session_list = vocabulary.copy()
    random.shuffle(session_list)

    print("=== WŁOSKI NAUKA wersja 1 ===")
    print("komendy: 'q' - wyjdź, 'h' - podpowiedź, 's' - pomiń")

    for entry in session_list:
        attempts = 0
        print(f"\nsłowo: {entry['it']}")

        while attempts < 3:
            user_input = input("po polsku to?: ").strip().lower()

            if user_input in ["q", "quit", "wyjdz"]:
                save_data(vocabulary)
                return

            if user_input == entry["pl"]:
                entry["lvl"] += 1
                entry["learned"] = True
                print(f" brawo! poziom słówka '{entry['it']}': {entry['lvl']} ")
                break

            elif user_input in ["h", "hint"]:
                get_hint(entry, attempts)
                """ podpowiedz nie jest bledem """
                continue

            elif user_input in ["s", "skip", "nwm"]:
                print(f" prawidłowa odpowiedź: '{entry['pl']}' ")
                break

            else:
                attempts += 1
                if attempts < 3:
                    print(f" błąd ({attempts}/3). spróbuj ponownie! ")
                else:
                    print(f" koniec prób. '{entry['it']}' oznacza: '{entry['pl']}' ")

    save_data(vocabulary)
    print("gratulacje. przerobiłeś całą dzisiejszą listę.")

if __name__ == "__main__":
    main()