"""Verifica a seleção no batch sem executar as baterias científicas longas."""
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "Scripts"))
import automate_simulations as batch
import inject_and_test as pipeline


class DatasetTests(unittest.TestCase):
    def test_batch_action_and_manifest(self):
        for action, count, split in [("PETR4", 5198, [2600, 1299, 1299]),
                                     ("VALE3", 5192, [2596, 1298, 1298])]:
            with self.subTest(action=action), tempfile.TemporaryDirectory(dir=ROOT) as tmp:
                process = MagicMock()
                process.stdout = iter([])
                process.returncode = 0
                with patch.object(batch, "RESULTS_DIR", tmp), \
                     patch.object(sys, "argv", ["automate_simulations.py", "--acao", action, "--test", "--run", "1"]), \
                     patch.object(batch.subprocess, "Popen", return_value=process) as launch, \
                     contextlib.redirect_stdout(io.StringIO()):
                    batch.main()
                manifests = list(Path(tmp).glob("*/dataset.json"))
                self.assertEqual(len(manifests), 1)
                data = json.loads(manifests[0].read_text(encoding="utf-8"))
                self.assertEqual(data["acao"], action)
                self.assertEqual(data["amostras"], count)
                self.assertEqual([data[k] for k in ("treino_n", "valida_n", "teste_n")], split)
                self.assertEqual(launch.call_count, 4)
                for call in launch.call_args_list:
                    self.assertEqual(call.args[0][-1], action)
                    self.assertIn(action, call.args[0][-2])

    def test_evaluation_uses_selected_action(self):
        best = dict(tam_reservoir=2, epoca_matrizes=1, win_file="win", w_file="w", wout_file="out",
                    a=0.8, sr=0.4, initLen=10, reg=0.001)
        # Os arquivos de matrizes não são o objeto deste teste.
        with patch.object(pipeline, "build_r_matrix_win", return_value=("Win <- matrix(0.1,2,2)", 2)), \
             patch.object(pipeline, "build_r_matrix_w", return_value="W <- diag(2)"), \
             patch.object(pipeline, "build_r_matrix_wout", return_value="Wout <- matrix(0.1,1,4)"):
            for action in ("PETR4", "VALE3"):
                script = pipeline.generate_r_script(dict(best, acao=action), "output", "data", MagicMock(), "val.png", "test.png")
                self.assertIn(f"'{action}_close com factor_2000-2020.txt'", script)
                self.assertIn(f"ESN {action}", script)
                self.assertIn("ceiling(length(data) / 2)", script)


if __name__ == "__main__":
    unittest.main()
