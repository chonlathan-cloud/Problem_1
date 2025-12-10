from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# For simplicity, we're just checking for token presence. 
# In a real app, this would validate the JWT token.

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    if credentials.credentials == "mock_jwt_token": # Placeholder token for testing
        return "mock_user_id" # Return a mock user ID
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
