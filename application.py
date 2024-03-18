import json

class App:
  information = 'Wrap up the chaos!'
  version = '2024.IV'
  badchoice = 'You chose a bad choice: {}'
  prompt = 'What do you want to do? '
  quit = -1

  def __init__(self):
    self.menu = {}
    self.actions = {}
    self.books = []
    self.loaded_books = []
    self.movies = []
    self.loaded_movies = []
    self.more_chosen = False
    self.opt('I', 'Info', self.info)
    self.opt('M', 'More', self.more)
    self.opt('Q', 'Quit', self.quit)

  def info(self):
    message = """This is app {}, version {}.\nApp was created to help you manage your books.\nIf this is your first time with this app, prepare text document with titles of your books or films."""
    print(message.format(self.information, self.version))

  def choice(self):
    print('\n'.join('[{}] {}'.format(k, v) for k, v in self.menu.items()))
    return input(self.prompt).upper()

  def opt(self, key, value, procedure):
    self.menu[key] = value
    self.actions[key] = procedure

  def print_badchoice(self, option):
    print(self.badchoice.format(option))

  def run_app(self):
    status = True
    while status:
      opt = self.choice()
      try:
        result = self.actions[opt]()
        status = result != self.quit and not self.more_chosen
        if not status:
          return self.quit
      except KeyError:
        self.print_badchoice(opt)
        
  def quit(self):
    return self.quit

  def more(self):
    self.more_chosen = True
    self.navigate_to(MainApp) 

  def navigate_to(self, target_class):
    new_instance = target_class(self) if self.more_chosen else target_class()
    new_instance.run_app()

class MainApp(App):
  def __init__(self, parent=None):
    super().__init__()
    self.parent = parent
    self.opt('B', 'Books', self.bookshelf)
    self.opt('MV', 'Movies', self.manage_movies)
    
  def bookshelf(self):
    try:
      self.more_chosen = True
      self.navigate_to(BookShelf)
    except Exception as e:
      print(f"Error occured: {e}")

  def manage_movies(self):
    try:
      self.more_chosen = True
      self.navigate_to(Movies)
    except Exception as e:
      print(f"Error occured: {e}")

def navigate_to(self, target_class):
  new_instance = target_class(self) if self.more_chosen else target_class()
  new_instance.run_app()
      
class BookShelf(App):
  def __init__(self, parent=None):
    super().__init__()
    self.parent = parent
    self.opt('A', 'Add new books', self.add_books)
    self.opt('R', 'Remove book', self.remove_book)
    self.opt('S', 'Show books', self.show_books)
    self.opt('C', 'Categorize', self.categorize)
    self.opt('SA', 'Save to file', self.save_to_file)
    self.opt('LO', 'Load from file', self.load_results)
    self.opt('G', 'Go back', self.go_back)

  def add_books(self):
    path = input('Enter the path to the file: ')
    try:
      with open(path, 'r') as file:
        for line in file:
          title = line.strip().capitalize()
          book_dict = {'title': title, 'status': '', 'person': '', 'date': ''}
          self.books.append(book_dict)
      if self.books:
        print('Books added successfully.')
        return self.books
      else:
        print('No books were added.')
        return
    except FileNotFoundError:
      print("File does not exist")
    except Exception as e:
      print(f"Error occured: {e}")
    return

  def remove_book(self):
    del_book = input('What book do you want to remove? ').capitalize()
    book_found = False
    for book in self.books:
      for _, _ in book.items():
        if del_book == book['title']:
          self.books.remove(book)
          print('Book removed successfully')
          book_found = True
          return self.books
    for loaded_book in self.loaded_books:
      for _, _ in loaded_book.items():
        if del_book == loaded_book['title']:
          self.loaded_books.remove(loaded_book)
          print('Book removed successfully')
          book_found = True
          return self.loaded_books
    if not book_found:
      print('Book not found')
    return

  def show_books(self):
    if self.books:
      for book in self.books:
        book_info = [f'{k}: {v}' for k, v in book.items() if v != '']
        print(' | '.join(book_info))
    elif self.loaded_books:
      for loaded_book in self.loaded_books:
        loaded_book_info = [f'{k}: {v}' for k, v in loaded_book.items() if v != '']
        print(' | '.join(loaded_book_info))
    else:
      print('No books')
    return

  def categorize(self):
    print('If you want to categorize books, please give the full book title.')
    self.opt('BR', 'Borrow book', self.borrowed_book)
    self.opt('RT', 'Return book', self.return_book)
    self.opt('L', 'Lend Books', self.lend_book)
    self.opt('RD', 'Read book', self.read_book)

  def borrowed_book(self):
    borrow_book = input('What book did you borrow? ').capitalize()
    borrower = input('Who did you borrow it from? ').capitalize()
    borrow_date = input('When did you borrow the book? ')
    deadline_date = input('When do you have to return this book? ')
    borrowed_book = {
        'title': borrow_book,
        'status': 'Borrowed',
        'person': borrower,
        'date': borrow_date,
        'deadline': deadline_date
    }
    if self.books is not None:
      self.books.append(borrowed_book)
      print(f'Book "{borrow_book}" added successfully')
      return self.books
    else:
      print("No books")
    if self.loaded_books is not None:
      self.loaded_books.append(borrowed_book)
      print(f'Book "{borrow_book}" added successfully')
      return self.loaded_books
    else:
      print("No books")
      return

  def return_book(self):
    n_book = input('Enter the title of the book returned: ').capitalize()
    book_found = False
    for book in self.books:
      for _, _ in book.items():
        if n_book == book['title'] and book['status'] == 'Lent':
          book['status'] = ''
          book['person'] = ''
          book['date'] = ''
          print('Book status changed successfully')
          book_found = True
          return self.books
        elif n_book == book['title'] and book['status'] != 'Lent':
          print(f'Chosen book "{n_book}" has no status: Lent')
          book_found = True
          return self.books
    for loaded_book in self.loaded_books:
      for _, _ in loaded_book.items():
        if n_book == loaded_book['title'] and loaded_book['status'] == 'Lent':
          loaded_book['status'] = ''
          loaded_book['person'] = ''
          loaded_book['date'] = ''
          print('Book status changed successfully')
          book_found = True
          return self.loaded_books
        elif n_book == loaded_book['title'] and loaded_book['status'] != 'Lent':
          print(f'Chosen book "{n_book}" has no status: Lent')
          book_found = True
          return self.books
    if not book_found:
      print('Book not found')
    return

  def lend_book(self):
    n_book = input('Add book title to lent: ').capitalize()
    person = input('Who is lent the book? ').capitalize()
    day = input('When you lent the book? ')
    book_found = False
    for book in self.books:
      for _, _ in book.items():
        if book['title'] == n_book:
          book['status'] = 'Lent'
          book['person'] = person
          book['date'] = day
          print('Book status changed successfully')
          book_found = True
          return self.books
    for loaded_book in self.loaded_books:
      for _, _ in loaded_book.items():
        if loaded_book['title'] == n_book:
          loaded_book['status'] = 'Lent'
          loaded_book['person'] = person
          loaded_book['date'] = day
          print('Book status changed successfully')
          book_found = True
          return self.loaded_books
    if not book_found:
      print('Book not found')
    return

  def read_book(self):
    n_book = input('Which book did you read? ').capitalize()
    book_found = False
    for book in self.books:
      for _, _ in book.items():
        if book['title'] == n_book:
          book['status'] = 'Read'
          print('Book status changed successfully')
          book_found = True
          return self.books
    for loaded_book in self.loaded_books:
      for _, _ in loaded_book.items():
        if loaded_book['title'] == n_book:
          loaded_book['status'] = 'Read'
          print('Book status changed successfully')
          book_found = True
          return self.loaded_books
    if not book_found:
      print('Book not found')
    return

  def save_to_file(self):
    filename = input('Enter path to save the file: ')
    try:
      with open(filename, 'w') as file:
        json.dump(self.books, file, indent=2)
        print(f'Results saved to {filename} successfully.')
      return self.loaded_books
    except Exception as e:
      print(f'Error saving results: {e}')
    return None

  def load_results(self):
    filename = input('Enter path to the file: ')
    try:
      with open(filename, 'r') as file:
        self.loaded_books = json.load(file)
        print('Results loaded successfully.')
      return self.loaded_books
    except FileNotFoundError:
      print(f'File {filename} not found.')
    except json.JSONDecodeError as e:
      print(f'Error decoding JSON in {filename}: {e}')
    except Exception as e:
      print(f'Error loading results: {e}')
    return None
    
  def go_back(self):
    main_app = MainApp()
    main_app.run_app()
    return
    
class Movies(App):
  def __init__(self, parent=None):
    super().__init__()
    self.parent = parent
    self.opt('A', 'Add movies', self.add_movies)
    self.opt('S', 'Show movies', self.show_movies)
    self.opt('C', 'Categorize', self.categorize)
    self.opt('SA', 'Save to file', self.save_to_file)
    self.opt('LO', 'Load from file', self.load_results)
    self.opt('G', 'Go back', self.go_back)

  def add_movies(self):
    path = input('Enter the path to the file: ')
    try:
      with open(path, 'r') as file:
        for line in file:
          title = line.strip().capitalize()
          movie_dict = {'title': title, 'status': ''}
          self.movies.append(movie_dict)
      if self.movies:
        print('Movies added successfully.')
        return self.movies
      else:
        print('No movies were added.')
        return
    except FileNotFoundError:
      print("File does not exist")
    except Exception as e:
      print(f"Error occured: {e}")
    return

  def show_movies(self):
    if self.movies:
      for movie in self.movies:
        movie_info = [f'{k}: {v}' for k, v in movie.items() if v != '']
        print(' | '.join(movie_info))
    elif self.loaded_movies:
      for loaded_movie in self.loaded_movies:
        loaded_movie_info = [f'{k}: {v}' for k, v in loaded_movie.items() if v != '']
        print(' | '.join(loaded_movie_info))
    else:
      print('No movies')
    return

  def categorize(self):
    print('If you want to categorize movies, please give the full movie title.')
    self.opt('W', 'Watched movie', self.watch_movie)

  def watch_movie(self):
    movie = input("Which movie you've watched? ").capitalize()
    movie_found = False
    for m in self.movies:
      for _, _ in m.items():
        if m['title'] == movie:
          m['status'] = 'Watched'
          print('Movie status changed successfully')
          movie_found = True
          return self.movies
    for m in self.loaded_movies:
      for _, _ in m.items():
        if m['title'] == movie:
          m['status'] = 'Watched'
          print('Movie status changed successfully')
          movie_found = True
          return self.loaded_movies
    if not movie_found:
      print('Movie not found')
    return

  def save_to_file(self):
    filename = input('Enter path to save the file: ')
    try:
      with open(filename, 'w') as file:
        json.dump(self.movies, file, indent=2)
        print(f'Results saved to {filename} successfully.')
      return
    except Exception as e:
      print(f'Error saving results: {e}')
    return None
    
  def load_results(self):
    filename = input('Enter path to the file: ')
    try:
      with open(filename, 'r') as file:
        self.loaded_movies = json.load(file)
        print('Results loaded successfully.')
      return self.loaded_books
    except FileNotFoundError:
      print(f'File {filename} not found.')
    except json.JSONDecodeError as e:
      print(f'Error decoding JSON in {filename}: {e}')
    except Exception as e:
      print(f'Error loading results: {e}')
    return None
  
  def go_back(self):
    main_app = MainApp()
    main_app.run_app()
    return
    
if __name__ == '__main__':
  main = App()
  main.run_app()
