from typing import List

import strawberry
import strawberry_django
from strawberry import auto
from .models import Book
from dataclasses import asdict
from typing import Annotated, List, Union




@strawberry_django.type(Book)
class BookType:
  id: auto
  title: auto
  author: auto
  published_date: auto

@strawberry_django.input(Book)
class BookInput:
  title: str
  author: str
  published_date: str

@strawberry_django.input(Book)
class BookUpdateInput:
  title: str | None = None
  author: str | None = None
  published_date: str | None = None

@strawberry.type
class Error:
  message: str

@strawberry.type
class Success:
    result: bool

Response = Annotated[
    Union[BookType, Error],
    strawberry.union("BookResponse")
]

DeleteResponse = Annotated[
    Union[Success, Error],
    strawberry.union("DeleteResponse")
]


@strawberry.type
class Mutation:
  create_book: BookType = strawberry_django.mutations.create(BookInput)

  @strawberry.mutation
  def update_book(self, book_id: int, data: BookUpdateInput) ->Response:
    try:
      book = Book.objects.get(id=book_id)
      for key, value in asdict(data).items():
        if value is not None:
          setattr(book, key, value)
      
      book.save()

      return book
    except Book.DoesNotExist:
      raise Error(message="Not Found")
    except Exception as e:
      return Error(f"An error occurred: {str(e)}")
  
  @strawberry.mutation
  def delete_book(self, book_id: int) -> DeleteResponse:
    try:
      book = Book.objects.get(pk=book_id)
      book.delete()

      return Success(result=True)
    except Book.DoesNotExist:
      raise Error(message="Not Found")
    except Exception as e:
      return Error(f"An error occurred: {str(e)}")

@strawberry.type
class Query:
  books: List[BookType] = strawberry_django.field()

schema = strawberry.Schema(query=Query, mutation=Mutation)

"""

    Convertimos nuestro Bookmodelo a un tipo Strawberry, asignando 
    los campos del modelo a campos GraphQL mediante el 
    @strawberry_django.typedecorador. La autoutilidad de Strawberry 
    se utiliza para inferir automáticamente los tipos de campo, 
    garantizando así la coherencia entre el modelo de Django y 
    el esquema GraphQL.

    La Queryclase define el tipo de consulta raíz para nuestra API 
    GraphQL. Este Querytipo se utiliza para definir las consultas 
    que los clientes pueden ejecutar sobre nuestros datos. En este 
    caso, solo tiene un campo booksque, al consultarse, devolvería 
    una lista de BookTypeobjetos. Dado que hemos asignado BookTypeel 
    tipo al Bookmodelo, la consulta booksconsultaría 
    automáticamente todos Booklos objetos de la base de datos.

"""