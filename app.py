import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "bloom-bowl-secret")

MENU = [
    {
        "name": "Sprout Spectrum",
        "tagline": "Crunchy protein glow",
        "description": "Activated sprouts swirled with citrus foam, mint oil, and chia crunch.",
        "variations": [
            {"label": "Light", "price": "₹45"},
            {"label": "Power", "price": "₹55"},
        ],
        "badge": "Glow Classic",
    },
    {
        "name": "Chana Pulse",
        "tagline": "Spiced & grounded",
        "description": "Slow-stewed chickpeas, neon slaw, and turmeric tahini drizzle.",
        "variations": [
            {"label": "Warm", "price": "₹55"},
        ],
        "badge": None,
    },
    {
        "name": "Peanut Quartz",
        "tagline": "Roasted energy brick",
        "description": "Smoky peanuts, amaranth puffs, and basil microgreens for deep satiety.",
        "variations": [
            {"label": "Classic", "price": "₹55"},
        ],
        "badge": None,
    },
    {
        "name": "Sweet Corn Halo",
        "tagline": "Golden comfort cloud",
        "description": "Buttered corn pearls with coconut crumble and lime zest.",
        "variations": [
            {"label": "Plain", "price": "₹40"},
            {"label": "Butter", "price": "₹50"},
            {"label": "Salad", "price": "₹60"},
        ],
        "badge": "Most Loved",
    },
    {
        "name": "Mix Nebula",
        "tagline": "Best of every farm orbit",
        "description": "Sprouts, legumes, seasonal greens, and umami seeds colliding in one bowl.",
        "variations": [
            {"label": "Signature", "price": "₹55"},
        ],
        "badge": None,
    },
    {
        "name": "Bloom Bowl Special",
        "tagline": "House-coded nourishment",
        "description": "Chef-stacked hero bowl layered with microgreens, citrus mist, and crunch.",
        "variations": [
            {"label": "Special", "price": "₹70"},
        ],
        "badge": "Signature",
    },
    {
        "name": "Prism Fruit",
        "tagline": "Hydration in technicolor",
        "description": "Seasonal fruits chilled with electrolite jelly and basil pearls.",
        "variations": [
            {"label": "Small", "price": "₹80"},
            {"label": "Big", "price": "₹100"},
        ],
        "badge": None,
    },
]

FEATURES = [
    {
        "title": "Zero-lag Freshness",
        "text": "Every bowl is prepped after you tap order. Nothing sits, everything blooms.",
    },
    {
        "title": "Future-forward Fuel",
        "text": "Plant protein, adaptogens, and colorful crunch build daily resilience.",
    },
    {
        "title": "Planet-kind Service",
        "text": "Reusable jars, electric deliveries, and seasonal sourcing keep us light.",
    },
]

CTA = {
    "phone": "+91 98765 43210",
    "email": "hello@bloombowl.studio",
    "address": "12 Bloom Street, Green Valley, Pune",
}

STATS = [
    {"value": "120+", "label": "Bowls minted / day"},
    {"value": "24g", "label": "Avg. plant protein"},
    {"value": "5 km", "label": "Eco delivery radius"},
]

SERVING_STYLES = [
    "Glow Classic",
    "Protein Surge",
    "Spiced Crunch",
    "Sweet Calm",
]

EXTRAS = [
    "Microgreen crunch",
    "Activated trail mix",
    "Citrus dressing",
    "Cocoa energy crumble",
]

SERVICE_MODES = [
    {
        "value": "Studio Pickup",
        "label": "Studio pickup",
        "description": "Swing by the Bloom kitchen and grab it piping fresh.",
        "eta": "Ready in ~15 min",
    },
    {
        "value": "Eco Delivery",
        "label": "Eco delivery",
        "description": "E-bike couriers within 5 km keep your bowl chilled.",
        "eta": "Drops in ~30 min",
    },
    {
        "value": "Weekly Ritual Subscription",
        "label": "Weekly ritual subscription",
        "description": "Plan your glow bowls ahead with scheduled drops.",
        "eta": "Plan shared within 12 hrs",
    },
]

SERVICE_MODE_LOOKUP = {mode["value"]: mode for mode in SERVICE_MODES}


def build_order_summary(form):
    customer_name = form.get("customer_name", "").strip() or "Bloom Friend"
    bowl_choice = form.get("bowl") or MENU[0]["name"]
    style = form.get("style") or SERVING_STYLES[0]
    mode_value = form.get("mode") or SERVICE_MODES[0]["value"]
    phone = form.get("phone", "").strip()
    email = form.get("email", "").strip()
    notes = form.get("notes", "").strip()

    extras_selected = [extra for extra in form.getlist("extras") if extra in EXTRAS]

    try:
        quantity_int = max(1, min(12, int(form.get("quantity", 1))))
    except ValueError:
        quantity_int = 1

    bowl_details = next((item for item in MENU if item["name"] == bowl_choice), MENU[0])
    price_hint = bowl_details["variations"][0]["price"] if bowl_details.get("variations") else None

    mode_meta = SERVICE_MODE_LOOKUP.get(mode_value)

    return {
        "customer_name": customer_name,
        "bowl": bowl_choice,
        "style": style,
        "mode": mode_meta["label"] if mode_meta else mode_value,
        "mode_description": mode_meta["description"] if mode_meta else "",
        "eta": mode_meta["eta"] if mode_meta else "Ready soon",
        "quantity": quantity_int,
        "extras": extras_selected,
        "notes": notes,
        "price_hint": price_hint,
        "reference": f"BB-{datetime.now().strftime('%H%M%S')}",
        "phone": phone,
        "email": email,
    }


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        summary = build_order_summary(request.form)
        session["order_feedback"] = summary
        return redirect(url_for("home", _anchor="order"))

    order_feedback = session.pop("order_feedback", None)

    return render_template(
        "index.html",
        menu=MENU,
        features=FEATURES,
        contact=CTA,
        stats=STATS,
        serving_styles=SERVING_STYLES,
        extras=EXTRAS,
        service_modes=SERVICE_MODES,
        order_feedback=order_feedback,
    )


if __name__ == "__main__":
    app.run(debug=True)
