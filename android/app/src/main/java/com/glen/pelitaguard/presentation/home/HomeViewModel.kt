package com.glen.pelitaguard.presentation.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.glen.pelitaguard.data.local.SessionManager
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val sessionManager: SessionManager
) : ViewModel() {

    fun logout(onSuccess: () -> Unit) {
        viewModelScope.launch {
            sessionManager.clearToken()
            onSuccess()
        }
    }
}
