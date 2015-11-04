from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catalog, Base, CatalogItem, User

engine = create_engine('postgresql://catalog:cat15log@localhost/catalogitems')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until the
# session.commit().

session = DBSession()

# Create dummy user
User1 = User(name="D. McCann", email="dmccann@ameritech.net",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()

User2 = User(name="Jane Doe", email="jdoe@hotmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User2)
session.commit()

# Beds Catagory items in catalog
category1 = Catalog(user_id=1, name="Beds")

session.add(category1)
session.commit()

## add catalog items
catalogItem1 = CatalogItem(user_id=1, name="Fleece Pet Bed", description="Soft sythetic sheepskin bed that fits in most crates",
                     price="$7.50", catalog=category1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Elevated Pet Bed", description="sturdy PVC frame that keeps dog above the hard, cold, uncomfortable ground",
                     price="$27.50", catalog=category1)
session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Pet Pad", description="self-cooling cushion that cools without refridgeration or water",
                     price="$14.99", catalog=category1)

session.add(catalogItem3)
session.commit()


# Crates Catagory items in catalog
category2 = Catalog(user_id=2, name="Crates")

session.add(category2)
session.commit()


## add catalog items
catalogItem1 = CatalogItem(user_id=2, name="Sky Pet Kennel", description="Best crate for traveling, and preferred by airlines",
                     price="$34.99", catalog=category2)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=2, name="Folding Crate", description="Easy to fold and transport crate.  Expands with growth dog",
                     price="$15.50", catalog=category2)
session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=2, name="Soft Crate", description="Crate made out of soft durable fabric.  Lightweight and portable",
                     price="$44.99", catalog=category2)

session.add(catalogItem3)
session.commit()


# Food Catagory items in catalog
category1 = Catalog(user_id=1, name="Food")

session.add(category1)
session.commit()

## add catalog items
catalogItem1 = CatalogItem(user_id=1, name="Beef & Potato Dry dog food", description="15lb bag of dry dog food formulated to nourish your dog with a beef and potato flavor",
                     price="$35.99", catalog=category1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Country Chicken Stew Canned dog food", description="A hearty soft food made with love and care like you mom made her stew. Made with real chicken. 12 cans in pack (12.5 oz per can)",
                     price="$27.50", catalog=category1)
session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Beef jerky dog treats", description="All natural dog treat.  Made with real meat",
                     price="$7.99", catalog=category1)

session.add(catalogItem3)
session.commit()


# Clothes Catagory items in catalog
category1 = Catalog(user_id=1, name="Clothes")

session.add(category1)
session.commit()

## add catalog items
catalogItem1 = CatalogItem(user_id=1, name="Basic dog T-Shirt", description="soft T-shirt made from lightweight poly-cotton blend with elastic neck",
                     price="$8.99", catalog=category1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Rainy day dog slicker", description="On wet rainy days it would be great to have rain slicker to throw on your dog to stay dry.  With hood and self-adjusting belly strap",
                     price="$14.99", catalog=category1)
session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Dog glasses", description="Protective glasses specifically designed for dogs",
                     price="$20.99", catalog=category1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(user_id=1, name="Dog Lifejacket", description="Durable construction with adjustable chest and neck.  Front float that keeps dog's head above water",
                     price="$25.99", catalog=category1)

session.add(catalogItem4)
session.commit()

# Toys Catagory items in catalog
category1 = Catalog(user_id=1, name="Toys")

session.add(category1)
session.commit()

## add catalog items
catalogItem1 = CatalogItem(user_id=1, name="Indestructible Dog Ball", description="Made from hard, high density product that is safe and washable.  Great fun.",
                     price="$5.99", catalog=category1) 

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Dog Chew Bone", description="Safe long-lasting chew bone for hours and hours of fun for your dog.",
                     price="$2.99", catalog=category1)
session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Soft Squeek", description="Soft plush chew toy that squeeks when squeezed",
                     price="$3.99", catalog=category1)

session.add(catalogItem3)
session.commit()



# Clean Up Catagory items in catalog
category1 = Catalog(user_id=1, name="Clean Up")

session.add(category1)
session.commit()

## add catalog items
catalogItem1 = CatalogItem(user_id=1, name="Pooch Pick Up Bags", description="Biodegradable bags make it easy to be responsible.  100ct",
                     price="$9.99", catalog=category1) 

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Order Eliminator spray", description="Spray eliminates order on the strongest smells",
                     price="$6.99", catalog=category1)
session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Stain and Oder remover", description="Spray that pentrates deep to destroy stains and orders fast",
                     price="$23.99", catalog=category1)

session.add(catalogItem3)
session.commit()



# Health Catagory items in catalog
category1 = Catalog(user_id=1, name="Health")

session.add(category1)
session.commit()

## add catalog items
catalogItem1 = CatalogItem(user_id=1, name="Flea and Tick treatment", description="Stops disease carrying fleas and ticks.  Eash to use, just dab on the skin.",
                     price="$79.99", catalog=category1) 

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(user_id=1, name="Doggie Toothpast", description="Enzymatic toothpasste that leaves your dogs teeth and mouth clean and fresh",
                     price="$6.99", catalog=category1)
session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(user_id=1, name="Joint Chewables", description="Chewable tablets that eat like a treat but helps your dogs joints feel better.  All natural ingredients",
                     price="$13.99", catalog=category1)

session.add(catalogItem3)
session.commit()


print "added menu items!"
