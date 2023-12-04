
class WishlistItem:
    def __init__(self, url: str, name: str, price: float):
        self.url = url
        self.name = name
        self.price = price
        self.checked_of = False
        self._id = "HQE&253" # set hash id based on time and name or random number
        self._belongs_to = "userid"

    @property
    def getID(self) -> str:
        return self._id

item = WishlistItem("bol.com", "lego", 4.5)
print("name " + item.name)
print("id " + item.getID)
print("checked? " + str(item.checked_of))
item.checked_of = True
print("checked now? " + str(item.checked_of))

