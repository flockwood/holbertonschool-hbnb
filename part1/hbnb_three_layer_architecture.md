# HBnB Three-Layer Architecture (Facade Pattern)

## Diagram

```mermaid
classDiagram

%% === Presentation Layer ===
%% --------------------------
class ServiceAPI {
  +create_user()
  +search_places()
  +submit_review()
}

%% == Business Logic Layer ===
%% ---------------------------
class HBnBFacade {
  +handle_user_creation()
  +handle_place_search()
  +handle_review_submission()
}

class User
class Place
class Review
class Amenity


%% === Persistance Layer ===
%% -------------------------
class UserDAO
class PlaceDAO
class ReviewDAO
class AmenityDAO


%% Connections
ServiceAPI --> HBnBFacade : uses
HBnBFacade --> User
HBnBFacade --> Place
HBnBFacade --> Review
HBnBFacade --> Amenity
User --> UserDAO
Place --> PlaceDAO
Review --> ReviewDAO
Amenity --> AmenityDAO
