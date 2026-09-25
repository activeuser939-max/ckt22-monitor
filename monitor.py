import requests
from bs4 import BeautifulSoup

TOPIC = "ckt22-ayaz-final-7382"

URL = (
    "https://generalsale.tickets-aichi-nagoya2026.org/"
    "showProduct.html?idProduct=492"
)

html = requests.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
).text

#
# CAPTCHA detection
#

if "captcha" in html.lower():

    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        headers={
            "Title": "CKT22 Monitor Warning",
            "Priority": "high"
        },
        data=(
            "CAPTCHA detected. "
            "Monitor may not be able to check tickets."
        )
    )

    print("CAPTCHA DETECTED")
    raise SystemExit

#
# Verify expected event exists
#

if "Cricket (T20) - CKT22" not in html:

    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        headers={
            "Title": "CKT22 Monitor Warning",
            "Priority": "high"
        },
        data=(
            "Expected CKT22 event page not found. "
            "Website structure may have changed."
        )
    )

    print("EVENT PAGE NOT FOUND")
    raise SystemExit

#
# Parse page
#

soup = BeautifulSoup(html, "html.parser")

ticket_row = soup.find(
    "div",
    id="productItem_3797"
)

if ticket_row is None:

    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        headers={
            "Title": "CKT22 Monitor Warning",
            "Priority": "high"
        },
        data=(
            "Category A section "
            "(productItem_3797) could not be found."
        )
    )

    print("CATEGORY A ROW NOT FOUND")
    raise SystemExit

available = False

plus_button = ticket_row.find(
    "div",
    class_="productPlus"
)

if plus_button:

    style = plus_button.get("style", "")

    #
    # Available if:
    # 1. no pointer-events:none
    # 2. onclick action exists
    #

    if (
        "pointer-events: none" not in style
        and
        plus_button.get("onclick") is not None
    ):
        available = True

#
# Send notification
#
# TEST ONLY
available = True

if available:

    requests.post(
        f"https://ntfy.sh/{TOPIC}",
        headers={
            "Title": "CKT22 Category A Available",
            "Priority": "urgent",
            "Click": (
                "https://generalsale.tickets-aichi-nagoya2026.org/"
                "showProduct.html?idProduct=492"
            ),
            "Tags": "warning,ticket"
        },
        data=(
            "Category A - General available.\n\n"
            "Price: ¥10,000\n\n"
            "Tap this notification to open the ticket page."
        )
    )

    print("AVAILABLE")

else:

    print("NOT AVAILABLE")
