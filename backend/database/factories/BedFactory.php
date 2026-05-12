<?php

namespace Database\Factories;

use App\Models\Model;
use App\Models\Bed;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Str;

/**
 * @extends Factory<Model>
 */
class BedFactory extends Factory
{
    protected $model = Bed::class;
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        $status = $this->faker->randomElement(['available', 'occupied', 'maintenance']);
        $isOccupied = $status === 'occupied';

        return [
            'id' => Str::uuid(),
            'tenant_id' => 'tenant-001',
            'ward_id' => 'ward-001',
            'bed_number' => 'B-' . $this->faker->unique()->numberBetween(100, 9999),
            'status' => $status,

            'has_oxygen' => $this->faker->boolean(80),
            'has_ventilator' => $this->faker->boolean(20),
            'has_monitor' => $this->faker->boolean(40),

            'current_patient_id' => $isOccupied ? 'patient-001' : null,
            'admission_date' => $isOccupied ? now()->subDays(rand(1, 5)) : null,
            'expected_discharge_date' => $isOccupied ? $this -> faker->dateTimeBetween('now', '+10 days') : null,

            'daily_rate_bdt' => 1500,

            'created_at' => now(),
            'updated_at' => now()
        ];
    }
}
