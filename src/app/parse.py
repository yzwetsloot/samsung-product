from bs4 import BeautifulSoup

from app.utils.Product import Product
from app.utils.utils import flatten


def parse_csrf_token(content: bytes) -> str:
    bs = BeautifulSoup(content, "lxml")
    container = bs.find("input", attrs={"name": "CSRFToken"})
    csrf_token = container["value"]
    return csrf_token


def parse_products(content: str) -> list:
    products = content["results"]

    if len(products) == 0:
        return []

    variant_options = map(lambda product: product["variantOptions"], products)

    products = flatten(variant_options)
    return products


def parse_product(page: bytes, info: dict) -> Product:
    bs = BeautifulSoup(page, "lxml")

    if info["msrpPrice"]:
        reference = info["msrpPrice"]["value"]
    else:
        reference = None

    id = info["code"]
    price = info["priceData"]["value"]
    url = info["url"]
    title = info["name"]

    if info["color"]:
        color = info["color"]["colorName"]
    else:
        color = None

    size = info["size"]

    if info["galleryImages"]:
        image = info["galleryImages"][0][id]["url"]
    else:
        image = _parse_image_url(bs)

    image = _parse_image_url(bs)
    ean = _parse_ean(bs)
    category = _parse_category(bs)
    rating = _parse_rating(bs)
    score = _parse_score(bs)

    return Product(
        id,
        ean,
        title,
        url,
        image,
        price,
        rating,
        score,
        category,
        color,
        size,
        reference,
    )


def _parse_image_url(bs):
    figure = bs.find("figure")
    image = figure.find("img")

    return image["src"]


def _parse_ean(bs):
    container = bs.find("input", attrs={"name": "eanCode"})
    ean = container["value"]

    return ean


def _parse_category(bs):
    container = bs.find("input", attrs={"name": "pvisubtype"})
    category = container["value"]

    return category


def _parse_rating(bs):
    container = bs.find("strong", class_="rating__point")
    text = container.find("span", class_="", recursive=False).text

    return float(text)


def _parse_score(bs):
    container = bs.find("em", class_="rating__review-count")
    text = container.find("span", class_="", recursive=False).text

    return int(text)
