from app import create_app
from app.extensions import db
from app.models import FollowUp, Interchange, Participant, User

app = create_app()

with app.app_context():
    print("Testing Interchange query...")
    try:
        interchanges = Interchange.query.all()
        print(f"Found {len(interchanges)} interchanges")
        for i in interchanges:
            print(f"Interchange: {i.id}, Giver: {i.giver}, Receiver: {i.receiver}")
    except Exception as e:
        print(f"Error querying Interchange: {e}")
        import traceback

        traceback.print_exc()

    print("\nTesting FollowUp query...")
    try:
        followups = FollowUp.query.all()
        print(f"Found {len(followups)} followups")
        for f in followups:
            print(f"FollowUp: {f.id}, Participant: {f.participant}")
    except Exception as e:
        print(f"Error querying FollowUp: {e}")
        import traceback

        traceback.print_exc()
