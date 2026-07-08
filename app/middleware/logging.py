import time

async def log_request(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    print(
        f"{request.method} {request.url.path} - {request.client.host} - {process_time:.4f}s"
    )

    return response