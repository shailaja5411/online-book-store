from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)

app.secret_key = "bookstore-secret-key"


# =========================
# BOOK DATA
# =========================

books = [

    {
        "id": 1,
        "title": "Python Programming",
        "author": "John Smith",
        "category": "Programming",
        "price": 499,
        "image":"python.jpg"
    },

    {
        "id": 2,
        "title": "The Alchemist",
        "author": "Paulo Coelho",
        "category": "Fiction",
        "price": 299,
        "image":"alchemist.jpg"
    },

    {
        "id": 3,
        "title": "Atomic Habits",
        "author": "James Clear",
        "category": "Self Help",
        "price": 399,
        "image":"atomic-habits.jpg"
    },

    {
        "id": 4,
        "title": "Rich Dad Poor Dad",
        "author": "Robert Kiyosaki",
        "category": "Finance",
        "price": 350,
        "image":"rich-dad.jpg"
    }

]


# =========================
# HOME
# =========================

@app.route("/")
def home():

    return render_template(
        "home.html",
        books=books
    )


# =========================
# BOOKS
# =========================

@app.route("/books")
def books_page():

    return render_template(
        "books.html",
        books=books
    )


# =========================
# BOOK DETAILS
# =========================

@app.route("/book/<int:book_id>")
def book_details(book_id):

    selected_book = None

    for book in books:

        if book["id"] == book_id:
            selected_book = book
            break

    if selected_book is None:
        return "Book not found", 404

    return render_template(
        "book_details.html",
        book=selected_book
    )


# =========================
# ADD TO CART
# =========================

@app.route("/add-to-cart/<int:book_id>")
def add_to_cart(book_id):

    if "cart" not in session:
        session["cart"] = []

    if "quantities" not in session:
        session["quantities"] = {}

    cart = session["cart"]
    quantities = session["quantities"]

    if book_id not in cart:

        cart.append(book_id)

        quantities[str(book_id)] = 1

    session["cart"] = cart
    session["quantities"] = quantities

    return redirect(url_for("cart"))


# =========================
# REMOVE FROM CART
# =========================

@app.route("/remove-from-cart/<int:book_id>")
def remove_from_cart(book_id):

    cart = session.get("cart", [])

    quantities = session.get("quantities", {})

    if book_id in cart:

        cart.remove(book_id)

    quantities.pop(str(book_id), None)

    session["cart"] = cart

    session["quantities"] = quantities

    return redirect(url_for("cart"))


# =========================
# INCREASE QUANTITY
# =========================

@app.route("/increase-quantity/<int:book_id>")
def increase_quantity(book_id):

    quantities = session.get("quantities", {})

    current_quantity = quantities.get(
        str(book_id),
        1
    )

    quantities[str(book_id)] = current_quantity + 1

    session["quantities"] = quantities

    return redirect(url_for("cart"))


# =========================
# DECREASE QUANTITY
# =========================

@app.route("/decrease-quantity/<int:book_id>")
def decrease_quantity(book_id):

    quantities = session.get("quantities", {})

    current_quantity = quantities.get(
        str(book_id),
        1
    )

    if current_quantity > 1:

        quantities[str(book_id)] = current_quantity - 1

    session["quantities"] = quantities

    return redirect(url_for("cart"))


# =========================
# CART
# =========================

@app.route("/cart")
def cart():

    cart_ids = session.get(
        "cart",
        []
    )

    quantities = session.get(
        "quantities",
        {}
    )

    cart_books = []

    total = 0

    for book in books:

        if book["id"] in cart_ids:

            quantity = quantities.get(
                str(book["id"]),
                1
            )

            book_copy = book.copy()

            book_copy["quantity"] = quantity

            book_copy["subtotal"] = (
                book["price"] * quantity
            )

            cart_books.append(book_copy)

            total += book_copy["subtotal"]

    return render_template(
        "cart.html",
        cart_books=cart_books,
        total=total
    )


# =========================
# LOGIN
# =========================

@app.route("/login")
def login():

    return render_template(
        "login.html"
    )


# =========================
# REGISTER
# =========================

@app.route("/register")
def register():

    return render_template(
        "register.html"
    )


# =========================
# CHECKOUT
# =========================

@app.route("/checkout")
def checkout():

    return render_template(
        "checkout.html"
    )


# =========================
# ORDERS
# =========================

@app.route("/orders")
def orders():

    return render_template(
        "orders.html"
    )


# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    app.run(debug=True)