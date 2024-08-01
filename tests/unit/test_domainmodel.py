import pytest
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Playlist, Review
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    with pytest.raises(ValueError):
        podcast3 = Podcast(-123, "Todd Clayton")

    podcast4 = Podcast(123, " ")
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "<User 1: shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) == "<User 3: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[<PodcastSubscription 1: Owned by shyamli>]"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 1
    my_user.remove_subscription(my_subscription)
    assert repr(my_user.subscription_list) == "[]"


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User 1: shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1


def test_playlist_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    playlist1 = Playlist(2, "My Podcasts 1", user1)
    assert playlist1.id == 2
    assert playlist1._owner == user1
    assert playlist1.title == "My Podcasts 1"
    assert playlist1.image is None

    assert repr(playlist1) == "<Playlist 2: My Podcasts 1>"

    with pytest.raises(ValueError):
        playlist2 = Playlist("My Podcasts 2", -999)

    playlist3 = Playlist(1)
    assert playlist3.id == 1
    assert playlist3.title == "Untitled"
    assert playlist3._owner is None


def test_playlist_equality():
    user1 = User(1, "Shyamli", "pw12345")
    playlist1 = Playlist(1, "My Podcasts 1", user1)
    playlist2 = playlist1
    assert playlist1 == playlist2


def test_playlist_hash():
    user1 = User(1, "Shyamli", "pw12345")
    playlist1 = Playlist(1, "My Podcasts 1", user1)
    playlist2 = Playlist(1, "My Podcasts 1", user1)
    sub_set = {playlist1 == playlist2}
    assert len(sub_set) == 1


def test_playlist_lt():
    playlist1 = Playlist(1, "Podcasts 1")
    playlist2 = Playlist(2, "Podcasts 2")
    playlist3 = Playlist(3, "Podcasts 3")

    assert playlist1 < playlist2
    assert playlist1 < playlist3
    assert playlist2 < playlist3
    assert playlist3 > playlist1
    assert playlist3 > playlist2

    playlist_list = [playlist3, playlist2, playlist1]
    assert sorted(playlist_list) == [playlist1, playlist2, playlist3]

def test_episode(my_podcast):
    episode1 = Episode(1, "Ep1", 100, "09-02-2005", "once upon a time..", my_podcast)
    assert episode1.id == 1
    assert episode1.title == "Ep1"
    assert episode1.description == "once upon a time.."
    assert episode1.date == "09-02-2005"
    assert episode1.audio_length == 100

    assert repr(episode1) == "<Episode 1: by <Author 1: Joe Toste>>"
    with pytest.raises(ValueError):
        episode2 = Episode(-1, "Ep1", 100, "09-02-2005", "once upon a time..", my_podcast)

    with pytest.raises(ValueError):
        episode3 = Episode(1, "Ep1", -100, "09-02-2005", "once upon a time..", my_podcast)

    with pytest.raises(ValueError):
        episode4 = Episode(1, "Ep1", 100, " ", "once upon a time..", my_podcast)

    with pytest.raises(ValueError):
        episode5 = Episode(1, "Ep1", 100, "", "once upon a time..", my_podcast)

    with pytest.raises(ValueError):
        episode6 = Episode(1, "", 100, "09-02-2005", "once upon a time..", my_podcast)

    with pytest.raises(ValueError):
        episode7 = Episode(1, "Ep1", 100, "09-02-2005", "", my_podcast)

    episode1.title = "Ep2"
    episode1.date = "08-01-2004"
    episode1.description = "twice upon a time.."
    episode1.audio_length = 99

    assert episode1.id == 1
    assert episode1.title == "Ep2"
    assert episode1.description == "twice upon a time.."
    assert episode1.date == "08-01-2004"
    assert episode1.audio_length == 99
    

def test_review_initialization():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    review1 = Review(1, user1, podcast1, 3, 'Hello World')
    review2 = Review(2, user2, podcast2, 7, 'Goodbye World')
    review3 = Review(3, user3, podcast3, 9, 'Lorem Ipsum    ')

    assert repr(review1) == "<Review 1: Written by 'shyamli' about 'Joe Toste Podcast - Sales Training Expert'>"
    assert repr(review2) == "<Review 2: Written by 'asma' about 'Voices in AI'>"
    assert repr(review3) == "<Review 3: Written by 'jenny' about 'Law Talk'>"
    assert review3.rating == 9
    assert review3.comment == "Lorem Ipsum"

    with pytest.raises(TypeError):
        review4 = Review(4, 3, podcast3, 6, 'Hellowork')

    with pytest.raises(TypeError):
        review5 = Review(5, user2, "hello", 1, "goodbye")

    with pytest.raises(TypeError):
        review6 = Review(6, user2, podcast2, 9, 33)

    with pytest.raises(TypeError):
        review7 = Review(7, user2, podcast1, user2, "Excellent podcast")
        
    with pytest.raises(ValueError):
        review8 = Review("haha", user1, podcast1, 2, "meh")

    with pytest.raises(ValueError):
        review9 = Review(-3, user1, podcast3, 2, "ok")    

    with pytest.raises(ValueError):
        review10 = Review(9, user1, podcast3, 23, "funny")    

def test_review_set_rating():
    user1 = User(1, "   Shyamli", "pw12345")
    author1 = Author(1, "Author A")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    review1 = Review(1, user1, podcast1, 3, 'Hello World')
    review1.rating = 4
    assert review1.rating == 4

    with pytest.raises(TypeError):
        review1.rating = "not a rating"

    with pytest.raises(ValueError):
        review1.rating = 99

def test_review_set_comment():
    user1 = User(1, "   Shyamli", "pw12345")
    author1 = Author(1, "Author A")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    review1 = Review(1, user1, podcast1, 3, 'Hello World')

    review1.comment = "Haha"
    assert review1.comment == "Haha"

    with pytest.raises(ValueError):
        review1.comment = 93
    
def test_review_equality():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    review1 = Review(1, user1, podcast1, 3, 'Hello World')
    review2 = Review(1, user2, podcast2, 7, 'Goodbye World')
    review3 = Review(3, user3, podcast3, 9, 'Lorem Ipsum    ')

    assert review1 == review2
    assert review1 != review3

def test_review_lt():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    review1 = Review(1, user1, podcast1, 3, 'Hello World')
    review2 = Review(2, user2, podcast2, 7, 'Goodbye World')
    review3 = Review(3, user3, podcast3, 9, 'Lorem Ipsum    ')

    assert review2 > review1
    assert review1 < review3
    assert review2 < review3
    review_list = [review2, review3, review1]
    assert sorted(review_list) == [review1, review2, review3]

def test_review_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    author1 = Author(1, "Author A")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    review1 = Review(1, user1, podcast1, 3, 'Hello World')
    review2 = Review(1, user1, podcast1, 4, 'Good Evening')
    review_set = {review1, review2}
    assert len(review_set) == 1