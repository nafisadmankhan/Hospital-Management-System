<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class beds extends Model
{
    /** @use HasFactory<\Database\Factories\BedsFactory> */
    use HasFactory;

    protected $fillable = [
        'id',
        'tenant_id',
        'ward_id',
        'bed_number',
        'status',
        'has_oxygen',
        'has_ventilator',
        'has_monitor',
        'daily_rate_bdt',
        'current_patient_id',
        'admission_date',
        'expected_discharge_date',
        'meta'
    ];
}
