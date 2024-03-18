import customtkinter as ctk
from tkinter import messagebox, simpledialog
import json

class Gui():
  def __init__(self):
    self.root = ctk.CTk()
    self.root.title('Wrap up the chaos!')
    self.root.geometry('300x250')
    self.toplevel_window = None
    self.movies_window = None

    self.label = ctk.CTkLabel(self.root, text='What do you want to wrap up?', font=('Arial', 16), fg_color="transparent")
    self.label.pack(pady=10)
    self.buttonB = ctk.CTkButton(self.root, text='Books', font=('Arial', 16), command=self.open_books, fg_color="DeepPink")
    self.buttonB.pack(pady=5)
    self.buttonM = ctk.CTkButton(self.root, text='Movies', font=('Arial', 16), command=self.open_movies, fg_color="DeepPink")
    self.buttonM.pack(pady=5)
    self.buttonI = ctk.CTkButton(self.root, text='Info', font=('Arial', 16), command=self.information, fg_color="DeepPink")
    self.buttonI.pack(pady=5)
    self.buttonQ = ctk.CTkButton(self.root, text="Quit", font=('Arial', 16), command=self.quit, fg_color="DeepPink")
    self.buttonQ.pack(pady=5)

    self.root.mainloop()

  def information(self):
    info_message = ("""This is app 'Wrap up the chaos!'. \nApp was created to help you manage your books and movies.
                 \nIf this is your first time with this app, prepare text document with titles of your books or films.""")
    messagebox.showinfo('Info', info_message)

  def open_books(self):
    if self.toplevel_window is None or not self.toplevel_window.master.winfo_exists():
      self.toplevel_window = Book(self.root)
      self.toplevel_window.master.grab_set()
      self.toplevel_window.master.focus()
    else:
      self.toplevel_window.master.focus()

  def open_movies(self):
    if self.movies_window is None or not self.movies_window.child.winfo_exists():
      self.movies_window = Movies(self.root)
      self.movies_window.child.grab_set()
    else:
      self.movies_window.child.focus()

  def quit(self):
    self.root.destroy()


class Book():
  def __init__(self, root):
    super().__init__()
    self.master = ctk.CTkToplevel(root)
    self.master.title('Books')
    self.master.geometry('300x350')
    self.master.grab_set()
    self.master.focus_set()
    self.categorize_window = None

    self.label = ctk.CTkLabel(self.master, text='Choose the option: ', font=('Arial', 16), fg_color="transparent")
    self.label.pack(pady=10)
    self.books = []
    self.loaded_books = []

    button1 = ctk.CTkButton(self.master, text='Add new books', font=('Arial', 16), command=self.add_books, fg_color="DeepPink")
    button1.pack(pady=5)
    
    button2 = ctk.CTkButton(self.master, text='Remove book', font=('Arial', 16), command=self.remove_book, fg_color="DeepPink")
    button2.pack(pady=5)

    button3 = ctk.CTkButton(self.master, text='Show books', font=('Arial', 16), command=self.show_books, fg_color="DeepPink")
    button3.pack(pady=5)

    button6 = ctk.CTkButton(self.master, text='Load from file', font=('Arial', 16), command=self.load_results, fg_color="DeepPink")
    button6.pack(pady=5)

    button4 = ctk.CTkButton(self.master, text='Categorize', font=('Arial', 16), command=self.open_categorize, fg_color="DeepPink")
    button4.pack(pady=5)

    button5 = ctk.CTkButton(self.master, text='Save to file', font=('Arial', 16), command=self.save_to_file, fg_color="DeepPink")
    button5.pack(pady=5)

    button7 = ctk.CTkButton(self.master, text="Go back", font=('Arial', 16), command=self.onbutton, fg_color="DeepPink")
    button7.pack(pady=5)


  def onbutton(self):
    self.master.destroy()


  def add_books(self):
    path = simpledialog.askstring("Add books", "Enter the path to the file:")
    try:
        with open(path, 'r') as file:
            for line in file:
              title = line.strip().capitalize() 
              book_dict = {'title': title, 'status': '', 'person': '', 'date': ''}
              self.books.append(book_dict)
        if self.books:
              messagebox.showinfo('Success', 'Books added successfully.')
              return self.books
        else:
              messagebox.showinfo('Info', 'No books were added.')
              return
    except FileNotFoundError:
        messagebox.showerror("Error", "File does not exist")
    except Exception as e:
        print("Error", f"Error occurred: {e}")
    return

  def remove_book(self):
    del_book = simpledialog.askstring("Remove Book", "Enter the title of the book you want to remove:").capitalize()
    book_found = False
    for book in self.books:
        if del_book == book['title']:
            self.books.remove(book)
            messagebox.showinfo('Success', 'Book removed successfully')
            book_found = True
            return self.books
    for loaded_book in self.loaded_books:
        if del_book == loaded_book['title']:
            self.loaded_books.remove(loaded_book)
            messagebox.showinfo('Success', 'Book removed successfully from loaded books')
            book_found = True
            return self.loaded_books
    if not book_found:
        messagebox.showinfo('Info', 'Book not found')
    return


  def show_books(self):
    if self.books:
      info_message = "\n".join([" | ".join([f'{k}: {v}' for k, v in book.items() if v != '']) for book in self.books])
      messagebox.showinfo('Books', info_message)
    elif self.loaded_books:
      info_message = "\n".join([" | ".join([f'{k}: {v}' for k, v in loaded_book.items() if v != '']) for loaded_book in self.loaded_books])
      messagebox.showinfo('Loaded Books', info_message)
    else:
      messagebox.showinfo('Info', 'No books')
    return


  def save_to_file(self):
    filename = simpledialog.askstring("Save books", "Enter the path to the file where you want to save:")
    try:
        with open(filename, 'w') as file:
          json.dump(self.books, file, indent=2)
          messagebox.showinfo('Success', f"Results saved to {filename} successfully.")
        return self.loaded_books
    except Exception as e:
        messagebox.showinfo('Info', f'Error saving results: {e}')
    return None

  def load_results(self, filename='results.json'):
    filename = simpledialog.askstring("Add books", "Enter the path to the file: ")
    try:
        with open(filename, 'r') as file:
          self.loaded_books = json.load(file)
          messagebox.showinfo('Success', f"Results loaded successfully.")
        return self.loaded_books
    except FileNotFoundError:
        messagebox.showinfo('Info', f"File {filename} not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {filename}: {e}")
    except Exception as e:
        print(f"Error loading results: {e}")
    return None


  def open_categorize(self):
    if self.categorize_window is None or not self.categorize_window.master2.winfo_exists():
      self.categorize_window = CategorizeWindow(self.master, self.books, self.loaded_books)
      self.categorize_window.master2.grab_set()
      self.categorize_window.master2.focus()
    else:
      self.categorize_window.master2.focus()

class CategorizeWindow():
  def __init__(self, master, books, loaded_books):
    super().__init__()
    self.master2 = ctk.CTkToplevel(master)
    self.master2.title('Categorize Books')
    self.master2.geometry('300x300')
    self.master2.grab_set()
    self.books = books  # Przypisujemy books do self.books
    self.loaded_books = loaded_books  # Przypisujemy loaded_books do self.loaded_books

    self.label = ctk.CTkLabel(self.master2, text='Choose the categorization option:', font=('Arial', 16), fg_color="transparent")
    self.label.pack(pady=10)

    self.button_lend = ctk.CTkButton(self.master2, text='Lend Books', font=('Arial', 16), command=self.lend_book, fg_color="DeepPink")
    self.button_lend.pack(pady=5)

    self.button_return = ctk.CTkButton(self.master2, text='Return Book', font=('Arial', 16), command=self.return_book, fg_color="DeepPink")
    self.button_return.pack(pady=5)

    self.button_read = ctk.CTkButton(self.master2, text='Read Book', font=('Arial', 16), command=self.read_book, fg_color="DeepPink")
    self.button_read.pack(pady=5)

    self.button_borrow = ctk.CTkButton(self.master2, text='Borrow Book', font=('Arial', 16), command=self.borrowed_book, fg_color="DeepPink")
    self.button_borrow.pack(pady=5)

    self.button_back = ctk.CTkButton(self.master2, text="Go back", font=('Arial', 16), command=self.goback, fg_color="DeepPink")
    self.button_back.pack(pady=5)

  def goback(self):
    self.master2.destroy()


  def borrowed_book(self):
    borrow_book = simpledialog.askstring("Borrow Book", "What book did you borrow? ").capitalize()
    borrower = simpledialog.askstring("Borrow Book", "Who did you borrow it from? ").capitalize()
    borrow_date = simpledialog.askstring("Borrow Book", "When did you borrow it? ").capitalize()
    borrowed_book = {
      'title': borrow_book,
      'status': 'Borrowed',
      'person': borrower,
      'date': borrow_date}
    if self.books is not None:
      self.books.append(borrowed_book)
      messagebox.showinfo('Success', f'Book "{borrow_book}" added to borrowed books successfully')
      return self.books
    if self.loaded_books is not None:
      self.loaded_books.append(borrowed_book)
      messagebox.showinfo('Success', f'Book "{borrow_book}" added to borrowed books successfully')
      return self.loaded_books

  def return_book(self):
    n_book = simpledialog.askstring("Return book", "Enter the title of the book it returns: ").capitalize()
    book_found = False
    for book in self.books:
      for _,_ in book.items():
        if n_book == book['title'] and book['status'] == 'Lent':
          book['status'] = ''
          book['person'] = ''
          book['date'] = ''
          book_found = True
          messagebox.showinfo('Success', 'Book status changed successfully')
          return self.books
        elif n_book == book['title'] and book['status'] != 'Lent':
          messagebox.showinfo('Info', "Book hasn't status Lent")
          book_found = True
          return self.books
    for loaded_book in self.loaded_books:
      for _,_ in loaded_book.items():
        if n_book == loaded_book['title'] and loaded_book['status'] == 'Lent':
          loaded_book['status'] = ''
          loaded_book['person'] = ''
          loaded_book['date'] = ''
          messagebox.showinfo('Success', 'Book status changed successfully')
          return self.loaded_books
        elif n_book == loaded_book['title'] and loaded_book['status'] != 'Lent':
          messagebox.showinfo('Info', "Book hasn't status Lent")
          book_found = True
          return self.loaded_books
    if not book_found:
        messagebox.showinfo('Info', 'Book not found')
    return

  def lend_book(self):
    n_book = simpledialog.askstring("Lend book", "Add book title to lent: ").capitalize()
    person = simpledialog.askstring("Lend book", "Who is lent the book? ").capitalize()
    day = simpledialog.askstring("Lend book", "When you lent the book? ").capitalize()
    book_found = False
    for book in self.books:
      for _,_ in book.items():
        if book['title'] == n_book:
            book['status'] = 'Lent'
            book['person'] = person
            book['date'] = day
            messagebox.showinfo('Success', 'Book lend sucessfully')
            book_found = True
            return self.books
    for loaded_book in self.loaded_books:
        for _,_ in loaded_book.items():
          if loaded_book['title'] == n_book:
            loaded_book['status'] = 'Lent'
            loaded_book['person'] = person
            loaded_book['date'] = day
            messagebox.showinfo('Success', 'Book lend sucessfully')
            book_found = True
            return self.loaded_books
    if not book_found:
        messagebox.showinfo('Info', 'Book not found.')
    return

  def read_book(self):
    n_book = simpledialog.askstring("Lend book", "Which book did you read? ").capitalize()
    book_found = False
    for book in self.books:
      for _,_ in book.items():
        if book['title'] == n_book:
          book['status'] = 'Read'
          messagebox.showinfo('Success', 'Book status changed successfully')
          book_found = True
          return self.books
    for loaded_book in self.loaded_books:
      for _,_ in loaded_book.items():
        if n_book == loaded_book['title']:
          loaded_book['status'] = 'Read'
          messagebox.showinfo('Success', 'Book status changed successfully')
          book_found = True
          return self.loaded_books
    if not book_found:
      messagebox.showinfo('Info', 'Book not found.')
    return

class Movies():
  def __init__(self, root):
    super().__init__()
    self.child = ctk.CTkToplevel(root)
    self.child.title('Movies')
    self.child.geometry('300x300')
    self.categorize = None
    self.movies = []

    self.label = ctk.CTkLabel(self.child, text='Choose the option: ', font=('Arial', 16), fg_color="transparent")
    self.label.pack(pady=10)

    button1 = ctk.CTkButton(self.child, text='Add movies', font=('Arial', 16), command=self.add_movies,
                            fg_color="DeepPink")
    button1.pack(pady=5)

    button2 = ctk.CTkButton(self.child, text='Show movies', font=('Arial', 16), command=self.show_movies,
                            fg_color="DeepPink")
    button2.pack(pady=5)

    button3 = ctk.CTkButton(self.child, text='Categorize', font=('Arial', 16), command=self.open_categorize,
                            fg_color="DeepPink")
    button3.pack(pady=5)

    button4 = ctk.CTkButton(self.child, text='Save to file', font=('Arial', 16), command=self.save_to_file,
                            fg_color="DeepPink")
    button4.pack(pady=5)

    button5 = ctk.CTkButton(self.child, text="Go back", font=('Arial', 16), command=self.go_back, fg_color="DeepPink")
    button5.pack(pady=5)

  def add_movies(self):
    path = simpledialog.askstring("Add movies", 'Enter the path to the file: ')
    try:
      with open(path, 'r') as file:
        for line in file:
          title = line.strip().capitalize()
          movie_dict = {'title': title, 'status': ''}
          self.movies.append(movie_dict)
      if self.movies:
        messagebox.showinfo('Success', 'Movies added successfully.')
        return self.movies
      else:
        messagebox.showinfo('Info', 'No movies were added.')
        return
    except FileNotFoundError:
      messagebox.showerror("Error", "File does not exist")
    except Exception as e:
      print(f"Error occured: {e}")
    return

  def show_movies(self):
    if self.movies:
      movie_info = "\n".join([" | ".join([f'{k}: {v}' for k, v in movie.items() if v != '']) for movie in self.movies])
      messagebox.showinfo('Movies', movie_info)
    else:
      messagebox.showinfo('Info', 'No movies.')
    return

  def save_to_file(self):
    filename = simpledialog.askstring("Add movies", 'Enter the path to save the file: ')
    try:
      with open(filename, 'w') as file:
        json.dump(self.movies, file, indent=2)
        messagebox.showinfo('Success', f'Results saved to {filename} successfully.')
      return
    except Exception as e:
      print(f'Error saving results: {e}')
    return None

  def go_back(self):
    self.child.destroy()
  def open_categorize(self):
    if self.categorize is None or not self.categorize.winfo_exists():
      self.categorize = Categorize(self.child, self.movies)
      self.categorize.grab_set()
      self.categorize.focus()
    else:
      self.categorize.focus()


class Categorize(ctk.CTkToplevel):
  def __init__(self, child, movies):
    super().__init__(child)
    self.title('Categorize Books')
    self.geometry('260x150')
    self.movies = movies

    self.label = ctk.CTkLabel(self, text='Choose the categorization option:', font=('Arial', 16),
                                fg_color="transparent")
    self.label.pack(pady=10)

    self.button_lend = ctk.CTkButton(self, text='Watched', font=('Arial', 16), command=self.watch_movie,
                                       fg_color="DeepPink")
    self.button_lend.pack(pady=5)

    self.button = ctk.CTkButton(self, text='Go back', font=('Arial', 16), command=self.goback,
                                       fg_color="DeepPink")
    self.button.pack(pady=5)

  def watch_movie(self):
    movie = simpledialog.askstring("Movie", 'Which movie did you watched: ?').capitalize()
    movie_found = False
    for m in self.movies:
      for _, _ in m.items():
        if m['title'] == movie:
          m['status'] = 'Watched'
          messagebox.showinfo('Success', 'Movie status changed successfully.')
          movie_found = True
          return self.movies
    if not movie_found:
      messagebox.showinfo('Info', 'Movie not found')
    return

  def goback(self):
    self.destroy()


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = Gui()




