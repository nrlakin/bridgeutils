#bridgeutils--Python utilities for interacting with Sage Bridge

##bridgeclient
Client-side functions for posting/retrieving surveys. If the environment variables BRIDGE_EMAIL and BRIDGE_PASSWORD are set, user authentication and session token handling will be dealt with automatically before requesting from Bridge endpoint. These variables can be added to your virtualenv's activation script for extra convenience.

##Dependencies
The only real dependency is Python `requests`. Installing from requirements.txt will also set up Jupyter/iPython in your working directory.

##Installation
After cloning the repository, set up a virtualenv in your working directory and install dependencies like so:

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```


