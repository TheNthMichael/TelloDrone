"""
For now, this class is just a
data struture for the return
value of the face detector.
This will later be used with
the lk optical flow algorithm
for tracking
"""
class Face:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
    