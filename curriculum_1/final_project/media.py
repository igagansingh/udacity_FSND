class Movie():
    """
        ==========================
            Movie DataStructure
        ==========================
        This class provides a way to store movie related information.
        The information stored is :
            1.) Title
            2.) Poster
            3.) Trailer URL
            4.) Running time
            5.) Rating provided by IMDb
    """

    def __init__(self, movie_title, poster_image, trailer_youtube,
                 running_time, imdb_rating):
        self.title = movie_title
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube
        self.running_time = running_time
        self.imdb_rating = imdb_rating
