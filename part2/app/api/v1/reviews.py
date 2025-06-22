from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Simple review model
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'user_id': fields.String(required=True, description='User ID'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    def post(self):
        """Create a new review"""
        try:
            new_review = facade.create_review(api.payload)
            return new_review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    @api.expect(review_model)
    def put(self, review_id):
        """Update review"""
        try:
            facade.update_review(review_id, api.payload)
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            if "not found" in str(e):
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))

    def delete(self, review_id):
        """Delete review"""
        try:
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        """Get all reviews for a place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))