import requests
import ttkbootstrap as tb
import webbrowser
from ttkbootstrap.dialogs import Messagebox
from .config import api_key
from .crud import create, read, delete
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO


window = None

def request_data(query,user_id):
    response = requests.get(
        f"https://www.googleapis.com/books/v1/volumes?q={query}&key={api_key}"
    )
    match response.status_code:
        case 200:
            data = response.json()
            try:
                if "items" in data and len(data["items"]) > 0:
                    book = data["items"][0]
                    volume_info = book.get("volumeInfo", {})
                    sale_info = book.get("saleInfo", {})

                    Title = volume_info.get("title", "Unknown")
                    Author = ", ".join(volume_info.get("authors", "Unknown"))
                    Publisher = volume_info.get("publisher", "Unknown")
                    PublishedDate = volume_info.get("publishedDate", "Unknown")
                    Description = volume_info.get("description", "Description: Unknown")
                    PageCount = volume_info.get("pageCount", "Unknown")
                    Language = volume_info.get("language", "Unknown")
                    ImageLink = volume_info.get("imageLinks", {}).get("thumbnail", None)
                    BuyLink = sale_info.get("buyLink", "Unknown")
                    request_data.user_id = user_id
                else:
                    Messagebox.show_info(
                        title="No Results Found",
                        message="No books found for your search. Please try a different query.",
                        parent=window
                    )
                    return
            except Exception as e:
                print(f"Error found: {e}")
                Messagebox.show_info(
                    title="No Results Found",
                    message="Error to find your book. Please try a different query.",
                    parent=window
                )
            user_id = request_data.user_id
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
                user_id
            )

            return data
        case 400:
            return Messagebox.show_error(
                title="400 Bad Request",
                message="The server could not understand the request due to invalid syntax.",
                parent=window
            )
        case 401:
            return Messagebox.show_error(
                title="401 Unauthorized",
                message="Authentication is required and has failed or has not yet been provided.",
                parent=window
            )
        case 403:
            return Messagebox.show_error(
                title="403 Forbidden",
                message="You do not have permission to access the requested resource.",
                parent=window
            )
        case 404:
            return Messagebox.show_error(
                title="404 Not Found",
                message="The requested resource could not be found on this server.",
                parent=window
            )
        case 405:
            return Messagebox.show_error(
                title="405 Method Not Allowed",
                message="The request method is not supported for the requested resource.",
                parent=window
            )
        case 408:
            return Messagebox.show_error(
                title="408 Request Timeout",
                message="The server timed out waiting for the request.",
                parent=window
            )
        case 500:
            return Messagebox.show_error(
                title="500 Internal Server Error",
                message="The server encountered an internal error and was unable to complete your request.",
                parent=window            
                )
        case 502:
            return Messagebox.show_error(
                title="502 Bad Gateway",
                message="The server received an invalid response from an upstream server.",
                parent=window
            )
        case 503:
            return Messagebox.show_error(
                title="503 Service Unavailable",
                message="The server is currently unable to handle the request due to temporary overloading or maintenance.",
                parent=window
            )
        case 504:
            return Messagebox.show_error(
                title="504 Gateway Timeout",
                message="The server did not receive a timely response from an upstream server.",
                parent=window
            )


def search(entry_query,user_id):
    query = entry_query.get()
    if query:
        request_data(query,user_id)
    else:
        Messagebox.show_info(title="Input Error", message="Please enter a search term!", parent=window)


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
    user_id 
):
    bookwindow = tb.Toplevel(window)
    bookwindow.title(f"{Title}")
    bookwindow.geometry("637x372")
    bookwindow.resizable(False, False)

    bookwindow.user_id = user_id

    canvas = Canvas(bookwindow, bg="black")
    canvas.pack(side=LEFT, fill=BOTH, expand=True)

    scrollbar = tb.Scrollbar(
        bookwindow, orient=VERTICAL, command=canvas.yview, style="TScrollbar"
    )
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.config(yscrollcommand=scrollbar.set)

    framebook = tb.Frame(canvas)
    canvas.create_window((0, 0), window=framebook, anchor="nw")

    try:
        response = requests.get(ImageLink)
        if response.status_code == 200:
            img_data = response.content
            image = Image.open(BytesIO(img_data))
            resized_image = image.resize((150, 200))
            tk_image = ImageTk.PhotoImage(resized_image)
            framebook.image = tk_image
          
    except Exception as e:
        print(f"Error loading image: {e}")

    titlelabel = tb.Label(framebook, text=f"{Title}", style="Allbold.TLabel")
    authorlabel = tb.Label(framebook, text=f"Author: {Author}", style="All.TLabel")
    publisherlabel = tb.Label(framebook, text=f"Publisher: {Publisher}", style="All.TLabel")
    publisherdatelabel = tb.Label(framebook, text=f"Publised Date: {PublishedDate}", style="All.TLabel")
    descriptionlabel = tb.Label(framebook, text=f"{Description}", style="All.TLabel")
    pagecountlabel = tb.Label(framebook, text=f"Page Count: {PageCount}", style="All.TLabel")
    languagelabel = tb.Label(framebook, text=f"Language: {Language}", style="All.TLabel")

    if tk_image:
        imagelinklabel = tb.Label(framebook, image=tk_image)
    else:
        imagelinklabel = tb.Label(framebook, text="Image not available")

    def safe_buy_link():
        if BuyLink != "Unknown":
            try:
                webbrowser.open(BuyLink)
            except Exception as e:
                print(f"Error opening buy link: {e}")
                Messagebox.show_error("Error opening buy link", 
                                      "Error",
                                      parent=bookwindow)

    def safe_wishlist():
        try:
            user_id = bookwindow.user_id 
            success = create(Title, Author, Publisher, PublishedDate, Description, 
                           PageCount, Language, ImageLink, BuyLink,user_id)
            if success:
                Messagebox.show_info("Book added to wishlist successfully!", 
                                     "Success",
                                     parent=bookwindow)
            else:
                Messagebox.show_error("Failed to add book to wishlist", 
                                      "Error",
                                      parent=bookwindow)
        except Exception as e:
            print(f"Error adding to wishlist: {e}")
            Messagebox.show_error("Error adding to wishlist", 
                                  "Error",
                                  parent=bookwindow)
     

    buybutton = tb.Button(
        framebook,
        text="Buy",
        bootstyle="dark",
        command=safe_buy_link,
    )
    wishlistbutton = tb.Button(
        framebook,
        text="Put this book on my wish list",
        bootstyle="secondary",
        command=safe_wishlist
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

    return bookwindow

def read_wishlist(root, user_id):
    print(f"UserID: {user_id}")
    books = read(user_id)
    if not books:
        Messagebox.show_info("No books found in the wishlist.","No books found",parent=window)
        return
    
    global confirm_buttons, selected_book_id, clicks
    confirm_buttons = {}
    selected_book_id = StringVar(value="")
    clicks = 0

    wishlist_window = tb.Toplevel(root)
    wishlist_window.title("Your Wishlist")
    wishlist_window.geometry("700x400")
    wishlist_window.resizable(False, False)

    top_frame = tb.Frame(wishlist_window)
    top_frame.pack(fill=BOTH, padx=10, pady=10)

    container = tb.Frame(wishlist_window)
    container.pack(fill=BOTH, expand=True)

    canvas = Canvas(container, bg="black")
    canvas.pack(side=TOP, fill=BOTH, expand=True)

    scrollbar_read = tb.Scrollbar(container, orient=HORIZONTAL, command=canvas.xview)
    scrollbar_read.pack(side=BOTTOM, fill=X)
    canvas.config(xscrollcommand=scrollbar_read.set)

    image = Image.open("assets/Images/trash-can.png")
    image = image.resize((20, 20))
    image_tk = ImageTk.PhotoImage(image)

    imageX = Image.open("assets/Images/close.png")
    imageX = imageX.resize((20, 20))
    image_tkX = ImageTk.PhotoImage(imageX)

    frame = tb.Frame(canvas, padding=10)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    images = []
    column_grid = 0

    def status_confirm():
        global clicks
        clicks += 1
        for btn in confirm_buttons.values():
            btn.grid_remove()
        if clicks % 2 != 0:
            delete_label.config(text="Select a book to delete")
            for book_id, btn in confirm_buttons.items():
                btn.grid(row=2, column=0, pady=5)
        else:
            delete_label.config(text="")

    def handle_delete(book_id):
        try:
            delete(book_id,user_id)
            wishlist_window.destroy()
            read_wishlist(root,user_id)
        except Exception as e:
            print(f"Error deleting book: {e}")


    button_delete = tb.Button(top_frame, image=image_tk, bootstyle="dark",
                               command=status_confirm)  
    button_delete.image = image_tk
    button_delete.pack(side=LEFT, padx=3)

    delete_label = tb.Label(top_frame, text="", font=("Raleway", 10), anchor="w")
    delete_label.pack(side=LEFT, padx=5)

    for book in books:
        try:
            #Getting elements from the list
            title, img_url, book_id = book[1], book[7], book[0]

            #Book Frame
            book_frame = tb.Frame(frame)
            book_frame.grid(row=0, column=column_grid, padx=10, pady=10,sticky=S)

            #Confirm Button
            confirm_button = tb.Button(
                book_frame,
                image=image_tkX,
                bootstyle="dark",
                command=lambda bid=book_id: handle_delete(bid)
            )
            confirm_buttons[book_id] = confirm_button
                
            #Getting Image
            response = requests.get(img_url)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            resized_image = image.resize((120, 180))
            img = ImageTk.PhotoImage(resized_image)
            images.append(img)

            #Button for image
            button_image = tb.Button(book_frame, image=img,
                                command=lambda t=title,uid=user_id: request_data(t,uid),
                                bootstyle="link")
            button_image.image = img

            #Label for title
            label_title = tb.Label(book_frame, text=title, font=("Raleway", 9), wraplength=120, justify="center")
            button_image.grid(row=0, column=0)
            label_title.grid(row=1, column=0)

            #Adding a column for each book 
            column_grid += 1  

        except Exception as e:
            print(f"Error loading image: {e}")

    #Update Window for Scrolling
    frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))
    wishlist_window.mainloop()


    


def main_window(root, user_id, username, password):
    global window, entry_query, image_tksearch
    print(f"UserID: {user_id}, Username: {username}, Password: {password}")

    window = tb.Toplevel(root)
    window.title("Pesquisar")
    window.geometry("350x325")
    window.resizable(False,False)

    frame = tb.Frame(window)
    frame.pack(pady=20, padx=20, fill="both", expand=True,side=LEFT)

    try:
        imagesearch = Image.open("assets/Images/research.png")
        imagesearch_resized = imagesearch.resize((100, 100))
        image_tksearch = ImageTk.PhotoImage(imagesearch_resized)

    except Exception as e:
        print(f"Erro ao carregar a imagem: {e}")


    labelimg = tb.Label(frame,image=image_tksearch)
    label = tb.Label(frame, text="Enter the book name:",foreground="white")
    entry_query = tb.Entry(frame, width=30, bootstyle="dark")
    button_search = tb.Button(frame, text="Search", 
                               command=lambda: search(entry_query,user_id), bootstyle="dark")
    button_wishlist = tb.Button(frame, text="See your wish list", 
                                 command=lambda: read_wishlist(window, user_id), bootstyle="secondary"
    )
    label_license = tb.Label(frame,text="© 2025 J.D.S. Moura – MIT.",foreground="white",font=("Raleway",7))

    label.pack(pady=5)
    labelimg.pack(pady=5)
    entry_query.pack(pady=5)
    button_search.pack(pady=5,fill=X)
    button_wishlist.pack(pady=5,fill=X)
    label_license.pack(side=BOTTOM)

    window.protocol("WM_DELETE_WINDOW", root.quit)


