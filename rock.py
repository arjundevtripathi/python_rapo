import random
user_wins = 0
computer_wins = 0

for num in range(1, 4):
    print(f"\n--- Round {num} ---")
    
    user = input("Choose [rock, paper, or scissors]: ")
    computer = random.choice(["rock", "paper", "scissors"])
    print("Computer chose:", computer)
    
    if user == computer:
        print("It's a tie!")
    elif user == "rock" and computer == "scissors":
        print("You win this round! Rock beats scissors.")
        user_wins += 1
    elif user == "paper" and computer == "rock":
        print("You win this round! Paper beats rock.")
        user_wins += 1
    elif user == "scissors" and computer == "paper":
        print("You win this round! Scissors beats paper.")
        user_wins += 1
    else:
        print("Computer wins this round!")
        computer_wins += 1

print("\n=== FINAL RESULT ===")
print(f"Your Score: {user_wins} | Computer Score: {computer_wins}")
if user_wins > computer_wins:
    print("Congratulations! You won the best of 3!")
elif computer_wins > user_wins:
    print("Computer wins the best of 3! Better luck next time.")
else:
    print("The overall match ended in a tie!")

