import requests
from bs4 import BeautifulSoup

TOPIC = "ckt22-ayaz-final-7382"

URL = (
    "https://generalsale.tickets-aichi-nagoya2026.org/"
    "showProduct.html?idProduct=492"
)

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(URL, headers=headers).text

soup = BeautifulSoup(html, "html.parser")

ticket_row = soup.find("div", id="productItem_3797")

available = False

if ticket_row:

    plus_button = ticket_row.find(
        "div",
        class_="productPlus"
    )

    if plus_button:

        style = plus_button.get("style", "")

        if (
            "pointer-events: none" not in style
            and plus_button.get("onclick") is not None
        ):
            available = True

# TEST ONLY
available = True

if available:

    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        headers={
            "Title": "TICKET AVAILABLE NOW",
            "Priority": "urgent",
            "Click": "https://generalsale.tickets-aichi-nagoya2026.org/showProduct.html?idProduct=492",
            "Tags": "warning"
        },
        data="Category A - General available. Tap to open."
    )

    print("AVAILABLE")

else:

    print("NOT AVAILABLE")
