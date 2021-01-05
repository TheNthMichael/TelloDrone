
class StateMachine:
    class States:
        WAITING = 0
        USER_CONTROL = 1
        AUTO = 2
        SEARCHING = 3
        TRACKING = 4
        EXIT = 5
    
    def __init__(self):
        # drone should initially be waiting
        self.state = States.WAITING
        self.state_machine = {
            States.WAITING : [
                States.USER_CONTROL,
                States.AUTO,
                States.EXIT
            ],
            States.USER_CONTROL : [
                States.AUTO,
                States.EXIT
            ],
            States.AUTO : [
                States.SEARCHING,
                States.TRACKING,
                States.EXIT
            ],
            States.SEARCHING : [
                States.TRACKING,
                States.USER_CONTROL,
                States.EXIT
            ],
            States.TRACKING : [
                States.SEARCHING,
                States.USER_CONTROL,
                States.EXIT
            ]

        }
    
