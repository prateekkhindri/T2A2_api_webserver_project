from flask import Blueprint
from src.models.Brand import Brand
from src.models.Cart import Cart
from src.models.CartItem import CartItem
from src.cli import my_input
from src.extension import db
from src.models.User import User
from src.models.Product import Product
from src.models.Category import Category
from src.models.Address import Address
from src.extension import bcrypt
import random


db_commands = Blueprint("db-cli", __name__)


@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Creating tables...")


@db_commands.cli.command('admin')
def admin_db():
    username = my_input("Username:")
    email = my_input("Email:")
    first_name = my_input("First Name:")
    last_name = my_input("Last Name:")
    password = my_input("Password:")
    password = bcrypt.generate_password_hash(password).decode('utf-8')
    phone_number = my_input("Phone Number:")
    new_admin = User(username=username,
                     email=email,
                     firstname=first_name,
                     lastname=last_name,
                     password=password,
                     phone_number=phone_number,
                     is_admin=True,
                     is_seller=False,
                     )

    db.session.add(new_admin)
    db.session.commit()


ADMIN = ["admin1", "admin2", "admin3"]
SELLER = ['Richard', 'Jack', 'John', "Jake", "Patrick"]
BUYER = ["Mitchell", "Michael", "Chris", "David", "Zac"]
CATEGORY_LIST = ['Men', 'Women', 'Children']
BRAND_LIST = ['Nike', 'Puma', 'Adidas']
PRODUCT_LIST = ['Product1', 'Product2', 'Product3', 'Product4', 'Product5', 'Product6', 'Product7', 'Product8', 'Product9',
                'Product10', 'Product11', 'Product12', 'Product13', 'Product14', 'Product15', 'Product16', 'Product17', 'Product18']


@db_commands.cli.command('seed')
def seed_db():

    print("Seeding database...")

    password = "Password1234"

    for admin in ADMIN:
        randInt = str(random.randint(10, 9000))
        user1 = User(username="admin"+randInt,
                     email=f"admin_{randInt}@example.com",
                     first_name="mr",
                     last_name=admin,
                     password=bcrypt.generate_password_hash(
                         password).decode('utf-8'),
                     phone_number="0400000000",
                     is_admin=True,
                     is_seller=False
                     )

        user1.save()

    for seller in SELLER:
        seller1 = User(username=seller,
                       email=f"{seller}@example.com",
                       first_name="mr",
                       last_name=seller,
                       password=bcrypt.generate_password_hash(
                           password).decode('utf-8'),
                       phone_number="0400000000",
                       is_admin=False,
                       is_seller=True
                       )

        seller1.save()

    for buyer in BUYER:
        buyer1 = User(username=buyer,
                      email=f"{buyer}@example.com",
                      first_name="mr",
                      last_name=buyer,
                      password=bcrypt.generate_password_hash(
                          password).decode('utf-8'),
                      phone_number="0400000000",
                      is_admin=False,
                      is_seller=False
                      )

        buyer1.save()

    for category in CATEGORY_LIST:
        category1 = Category(
            name=category.lower(),
            description="""lorem ipsum Eius mod esse veniam ut enim fugiat. 
                            Ullamco aute Lorem ut amet voluptate est reprehenderit dolor.
                            Fugiat officia excepteur Lorem minim."""
        )
        category1.save()

    for brand in BRAND_LIST:
        brand1 = Brand(
            name=brand.lower(),
            description="""lorem ipsum Eius mod esse veniam ut enim fugiat. 
                            Ullamco aute Lorem ut amet voluptate est reprehenderit dolor.
                            Fugiat officia excepteur Lorem minim."""

        )
        brand1.save()

    users = list(User.query.all())
    users = users if len(users) == 1 else random.sample(
        users, random.randint(1, len(users)-1))

    for _ in users:
        address1 = Address(
            user_id=random.choice(users).id,
            street_address=str(random.randint(100, 300))+" Main Street",
            suburb=random.choice(["ABC", "CDE", "XYZ", "MNP", "ZYX", "LTE"]),
            state=random.choice(
                ["NSW", "VIC", "ACT", "WA", "SA", "QLD", "TAS", "NT"]),
            postcode=random.randint(1000, 5000),
            default=False
        )
        address1.save()

    buyers = list(User.query.filter_by(is_seller=False, is_admin=False))
    buyers = buyers if len(buyers) == 1 else random.sample(
        buyers, random.randint(1, len(buyers)-1))

    for buyer in buyers:
        cart1 = Cart(user_id=buyer.id)
        cart1.save()

    brands = list(Brand.query.all())
    categories = list(Category.query.all())
    sellers = list(User.query.filter_by(is_seller=True, is_admin=False))

    for product in PRODUCT_LIST:
        price = random.randint(30, 80)
        product1 = Product(
            name=product.lower(),
            description="""lorem ipsum Eius mod esse veniam ut enim fugiat. 
                            Ullamco aute Lorem ut amet voluptate est reprehenderit dolor.
                            Fugiat officia excepteur Lorem minim.""",
            seller_id=random.choice(sellers).id,
            category_id=random.choice(categories).id,
            brand_id=random.choice(brands).id,
            price=price,
            discount_price=price-10,
            quantity=random.randint(1, 50),
            rating=0
        )
        product1.save()

    products = list(Product.query.all())
    carts = list(Cart.query.all())
    carts = carts if len(carts) == 1 else random.sample(
        carts, random.randint(1, len(carts)-1))

    for _ in carts:
        product = random.choice(products)
        cartitem1 = CartItem(
            # user_id=random.choice(buyers).id,
            # seller_id=random.choice(sellers).id,
            cart_id=random.choice(carts).id,
            product_id=product.id,
            quantity=random.randint(1, product.quantity),
        )
        cartitem1.save()


@db_commands.cli.command('clear')
def clear():
    print("Clearing all tables...")
    db.session.query(CartItem).delete()
    db.session.query(Cart).delete()
    db.session.query(Address).delete()
    db.session.query(Product).delete()
    db.session.query(Category).delete()
    db.session.query(Brand).delete()
    db.session.query(User).delete()
    db.session.commit()


@db_commands.cli.command("drop")
def drop():
    print("Dropping all tables...")
    db.drop_all()
