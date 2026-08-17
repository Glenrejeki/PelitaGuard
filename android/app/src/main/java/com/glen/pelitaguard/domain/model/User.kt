package com.glen.pelitaguard.domain.model

data class User(
    val id: Int,
    val username: String,
    val email: String
)

data class AuthResponse(
    val access_token: String,
    val token_type: String
)
