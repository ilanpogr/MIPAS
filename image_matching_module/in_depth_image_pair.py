
class InDepthImagePair:
    """
    This class represents a customer image and a store image that passed the in-depth
    image matching filtering.

    Attributes
    ----------
    customer_image_path : str
        a string representing the customer's image directory's path.
    customer_image_name : str
        a string representing the customer's image name.
    store_image_path : str
        a string representing the store's image directory's path.
    store_image_name : str
        a string representing the store's image name.
    final_score : float
        a float representing the final after the in-depth filtering for
        the customer and store images.
    """

    def __init__(self, customer_image_path: str, customer_image_name:str, store_image_path: str, store_image_name: str,
                 final_score: float):
        """
        :param customer_image_path: a string representing the customer's image directory's path.
        :param customer_image_name: a string representing the customer's image name.
        :param store_image_path: a string representing the store's image directory's path.
        :param store_image_name: a string representing the store's image name.
        :param final_score: a float representing the final after the in-depth filtering for
        the customer and store images.
        """
        self.customer_image_path = customer_image_path
        self.customer_image_name = customer_image_name
        self.store_image_path = store_image_path
        self.store_image_name = store_image_name
        self.final_score = final_score

    def __eq__(self, other):
        return self.final_score == other

    def __lt__(self, other):
        return self.final_score < other

    def __gt__(self, other):
        return self.final_score > other

    def __ge__(self, other):
        return self.final_score >= other

    def __le__(self, other):
        return self.final_score <= other
