flowchart TD

subgraph Presentation_Layer [Presentation Layer]
    A[ServiceAPI]
end

subgraph Business_Logic_Layer [Business Logic Layer]
    B[HBnBFacade]
    C1[User]
    C2[Place]
    C3[Review]
    C4[Amenity]
end

subgraph Persistence_Layer [Persistence Layer]
    D1[UserDAO]
    D2[PlaceDAO]
    D3[ReviewDAO]
    D4[AmenityDAO]
end

%% Arrows
A --> B
B --> C1
B --> C2
B --> C3
B --> C4
C1 --> D1
C2 --> D2
C3 --> D3
C4 --> D4
