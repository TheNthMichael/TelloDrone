class States:
        WAITING = 0
        USER_CONTROL = 1
        SEARCHING = 2
        TRACKING = 3
        EXIT = 4

class StateMachine:
    def __init__(self):
        # drone should initially be waiting
        self.state = States.WAITING
        self.state_machine = {
            States.WAITING : [
                States.USER_CONTROL,
                States.SEARCHING,
                States.EXIT
            ],
            States.USER_CONTROL : [
                States.SEARCHING,
                States.WAITING,
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
    
    def state_change(self, input):
        state_changes = self.state_machine[self.state]
        state = state_changes[input]
    
