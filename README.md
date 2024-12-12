# Knight's Problem

## Problem Description

The Knight's Problem is a puzzle where, for a given initial and target chessboard configuration with knights placed on it, it returns a sequence of moves that lead to the solution in the minimum number of moves, if a solution exists.

The input parameters are two strings: the first string represents the initial configuration on the chessboard, and the second string represents the target configuration. From these input parameters, we get information about the dimensions of the chessboard, so we will label the positions on the chessboard with numbers from 0 to n, in our case, from 0 to 11. In this puzzle, knights are placed on the chessboard, chess pieces that move in an "L" shape. There are a total of twelve positions that need to be connected in a way that reflects how the knight moves across the chessboard. The positions marked with numbers will be shown as vertices, and the edges will represent the connection between two positions. We will create a dictionary where the keys are vertices, and the values are sets of vertices incident to the key vertex.

![Alt text](images/knight_problem.png)
### Figure 2.1 Initial and Target State on the Chessboard

![Alt text](images/graph_example.png)
### Figure 2.2 Numbered Positions and Graph of Connected Positions

In Figure 2.2, a table with positions and the graph showing the connection of positions is displayed. From the image, we can see how each knight can move. For example, the black knight at position 0 can move to position 7 or position 5, as long as those positions are free. Figure 2.1 shows a visualization of the initial and target chessboards. The output of the problem will be a sequence of moves that lead to the solution in the minimum number of moves.

In a case where we start, for example, with the black knight at position 2 and move it to position 3, the next move cannot be to return the knight to the previous position. Therefore, the idea for solving the problem will be to avoid revisiting any position more than once.
