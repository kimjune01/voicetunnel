# Voicetunnel
A hands-free app for messaging your friends!

Repository the Voicetunnel server at NWHacks 2018
by June Kim, James Leong


### Environment Setup
Install python3:
```
> brew upgrade python3
```

Install and configure virtualenv:
```
> pip install virtualenv
> mkdir ~/Python_envs
> cd ~/Python_envs
> virtualenv -p /usr/local/Cellar/python3/3.6.2/bin/python3 voicetunnel
```

# Using and Updating the Environment:
Anytime you want to activate this environment:
```
> source ~/Python_envs/voicetunnel/bin/activate
```

You will know if you have the environment activated or not from your
command line prompt:
```
(voicetunnel) >
```

All the required python packages are defined in the
requirements.txt file. Use the `pip` command to install or
upgrade. Remember you need to do this each time someone adds a required
package to the project.
```
(voicetunnel) > pip3 install -r requirements.txt
```

To add a required package to the project, use the `pip freeze` command:
```
(voicetunnel) > pip3 freeze > requirements.txt
```

Run instructions
to export env variables, copy and paste voicetunnel.env from wiki into repo and change python path
export environment variables:
```
(voicetunnel) > source voicetunnel.env

```
then install mysql, create a database called voicetunnel 

install localtunnel via localtunnel.me
launch in terminal
> lt -s voiceminder -p 5000

This launches api as https://voicetunnel.localtunnel.me
