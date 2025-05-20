from itertools import count as counter

import app.config as config
import app.service.request as request
import app.query as query
from app.parse import parse_products, parse_product
from app.navigate import enter_store
from app.service.log import logger


count = 0


def run():
    global count

    enter_store()

    # fetch products per category
    for category in config.categories:
        for i in counter():
            logger.info("Fetch page %d of category '%s'", i + 1, category)

            response = request.get(
                f"https://shop.samsung.com/nl/multistore/np/ing/All/c/{category}/results?q=&page={i}",
            )

            if not response:
                continue

            logger.debug("Parse products on page %d of category '%s'", i + 1, category)

            products = parse_products(response.json())
            if not products:
                logger.debug(
                    "0 products found on page %s of category '%s'", i + 1, category
                )
                break

            for product in products:
                product_id = product["code"]

                logger.info("Process product '%s'", product_id)

                logger.debug("Fetch product page")

                # deal with ID's like SM-G970FZKAB/TU
                escaped_product_id = product_id.replace("/", "")
                response_page = request.get(
                    f"https://www.samsung.com/nl/multistore/ing/buy.{escaped_product_id}/",
                )

                if not response_page:
                    logger.debug("No product page found")
                    continue

                logger.info("Parse product")

                try:
                    product = parse_product(response_page.content, product)
                except Exception as e:
                    logger.warning("Failed to parse product '%s': %s", product_id, e)
                    continue

                # persist data
                query.persist_product(product)

                count = count + 1
                logger.info("[%d] Store product '%s'", count, product_id)
