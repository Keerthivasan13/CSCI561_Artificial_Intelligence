# AI-CSCI561
Programs developed for CSCI561 Foundations of Artificial Intelligence course taught by Prof. Laurent Itti

**Language:** Python

## 1. Search 
**Mars Exploration mission path finder**  
Given the topographical map of the mission site with Z value assigned to each cell identifying the elevation of the planet, the Program moves the rover optimally from its landing site to all of its target locations for experiments.

**Approaches:** Breadth First Search, Uniform Cost Search, A\* Search  

## 2. Game Playing using Minimax
 **Halma Game playing agent**  
Designed a Game Playing agent for Halma, a version of Chinese checkers, using Minimax algorithm. The game consists of Black and White pawns located at the opposite ends of a square board. Pawns can move one step or two steps or even jump over the adjacent pawns for any number of times. Modified Minimax to suit the time-restricted environment and used Alpha-beta pruning to reduce the branching factor significantly.

**Configuration:** Dynamic depth control (Max: 2 Ply or 3 Depth)  
**Evalution Function:** Combination of Euclidean distances  
**Result:** Agent came in the top 7th of 750 students in the AI Tournament sponsored by Google  

## 3. First Order Logic
 **Logic Resolution Engine**  
Implemented a First Order Logic Resolution engine for sentences after converting to CNF form. Used Backward chaining with unification of sentences, including variable to variable unification.

**Algorithms implemeted:** Unification, Resolution
