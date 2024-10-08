# MyLestari Faperta IPC Program

This program made for IPC to read sensor then send it to API and read feedback from API and do something with Modbus TCP/IP.

## Installation

Download and install [python3](https://www.python.org/downloads) and requirements to run this program.

```bash
sudo apt install python python-pip python-dev build-essential -y

sudo pip install --upgrade pip 

sudo pip install -r requirements.txt
```

## Usage


```bash
#create service to realtime check API (then copy and paste source code)
sudo nano /etc/systemd/system/faperta_modapi.service

#create service to auto run chrome in full screen (then copy and paste source code)
sudo nano /etc/systemd/system/ipc.service

#register service to system and make it autorun when ipc start
sudo systemctl daemon-reload
sudo systemctl enable faperta_modapi.service
sudo systemctl start faperta_modapi.service
sudo systemctl enable ipc.service
sudo systemctl start ipc.service

#check status service
sudo systemctl status faperta_modapi.service
sudo systemctl status ipc.service


# note: adjust ExecStart, User, and WorkingDirectory according to your needs
```


## Author
[Willy](https://github.com/willygoid) Inastek\
Kalasan, August 2024
