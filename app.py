from flask import Flask, render_template

app = Flask(__name__)

MENU = [
    {
        "name": "Sprout Bowl",
        "tagline": "Plain or salad-style goodness",
        "description": "Protein-rich sprouts tossed with crisp vegetables for a clean energy boost.",
        "variations": [
            {"label": "Plain", "price": "₹45"},
            {"label": "Salad", "price": "₹55"},
        ],
        "badge": "Customer Favorite",
    },
    {
        "name": "Chana Bowl",
        "tagline": "Spiced chickpeas with crunch",
        "description": "Slow-cooked chana finished with herbs and a zingy salad mix.",
        "variations": [
            {"label": "Salad", "price": "₹55"},
        ],
        "badge": None,
    },
    {
        "name": "Peanut Bowl",
        "tagline": "Roasted & hearty",
        "description": "Smoky peanuts, fresh greens, and a drizzle of house dressing.",
        "variations": [
            {"label": "Classic", "price": "₹55"},
        ],
        "badge": None,
    },
    {
        "name": "Sweet Corn Bowl",
        "tagline": "Sweet, buttery comfort",
        "description": "Golden kernels served your way—plain, buttery, or salad-style.",
        "variations": [
            {"label": "Plain", "price": "₹40"},
            {"label": "Butter", "price": "₹50"},
            {"label": "Salad", "price": "₹60"},
        ],
        "badge": "Most Versatile",
    },
    {
        "name": "Mix Bowl",
        "tagline": "Best of every bite",
        "description": "A vibrant medley of sprouts, legumes, and seasonal veggies.",
        "variations": [
            {"label": "Signature Mix", "price": "₹55"},
        ],
        "badge": None,
    },
    {
        "name": "Bloom Bowl Special",
        "tagline": "House special experience",
        "description": "Our chef-crafted hero bowl layered with microgreens and crunchy toppings.",
        "variations": [
            {"label": "Bloom Bowl Special", "price": "₹70"},
        ],
        "badge": "Signature",
    },
    {
        "name": "Fruit Bowl",
        "tagline": "Naturally sweet hydration",
        "description": "Seasonal fruits served chilled with a hint of citrus.",
        "variations": [
            {"label": "Small", "price": "₹80"},
            {"label": "Big", "price": "₹100"},
        ],
        "badge": None,
    },
]

FEATURES = [
    {
        "title": "Freshly Prepped Daily",
        "text": "We chop, toss, and serve every bowl only after you order for maximum freshness.",
    },
    {
        "title": "Wholesome Ingredients",
        "text": "Locally sourced produce, sprouted legumes, and homemade toppings keep it clean and tasty.",
    },
    {
        "title": "Bloom with Love",
        "text": "Each bowl is crafted with care, color, and crunch so you can feel the love in every bite.",
    },
]

CTA = {
    "phone": "+91 98765 43210",
    "email": "hello@blooommbowl.com",
    "address": "12 Bloom Street, Green Valley, Pune",
}


@app.route("/")
def home():
    return render_template("index.html", menu=MENU, features=FEATURES, contact=CTA)


if __name__ == "__main__":
    app.run(debug=True)
