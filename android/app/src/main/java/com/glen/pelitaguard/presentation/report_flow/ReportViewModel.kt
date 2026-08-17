package com.glen.pelitaguard.presentation.report_flow

import android.net.Uri
import androidx.compose.runtime.State
import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.glen.pelitaguard.data.api.ReportApi
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.launch
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.RequestBody.Companion.toRequestBody
import javax.inject.Inject

@HiltViewModel
class ReportViewModel @Inject constructor(
    private val reportApi: ReportApi
) : ViewModel() {

    private val _isLoading = mutableStateOf(false)
    val isLoading: State<Boolean> = _isLoading

    private val _error = mutableStateOf<String?>(null)
    val error: State<String?> = _error

    fun submitReport(
        title: String,
        description: String,
        imageBytes: ByteArray?,
        imageName: String?,
        onSuccess: () -> Unit
    ) {
        viewModelScope.launch {
            _isLoading.value = true
            _error.value = null
            try {
                val titlePart = title.toRequestBody("text/plain".toMediaTypeOrNull())
                val descPart = description.toRequestBody("text/plain".toMediaTypeOrNull())
                
                var imagePart: MultipartBody.Part? = null
                if (imageBytes != null && imageName != null) {
                    val requestFile = imageBytes.toRequestBody("image/*".toMediaTypeOrNull())
                    imagePart = MultipartBody.Part.createFormData("image", imageName, requestFile)
                }

                reportApi.createReport(titlePart, descPart, imagePart)
                onSuccess()
            } catch (e: Exception) {
                _error.value = e.message ?: "Gagal mengirim laporan"
            } finally {
                _isLoading.value = false
            }
        }
    }
}
