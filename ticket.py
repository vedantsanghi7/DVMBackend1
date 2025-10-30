import uuid

class Ticket:
    def __init__(self, src, dest, price, path):
        self.id = str(uuid.uuid4())[:8]
        self.src = src
        self.dest = dest
        self.price = price
        self.path = path

    def __repr__(self):
        return f"Ticket[{self.id}] {self.src} → {self.dest} (₹{self.price})"
