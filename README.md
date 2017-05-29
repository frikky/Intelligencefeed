# Threat intel frameworkish
Simple OSint framework to grab data from locations, accumulated and aggregate.

## Inspiration
Because there aren't any others that work well.

## Usage
Edit the config file with more information, run the server and try something on the specified port. Can also be done with docker.

### For normal usage:
1. pip install wget
2. python intelfeed <port>

### Docker usage:
1. Get docker working 
2. sudo docker build . -t <name>
3. sudo docker run -d -p "1337:1337" <name>

## Addons
This is where I try to actually implement all the data into different systems. Per now its only done using QRadar reference sets. The SIEM only thing necessary then is to create simple IoC rules for the different categories.

## Addons todo
Add cronjobs (or infinite loop) that works, and maybe a docker implementation

## Todos 
* Reverse search possibilities for reference (Might take a while)
* Change to a not idiot DB. Should be remote or other docker container.
* Stop using freaking wget and swap to request
* Proper web GUI (?)
* Make it work manually with e.g. Chrome (Works with Firefox)

## More todos?
* Better file movement for less file instability problems
* Faster rollout of new IOCs (Attempt automation)
* Compress for better storage (Need a proper DB)
* (Done) Create a docker file
* Set up self hosting. Sockets are safe \o/
* RSS feed :D

## Done
* Categorization 

### Creds
- https://github.com/hslatman/awesome-threat-intelligence
- da\_667 :^) 
