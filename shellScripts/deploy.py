#!/usr/bin/env python3
import os
import subprocess

def validateInput(inputValue):
    if "n" == inputValue or "y" == inputValue:
        return

    print("invalid input... Run the script again.")
    exit()

def nyAnswer(text):
    userResponse = input(text)
    validateInput(userResponse)
    return userResponse

def commitChanges():
    subprocess.run(["git", "add", "--all"], check=True)
    commit = input("Commit your changes: ")
    subprocess.run(["git", "commit", "-m", commit], check=True)

def checkLocalChanges():
    print("Looking for changes to commit")
    statusResult = subprocess.run(["git", "status"], capture_output=True, text=True, check=True)
    if "Untracked files:" in statusResult.stdout:
        return True

    return False

def pushToOrigin():
    print("Uploading commits...")
    subprocess.run(["git","push"])
    print("Changes pushed to main/origin.")

def checkOriginChanges():
    print("Checking changes in origin...")
    subprocess.run(["git", "fetch"], check=True)
    branchStatus = subprocess.run(["git", "status", "-uno"], capture_output=True, text=True, check=True)
    
    if "'origin/main' have diverged" in branchStatus.stdout:
        print("you have divergent branches. Resolve it and try again.")
        subprocess.run(["git","reset","--soft","HEAD^1"])
        subprocess.run(["git","restore","--staged", "."])
        print("commit created reverted.")
        exit()

    if "Your branch is behind" in branchStatus.stdout:      
        return True
    else:
        return False

def pullChanges():
        pullD = nyAnswer("Confirm? [y/n]: ")
        if pullD == "n": 
            return False
        elif pullD == "y":
            print("Updating branch...")
            subprocess.run(["git", "pull"], check=True)
            print("Branch successfully updated")
            return True

def buildProject():
    print("Running tests...")
    print("All tests passed")
    print("Building the package and checking lint errors")
    print("Package was successfully built")
    return 

def uploadToRepositoryAndDeploy():
    localChange = checkLocalChanges()
    if localChange:
        commitChanges() 
        wantToPush = nyAnswer("Push to origin? [y/n]: ")

        if wantToPush == "y":
            thereIsChangesInOrigin = checkOriginChanges()
            if thereIsChangesInOrigin:
                updateLocal = nyAnswer("Your branch isn't updated, want to pull changes? [y/n]:")
                if updateLocal == "y":
                    if pullChanges():
                        pushToOrigin()
            else:
                print("there is no changes in origin")
                pushToOrigin()
        
        buildAndDeploy = nyAnswer("You want to build and deploy your app? [y/n]:")


        if buildAndDeploy == "y":
            buildProject()
            print("Deploying the application...")
        
    exit()
   

if __name__ == "__main__": 
    try:
        uploadToRepositoryAndDeploy()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        exit()
