from user import User
from place import Place
from review import Review
from amenity import Amenity

def run_tests():
    print("🧪 Starting tests...")

    # Test User creation
    user = User(first_name="Ana", last_name="Lopez", email="ana@example.com", password="secret123")
    assert user.first_name == "Ana"
    assert user.verify_password("secret123") is True
    print("✅ User creation and password hashing: PASSED")

    # Test Place creation
    place = Place(
        title="Ocean View Apartment",
        description="A lovely place by the beach.",
        price=150,
        latitude=18.47,
        longitude=-66.12,
        owner_id=user.id
    )
    assert place.owner_id == user.id
    print("✅ Place creation and ownership: PASSED")

    # Test Amenity
    wifi = Amenity(name="Wi-Fi")
    pool = Amenity(name="Pool")
    place.add_amenity(wifi.id)
    place.add_amenity(pool.id)
    assert wifi.id in place.amenities and pool.id in place.amenities
    print("✅ Amenity creation and linking to place: PASSED")

    # Test Review
    review = Review(text="Amazing stay!", rating=5, place_id=place.id, user_id=user.id)
    assert review.place_id == place.id
    assert review.user_id == user.id
    assert len(review.validate()) == 0
    place.reviews.append(review.id)
    assert review.id in place.reviews
    print("✅ Review creation, validation, and linking: PASSED")

    print("🎉 All tests passed!")

if __name__ == "__main__":
    run_tests()
