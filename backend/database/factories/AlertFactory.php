<?php

namespace Database\Factories;

use App\Models\Alert;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Alert>
 */
class AlertFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'id' => 'alert-' . $this->faker->unique()->uuid(),
            'tenant_id' => 'tenant-001',
            'trigger_type' => 'critical_lab_result',
            'severity' => $this->faker->randomElement(['low', 'medium', 'high', 'critical']),
            'status' => 'delivered',
            'title' => $this->faker->sentence(),
            'message' => $this->faker->paragraph(),
        ];
    }
}
