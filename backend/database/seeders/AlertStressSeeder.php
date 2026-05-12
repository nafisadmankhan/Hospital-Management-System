<?php

namespace Database\Seeders;

use App\Models\Alert;
use Illuminate\Database\Seeder;

class AlertStressSeeder extends Seeder
{
    public function run(): void
    {
        $total = 1000000;
        $chunkSize = 5000; 

        $this->command->getOutput()->progressStart($total);

        for ($i = 0; $i < ($total / $chunkSize); $i++) {
            Alert::factory()->count($chunkSize)->create([
                'tenant_id' => 'tenant-001',
                'status' => 'delivered'
            ]);
            $this->command->getOutput()->progressAdvance($chunkSize);
        }

        $this->command->getOutput()->progressFinish();
    }
}