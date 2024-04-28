# THE CORE SIMULATION 

import random
from matplotlib import pyplot as plt
import numpy as np

class ShutTheBoxSimulation:
    def __init__(self):
        self.board = list(range(1, 10))  # Initialize the game board with numbers 1 to 12
        self.gameStatus = "Running"
        self.wins = 0
        self.losses = 0
        
    def plot_multiplots(self, win_rates, win_counts, sums_before_end):
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))

        # Plot Win Rate Over Time
        axes[0, 0].plot(range(1, len(win_rates) + 1), win_rates)
        axes[0, 0].set_title('Win Rate Over Time')
        axes[0, 0].set_xlabel('Games Played')
        axes[0, 0].set_ylabel('Win Rate (%)')
        axes[0, 0].grid(True)

        # Plot Wins vs. Losses Distribution
        labels = ['Wins', 'Losses']
        values = [self.wins, self.losses]
        axes[0, 1].bar(labels, values)
        axes[0, 1].set_title('Wins vs. Losses Distribution')
        axes[0, 1].set_xlabel('Outcome')
        axes[0, 1].set_ylabel('Count')

        # Plot Histogram of Game Wins
        axes[1, 0].hist(win_counts, bins=20, color='skyblue', edgecolor='black')
        axes[1, 0].set_title('Histogram of Game Wins')
        axes[1, 0].set_xlabel('Number of Wins')
        axes[1, 0].set_ylabel('Frequency')
        
        # Plot Histogram of Sums Before Game End
        counts, bin_edges = np.histogram(sums_before_end, bins=20)
        cdf = np.cumsum(counts)
        total_samples = len(sums_before_end)
        probabilities = counts / total_samples

        # Plotten der CDF
        fig, ax1 = plt.subplots(figsize=(8, 6))

        # Plot CDF
        ax1.plot(bin_edges[1:], cdf / total_samples, color='lightgreen', label='CDF')
        ax1.set_xlabel('Sum of Dice Rolls')
        ax1.set_ylabel('CDF', color='lightgreen')
        ax1.tick_params(axis='y', labelcolor='lightgreen')
        ax1.legend(loc='upper left')

        # Erstelle ein zweites Achsenobjekt für die Wahrscheinlichkeiten
        ax2 = ax1.twinx()
        ax2.plot(bin_edges[1:], probabilities, color='blue', label='Probability')
        ax2.set_ylabel('Probability', color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')
        ax2.legend(loc='upper right')


        # Adjust layout
        plt.tight_layout()

        plt.show()

    def roll_dice(self):
        return random.randint(1, 6), random.randint(1, 6)  # Roll two dice

    def flip_numbers(self, numbers):
            
        # rd_choice = random.choice(numbers)  # Zufällige Auswahl einer Kombination von Zahlen
        
        rd_choice = numbers[0]  # Auswahl der ersten Kombination von Zahlen
        
        if isinstance(rd_choice, int):  # Wenn nur eine einzelne Zahl ausgewählt wurde
            rd_choice = (rd_choice,)
            
        for number in rd_choice:  # Iteration über die ausgewählte Kombination
            if number in self.board:
                self.board.remove(number)   # Flip down the selected numbers
                
        if not self.board:  
            self.gameStatus = "Over"

    def play_turn(self):
        dice1, dice2 = self.roll_dice()  # Roll the dice
        total = dice1 + dice2
        remaining_numbers = sorted(self.board, reverse=True)
        
        numbers_to_flip = []
        for i, number1 in enumerate(remaining_numbers):
            for number2 in remaining_numbers[i:]:
                if number1 + number2 == total and number1!=number2:
                    numbers_to_flip.append((number1, number2))
                    break
                elif number1 == total:
                    numbers_to_flip.append((number1))
                    break
        
        if not numbers_to_flip:
            self.gameStatus = "Over"
            return total
        
        # print(numbers_to_flip)
        
        self.flip_numbers(numbers_to_flip)  # Flip the selected numbers
        
        return total

    def simulate_game(self):
        
        gameCount = 100000
        currentGame = 0
        
        win_rates = []
        win_counts = []
        sums_before_end = []
        
        
        while currentGame<gameCount:
            sum_before_end = 0
            
            currentGame += 1
            self.gameStatus = "Running"
            self.board = list(range(1, 10))
            while self.gameStatus == "Running":
                total = self.play_turn()
                if self.gameStatus == "Over":
                    break
                sum_before_end += total
                
            if not self.board:
                self.wins += 1
            else:
                self.losses += 1

            win_rates.append(self.wins / currentGame * 100)
            win_counts.append(self.wins)
            sums_before_end.append(sum_before_end)
            
            print("     Wins: " + str(self.wins)+" || Looses: " + str(self.losses)+ " || Total Games: " + str(gameCount)+ " || Win Rate: " + str(round(100*self.wins/(self.losses+self.wins),2))+"%", end='\r')
        print("     Wins: " + str(self.wins)+" || Looses: " + str(self.losses)+ " || Total Games: " + str(gameCount)+ " || Win Rate: " + str(round(100*self.wins/(self.losses+self.wins),2))+"%")

        self.plot_multiplots(win_rates, win_counts,sums_before_end)
        
        
        
if __name__ == "__main__":
    simulation = ShutTheBoxSimulation()
    simulation.simulate_game()