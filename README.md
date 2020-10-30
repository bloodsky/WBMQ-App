# WBMQ-App

Multithreaded controller application written in python for [WBMQSystemProject](https://github.com/CecBazinga/WBMQSystemProject). Spawning variable numbers of publisher (sensors) and subscribers (bots) as main use case. GUI included to show proper operations both FE and BE side.  

## Installation

Controller is working on internal IP address of the machine, listening on port "5001". It is necessary to port forwarding. 

```bash
  	# Dependencies
  	pip install Flask
	pip install requests
  
  	# Actual running
	python WBMQApp.py
```

## Show case
![alt text](https://github.com/bloodsky/WBMQ-App/blob/master/SensorsApp/runningex.png)
