""" In this project the guess game
is recast using a function """ 
import random
computers_number= random.randint(1,50)
prompt='What is your guessing? '
quit_program=-1
quit_text='q'
confirm_quit_message='Are you sure you want to quit(y/n)? '
def confirm_quit():
    confirm=input(confirm_quit_message)
    if confirm=='n':
        return False
    else:
        return True
def do_guess_round():
    """Choose a random number, ask the user for a guess check whether the guess is true
and repeat until the user is correct"""
    computers_number= random.randint(1,50) # Added
    number_of_guesses=0
    while True:
        players_guess=input(prompt)
        if players_guess==quit_text:
            if confirm_quit():
                return quit_program
            else:
                continue
        number_of_guesses=number_of_guesses+1
        if computers_number==int(players_guess):
            print("Correct! ")
            return number_of_guesses
        elif computers_number>int(players_guess):
            print("Too low!")
        else:
            print("Too high!")
total_rounds=0
total_guesses=0
while True:
    total_rounds=total_rounds+1
    print("Starting round number: " +str(total_rounds))
    this_round=do_guess_round()
    if this_round==quit_program:
        total_rounds=total_rounds-1
        avg=str(total_guesses/float(total_rounds))
        if total_rounds==0:
            stats_message='You completed no rounds. '+ ' Please try again later '
        else:
            stats_message='You played ' +str(total_rounds) + ' round, with an average of '+ str(avg)
        break
    total_guesses=total_guesses + this_round
    print("you took " +str(this_round)+" guesses")
    avg=str(total_guesses/float(total_rounds))
    print("Your guessing average= "+avg)
    print("") #blank line
print(stats_message)
