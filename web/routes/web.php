<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AdminController;
use App\Http\Controllers\UserController;
use App\Http\Controllers\RiwayatController;

Route::get('/', function () {
    return view('landing_page.landing');
});

Route::get('/admin/dashboard', [AdminController::class, 'dashboard']);

// RIWAYAT
Route::get('/admin/riwayat', [RiwayatController::class, 'index']);
Route::get('/admin/riwayat/edit/{id}', [RiwayatController::class, 'edit']);
Route::post('/admin/riwayat/update/{id}', [RiwayatController::class, 'update']);
Route::get('/admin/riwayat/delete/{id}', [RiwayatController::class, 'delete']);