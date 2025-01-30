import requests
import ttkbootstrap as ttk
import webbrowser
from ttkbootstrap.dialogs import Messagebox
from .Entries.configapi import GOOGLE_API_KEY
from .crud import create, read, delete
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
                    Title = book["volumeInfo"].get("title", "Unknown")
                    Author = ", ".join(book["volumeInfo"].get("authors", "Unknown"))
                    Publisher = book["volumeInfo"].get("publisher", "Unknown")
                    PublishedDate = book["volumeInfo"].get("publishedDate", "Unknown")
                    Description = book["volumeInfo"].get(
                        "description", "Description: Unknown"
                    )
                    PageCount = book["volumeInfo"].get("pageCount", "Unknown")
                    Language = book["volumeInfo"].get("language", "Unknown")
                    ImageLink = book["volumeInfo"]["imageLinks"]["thumbnail"]
                    BuyLink = book["saleInfo"]["buyLink"]
                else:
                    Messagebox.showinfo(
                        title="No Results Found",
                        message="No books found for your search. Please try a different query.",
                    )
            except Exception as e:
                print(f"Error found: {e}")
                Messagebox.showinfo(
                    title="No Results Found",
                    message="Error to find your book. Please try a different query.",
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
                BuyLink,
            )

            return data
        case 400:
            return Messagebox.showinfo(
                title="400 Bad Request",
                message="The server could not understand the request due to invalid syntax.",
            )
        case 401:
            return Messagebox.showinfo(
                title="401 Unauthorized",
                message="Authentication is required and has failed or has not yet been provided.",
            )
        case 403:
            return Messagebox.showinfo(
                title="403 Forbidden",
                message="You do not have permission to access the requested resource.",
            )
        case 404:
            return Messagebox.showinfo(
                title="404 Not Found",
                message="The requested resource could not be found on this server.",
            )
        case 405:
            return Messagebox.showinfo(
                title="405 Method Not Allowed",
                message="The request method is not supported for the requested resource.",
            )
        case 408:
            return Messagebox.showinfo(
                title="408 Request Timeout",
                message="The server timed out waiting for the request.",
            )
        case 500:
            return Messagebox.showinfo(
                title="500 Internal Server Error",
                message="The server encountered an internal error and was unable to complete your request.",
            )
        case 502:
            return Messagebox.showinfo(
                title="502 Bad Gateway",
                message="The server received an invalid response from an upstream server.",
            )
        case 503:
            return Messagebox.showinfo(
                title="503 Service Unavailable",
                message="The server is currently unable to handle the request due to temporary overloading or maintenance.",
            )
        case 504:
            return Messagebox.showinfo(
                title="504 Gateway Timeout",
                message="The server did not receive a timely response from an upstream server.",
            )


def search():
    query = entry_query.get()
    if query:
        request_data(query)
    else:
        Messagebox.showinfo(title="Input Error", message="Please enter a search term!")


def create_book_window(
    Title,
    Author,
    Publisher,
    PublishedDate,
    Description,
    PageCount,
    Language,
    ImageLink,
    BuyLink,
):
    bookwindow = ttk.Toplevel(window)
    bookwindow.title(f"{Title}")
    bookwindow.geometry("637x372")
    bookwindow.resizable(False, False)

    canvas = Canvas(bookwindow, bg="black")
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = ttk.Scrollbar(
        bookwindow, orient=VERTICAL, command=canvas.yview, style="TScrollbar"
    )
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.config(yscrollcommand=scrollbar.set)

    framebook = Frame(canvas)
    canvas.create_window((0, 0), window=framebook, anchor="nw")

    response = requests.get(ImageLink)
    if response.status_code == 200:
        img_data = response.content
        image = Image.open(BytesIO(img_data))
        resized_image = image.resize((150, 200))
        tk_image = ImageTk.PhotoImage(resized_image)
        bookwindow.iconphoto(False, tk_image)
    titlelabel = ttk.Label(framebook, text=f"{Title}", style="Allbold.TLabel")

    authorlabel = ttk.Label(framebook, text=f"Author: {Author}", style="All.TLabel")
    publisherlabel = ttk.Label(
        framebook, text=f"Publisher: {Publisher}", style="All.TLabel"
    )
    publisherdatelabel = ttk.Label(
        framebook, text=f"Publised Date: {PublishedDate}", style="All.TLabel"
    )
    descriptionlabel = ttk.Label(framebook, text=f"{Description}", style="All.TLabel")
    pagecountlabel = ttk.Label(
        framebook, text=f"Page Count: {PageCount}", style="All.TLabel"
    )
    languagelabel = ttk.Label(
        framebook, text=f"Language: {Language}", style="All.TLabel"
    )
    imagelinklabel = ttk.Label(framebook, image=tk_image)

    buybutton = ttk.Button(
        framebook,
        text="Buy",
        bootstyle="success",
        command=lambda: webbrowser.open(BuyLink),
    )
    wishlistbutton = ttk.Button(
        framebook,
        text="Put this book on my wish list",
        bootstyle="secondary",
        command=lambda: create(
            Title,
            Author,
            Publisher,
            PublishedDate,
            Description,
            PageCount,
            Language,
            ImageLink,
            BuyLink,
        ),
    )

    titlelabel.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    authorlabel.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    publisherlabel.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    publisherdatelabel.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    descriptionlabel.grid(row=4, column=0, padx=10, pady=5, sticky="w")
    pagecountlabel.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    languagelabel.grid(row=6, column=0, padx=10, pady=5, sticky="w")

    imagelinklabel.grid(row=2, column=1, rowspan=4, padx=10, pady=5)

    buybutton.grid(row=7, column=0, padx=10, pady=5, sticky="w")
    wishlistbutton.grid(row=7, column=1, padx=10, pady=5, sticky="w")

    publisherlabel.config(wraplength=400)
    descriptionlabel.config(wraplength=400)
    titlelabel.config(wraplength=400)

    framebook.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    bookwindow.mainloop()


def read_wishlist():
    read()


def main_window():
    global window, entry_query

    window = Tk()
    #window.iconphoto(True, PhotoImage(file="assets/Icons/images.png"))

    style = ttk.Style()
    style.theme_use("cyborg")
    style.configure("All.TLabel", font=("Raleway", 10), foreground="#A9A9A9")
    style.configure(
        "Allbold.TLabel", font=("Raleway", 11, "bold"), foreground="#A9A9A9"
    )
    style.configure(
        "TScrollbar",
        gripcount=5,
        background="#1a1a1a",
        throughcolor="#333333",
        relief="flat",
        thickness=30,
    )

    entry_query = ttk.Entry(window, width=30, bootstyle="primary")
    button_search = ttk.Button(
        window, text="Search", command=search, bootstyle="primary"
    )
    button_wishlist = ttk.Button(
        window, text="See your wish list", command=read_wishlist, bootstyle="secondary"
    )
    button_search.pack()
    entry_query.pack()
    button_wishlist.pack()
    window.mainloop()



