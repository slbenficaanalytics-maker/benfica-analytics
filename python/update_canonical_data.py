"""
Atualiza toda a camada canónica dos jogos da Liga Portugal 2025/26.
"""

import subprocess
import sys


scripts = [
    "python/create_match_id_crosswalk.py",
    "python/add_football_data_to_crosswalk.py",
    "python/create_canonical_matches.py",
    "python/add_canonical_id_to_sofascore.py",
    "python/add_canonical_id_to_fotmob.py",
    "python/add_canonical_id_to_sofascore_incidents.py",
    "python/add_canonical_id_to_sofascore_shots.py",
    "python/add_canonical_id_to_sofascore_players.py",
    "python/create_liga_match_analysis.py",
    "python/audit_liga_match_analysis.py",
    "python/calculate_result_performance_gap.py",
    "python/create_result_xg_summary.py",
]


for script in scripts:
    print(f"\n{'=' * 70}")
    print(f"A executar: {script}")
    print("=" * 70)

    result = subprocess.run(
        [sys.executable, script],
        check=False
    )

    if result.returncode != 0:
        raise SystemExit(
            f"Falhou o script: {script}"
        )


print("\nAtualização canónica concluída com sucesso.")
