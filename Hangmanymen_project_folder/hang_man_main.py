import random
import json 
import os

# This gets the directory where your script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
RULES_PATH = os.path.join(SCRIPT_DIR, "rules.txt")
WORD_LISTS_PATH = os.path.join(SCRIPT_DIR, "word_lists.json")

def load_rules():
    try:
        with open(RULES_PATH) as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: Rules file not found at {RULES_PATH}")
        return "Game rules file not found. Try to guess the word letter by letter or guess the entire word at once before the hangman is complete!"

# Load rules at startup
rules = load_rules()

def load_word_lists():
    """Load word lists from JSON file with better error handling"""
    # Default word lists in case file loading fails
    default_lists = {
        "easy_words": ["card", "star", "tree", "game", "milk"],
        "medium_words": ["bicycle", "dancing", "sunrise", "rainbow", "diamond"],
        "hard_words": ["elephant", "computer", "sunshine", "calendar", "butterfly"],
        "custom_words": []
    }
    
    try:
        # Print the path we're trying to open (for debugging)
        print(f"Trying to open word lists from: {WORD_LISTS_PATH}")
        
        with open(WORD_LISTS_PATH, 'r') as file:
            data = json.load(file)
            
        print("Successfully loaded word lists JSON")
        
        # Handle different possible JSON structures
        if "all_words" in data:
            return data["all_words"]
        elif "word_lists" in data:
            return data["word_lists"]
        else:
            # Check if it's a direct dictionary with our expected keys
            if "easy_words" in data:
                return data
            else:
                print("Warning: JSON format doesn't match expected structure")
                return default_lists
                
    except FileNotFoundError:
        print(f"Word lists file not found at {WORD_LISTS_PATH}")
        print("Creating a new word lists file with default values")
        
        # Create the file with default values
        try:
            with open(WORD_LISTS_PATH, 'w') as file:
                json.dump({"word_lists": default_lists}, file, indent=2)
        except Exception as e:
            print(f"Error creating word lists file: {e}")
            
        return default_lists
        
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Error parsing word lists JSON: {e}")
        return default_lists

def save_word_lists(all_words):
    """Save word lists to JSON file with proper path handling"""
    try:
        # Print the path we're saving to (for debugging)
        print(f"Saving word lists to: {WORD_LISTS_PATH}")
        
        with open(WORD_LISTS_PATH, 'w') as file:
            # Maintain the same structure as when we loaded it
            json.dump({"word_lists": all_words}, file, indent=2)
            
        print("Word lists saved successfully")
    except Exception as e:
        print(f"Error saving word lists: {e}")

def difficulty(all_words):
    """Choose difficulty level and handle custom words"""
    difficulty = input("Please choose a difficulty easy, medium, hard, custom (e, m, h, c): ").lower()
    
    if difficulty == "e":
        word_list = all_words["easy_words"]
    elif difficulty == "m":
        word_list = all_words["medium_words"]
    elif difficulty == "h":
        word_list = all_words["hard_words"]
    elif difficulty == "c":
        # Custom mode chosen
        if all_words["custom_words"]:  # Check if custom list has words
            print("Your custom word list contains:", all_words["custom_words"])
            
            # Ask if user wants to clear the list
            clear_list = input("Would you like to clear your custom word list? (y/n): ").lower()
            if clear_list == "y":
                all_words["custom_words"] = []
                print("Custom word list has been cleared.")
                
                # Save the updated list with the correct path
                save_word_lists(all_words)
        else:
            print("Your custom word list is currently empty.")
        
        # Ask if user wants to add words
        add_words = input("Would you like to add words to your custom list? (y/n): ").lower()
        
        if add_words == "y":
            while True:
                new_word = input("Enter a word to add (or type 'done' to finish): ").lower()
                if new_word == "done":
                    break
                elif new_word == "":
                    print("Please enter a valid word.")
                elif new_word in all_words["custom_words"]:
                    print(f"'{new_word}' is already in your custom list.")
                else:
                    all_words["custom_words"].append(new_word)
                    print(f"Added '{new_word}' to your custom list.")
            
            # Show the current custom word list
            print("Your custom word list now contains:", all_words["custom_words"])
            
            # Save with the correct path
            save_word_lists(all_words)
        
        word_list = all_words["custom_words"]
    else:
        print("That's not an option")
        return None  # Return None for invalid input
    
    # Check if the selected list is empty
    if not word_list:
        print("The selected word list is empty. Please choose another difficulty or add words to custom.")
        return None
    
    return word_list  # Return the selected word list

def choose_word(word_list):
    return random.choice(word_list)

def display_word(word, guessed_letters):
    """Display the word with underscores for letters not yet guessed"""
    displayed = ""
    for letter in word:
        if letter in guessed_letters:
            displayed += letter + " "
        else:
            displayed += "_ "
    return displayed.strip()

def count_hidden_letters(word, guessed_letters):
    """Count the number of letters that haven't been guessed yet"""
    hidden_count = 0
    for letter in word:
        if letter not in guessed_letters:
            hidden_count += 1
    return hidden_count

def get_hint_letter(word, guessed_letters):
    """Find a letter in the word that hasn't been guessed yet"""
    unguessed_letters = [letter for letter in word if letter not in guessed_letters]
    
    if unguessed_letters:
        # Choose a random letter from the unguessed letters
        return random.choice(unguessed_letters)
    else:
        return None  # All letters have been guessed already

def display_hangman(wrong_guesses):
    """Display ASCII art for hangman based on wrong guesses"""
    stages = [
        """
           -----
           |   |
               |
               |
               |
               |
        """,
        """
           -----
           |   |
           O   |
               |
               |
               |
        """,
        """
           -----
           |   |
           O   |
           |   |
               |
               |
        """,
        """
           -----
           |   |
           O   |
          /|   |
               |
               |
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
               |
               |
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          /    |
               |
        """,
        """
           -----
           |   |
           O   |
          /|\\  |
          / \\  |
               |
        """
    ]
    
    return stages[min(wrong_guesses, len(stages) - 1)]
    
def main():
    print("Welcome to Hangman!")
    print("-------------------")
    
    while True:
        print("\nMenu Options:")
        print("1. View Rules")
        print("2. Play Game")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            # Display rules
            print("\n--- GAME RULES ---")
            print(rules)
            input("Press Enter to continue...")
            
        elif choice == "2":
            # Play the game
            all_words = load_word_lists()
            word_list = difficulty(all_words)
            
            if word_list and len(word_list) > 0:
                word = choose_word(word_list)
                guessed_letters = []
                wrong_guesses = 0
                max_wrong_guesses = 6
                word_attempts = []  # Track whole word guesses
                hint_used = False   # Track if hint has been used
                
                # Initialize score
                score = 100
                
                print("Starting score: 100 points")
                
                while wrong_guesses < max_wrong_guesses:
                    # Clear screen (using multiple newlines)
                    print("\n" * 2)
                    
                    print(display_hangman(wrong_guesses))
                    print("\nCurrent word:", display_word(word, guessed_letters))
                    print("Guessed letters:", ", ".join(guessed_letters) if guessed_letters else "None")
                    if word_attempts:
                        print("Word attempts:", ", ".join(word_attempts))
                    print(f"Wrong guesses: {wrong_guesses}/{max_wrong_guesses}")
                    print(f"Current score: {score}")
                    
                    # Check if player has won by guessing all letters
                    if all(letter in guessed_letters for letter in word):
                        print("\nCongratulations! You've guessed the word:", word)
                        print(f"Final score: {score}")
                        break
                    
                    # Offer hint when 3 lives remaining (after 3 wrong guesses) and hint not used yet
                    if wrong_guesses == 3 and not hint_used:
                        print("\n*** You have 3 lives remaining! Would you like a hint? ***")
                        hint_choice = input("Take a hint? This will reveal a letter but cost 5 points. (y/n): ").lower()
                        
                        if hint_choice == 'y':
                            hint_letter = get_hint_letter(word, guessed_letters)
                            
                            if hint_letter:
                                # Add the hint letter to guessed letters
                                guessed_letters.append(hint_letter)
                                hint_used = True
                                score -= 5  # Small penalty for using hint
                                
                                print(f"\nHINT: The letter '{hint_letter}' is in the word!")
                                print("Updated word:", display_word(word, guessed_letters))
                                print(f"-5 points for using hint. Current score: {score}")
                                input("Press Enter to continue...")
                                continue  # Skip to next iteration to redraw the game state
                            else:
                                print("No hint available - you've already guessed most letters!")
                    
                    # Get player's guess
                    guess = input("\nGuess a letter or the whole word: ").lower()
                    
                    # Empty input handling
                    if not guess:
                        print("Please enter a letter or word.")
                        continue
                        
                    # Check if it's a whole word guess or a single letter
                    if len(guess) > 1:
                        # It's a whole word guess!
                        if guess in word_attempts:
                            print("You've already tried that word.")
                            continue
                            
                        word_attempts.append(guess)
                        
                        if guess == word:
                            # Correct word guess!
                            # Calculate bonus points for remaining hidden letters
                            hidden_letters = count_hidden_letters(word, guessed_letters)
                            bonus_points = hidden_letters * 10
                            score += bonus_points
                            
                            print("\nCongratulations! You've guessed the word correctly:", word)
                            print(f"You earned {bonus_points} bonus points for guessing {hidden_letters} hidden letters!")
                            print(f"Final score: {score}")
                            break
                        else:
                            # Wrong word guess
                            wrong_guesses += 1
                            score -= 10  # Penalty for wrong guess
                            print(f"'{guess}' is not the correct word. {max_wrong_guesses - wrong_guesses} attempts remaining.")
                            print(f"-10 points! Current score: {score}")
                            
                            if wrong_guesses >= max_wrong_guesses:
                                print(display_hangman(wrong_guesses))
                                print("\nGame Over! You lost.")
                                print(f"The word was: {word}")
                                print("Your final score is set to 0.")
                                score = 0
                    else:
                        # Single letter guess
                        if not guess.isalpha():
                            print("Please enter a valid letter or word.")
                            continue
                            
                        if guess in guessed_letters:
                            print("You've already guessed that letter.")
                            continue
                        
                        guessed_letters.append(guess)
                        
                        if guess in word:
                            # Correct letter guess
                            occurrences = word.count(guess)
                            points_earned = 10  # 10 points per correct guess
                            score += points_earned
                            print(f"Good guess! The letter '{guess}' appears in the word.")
                            print(f"+{points_earned} points! Current score: {score}")
                        else:
                            # Wrong letter guess
                            wrong_guesses += 1
                            score -= 10  # Penalty for wrong guess
                            print(f"Wrong guess! {max_wrong_guesses - wrong_guesses} attempts remaining.")
                            print(f"-10 points! Current score: {score}")
                            
                            if wrong_guesses >= max_wrong_guesses:
                                print(display_hangman(wrong_guesses))
                                print("\nGame Over! You lost.")
                                print(f"The word was: {word}")
                                print("Your score is set to 0.")
                                score = 0
                
                
                play_again = input("\nWould you like to play again? (y/n): ").lower()
                if play_again != "y":
                    print("Thanks for playing! Goodbye.")
                    # Exit the program instead of continuing to the main menu
                    break
            
        elif choice == "3":
            print("Thanks for playing! Goodbye.")
            break
            
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()