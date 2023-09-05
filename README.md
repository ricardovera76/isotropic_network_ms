# Isotropic Network's Micro-Service

This project was developed using the following tools and software

<div>
<a href="https://www.python.org/">
<img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="Python" width="100" height="100" />
</a><a href="https://flask.palletsprojects.com/en/2.3.x/">
<img src="https://camo.githubusercontent.com/3638770a498aa8a62be0fb35f9217dbc78a50d739e1f6cdc64ef88def23aa1ec/68747470733a2f2f666c61736b2e70616c6c65747370726f6a656374732e636f6d2f656e2f312e312e782f5f696d616765732f666c61736b2d6c6f676f2e706e67" alt="Flask" width="200" height="100" />
</a><a href="https://www.netify.ai">
<img src="https://www.netify.ai/images/netify-dark.svg" alt="Netify" width="200" height="100" />
</a><a href="https://redis.io/">
<img src="https://www.stackery.io/assets/images/posts/redis-cache-cluster-support/featured.svg" alt="Redis" width="100" height="100" />
</a><a href="https://www.docker.com/">
<img src="https://www.svgrepo.com/show/331370/docker.svg" alt="Docker" width="100" height="100" />
</a>
<a href="https://restfulapi.net/">
<img src="https://www.snmpcenter.com/wp-content/uploads/2016/10/RESTful-API-logo-for-light-bg.png" alt="RESTful" width="300" height="100" />
</a>
<div>

## Architecture
### 1. Web Application Thread:

This thread handles user requests through a web interface built using Python and Flask.
The primary purpose of this thread is to retrieve data from the Redis DB and display it to the users via the web api.
#### Web Application Components:
  1.1. Flask Application: Create a Flask web application to serve as the API.
  1.2. Routes: Define routes and endpoints to handle user requests.
  1.3. Data Retrieval: Use Python libraries or custom functions to fetch data from Redis.
  1.4. Data Presentation: Format and render the retrieved data for display on the web API.
  1.5. Redis Integration: Use Redis to retrieve network data saved from the parser.

### 2. Listener and Parser Thread:
This thread is responsible for listening to data from Netify's daemon and parsing that information.
It also saves the parsed data into a Redis database for further processing or retrieval by the web API.
#### Listener and Parser Components:
  2.1 Daemon Communication: Establish a communication mechanism with Netify's daemon to receive data updates.
  2.2 Data Parsing: Parse the data received from the daemon, extracting relevant information.
  2.3 Redis Storage: Use a Redis client library to store the parsed data in a Redis database.
  2.4 Threading: Implement multithreading to ensure efficient listening and parsing every 15 seconds without blocking the main application.

### 3. Redis Database:
  3.1 Set up a Redis database as a central data store for the project using docker.
  3.2 Create appropriate data structures (hash) within Redis to store the parsed data from the daemon.


## Primary Objective

The objective of this project is to develop a Python 3 micro service that captures data from the Netify statistics socket, stores it in a Redis database, and exposes the stored data through a RESTful API in a standardized JSON format. The micro service will enhance the functionality of the Netify platform by providing efficient data storage and easy access through a user-friendly API.

## Functionality

The project primarily uses 2 threads, 1 for the web app for retrieving the data using python ,flask and redis, and the other thread listening and parsing information from the netify's daemon using python and saving that data into Redis db.

The Flask App is  listening on port 7000 on the localhost getting 2 primary endpoints.

- The root endpoint `/`, which gets all the information across the entire network and its users and the applications being used by those users
- The `/<mac-addr>`, which gets all the info regarding a specific user in the network.

## Getting started
### 1. Download and Install the required packages
run the following commands to get started (NOTE: this project is started on Windows 11 22H2 using WSL 2 Ubuntu 22.04)

```bash
chmod +x ./config.sh && ./config.sh
```

NOTE: 
once installed to stop use CTRL+C and use the command:
```bash
sudo systemctl stop netifyd.service
```
to start again:
```bash
sudo systemctl start netifyd.service && sudo nc -U /var/run/netifyd/netifyd.sock
```
### 2. Start APP
Once the daemon is started wait 15 seconds to let it retrieve the first streams of packets in the network, then run the app by:
First run the redis container in a terminal window
```bash
docker-compose up -d && docker exec -it redis redis-cli
```
Then run the Main APP in another terminal window
```bash
python main.py
```
The app will run on http://localhost:7000
then make the GET request to the root "/" or the "/[mac-addr]" to get the required info.

Isotropic Networks's Micro-Service Project started on 23-aug-2023
