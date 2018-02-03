from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base, User, Categories, CategoryItem

engine = create_engine('sqlite:///itemCatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(username="Peter", email="peter@example.com")
User1.password_hash = User1.hash_password('Pan')
session.add(User1)
session.commit()

# Category Soccer
category1 = Categories(user_id=1, name="Soccer")

session.add(category1)
session.commit()

category1_item1 = CategoryItem(
       name="Balls",
       description="A football is a ball inflated with air that is used to "
       "play one of the various sports known as football.",
       price="$9.99",
       category_id=1,
       categories=category1,
       user_id=1,
       user=User1)

session.add(category1_item1)
session.commit()

category1_item2 = CategoryItem(
       name="Gloves",
       description=" Goalkeepers wear gloves to protect their hands and "
       "enhance their grip of the ball.",
       price="$4.99",
       category_id=1,
       categories=category1,
       user_id=1,
       user=User1)

session.add(category1_item2)
session.commit()


# Category Basketball
category2 = Categories(user_id=1, name="Basketball")

session.add(category2)
session.commit()

category2_item1 = CategoryItem(
       name="Air Jordan",
       description="Air Jordan is a brand of basketball footwear and "
       "athletic clothing produced by Nike. It was created for "
       "former professional basketball player, Michael Jordan.",
       price="$499.99",
       category_id=2,
       categories=category2,
       user_id=1,
       user=User1)

session.add(category2_item1)
session.commit()

category2_item2 = CategoryItem(
       name="Backboard",
       description="A backboard is a piece of basketball equipment. "
       "It is a raised vertical board with a basket attached.",
       price="$19.99",
       category_id=2,
       categories=category2,
       user_id=1,
       user=User1)

session.add(category2_item2)
session.commit()


# Category Baseball
category3 = Categories(user_id=1, name="Baseball")

session.add(category3)
session.commit()

category3_item1 = CategoryItem(
       name="Bat",
       description="A baseball bat is a smooth wooden or metal club used "
       "in the sport of baseball to hit the ball after it is thrown "
       "by the pitcher.",
       price="$9.99",
       category_id=3,
       categories=category3,
       user_id=1,
       user=User1)

session.add(category3_item1)
session.commit()


# Category Hockey
category4 = Categories(user_id=1, name="Hockey")

session.add(category4)
session.commit()

category4_item1 = CategoryItem(
       name="Stick",
       description="A hockey stick is a piece of equipment used by the "
       "players in most forms of hockey to move the ball or puck.",
       price="$14.99",
       category_id=4,
       categories=category4,
       user_id=1,
       user=User1)

session.add(category4_item1)
session.commit()


# Create dummy user
User2 = User(username="Jon", email="jon@example.com")
User2.password_hash = User2.hash_password('Nash')
session.add(User2)
session.commit()

# Category Snowboarding
category5 = Categories(user_id=2, name="Snowboarding")

session.add(category5)
session.commit()

category5_item1 = CategoryItem(
       name="Snowboard",
       description="A snowboard is a flat board with bindings that hold "
       "your feet in place while gliding down the mountain.",
       price="$9.99",
       category_id=5,
       categories=category5,
       user_id=2,
       user=User2)

session.add(category5_item1)
session.commit()

category5_item2 = CategoryItem(
       name="Goggles",
       description="Snow goggles are a type of eyewear traditionally used "
       "to prevent snow blindness.",
       price="$14.99",
       category_id=5,
       categories=category5,
       user_id=2,
       user=User2)

session.add(category5_item2)
session.commit()

# Category Rock Climbling
category6 = Categories(user_id=2, name="Rock Climbing")

session.add(category6)
session.commit()

category6_item1 = CategoryItem(
       name="Harness",
       description="A climbing harness is an item of climbing equipment for "
       "rock-climbing requiring the use of ropes to provide access or safety.",
       price="$24.99",
       category_id=6,
       categories=category6,
       user_id=2,
       user=User2)

session.add(category6_item1)
session.commit()

category6_item2 = CategoryItem(
       name="Quickdraw",
       description="Quickdraw is a piece of climbing equipment used by rock "
       "climbers to allow the climbing rope to run freely through bolt "
       "anchors or other protection while leading.",
       price="$4.99",
       category_id=6,
       categories=category6,
       user_id=2,
       user=User2)

session.add(category6_item2)
session.commit()
print "added items!"
