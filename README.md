# SAT
### Sustainability Auditing Tool

# DEVELOPMENT GUIDE

## Clone the GitHub Repo

Clone the SAT-7/sat repository to your local machine:

`git clone git@github.com:SAT-7/sat.git` or

`git clone https://github.com:SAT-7/sat.git`

You should now have all files in the 'sat' directory, within whatever directory your terminal was in when you called this command.

## Run the Flask App Locally

`cd` into the `sat` directory within your terminal, then run:

`flask run`

Which should automatically open a web browser and show you the Flask application at `localhost:5000`

### Dev/Debug Mode

For the code to automatically update when changes are made in your browser, add the Debug flag to Flask:

`flask --debug run`

If you don't see changes immediately, reload the page!

### Troubleshooting

If this returns an error that port 5000 is already in use (some other frameworks like Docker use this port by default also), run something like:

`flask run -p 5001`

Which will attempt to host Flask on port 5001 instead.

## SSH into the Server

To get into the server from your local machine, write the following in the terminal:

`ssh sat-admin@157.230.50.131`
and enter the password `P@$$word12345!`

One could also set up a GUI program to do this, but this is way more fun!
