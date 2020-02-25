## MAT-CODING CHALLENGE

## Prerequisites:
* [git console](https://git-scm.com/downloads)
* [docker](https://docs.docker.com/)
* [docker-compose](https://docs.docker.com/compose/)
* [python 3.7 (dev version: 3.7.4)](https://www.python.org/)
* Add python 3 to PATH

# Instructions for executing the project
First step is to clone the project, you can do it with the following command:
```console
$ git clone https://github.com/MagicElyas/MAT-Coding-Challenge.git
```
I have provided 2 different files for configuring and executing depending if you are working on Windows or in Mac/Linux. Since the PC where I've completed the challenge is a windows one, I haven't been able to test the .sh code, so, in case something goes wrong, check the instructions provided and go one by one but it shouldn't fail.  
If you are executing from a windows machine you should navigate to the MAT-Coding-Challenge with the console and just execute.  
```console
$ .\run_project.bat
```
In case you are running this from a Linux machine you should either run:
```console
$ ./run_project.sh
```
With those files the project will:
- Pull the docker-compose
- Install pipenv with pip
- cd to the app directory
- Install all the packages used for the project
- Restart the docker-compose in case it was running before
- Launch the Challenge MQTT service.

# Decisions made
* The assign position function is made taking into consideration that we start a race everytime the program executes.  
States where a race is started should be considered invalid as I have defined the positions based on the premise that "The car that travels further, is the one that is the leader". I know that in the real world a car can travel more distance than the leader and still not be the leader due to the fact that all the cars do not always follow the racing line, but for this challenge, it works as intended.

# Interesting features of the implementation
* When assigning the positions to the cars in the race, since python saves the references to the objects, we don't need to reinsert every car into the cars dictionary after sorting them.
* Some events are more likely to ocurr than others
* All kind of events are built with the extensibility in mind, since you can add whatever new event string to the existing json files and they will work perfectly. 