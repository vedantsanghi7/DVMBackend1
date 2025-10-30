class Line:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"{self.name} Line ({self.id})"
