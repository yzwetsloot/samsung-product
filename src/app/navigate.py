import app.service.request as request
from app.parse import parse_csrf_token
from app.service.log import logger


BASE_URL = "https://shop.samsung.com/nl/multistore/np/ing/registration"

ENTRY_CODE = "2SP7Q9R"


def enter_store():
    logger.info("Entering store...")

    response = request.get(BASE_URL)
    if not response:
        raise Exception("Failed to enter store")

    csrf_token = parse_csrf_token(response.content)

    response = request.post(
        BASE_URL,
        data={"verificationCode": ENTRY_CODE, "CSRFToken": csrf_token},
    )

    if response.status_code != 200:
        raise Exception("Failed to enter store")

    logger.debug("Store entry successful")
