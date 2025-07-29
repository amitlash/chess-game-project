import logging

from app.api.routes import router as chess_router
from app.core.error_middleware import setup_error_handlers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

app = FastAPI(
    title="Chess Game API",
    description="A chess game API with AI integration",
    version="1.0.0",
    debug=True,  # Enable debug mode for development
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up error handlers
setup_error_handlers(app)


# Add custom 404 handler
@app.exception_handler(404)
async def not_found_handler(request, exc):
    from fastapi.responses import JSONResponse

    return JSONResponse(
        status_code=404,
        content={
            "error": True,
            "message": "Not Found",
            "error_code": "HTTP_404",
            "status_code": 404,
            "details": {"path": request.url.path, "method": request.method},
        },
        headers={"x-error-handled": "true", "x-request-id": str(id(request))},
    )


app.include_router(chess_router)
