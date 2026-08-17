package com.glen.pelitaguard.data.api

import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.http.*

interface ReportApi {
    @Multipart
    @POST("report/")
    suspend fun createReport(
        @Part("title") title: RequestBody,
        @Part("description") description: RequestBody,
        @Part image: MultipartBody.Part?
    ): Any 
}
