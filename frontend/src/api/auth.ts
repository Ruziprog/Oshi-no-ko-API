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
        const formData = new URLSearchParams();

        formData.append('username', data.username);
        formData.append('password', data.password);

        const response = await api.post<TokenResponse>('/auth/login', formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
        return response.data;
    }

export function saveToken(token: string) {
    localStorage.setItem('access_token', token)
}

export async function getCurrentUser(): Promise<UserResponse> {
    const response = await api.get<UserResponse>('/auth/me')
    return response.data
}

export async function uploadAvatar(file: File): Promise<{ avatar_url: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/users/me/avatar', formData);

    return response.data;
}


export async function deleteAvatar(): Promise<void> {
    await api.delete('/users/me/avatar');
}