import argparse
import sys


class FlashCard:
    def __init__(self, term, definition, mistakes):
        self.term = term
        self.definition = definition
        self.mistakes = mistakes

    def print_card(self):
        print(f"Card:\n{self.term}")
        print(f"Definition:\n{self.definition}")

    def save_card(self):
        return f"{self.term}-{self.definition}-{self.mistakes}\n"

    def check_definition(self, definition):
        if definition == self.definition:
            return True
        else:
            return False

    def get_term(self, definition):
        if definition == self.definition:
            return self.term
        else:
            return False


class FlashDeck:
    def __init__(self):
        self.deck = dict()
        self.card_index = 0

    def add_card(self, flashcard):
        self.card_index += 1
        self.deck[self.card_index] = flashcard

    def remove_card_term(self, term):
        for card in self.deck:
            if self.deck[card].term == term:
                self.deck.pop(card)
                return True
        return False

    def get_card(self, card_number):
        return self.deck[card_number]

    def term_exists(self, term):
        for card in self.deck:
            if self.deck[card].term == term:
                return True
        return False

    def definition_exists(self, definition):
        for card in self.deck:
            if self.deck[card].definition == definition:
                return True
        return False

    def get_card_term(self, definition):
        for card in self.deck:
            if self.deck[card].definition == definition:
                return self.deck[card].term
        return False

    def update_card_term(self, term, definition, mistakes):
        for card in self.deck:
            if self.deck[card].term == term:
                self.deck[card].definition = definition
                self.deck[card].mistakes = mistakes
                return True
        return False


def receive_user_action():
    while True:
        text = input()
        logger.append(text)
        if text == "add" or text == "remove" or text == "import" \
                or text == "export" or text == "ask" or text == "exit" \
                or text == "log" or text == "hardest card" or "reset stats":
            return text
        else:
            func_message = "Wrong action, try again"
            print(func_message)
            logger.append(func_message)


def process_user_input(text, deck):
    if text == "add":
        add_action(deck)
    elif text == "remove":
        remove_action(deck)
    elif text == "import":
        import_action(deck)
    elif text == "export":
        export_action(deck)
    elif text == "ask":
        ask_action(deck)
    elif text == "exit":
        exit_action(deck, export_to)
    elif text == "log":
        log_action()
    elif text == "hardest card":
        hardest_card_action(deck)
    elif text == "reset stats":
        reset_stats_action(deck)
    else:
        return False


def add_action(deck):
    func_input = "The card:"
    print(func_input)
    logger.append(func_input)
    while True:
        term_to_add = input()
        logger.append(term_to_add)
        if deck.term_exists(term_to_add):
            func_message = f"The card \"{term_to_add}\" already exists. Try again:"
            print(func_message)
            logger.append(func_message)
        else:
            break

    func_input = "The definition of the card:"
    print(func_input)
    logger.append(func_input)
    while True:
        def_to_add = input()
        logger.append(def_to_add)
        if deck.definition_exists(def_to_add):
            func_message = f"The definition \"{def_to_add}\" already exists. Try again:"
            print(func_message)
            logger.append(func_message)
        else:
            break

    deck.add_card(FlashCard(term_to_add, def_to_add, 0))
    func_message = f"The pair (\"{term_to_add}\":\"{def_to_add}\") has been added.\n"  # ERASE THE \n IF NOT NEEDED
    print(func_message)
    logger.append(func_message)

    return deck


def remove_action(deck):
    func_input = "Which card?"
    print(func_input)
    logger.append(func_input)
    term_to_remove = input()
    logger.append(term_to_remove)
    if deck.remove_card_term(term_to_remove):
        func_message = "The card has been removed.\n"
    else:
        func_message = f"Can't remove \"{term_to_remove}\": there is no such card.\n"

    print(func_message)
    logger.append(func_message)

    return deck


# Assumption - the format of the file
# is always the same, with a "-" as sep
def import_action(deck, input_file=None):
    if input_file is not None:
        file_name = str(input_file)
    else:
        func_input = "File name:"
        print(func_input)
        logger.append(func_input)
        file_name = input()
        logger.append(file_name)

    try:
        with open(file_name, "r") as f:
            imported_cards = f.readlines()
            for card in imported_cards:
                words = card.split(sep="-", maxsplit=2)
                term_to_import = words[0]
                def_to_import = words[1]  # hardcoded -1 to remove the \n
                mistakes_to_import = int(words[2][:-1])

                if not deck.update_card_term(term_to_import, def_to_import, mistakes_to_import):
                    deck.add_card(FlashCard(term_to_import, def_to_import, mistakes_to_import))

        func_message = f"{len(imported_cards)} cards have been loaded\n"
        print(func_message)
        logger.append(func_message)
    except FileNotFoundError:
        func_message = "File not found\n"
        print(func_message)
        logger.append(func_message)

    return deck


def export_action(deck, export_file=None):
    if export_file is not None:
        file_name = str(export_file)
    else:
        func_input = "File name:"
        print(func_input)
        logger.append(func_input)
        file_name = input()
        logger.append(file_name)

    with open(file_name, "w") as f:
        for card_key in deck.deck:
            f.write(deck.deck[card_key].save_card())

        func_message = f"{len(deck.deck)} cards have been saved\n"
        print(func_message)
        logger.append(func_message)
    return deck


def ask_action(deck):
    func_message = "How many times to ask?"
    print(func_message)
    logger.append(func_message)
    n_questions = int(input())
    logger.append(str(n_questions))
    questions_answered = 0
    while questions_answered < n_questions:
        for card_key in deck.deck:
            func_input = f"Print the definition of \"{deck.deck[card_key].term}\":"
            print(func_input)
            logger.append(func_input)
            guess_definition = input()
            logger.append(guess_definition)

            if deck.deck[card_key].check_definition(guess_definition):
                func_message = "Correct!"
            elif deck.definition_exists(guess_definition):
                deck.deck[card_key].mistakes += 1
                func_message = f"Wrong. The  right answer is \"{deck.deck[card_key].definition}\", but your definition is correct for \"{deck.get_card_term(guess_definition)}\"."
            else:
                deck.deck[card_key].mistakes += 1
                func_message = f"Wrong. The  right answer is \"{deck.deck[card_key].definition}\"."

            print(func_message)
            logger.append(func_message)

            questions_answered += 1
            if questions_answered == n_questions:
                break

    print()
    logger.append("")

    return deck


# does not need to be logged
def exit_action(deck, export_file):
    print("Bye bye!")
    if export_file is not None:
        export_action(deck, export_file)
    sys.exit()


def log_action():
    func_input = "File name:"
    print(func_input)
    logger.append(func_input)
    file_name = input()
    logger.append(file_name)
    func_message = "The log has been saved"
    logger.append(func_message)
    with open(file_name, "w") as f:
        f.writelines(log + "\n" for log in logger)
    print(func_message)


def hardest_card_action(deck):
    max_mistakes = 0
    hardest_term = []
    for card_key in deck.deck:
        if deck.deck[card_key].mistakes > max_mistakes:
            max_mistakes = deck.deck[card_key].mistakes

    if max_mistakes == 0:
        func_message = "There are no cards with errors.\n"
    else:
        for card_key in deck.deck:
            if deck.deck[card_key].mistakes == max_mistakes:
                hardest_term.append(deck.deck[card_key].term)

        if len(hardest_term) == 1:
            func_message = f"The hardest card is \"{hardest_term[0]}\". You have {max_mistakes} errors answering it.\n"
        else:
            func_message = f"The hardest cards are"
            for i in range(len(hardest_term)):
                func_message += " \"" + hardest_term[i] + "\","
            func_message = func_message[:-1]  # remove the last comma
            func_message += f". You have {max_mistakes} errors answering them\n"

    print(func_message)
    logger.append(func_message)

    return deck


def reset_stats_action(deck):
    for card_key in deck.deck:
        deck.deck[card_key].mistakes = 0
    func_message = "Card statistics have been reset.\n"
    print(func_message)
    logger.append(func_message)
    return deck


# Program start
flash_deck = FlashDeck()
# ad-hoc logger
logger = list([])
# parser
parser = argparse.ArgumentParser()
parser.add_argument("--import_from")
parser.add_argument("--export_to")
args = parser.parse_args()
export_to = None

if args.import_from is not None:
    import_action(flash_deck, args.import_from)
if args.export_to is not None:
    export_to = args.export_to

while True:
    message = "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):"
    print(message)
    logger.append(message)
    user_action = receive_user_action()
    process_user_input(user_action, flash_deck)
