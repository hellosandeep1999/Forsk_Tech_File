"""
GIT Commands
"""
# Why git and what git can do
# Install git locally and Goto Github and create an account
# Create a new empty remote repo on Github
# Repository Name = python and Description (optional) = python 
# which should be Public and DO NOT initialize it with a README 
# Click on Create repository
# copy the HTTPS URL of repo (https://github.com/hellosandeep1999/python.git  )
# Goto terminal or Command Prompt and change directory to the desktop 
# Run the below command to clone as a local repo
# git clone https://github.com/hellosandeep1999/python.git
# Change directory to  python
# create a test.py file on desktop/python
# git config user.email "sandeepjain20178@gmail.com"
# git config user.name "hellosandeep1999"


# Example to understand the concept 
# git status  # Untracked file 
# git add test.py 
# git status  # New file 
# git commit -m "Added new file"
# git status # nothing to commit
# git push
# Goto github.com and refresh your page to see the test.py


# Onetime Workflow for old files
# Add all the files in the new folder FSDP_2019
# git add --all
# git commit -m "Adding all files"
# git status
# git push
# Goto github.com and refresh your page to see all the files


# Everyday Workflow for new files
# Create files in the new folder FSDP_2019
# git add <filename>
# git commit -m "Added new file"
# git status # nothing to commit
# git push
# Goto github.com and refresh your page to see all the new file added



# How to ignore files in git
# https://github.com/github/gitignore/blob/master/Python.gitignore

# Download the file from the above link and store in the project directory 
# Rename the file to .gitignore





# Goto Github, edit and commit changes 
# Edit locally and git add test.py and git commit -m "Did some more changes"
# git pull
# Merge Conflicts needs to be solved
# Open Locally and edit, remove all <<<<<, ====== and >>>>>> and solve the error
# git add <filename>
# git commit -m "Fix Merge Conflict"
# git push

# git log ( history of commit )
# git reset --hard <commit>   ( to have a copy of the commit number )
# git reset --hard origin/master ( to have a fresh copy as you started )  


# Messed working but NOT staged git checkout HEAD path/to/file
# Messed working (but staged) git reset HEAD path/to/file and then git checkout HEAD path/to/file
# Messed working (staged and commit)  git checkout HEAD^ path/to/file


#. git reflog ... # http://ohshitgit.com/


+++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++


#if our file empty and we to find again
# git checkout HEAD file_name.py


#if empty file is pushed and we want to again so we need to second last file
#git checkout HEAD~1 file_name.py


## git log ( history of commit )


#it will show the lines of code
#git show 90f58fa


#difference between 200 lines of code
#git diff 90f58fa 90f58fb

+++++++++++++++++++++++++++++++++++++++++++++++++++++++
+++++++++++++++++++++++++++++++++++++++++++++++++++++++




"""
Example dataset for Hash Tables explanation

Jan, Tim, Mia, Sam, Leo, Ted, Bea, Lou, Ada, Max, Zoe

Mia, Tim, Bea, Zoe, Sue, Len, Moe, Lou, Rae, Max, Tod

# Setting up virtual Environment
virtualenv -p python3 venu
virtualenv venu
source venu/bin/activate 
which python
deactivate

"""
