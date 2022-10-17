# SAT
### Sustainability Auditing Tool

# LOCAL DEVELOPMENT GUIDE

## Clone the GitHub Repo

Clone the SAT-7/sat repository to your local machine:

`git clone git@github.com:SAT-7/sat.git` or

`git clone https://github.com:SAT-7/sat.git`

You should now have all files in the 'sat' directory, within whatever directory your terminal was in when you called this command.

## Run the Flask App Locally

`cd` into the `sat` directory within your terminal, then get into your virtual environment to make running Python easy and cool:

`source env/bin/activate`

Once you've done that, you can run Flask without worrying about having the right Python packages and all that nonsense:

`flask run`

Which should automatically open a web browser and show you the Flask application in your browser at `localhost:5000`

## Start a new branch or use the branch you've been working on

If we all work on `main` at the same time, this will be insane.

When you first start your part of the project, start a new branch:

`git checkout -b your-branch-name`

If the branch you want to work on already exists, do this:

`git checkout that-branch-name`

## Make changes, watch things change

When you make changes in your code editor, you should be able to see those changes in the browser after saving the file you've altered.

## Push your changes to the Repo

From within your `sat` directory, run:

`git add --all`

`git commit -m "SOME MESSAGE ABOUT WHAT YOU DID"`

`git push -u origin your-branch-name`

If you're feeling REALLY good about what you did, submit a Pull Request and we'll pull your changes into `main`!

## Deployment Situation

When your changes get pulled into `main` - they're deployed to our Heroku app at [https://sustainabilityauditingtool.herokuapp.com](https://sustainabilityauditingtool.herokuapp.com).

As we get closer to the end of the project, we'll transition to our website/domain/whathaveyou.

### Troubleshooting

If this returns an error that port 5000 is already in use (some other frameworks like Docker use this port by default also), run something like:

`flask run -p 5001`

Which will attempt to host Flask on port 5001 instead.

---

If you can't find a remote branch, use `git fetch` to get the remote information.