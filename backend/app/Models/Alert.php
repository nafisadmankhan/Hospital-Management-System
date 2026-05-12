<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Alert extends Model
{
    use HasFactory; 

    protected $fillable = [
        'id', 
        'tenant_id', 
        'trigger_type', 
        'severity', 
        'status', 
        'title', 
        'message'
    ];  

    protected $keyType = 'string';
    public $incrementing = false;
}
