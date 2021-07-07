"""
CS50 Lab 6: Tournament
Simulate a sports tournament FIFA World Cup.
"""
import csv
import sys
import random
from collections import defaultdict

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage;
    if len(sys.argv) != 2:
        sys.exit(f"Usage: python {sys.argv[0]} FILENAME.csv")

    teams = []
    win_counts = defaultdict(int)

    # Read teams into memory from file;
    with open(sys.argv[1], "r") as ratings:
        reader = csv.DictReader(ratings)
        for dct in reader:
            dct["rating"] = int(dct["rating"])
            teams.append(dct)

    # Simulate N tournaments and keep track of win counts;
    for i in range(N):
        team_name = simulate_tournament(teams)
        win_counts[team_name] += 1

    # Print each team's chances of winning, according to simulation.
    for team in sorted(win_counts, key=lambda team: win_counts[team], reverse=True):
        chanses = win_counts[team] * 100 / N
        print(f"{team}: {chanses:.1f}% chance of winning")

    sys.exit(0)


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""

    while True:
        teams = simulate_round(teams)
        if len(teams) == 1:
            return teams[0]['team']


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""

    winners = []
    # Simulate games for all pairs of teams:
    for i in range(0, len(teams), 2):
        team1 = teams[i]
        team2 = teams[i + 1]
        if simulate_game(team1, team2):
            winners.append(team1)
        else:
            winners.append(team2)

    return winners


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""

    rating1 = team1["rating"]
    rating2 = team2["rating"]

    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))

    return random.random() < probability


if __name__ == "__main__":
    main()
