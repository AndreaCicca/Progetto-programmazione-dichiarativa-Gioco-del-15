import sys
from typing import Optional, Sequence, cast

from clingo.symbol import Number, SymbolType
from clingo.solving import Model, SolveResult
from clingo.control import Control
from clingo.application import clingo_main, Application

class EightPuzzleApp(Application):
    '''
    Multi-shot solving application for the 8-puzzle problem.
    '''
    program_name: str = "8-puzzle-solver"
    version: str = "1.0"
    _solution_steps: Optional[int]

    def __init__(self):
        self._solution_steps = None

    def _on_model(self, model: Model):
        '''
        Callback to process each found model and track solution length.
        '''
        # Count the number of times goal_reached is true
        goal_reached_count = sum(
            1 for atom in model.symbols(atoms=True) 
            if atom.name == "goal_reached"
        )
        
        if goal_reached_count > 0:
            # Find the minimum step where goal is reached
            goal_steps = [
                atom.arguments[0].number 
                for atom in model.symbols(atoms=True) 
                if atom.name == "goal_reached"
            ]
            self._solution_steps = min(goal_steps)
            print(f"Found solution with {self._solution_steps} steps")

    def main(self, ctl: Control, files: Sequence[str]):
        '''
        Main function implementing multi-shot solving for 8-puzzle.
        '''
        # Load the ASP program
        if not files:
            files = ["-"]
        for file_ in files:
            ctl.load(file_)
        
        # Add a constraint to limit the number of steps
        ctl.add("bound", ["b"], 
                ":- goal_reached(T), T >= b.")

        # Ground the base program
        ctl.ground([("base", [])])

        # Multi-shot solving with increasing step bound
        current_max_steps = 30  # Maximum steps to try
        while current_max_steps > 0:
            # Ground the bound part with current max steps
            ctl.ground([("bound", [Number(current_max_steps)])])

            # Solve and check for satisfiability
            solve_result = cast(SolveResult, ctl.solve(on_model=self._on_model))
            
            # If a solution is found, we're done
            if solve_result.satisfiable and self._solution_steps is not None:
                print(f"Optimal solution found in {self._solution_steps} steps")
                break
            
            # Reduce the max steps if no solution found
            current_max_steps -= 1

        # If no solution found after all attempts
        if self._solution_steps is None:
            print("No solution found within the given step bounds")

# Run the application
clingo_main(EightPuzzleApp(), sys.argv[1:])