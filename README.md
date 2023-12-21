<h1>Conway's Game Of Life </h1>

<h2> About Program </h2>

<p>
In the 1970s, a British mathematician named John Conway devised a cellular automata,
demonstrating that complex structures and patterns can emerge from a very basic set 
of rules coupled with a particular initial state of the simulation. Since the creation
of the Game of Life, many game enthusiasts have recognized interesting patters that
have the capacity to act similarly to living forms as they move through the grid,
reproduce, interact with one another, ect. Herein documented program aims to enable user
interaction with Conway's Game of Life and explore the behavior of unique patterns via
a GUI, allowing the user to store newly discovered structures. 
</p>

<h2> Game Rules </h2>

<p> 
1. Every cell is either <i>alive</i> or <i>dead</i>. <br/>
2. If a dead cell in surrounded by exactly 3 living cells, it is born (becomes alive).<br/> 
3. A living cell remains alive if it is surrounded by 2 or 3 other living cells. <br/>
4. If a living cell is surrounded by less than 2 or more than 3 living cells, it dies. <br/>
</p>

<h2> How To Run Game</h2>

The game implementation can be run through the <i>Main()</i> method found in the <i>Main</i> class
in compilation with command line arguments indicating the dimensions of the game grid: <br/>

- <b>"-height"</b> is followed by the integer value corresponding to desired amount of rows (default of 30) <br/>
- <b>"-width"</b> is followed by the integer value corresponding to desired amount of columns (default of 50) <br/>

<h4> Examples:</h4>
<p>
<b>"-height 40 -width 60"</b>: will generate a 40 x 60 game grid <br/>
<b>" "</b>: will generate a 30 x 50 game grid <br/>
</p>

<h2> Game Features</h2>
<h3> Changing Color</h3>
<p>
Users can change the color of the grid between 3 various coloring styles (<i>Light</i>, <i>Dark</i>,
and <i>No Grid</i>) by navigating to the <i><b>View Mode</b></i> menu:<br/>

<img src="src/Resources/Game Demo Images/Coloring Change Menu.png" width="800"><br/>
<img src="src/Resources/Game Demo Images/Coloring Change Result.png" width="800"><br/>

</p>

<h3> Generating Patterns From the Library </h3>
<p>
Users can generate previously saved patterns by navigating to the <i><b>Generate</b></i> menu:<br/>

<img src="src/Resources/Game Demo Images/Structure Generation Menu.png" width="800"><br/>
<img src="src/Resources/Game Demo Images/Structure Generation Result.png" width="800"><br/>

</p>

<h3> Adding Patters to the Library </h3>
<p>
Users can add desired patterns to the game library by navigating to the <i><b>Add Structure</b></i> button:<br/>

<img src="src/Resources/Game Demo Images/Adding Structure to Library.png" width="800"><br/>
<img src="src/Resources/Game Demo Images/Added Structure in Library.png" width="800"><br/>
<img src="src/Resources/Game Demo Images/Generation of Added Structure.png" width="800"><br/>
\*Added patterns will remain in the library after the termination of the program!

</p>

<h3> Deleting Patters From the Library </h3>
<p>
Users can delete undesired patterns from the game library by navigating to the <i><b>Manage Structure</b></i>
button:<br/>

<img src="src/Resources/Game Demo Images/Structure Library Management.png" width="800"/><br/>
<img src="src/Resources/Game Demo Images/Deleting Structures From Library Result.png" width="800"><br/>

*Deleted patterns will be absent from the library after the termination of the program! <br/>
*Structure Library can be reset to its initial state by pressing <i><b>Reset To Default</b></i> in
the<i><b>Structure Manager</i></b>.

</p>
