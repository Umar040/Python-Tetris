# Python-Tetris

For the python files just download and make sure you have pygame installed and then you can just run the script.

Pip Command to install globally:

pip install pygame

Pygame Wiki for More Information:
https://www.pygame.org/wiki/GettingStarted
-----------------------------------------------------------------------------------------------------------------------------
The one that does not have the word AI in it is the playable one whereas the AI one plays itself but you can adjust the the weights in the code but I left what I found to be the best on average.

Genetic Algorithm was implement and uploaded which simulates the game without visuals and tries to find the best weights for the AI. Below is an example of the code running
![image](https://github.com/user-attachments/assets/878338f8-72fc-484d-959a-347417e67e02)

The best from testing a 100 population size for 20 generations for 1 minute maximum time was
[4.95,7.4,1,1,7.5] (Rounded)
When testing these values back into the visual AI the game ran for 20,000 lines without dying which is where I stopped.
