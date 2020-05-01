
class InDepthImagePair:

    def __init__(self, customer_image_name, store_image_name, final_score):
        self.customer_image_name = customer_image_name
        self.store_image_name = store_image_name
        self.final_score = final_score

    def __eq__(self, other):
        return self.final_score == other.final_score

    def __lt__(self, other):
        return self.final_score < other.final_score

    def __gt__(self, other):
        return self.final_score > other.final_score

    def __ge__(self, other):
        return self.final_score >= other.final_score

    def __le__(self, other):
        return self.final_score <= other.final_score
