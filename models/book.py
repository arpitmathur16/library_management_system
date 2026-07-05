class Book:
    def __init__(self, book_id, title, author, isbn, quantity, available_quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.quantity = quantity
        self.available_quantity = available_quantity

    def __str__(self):
        return (f"[{self.book_id}] {self.title} by {self.author} "
                f"(ISBN: {self.isbn}) — Available: {self.available_quantity}/{self.quantity}")
