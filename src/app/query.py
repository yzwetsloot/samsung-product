import app.config as config
from app.utils.Product import Product
from app.service.database import Session, SQLError
from app.service.log import logger


def persist_product(product: Product):
    """
    Persist product data to database.

    Single transaction to insert or update product and price history.
    """
    try:
        with Session(config.database) as cursor:
            _upsert(product, cursor)
            _update_price_history(product, cursor)
    except SQLError as e:
        logger.error("Failed to persist product '%s': %s", product.id, e)


def _update_price_history(product: Product, cursor):
    """
    Update price history for product.

    If price value changed, insert new price record.
    Else, update weight and timestamp of last price record.
    """

    # UPDATE PRICE HISTORY
    cursor.execute(
        """
        SELECT value
        FROM price
        WHERE id = %s
        ORDER BY modified_at DESC
        LIMIT 1
        """,
        (product.id,),
    )

    result = cursor.fetchone()
    if result:
        last_price = result[0]
    else:
        last_price = None

    if last_price != product.price:
        logger.debug("Insert new price record for '%s'", product.id)

        # INSERT NEW PRICE RECORD
        cursor.execute(
            "INSERT INTO price (id, value) \
                        VALUES (%s, %s)",
            (
                product.id,
                product.price,
            ),
        )
    else:
        logger.debug("Update price record for '%s'", product.id)

        # UPDATE WEIGHT AND TIMESTAMP
        cursor.execute(
            "UPDATE price SET weight = price.weight + 1 WHERE \
            id = %s AND value = %s AND created_at = (SELECT created_at FROM price WHERE id = %s ORDER BY created_at DESC LIMIT 1)",
            (
                product.id,
                product.price,
                product.id,
            ),
        )


def _upsert(product: Product, cursor):
    logger.debug("Upsert product '%s'", product.id)

    # UPSERT PRODUCT
    cursor.execute(
        """
        INSERT INTO product (
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
            reference_price
        ) VALUES (
            %(id)s,
            %(ean)s,
            %(title)s,
            %(url)s,
            %(image)s,
            %(price)s,
            %(rating)s,
            %(score)s,
            %(category)s,
            %(color)s,
            %(size)s,
            %(reference_price)s
        ) ON CONFLICT (id) DO UPDATE SET (
            price,
            rating,
            score
        ) = (
            %(price)s,
            %(rating)s,
            %(score)s
        )""",
        product.__dict__,
    )
