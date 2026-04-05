from app import create_app, db
from app.services.facade import HBnBFacade
from app.models.user import User

app = create_app()
facade = HBnBFacade()

with app.app_context():
    print("Création de la base de données...")
    db.create_all()

    print("Suppression des anciennes données (optionnel) - on garde pour l'instant...")
    # On peut vider la base, mais on va plutôt créer si ça n'existe pas
    
    # 1. Création de l'Administrateur (le premier user est admin auto d'après le modèle métier)
    try:
        admin = facade.create_user({
            "first_name": "Admin",
            "last_name": "System",
            "email": "admin@hbnb.com",
            "password": "password123"
        })
        print("✅ Utilisateur Admin créé (admin@hbnb.com / password123)")
    except ValueError:
        admin = facade.get_user_by_email("admin@hbnb.com")
        print("✅ Utilisateur Admin existe déjà.")

    # 2. Création d'un hôte normal
    try:
        host = facade.create_user({
            "first_name": "Alice",
            "last_name": "Host",
            "email": "alice@hbnb.com",
            "password": "password123"
        })
        print("✅ Utilisateur Hôte créé (alice@hbnb.com / password123)")
    except ValueError:
        host = facade.get_user_by_email("alice@hbnb.com")
        print("✅ Utilisateur Hôte existe déjà.")

    # 3. Création des commodités (Amenities)
    amenities = ["WiFi", "Pool", "Air Conditioning", "Free Parking", "Kitchen"]
    amenity_objects = []
    
    existing_amenities = facade.get_all_amenities()
    amenity_names = [a.name for a in existing_amenities]
    
    for name in amenities:
        if name not in amenity_names:
            try:
                am = facade.create_amenity({"name": name})
                amenity_objects.append(am)
                print(f"✅ Amenity créée : {name}")
            except Exception as e:
                pass

    # Recharger les commodités pour les assignations
    all_amenities = facade.get_all_amenities()

    # 4. Création des Lieux (Places)
    places_data = [
        {
            "title": "Cozy Parisian Studio",
            "description": "Lovely studio in the heart of Paris, close to the Eiffel Tower.",
            "price": 85.0,
            "latitude": 48.8584,
            "longitude": 2.2945,
            "country": "France",
            "owner_id": host.id if host else admin.id
        },
        {
            "title": "Luxury Villa in Bali",
            "description": "Breathtaking villa with a private pool and rice terrace views.",
            "price": 250.0,
            "latitude": -8.4095,
            "longitude": 115.1889,
            "country": "Indonesia",
            "owner_id": admin.id
        },
        {
            "title": "Modern Loft in New York",
            "description": "Spacious loft in Brooklyn with a stunning city skyline view.",
            "price": 150.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "country": "United States",
            "owner_id": host.id if host else admin.id
        }
    ]

    existing_places = facade.get_all_places()
    titles = [p.title for p in existing_places]
    created_places = []

    for p_data in places_data:
        if p_data["title"] not in titles:
            place = facade.create_place(p_data)
            created_places.append(place)
            
            # Associer aléatoirement des commodités si géré
            if len(all_amenities) > 0:
                try:
                    setattr(place, 'amenities', all_amenities[:3])  # Les 3 premières
                    db.session.commit()
                except Exception:
                    pass
            
            print(f"✅ Lieu créé : {place.title} ({p_data['country']})")

    # 5. Création des Avis (Reviews)
    if 'place_review_1' not in [p.title for p in existing_places]:
        pass # The script uses logic that creates the initial DB if empty.

    print("🎉 Base de données peuplée avec succès !")
    print("-------------------------------------------------")
    print("👉 Vous pouvez tester en vous rendant sur index.html")
    print("👉 Connectez-vous avec 'alice@hbnb.com' et 'password123'")
