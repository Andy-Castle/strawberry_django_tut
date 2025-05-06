# How to setup enviroment in windows

```
python -m venv .env

.env\Scripts\activate

pip install django

pip install 'strawberry-graphql[debug-server]'

pip install strawberry-graphql-django

python manage.py runserver
```

## In case you dont have the database use this commands

```
python manage.py makemigrations

python manage.py migrate
```

### How to use GraphQL

CREATE

```
mutation CREATE_BOOKS {
  createBook(data: {
    title: "My New Book",
    author: "Oluwole",
    publishedDate: "2024-05-31"
  }) {
    id
    title
  }
}
```

GET

```
query GET_BOOKS {
  books {
    id
    title
    author
    publishedDate
  }
}
```

UPDATE

```
mutation UPDATE_BOOK {
  updateBook(bookId: 2, data: {
    title: "Updated Title Book"
  }){
    __typename
    ... on BookType {
      id
      title
    }
    ... on Error {
      message
    }
  }
}
```

DELETE

```
mutation DELETE_BOOK {
  deleteBook(bookId: 2){
    __typename
    ... on Success {
      result
    }
    ... on Error {
      message
    }
  }
}
```

#### Other commands for testing

```
pip install pytest pytest-django

python -m pytest
```

##### Esto es de los anteriores UPDATE y DELETE

```
mutation UPDATE_BOOK {
  updateBook(bookId:1, data: {
    title: "My Biography"
  }){
    id
    title
  }
}

mutation DELETE_BOOK {
  deleteBook(bookId: 1)
}

```
