ICSI499 CAPSTONE PROJECT FINAL README

HOW TO COMPILE AND RUN THIS CODE

There are a few ways to see this project. One way is to visit https://sustainabilityauditingtool.herokuapp.com and see the site in action there.

HEROKU APP NOTES

The deployed site is a Docker container created by GitHub actions and pushed to Heroku automatically whenever we update the `main` branch.

RUNNING LOCALLY

To ensure our code compiles correctly, there is another branch available, the `main-local` branch, which is connected to another GitHub OAuth client that will run successfully locally.

(1) First git clone this `main-local` branch, or check it out if you already have the sat repository from the SAT-7 group on GitHub (https://github.com/SAT-7/sat/).

(2) From there, run `source env/bin/activate` from the repo folder ('sat') to boot up the included environment. If it doesn't work make sure venv is installed on your machine.

(3) After this, copy and paste the provided `.env` file with the environment variables contained (not provided with the GitHub files, sensitive information) into the 'sat' folder.

(4) Now run the command `flask run -p 5002` which will spin up the Flask app and make it available on port 5002 (this port is crucial to the GitHub OAuth settings). Now go to your browser and visit `http://localhost:5002` - the site should be there.

DEBUG NOTES

This site has not been extensively tested, there may be unexpected errors, but it is confirmed to work correctly on Firefox running in Linux.