class Product:
    def __init__(
        self,
        id: str,
        ean: str,
        title: str,
        url: str,
        image: str,
        price: float,
        rating: float,
        score: int,
        category: str,
        color: str,
        size: str,
        reference_price: float,
    ) -> None:
        self.id = id
        self.ean = ean
        self.title = title
        self.url = url
        self.image = image
        self.price = price
        self.rating = rating
        self.score = score
        self.category = category
        self.color = color
        self.size = size
        self.reference_price = reference_price
