
class InDepthImagePair:

    def __init__(self,customer_image_path, customer_image_name,store_image_path, store_image_name, final_score):
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
