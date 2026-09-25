import requests

TOPIC = "ckt22-ayaz-final-7382"

URL = (
    "https://generalsale.tickets-aichi-nagoya2026.org/"
    "showProduct.html?idProduct=492"
)

html = requests.get(
    URL,
    headers={
        "User-Agent":
        "Mozilla/5.0"
    }
).text

# available = (
#     "productItem_3797" in html
#     and
#     'pointer-events: none;" title="Increase" class="productPlus'
#     not in html
# )
available = True

if available:

    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        data="🏏 CKT22 Category A General Available!"
    )

    print("AVAILABLE")

else:

    print("NOT AVAILABLE")
