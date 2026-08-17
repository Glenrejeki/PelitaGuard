package com.glen.pelitaguard.navigation

sealed class Screen(val route: String) {
    object Landing : Screen("landing")
    object Login : Screen("login")
    object Register : Screen("register")
    object Home : Screen("home")
    object Report : Screen("report")
    object Preview : Screen("preview")
}
