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
        return [
            'id' => Str::uuid(),
            'tenant_id' => 'tenant-001',
            'ward_id' => 'ward-001',
            'bed_number' => 'B-' . $this->faker->unique()->numberBetween(100, 9999),
            'status' => $this->faker->randomElement(['available', 'occupied', 'maintenance']),
            'has_oxygen' => $this->faker->boolean(80),
            'daily_rate_bdt' => 1500,
            'created_at' => now(),
            'updated_at' => now()
        ];
    }
}
