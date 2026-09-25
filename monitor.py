import requests
from bs4 import BeautifulSoup

TOPIC = "YOUR_NTFY_TOPIC"

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

        if "pointer-events: none" not in style:
            available = True

if available:

    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        headers={
            "Title": "🚨 CKT22 AVAILABLE",
            "Priority": "urgent",
            "Tags": "warning,ticket"
        },
        data="""
Category A - General available

Price: ¥10,000

Open ticket site NOW!
"""
    )

    print("AVAILABLE")

else:

    print("NOT AVAILABLE")
