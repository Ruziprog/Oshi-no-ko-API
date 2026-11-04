import api from './client';

import type {
    RegisterRequest,
    LoginRequest, 
    UserResponse, 
    TokenResponse 
} from '../types/auth';

export async function registerUser(data: RegisterRequest):
    Promise<UserResponse> {
        const response = await api.post<UserResponse>('/auth/register', data);
        return response.data;
    }

export async function loginUser(data: LoginRequest):
    Promise<TokenResponse> {
        const FormData = new URLSearchParams();

        FormData.append('username', data.username);
        FormData.append('password', data.password);

        const response = await api.post<TokenResponse>('/auth/login', FormData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
        return response.data;
    }

export function saveToken(token: string) {
    localStorage.setItem('access_token', token)
}
