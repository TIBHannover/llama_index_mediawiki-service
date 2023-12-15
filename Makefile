up:
	docker compose up 

build:
	docker compose build --no-cache

down:
	docker compose down

destroy:
	docker compose down -v

install-lcpp-cuda:
	CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
