import random
import streamlit as st

# Set up the web page title and description
st.title("🪨 📄 ✂️ Rock, Paper, Scissors")
st.subheader("Best of 3 Match")

# Initialize session state variables to remember data across clicks
if "user_wins" not in st.session_state:
    st.session_state.user_wins = 0
if "computer_wins" not in st.session_state:
    st.session_state.computer_wins = 0
if "round_num" not in st.session_state:
    st.session_state.round_num = 1
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "history" not in st.session_state:
    st.session_state.history = []


# Function to reset the game state
def reset_game():
    st.session_state.user_wins = 0
    st.session_state.computer_wins = 0
    st.session_state.round_num = 1
    st.session_state.game_over = False
    st.session_state.history = []


# Game interface logic
if not st.session_state.game_over:
    st.markdown(f"### 🎯 Round **{st.session_state.round_num}** of 3")

    # Dropdown menu for the user's move selection
    user_choice = st.selectbox(
        "Make your move:", ["Select...", "rock", "paper", "scissors"]
    )

    # Trigger action when user clicks the Play button
    if st.button("Play Round") and user_choice != "Select...":
        computer_choice = random.choice(["rock", "paper", "scissors"])

        # Game rules checking
        if user_choice == computer_choice:
            result_text = f"Round {st.session_state.round_num}: It's a tie! Both chose {user_choice}."
        elif (
            (user_choice == "rock" and computer_choice == "scissors")
            or (user_choice == "paper" and computer_choice == "rock")
            or (user_choice == "scissors" and computer_choice == "paper")
        ):
            result_text = f"Round {st.session_state.round_num}: You win! {user_choice.capitalize()} beats {computer_choice}."
            st.session_state.user_wins += 1
        else:
            result_text = f"Round {st.session_state.round_num}: Computer wins! {computer_choice.capitalize()} beats {user_choice}."
            st.session_state.computer_wins += 1

        # Save this round's message to the text history log
        st.session_state.history.append(result_text)

        # Check if the 3-round series is now finished
        if st.session_state.round_num >= 3:
            st.session_state.game_over = True
        else:
            st.session_state.round_num += 1

        # Force a quick rerun to immediately update the visual scoreboard layout
        st.rerun()

# Display the ongoing scoreboard layout on the screen
st.write("---")
col1, col2 = st.columns(2)
col1.metric("Your Score", st.session_state.user_wins)
col2.metric("Computer Score", st.session_state.computer_wins)

# Print out the text history logs from earlier rounds
if st.session_state.history:
    st.write("#### Round Logs:")
    for log in st.session_state.history:
        st.write(log)

# Handle final match outcomes after 3 full rounds conclude
if st.session_state.game_over:
    st.write("---")
    st.write("### 🏆 FINAL RESULT 🏆")

    if st.session_state.user_wins > st.session_state.computer_wins:
        st.success("Congratulations! You won the best of 3!")
    elif st.session_state.computer_wins > st.session_state.user_wins:
        st.error("Computer wins the best of 3! Better luck next time.")
    else:
        st.warning("The overall match ended in a tie!")

    # Button to quickly wipe scores and start fresh
    if st.button("Play Again 🔄"):
        reset_game()
        st.rerun()
