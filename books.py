from fastapi import FastAPI
from pydantic import BaseModel, Field
app=FastAPI()
from typing import Optional
from starlette import status

class Book:

    id:int
    title:str
    author:str
    description:str
    rating:int
   

    def __init__(self,id,title,author,description,rating):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating

class BookRequest(BaseModel):

    id: Optional[int] = None
    title: str = Field(min_length=3, max_length=100)
    author: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=0, lt=6)

BOOKS = [
    Book(1, "To Kill a Mockingbird", "Harper Lee", "A novel about the serious issues of rape and racial inequality in the Depression-era South, told through the eyes of a young girl.", 5),
    Book(2, "1984", "George Orwell", "A dystopian novel set in a totalitarian society under constant surveillance, addressing themes of government control and individual freedom.", 5),
    Book(3, "The Great Gatsby", "F. Scott Fitzgerald", "A tragic story of Jay Gatsby's love for Daisy Buchanan, set against the backdrop of the Roaring Twenties in America.", 4),
    Book(4, "Moby-Dick", "Herman Melville", "The story of Captain Ahab's obsessive quest to hunt down the elusive white whale, Moby Dick.", 4),
    Book(5, "Pride and Prejudice", "Jane Austen", "A romantic novel that explores themes of love, reputation, and class, focusing on the complex relationship between Elizabeth Bennet and Mr. Darcy.", 5),
    Book(6, "The Catcher in the Rye", "J.D. Salinger", "A story of a disillusioned teenager, Holden Caulfield, who narrates his thoughts on his life and the world around him.", 4),
    Book(7, "The Hobbit", "J.R.R. Tolkien", "A fantasy novel that follows the journey of Bilbo Baggins, a hobbit who is thrust into an epic adventure to reclaim a treasure guarded by a dragon.", 5),
    Book(8, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "The first book in the Harry Potter series, which follows a young wizard discovering his magical heritage and facing the dark forces of the wizarding world.", 5),
    Book(9, "The Alchemist", "Paulo Coelho", "A philosophical novel about a shepherd named Santiago who embarks on a journey to find a hidden treasure, learning life lessons along the way.", 4),
    Book(10, "Brave New World", "Aldous Huxley", "A dystopian novel that explores the dangers of a society driven by technology, consumerism, and the suppression of individuality.", 4)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id:int):
    for book in BOOKS:
        if book.id==book_id:
            return book
    return "Book not found!"

@app.get("/book/",  status_code=status.HTTP_200_OK)
async def get_books_by_rating(book_rating:int):
    books_to_return=[]
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book",  status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):

    new_book=Book(**book_request.model_dump())
    BOOKS.append(create_book_id(new_book))
    
def create_book_id(book: Book):
    if len(BOOKS)>0:
        book.id=BOOKS[-1].id + 1
    else:
        book.id=1

    return book

@app.put("/books/update_book",  status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book.id:
            BOOKS[i]=book

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)

async def delete_book(book_id:int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id==book_id:
            BOOKS.pop(i)
            break