
shutdown = False

def update():
    global shutdown # telling python "I want to access the global shutdown"
    shutdown = True

def getValue():
    return shutdown

def main():
    print("Status is: ", getValue())

    update()

    print("Status is: ", getValue())

main()