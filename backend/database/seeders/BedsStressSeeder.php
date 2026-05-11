<?php

namespace Database\Seeders;

use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use Illuminate\Database\Seeder;

class BedsStressSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        \Illuminate\Support\Facades\DB::table('beds')->truncate();
        ini_set('memory_limit', '-1');

        $total = 1000000;
        $batchSize = 5000;

        $this->command->getOutput()->progressStart($total);

        for ($i = 0; $i < ($total / $batchSize); $i++) {
            $data = [];

            for ($j = 0; $j < $batchSize; $j++) {
                $data[] = [
                    'id' => (string) \Illuminate\Support\Str::uuid(),
                    'tenant_id' => 'tenant-001',
                    'ward_id' => 'ward-001',
                    'bed_number' => 'B-' . (($i * $batchSize) + $j),
                    'status' => 'available',
                    'has_oxygen' => false,
                    'has_ventilator' => false,
                    'has_monitor' => false,
                    'daily_rate_bdt' => 1000.00,
                    'meta' => json_encode(['note' => 'auto-generated']),
                    'created_at' => now(),
                    'updated_at' => now(),
                ];
            }

            \Illuminate\Support\Facades\DB::table('beds')->insert($data);
            $this->command->getOutput()->progressAdvance($batchSize);

            unset($data);
            gc_collect_cycles();
        }

        $this->command->getOutput()->progressFinish();
    }
}
