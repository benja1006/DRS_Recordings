"""A set of multiuse modules."""
import os


def getEnv(envPath):
    """Return the .env file as a dictionary."""
    # if(not os.path.isfile('.env')):
    #     with open(envPath, 'w') as env:
    #         env.write('SOURCE=\nDEST=\nEXCEL=')
    #         print('Env created')
    with open(envPath, 'r') as env:
        envvars = env.read().split('\n')
        ENV = {}
        for line in envvars:
            if(len(line) == 0):
                break
            ENV[line.split('=', 1)[0]] = line.split('=', 1)[1]
    return ENV


def updateEnv(newEnv, envPath):
    """Update the env file and return it."""
    currEnv = getEnv(envPath)
    with open(envPath, 'w+') as env:
        if len(currEnv) == len(newEnv):
            for key in newEnv:
                env.write(key + '=' + newEnv[key] + '\n')
    return getEnv(envPath)
