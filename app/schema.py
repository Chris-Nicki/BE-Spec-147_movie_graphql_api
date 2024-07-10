import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import Movie
from app import db


class MovieType(SQLAlchemyObjectType):
    class Meta:
        model = Movie

class AddNewMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        release_year = graphene.String(required=True)
        genre = graphene.String(required=True)
        rating = graphene.String(required=True)

    movie = graphene.Field(MovieType)
        
    def mutate(root, info, title, director, release_year, genre, rating):
        new_movie = Movie(title=title, director=director, release_year=release_year, genre=genre, rating=rating)
        return AddNewMovie(movie=new_movie)

class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)
        title = graphene.String()
        director = graphene.String()
        release_year = graphene.String()
        genre = graphene.String()
        rating = graphene.String()

    movie = graphene.Field(MovieType)

    def mutate(root, info, id, title=None, director=None, release_year=None, genre=None, rating=None):
        movie = db.session.get(Movie, id)
        if movie is None:
            return None
        if title:
            movie.title = title
        if director:
            movie.director = director
        if release_year:
            movie.release_year = release_year
        if genre:
            movie.genre = genre
        if rating:
            movie.rating =rating
        return UpdateMovie(movie=movie)

class DeleteMovie(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    message = graphene.String()

    def mutate(root, info, id):
        movie = db.session.get(Movie, id)
        if movie is None:
            return DeleteMovie(message=f"Movie with ID {id} does not exist")
        else:
            db.session.delete(movie)
            db.session.commit()
            return DeleteMovie(message='Movie has been deleted')


class Query(graphene.ObjectType):
    movies = graphene.List(MovieType)
    movie = graphene.Field(MovieType, movie_id=graphene.ID(required=True))
    search_movies = graphene.List(MovieType, title=graphene.String())

    def resolve_movies(root, info):
        query = db.select(Movie)
        return db.session.scalars(query)
    
    def resolve_movie(root, self, title):
        query = db.session.get(Movie, title)
        return db.session.scalars(query)
    
    def resolve_search_movies(root, info, id=None, title=None, director=None):
        query = db.select(Movie)
        if id:
            query = query.where(Movie.id.ilike(f"%{id}%"))
        if title:
            query = query.where(Movie.id.ilike(f"%{title}"))
        if director:
            query = query.where(Movie.director.ilike(f"%{director}"))
        return db.session.scalars(query)
    
class Mutation(graphene.ObjectType):
    add_new_movie = AddNewMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()

        
    
schema = graphene.Schema(query=Query)