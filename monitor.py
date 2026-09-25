import requests
from bs4 import BeautifulSoup

TOPIC = "ckt22-ayaz-final-7382"

URL = (
    "https://generalsale.tickets-aichi-nagoya2026.org/"
    "showProduct.html?idProduct=492"
)

headers = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "Chrome/140 Safari/537.36"
    )
}

try:

    html = requests.get(
        URL,
        headers=headers,
        timeout=20
    ).text

    #
    # CAPTCHA detection
    #

    if "captcha" in html.lower():

        requests.post(
            f"https://ntfy.sh/{TOPIC}",
            headers={
                "Title": "CKT22 CAPTCHA Warning",
                "Priority": "high"
            },
            data=(
                "CAPTCHA detected. "
                "Monitor may not be able to verify availability."
            )
        )

        print("CAPTCHA DETECTED")
        raise SystemExit

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
                "(productItem_3797) not found."
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

        if (
            "pointer-events: none" not in style
            and
            plus_button.get("onclick") is not None
        ):
            available = True
    available = True
    if available:

        requests.post(
            f"https://ntfy.sh/{TOPIC}",
            headers={
                "Title": "CKT22 Category A Available",
                "Priority": "urgent",
                "Click":
                    "https://generalsale.tickets-aichi-nagoya2026.org/showProduct.html?idProduct=492",
                "Tags": "warning,ticket"
            },
            data=(
                "Category A - General available.\n\n"
                "Price: ¥10,000\n\n"
                "Tap to open the ticket page."
            )
        )

        print("AVAILABLE")

    else:

        print("NOT AVAILABLE")

except Exception as e:

    print(f"ERROR: {e}")
