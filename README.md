# Threat intel frameworkish
Simple OSint framework to grab data from locations, accumulated and aggregate.

## Inspiration
Because there aren't any others that work well.

## Usage
Edit the config file with more information, run the server and try something on the specified port. Can also be done with docker.

### For normal usage:
1. pip install wget
2. python intelfeed port

### Docker usage:
1. Get docker working 
2. sudo docker build . -t name
3. sudo docker run -d -p "localport:dockerport" name

* Note: If you want realtime configuration of new sources - expose directory config:
3. sudo docker run -d -v /app/config/:$(pwd)/config/ -v /app/scripts/:$(pwd)/scripts -p "1337:1337" name

## Addons
This is where I try to actually implement all the data into different systems. Per now its only done using QRadar reference sets. The SIEM only thing necessary then is to create simple IoC rules for the different categories.

## Addons todo
Add cronjobs (or infinite loop) that works, and maybe a docker implementation

## Todos 
* Create REST API associated with the data
* Reverse search possibilities for reference (Might take a while)
* Change to a normal database. Should be remote or other docker container.
* Stop using freaking wget and swap to request (pip)
* Proper web GUI (?)
* Make it work manually with e.g. Chrome (Works with Firefox)

## More todos?
* Logging and verbosity for the server
* Better file movement for less file instability problems
* Faster rollout of new IOCs (Attempt automation)
* Compress for better storage (Need a proper DB)
* (Done) Create a docker file
* Set up self hosting. Sockets are safe \o/
* RSS feed :D

## Done
* Categorization 

### Creds
- da\_667 for inspiration
- https://github.com/hslatman/awesome-threat-intelligence
- http://osintframework.com/
