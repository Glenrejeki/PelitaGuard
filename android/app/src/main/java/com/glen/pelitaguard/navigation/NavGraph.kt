package com.glen.pelitaguard.navigation

import androidx.compose.runtime.Composable
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import com.glen.pelitaguard.presentation.auth.AuthViewModel
import com.glen.pelitaguard.presentation.auth.LoginScreen
import com.glen.pelitaguard.presentation.auth.RegisterScreen
import com.glen.pelitaguard.presentation.home.HomeScreen
import com.glen.pelitaguard.presentation.home.HomeViewModel
import com.glen.pelitaguard.presentation.landing.LandingScreen

@Composable
fun NavGraph(
    navController: NavHostController, 
    startDestination: String = Screen.Landing.route
) {
    NavHost(
        navController = navController,
        startDestination = startDestination
    ) {
        composable(Screen.Landing.route) {
            LandingScreen(
                onNavigateToLogin = { navController.navigate(Screen.Login.route) },
                onNavigateToRegister = { navController.navigate(Screen.Register.route) }
            )
        }
        
        composable(Screen.Login.route) {
            val viewModel: AuthViewModel = hiltViewModel()
            LoginScreen(
                viewModel = viewModel,
                onLoginSuccess = {
                    navController.navigate(Screen.Home.route) {
                        popUpTo(Screen.Landing.route) { inclusive = true }
                    }
                }
            )
        }
        
        composable(Screen.Register.route) {
            val viewModel: AuthViewModel = hiltViewModel()
            RegisterScreen(
                viewModel = viewModel,
                onRegisterSuccess = {
                    navController.navigate(Screen.Home.route) {
                        popUpTo(Screen.Landing.route) { inclusive = true }
                    }
                }
            )
        }
        
        composable(Screen.Home.route) {
            val viewModel: HomeViewModel = hiltViewModel()
            HomeScreen(
                onNavigateToReport = { navController.navigate(Screen.Report.route) },
                onLogout = {
                    viewModel.logout {
                        navController.navigate(Screen.Landing.route) {
                            popUpTo(Screen.Home.route) { inclusive = true }
                        }
                    }
                }
            )
        }

        composable(Screen.Report.route) {
            // Placeholder for ReportScreen
        }
    }
}
