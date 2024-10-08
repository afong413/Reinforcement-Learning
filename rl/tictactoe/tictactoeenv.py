from termcolor import colored

from ..environment import Environment
from ..bot import Bot
from .tictactoebot import TicTacToeBot
from .human import Human


class TicTacToeEnv(Environment):  # MARK: TicTacToeEnv
    """An environment designed for TicTacToe."""

    def __init__(self):
        self.starting_state = [None] * 9

    def get_valid_states(
        self, current_state: list[str], agent: TicTacToeBot | Human
    ) -> list[list[str]]:
        """Gets valid states for given agent using their `symbol`."""
        valid_states = []

        for i in range(9):
            if current_state[i] is None:
                valid_state = current_state.copy()
                valid_state[i] = agent.symbol
                valid_states.append(valid_state)

        return valid_states

    def evaluate_state(self, state: list[str]) -> str | bool:
        """Checks for winners or if there's a tie."""
        winning_methods = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),
            (0, 4, 8),
            (2, 4, 6),
        ]

        for winning_method in winning_methods:
            if (
                state[winning_method[0]]
                == state[winning_method[1]]
                == state[winning_method[2]]
                != None
            ):
                return state[winning_method[0]]

        if None in state:
            return True

        return False

    def display_state(self, state, symbols):
        """
        Uses `termcolor` to make the board look fancy on the console.
        """
        for i in range(3):
            for j in range(3):
                if state[3 * i + j] == symbols[0]:
                    print(
                        colored(f" { symbols[0] } ", "red", attrs=["bold"]),
                        end="",
                    )
                elif state[3 * i + j] == symbols[1]:
                    print(
                        colored(f" { symbols[1] } ", "white", attrs=["bold"]),
                        end="",
                    )
                else:
                    print(colored(f" {3 * i + j + 1} ", "blue"), end="")
                if j < 2:
                    print(colored("|", "blue"), end="")
            print()
            if i < 2:
                print(colored("---+---+---", "blue"))

    def game(
        self,
        agent1: TicTacToeBot | Human,
        agent2: TicTacToeBot | Human,
        reward=False,
        display=True,
    ):
        """
        Plays the game! Once again this is basically`Environment.game`,
        except this one prints a whole bunch of stuff to the console.
        (That is when `display!=False`!)
        """
        agents = [agent1, agent2]

        state = self.starting_state

        agent_turn = False

        outcome = self.evaluate_state(state)

        # Empty board

        if display:
            print()
            self.display_state(state, [agents[0].symbol, agents[1].symbol])
            print()

        while outcome is True:  # While game still going
            # Get possible moves
            valid_states = self.get_valid_states(state, agents[agent_turn])

            if display:
                print(f"{agents[agent_turn].name}'s turn!")

            # Get agent move
            state = agents[agent_turn].get_action(state, valid_states, display)

            # Switch whose turn it is
            agent_turn = not agent_turn

            # Check if the game ended
            outcome = self.evaluate_state(state)

            if display:
                print()
                self.display_state(state, [agents[0].symbol, agents[1].symbol])
                print()

        if display:
            if outcome == agents[0].symbol:
                print(f"{agents[0].name} wins!")
            elif outcome == agents[1].symbol:
                print(f"{agents[1].name} wins!")
            else:
                print("Its a tie!")
            print()

        # Train the agents
        if reward:
            for agent in agents:
                if isinstance(agent, Bot):
                    agent.distribute_reward(outcome)

        return outcome
