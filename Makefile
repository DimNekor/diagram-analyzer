DOCKER_COMPOSE = docker-compose -f docker/docker-compose.yml

.PHONY: up down logs backend-up frontend-up backend-build frontend-build rebuild

# Запустить оба сервиса
up:
	$(DOCKER_COMPOSE) up --build

# Остановить и удалить контейнеры
down:
	$(DOCKER_COMPOSE) down

# Логи сразу обоих
logs:
	$(DOCKER_COMPOSE) logs -f

# Собрать только backend образ
backend-build:
	$(DOCKER_COMPOSE) build backend

# Собрать только frontend образ
frontend-build:
	$(DOCKER_COMPOSE) build frontend

# Запустить только backend (без frontend)
backend-up:
	$(DOCKER_COMPOSE) up --build backend

# Запустить только frontend (backend должен уже работать)
frontend-up:
	$(DOCKER_COMPOSE) up --build frontend

# Полная пересборка обоих
rebuild:
	$(DOCKER_COMPOSE) down
	$(DOCKER_COMPOSE) up --build
