demo:
	@echo "Seeding demo data and starting services..."
	# NOTE: Customize these as per your manage.py and compose setup
	docker compose up -d db redis
	docker compose up -d backend
	sleep 5
	docker compose exec backend python manage.py migrate
	docker compose exec backend python manage.py loaddata demo_fixtures.json || true
	docker compose up -d rqworker frontend nginx
	@echo "Demo environment is up. Open: http://localhost:3000"
