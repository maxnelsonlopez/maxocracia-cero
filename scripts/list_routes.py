from app import create_app

app = create_app()


def list_routes():
    print(f"{'Endpoint':<40} {'Methods':<20} {'Rule'}")
    print("-" * 100)

    routes = []
    for rule in app.url_map.iter_rules():
        methods = ", ".join(sorted(rule.methods))
        routes.append((rule.endpoint, methods, str(rule)))

    # Sort by rule for better readability
    routes.sort(key=lambda x: x[2])

    for endpoint, methods, rule in routes:
        print(f"{endpoint:<40} {methods:<20} {rule}")


if __name__ == "__main__":
    with app.app_context():
        list_routes()
