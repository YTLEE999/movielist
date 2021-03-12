# MovieList
Using the movieDB APIs to build a python + flask + SQLite website with movie info

## What is this

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/flowchart.jpg)

This is a website that you can find some recommend movies from latest to top rated movies.

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/movielist_%20home.gif)

Want to make your own interested movie list? Sign up an account and you can store the movie in your "My List".

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/movielist_%20register.gif)

The list is editable. You can not only add a movie but also deleting movies from your list.

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/movielist_add&delete.gif)

## Features

This website can be separated into 3 parts:

- It's a full-stack project: Python + Flask + Jinja2 + SQLite
- Using API to receive data
- Ensuring user account is safe with authentication and password management

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/features.JPG)

## How it runs

The document is simple, but with the structure could make easier and faster to read.

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/structure.JPG)

#### Web framework

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/flask_basic_template.JPG)

#### Configuring with flask

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/flask_basic_template.JPG)

#### TMDB APIs

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/api.JPG)

#### User account

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/useraccount.jpg)

#### Database

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/database_relations.JPG)

The database is one-to-one relation. The user's id is the key to connect the 2 model: user and movie.

![](https://github.com/YTLEE999/movielist/blob/9de54970ca11fe24ec29d9328a87e4351c599684/demo/database.JPG)
