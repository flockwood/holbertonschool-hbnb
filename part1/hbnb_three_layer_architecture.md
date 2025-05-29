# HBnB Three-Layer Architecture (Facade Pattern)

```mermaid
classDiagram
class ServiceAPI {
  +create_user()
  +search_places()
  +submit_review()
}

class HBnBFacade {
  +handle_user_creation()
  +handle_place_search()
  +handle_review_submission()
}

class User
class Place
class Review
class Amenity

class UserDAO
class PlaceDAO
class ReviewDAO
class AmenityDAO

ServiceAPI --> HBnBFacade : uses
HBnBFacade --> User
HBnBFacade --> Place
HBnBFacade --> Review
HBnBFacade --> Amenity
User --> UserDAO
Place --> PlaceDAO
Review --> ReviewDAO
Amenity --> AmenityDAO

## Layer Responsibilities

- **Presentation Layer**:
  - `ServiceAPI`: Handles user-facing methods and calls the facade.

- **Business Logic Layer**:
  - `HBnBFacade`: Unified interface that encapsulates business logic.
  - `User`, `Place`, `Review`, `Amenity`: Core model entities.

- **Persistence Layer**:
  - `UserDAO`, `PlaceDAO`, etc.: Communicate directly with the database.

## Facade Pattern

The `HBnBFacade` acts as the bridge between the Presentation and Business layers, simplifying how external services interact with internal logic.
