import requests
from Entries.configapi import GOOGLE_API_KEY
from CRUD import create, read, delete
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO


def request_data(query):
    response = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q={query}&key={GOOGLE_API_KEY}"
    )
    match response.status_code:
        case 200:
            data = response.json()
            try:
                if "items" in data and len(data["items"]) > 0:
                    book = data["items"][0]
                    Title = book["volumeInfo"]["title"]
                    Author = ", ".join(book["volumeInfo"]["authors"])
                    Publisher = book["volumeInfo"].get("publisher", "Unknown")
                    PublishedDate = book["volumeInfo"].get("publishedDate", "Unknown")
                    Description = book["volumeInfo"]["description"]
                    PageCount = book["volumeInfo"]["pageCount"]
                    Language = book["volumeInfo"]["language"]
                    ImageLink = book["volumeInfo"]["imageLinks"]["thumbnail"]
                else:
                    messagebox.showinfo(
                        title="No Results Found",
                        message="No books found for your search. Please try a different query."
                    )
            except Exception as e:
                print(f'Error found: {e}')
                messagebox.showinfo(
                        title="No Results Found",
                        message="Error to find your book. Please try a different query."
                    )
            create_book_window(
                Title,
                Author,
                Publisher,
                PublishedDate,
                Description,
                PageCount,
                Language,
                ImageLink,
            )

            return data
        case 400:
            return messagebox.showerror(
                title="400 Bad Request",
                message="The server could not understand the request due to invalid syntax.",
            )
        case 401:
            return messagebox.showerror(
                title="401 Unauthorized",
                message="Authentication is required and has failed or has not yet been provided.",
            )
        case 403:
            return messagebox.showerror(
                title="403 Forbidden",
                message="You do not have permission to access the requested resource.",
            )
        case 404:
            return messagebox.showerror(
                title="404 Not Found",
                message="The requested resource could not be found on this server.",
            )
        case 405:
            return messagebox.showerror(
                title="405 Method Not Allowed",
                message="The request method is not supported for the requested resource.",
            )
        case 408:
            return messagebox.showerror(
                title="408 Request Timeout",
                message="The server timed out waiting for the request.",
            )
        case 500:
            return messagebox.showerror(
                title="500 Internal Server Error",
                message="The server encountered an internal error and was unable to complete your request.",
            )
        case 502:
            return messagebox.showerror(
                title="502 Bad Gateway",
                message="The server received an invalid response from an upstream server.",
            )
        case 503:
            return messagebox.showerror(
                title="503 Service Unavailable",
                message="The server is currently unable to handle the request due to temporary overloading or maintenance.",
            )
        case 504:
            return messagebox.showerror(
                title="504 Gateway Timeout",
                message="The server did not receive a timely response from an upstream server.",
            )


def search():
    query = entry_query.get()
    if query:
        request_data(query)
    else:
        messagebox.showwarning(
            title="Input Error", message="Please enter a search term!"
        )


def create_book_window(
    Title, Author, Publisher, PublishedDate, Description, PageCount, Language, ImageLink
):
    bookwindow = Toplevel(window)
    bookwindow.title(f"{Title}")
    bookwindow.geometry("627x350")
    bookwindow.resizable(False, False)
   

    canvas = Canvas(bookwindow)
    canvas.pack(side=LEFT,fill=BOTH, expand=True)

    scrollbar = Scrollbar(bookwindow,orient=VERTICAL,command=canvas.yview)
    scrollbar.pack(side=RIGHT,fill=Y)
    canvas.config(yscrollcommand=scrollbar.set)

    framebook = Frame(canvas)
    canvas.create_window((0, 0), window=framebook, anchor="nw")

    response = requests.get(ImageLink)
    if response.status_code == 200:
        img_data = response.content
        image = Image.open(BytesIO(img_data))
        resized_image = image.resize((150, 200))
        tk_image = ImageTk.PhotoImage(resized_image)
        bookwindow.iconphoto(False,tk_image)
    titlelabel = Label(framebook, text=f"{Title}")

    authorlabel = Label(framebook, text=f"Author: {Author}")
    publisherlabel = Label(framebook, text=f"Publisher: {Publisher}")
    publisherdatelabel = Label(framebook, text=f"Publised Date: {PublishedDate}")
    descriptionlabel = Label(framebook, text=f"{Description}")
    pagecountlabel = Label(framebook, text=f"Page Count: {PageCount}")
    languagelabel = Label(framebook, text=f"Language: {Language}")
    imagelinklabel = Label(framebook, image=tk_image)

    buybutton = Button(framebook, text="Buy")
    wishlistbutton = Button(framebook, text="Put this book on my wish list")

    titlelabel.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    authorlabel.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    publisherlabel.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    publisherdatelabel.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    descriptionlabel.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    pagecountlabel.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    languagelabel.grid(row=6, column=0, padx=10, pady=5, sticky="w")

    imagelinklabel.grid(row=2, column=1, rowspan=4, padx=10, pady=5)

    buybutton.grid(row=7, column=0, padx=10, pady=5, sticky="w")
    wishlistbutton.grid(row=7, column=1, padx=10, pady=5)


    descriptionlabel.config(wraplength=400)
    titlelabel.config(wraplength=400)

    framebook.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))



    bookwindow.mainloop()


window = Tk()
window.iconphoto(True,PhotoImage(file="assets/Icons/images.png"))

entry_query = Entry(window, width=30)
button_search = Button(window, text="Search", command=search)
button_search.pack()
entry_query.pack()
window.mainloop()
