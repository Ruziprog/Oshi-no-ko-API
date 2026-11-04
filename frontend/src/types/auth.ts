export interface RegisterRequest {
    username: string;
    email: string;
    password: string;
}

export interface LoginRequest {
    username: string;
    password: string;
}

export interface UserResponse {
    id: string;
    username: string;
    email: string;
}

export interface TokenResponse {
    access_token: string;
    token_type: string;
}