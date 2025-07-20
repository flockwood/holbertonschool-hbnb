from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Simple review model
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating (1-5)'),
    'place_id': fields.String(required=True, description='Place ID')
})

@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Authentication required')
    def post(self):
        """Create a new review (Authentication required)"""
        try:
            # Get current authenticated user
            current_user = get_jwt_identity()
            
            review_data = api.payload.copy()
            place_id = review_data.get('place_id')
            
            # Check if place exists
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, f"Place with id {place_id} not found")
            
            # Check if user is trying to review their own place
            if place.get('owner', {}).get('id') == current_user:
                api.abort(400, 'You cannot review your own place')
            
            # Check if user has already reviewed this place
            existing_reviews = facade.get_reviews_by_place(place_id)
            user_already_reviewed = any(
                review.user_id == current_user for review in existing_reviews
            )
            if user_already_reviewed:
                api.abort(400, 'You have already reviewed this place')
            
            # Set user_id to current authenticated user
            review_data['user_id'] = current_user
            
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
            
        except ValueError as e:
            api.abort(400, str(e))

    def get(self):
        """Get all reviews (Public access)"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        """Get review by ID (Public access)"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, "Review not found")
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update review (Authentication required - Author or Admin)"""
        try:
            # Get current authenticated user and claims
            current_user = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Get the review to check ownership
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, "Review not found")
            
            # Check if current user created the review OR is an admin
            if not is_admin and review.user_id != current_user:
                api.abort(403, 'Unauthorized action')
            
            review_data = api.payload
            facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200
            
        except ValueError as e:
            if "not found" in str(e):
                api.abort(404, str(e))
            else:
                api.abort(400, str(e))

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete review (Authentication required - Author or Admin)"""
        try:
            # Get current authenticated user and claims
            current_user = get_jwt_identity()
            claims = get_jwt()
            is_admin = claims.get('is_admin', False)
            
            # Get the review to check ownership
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, "Review not found")
            
            # Check if current user created the review OR is an admin
            if not is_admin and review.user_id != current_user:
                api.abort(403, 'Unauthorized action')
            
            facade.delete_review(review_id)
            return {'message': 'Review deleted successfully'}, 200
            
        except ValueError as e:
            api.abort(404, str(e))

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        """Get all reviews for a place (Public access)"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [review.to_dict() for review in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))
