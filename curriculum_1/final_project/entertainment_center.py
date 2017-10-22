import media    # media file is imported to use Movie class.
import fresh_tomatoes    # fresh_tomatoes to dynamically create the website.

toy_story = media.Movie("Toy Story",
                        "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Toy_Story.jpg/220px-Toy_Story.jpg",
                        "https://www.youtube.com/watch?v=KYz2wyBy3kc",
                        "81",
                        "8.3")

avatar = media.Movie("Avatar",
                     "https://upload.wikimedia.org/wikipedia/en/b/b0/Avatar-Teaser-Poster.jpg",
                     "https://www.youtube.com/watch?v=5PSNL1qE6VY",
                     "162",
                     "7.8")

godfather = media.Movie("The Godfather",
                        "https://upload.wikimedia.org/wikipedia/en/1/1c/Godfather_ver1.jpg",
                        "https://www.youtube.com/watch?v=sY1S34973zA",
                        "178",
                        "9.2")

shawshank = media.Movie("The Shawshank Redemption",
                        "https://upload.wikimedia.org/wikipedia/en/8/81/ShawshankRedemptionMoviePoster.jpg",
                        "https://www.youtube.com/watch?v=6hB3S9bIaco",
                        "142",
                        "9.3")

# An array of movies to be passed as an argument to fresh_tomatoes function
movies = [toy_story, avatar, godfather, shawshank]

# From here on 'fresh_tomatoes' 'open_movie_page' function will be called which
# will in turn create a web page dynamically and open the same in an browser
fresh_tomatoes.open_movies_page(movies)
