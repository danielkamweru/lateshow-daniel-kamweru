from __init__ import create_app, db
from models import Episode, Guest, Appearance

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()
    
    # Create episodes
    e1 = Episode(date="1/11/99", number=1)
    e2 = Episode(date="1/12/99", number=2)
    e3 = Episode(date="1/13/99", number=3)
    
    # Create guests
    g1 = Guest(name="Michael J. Fox", occupation="actor")
    g2 = Guest(name="Sandra Bernhard", occupation="comedian")
    g3 = Guest(name="Tracey Ullman", occupation="television actress")
    g4 = Guest(name="Jerry Seinfeld", occupation="comedian")
    
    db.session.add_all([e1, e2, e3, g1, g2, g3, g4])
    db.session.commit()
    
    # Create appearances
    a1 = Appearance(rating=4, episode_id=e1.id, guest_id=g1.id)
    a2 = Appearance(rating=5, episode_id=e2.id, guest_id=g3.id)
    a3 = Appearance(rating=3, episode_id=e1.id, guest_id=g2.id)
    a4 = Appearance(rating=5, episode_id=e3.id, guest_id=g4.id)
    
    db.session.add_all([a1, a2, a3, a4])
    db.session.commit()
    
    print(" Database seeded successfully")