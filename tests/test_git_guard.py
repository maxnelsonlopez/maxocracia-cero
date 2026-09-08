# -*- coding: utf-8 -*-
"""Tests del guard de historial de git (blindaje del custodio).

Decreto: prohibir comandos que atenten contra el historial; el resto se
confía. Aquí se verifican ambos lados de la línea.
"""

import subprocess
from pathlib import Path

import pytest

from maxocontracts.concilio.executor import EjecutorGuardado, GuardDeniedError
from maxocontracts.concilio.git_guard import (
    guard_git_command,
    git_denial,
    parse_command,
)
from scripts.git_hooks.pre_push_guard import check_ancestor, parse_push_lines

PELIGROSOS = [
    ["push", "origin", "main", "--force"],
    ["push", "-f", "origin", "main"],
    ["push", "origin", "+main"],
    ["push", "origin", ":feature"],
    ["push", "--delete", "origin", "feature"],
    ["commit", "--amend", "-m", "x"],
    ["rebase", "origin", "main"],
    ["reset", "--hard", "HEAD~1"],
    ["clean", "-fdx"],
    ["checkout", "--force", "."],
    ["fetch", "--force", "origin"],
    ["reflog", "expire", "--all"],
    ["gc", "--prune=now"],
    ["filter-branch", "--force"],
    ["filter-repo", "--force"],
]

SEGUROS = [
    ["push", "origin", "main"],
    ["commit", "-m", "feat(x): algo"],
    ["add", "maxocontracts"],
    ["status"],
    ["log", "--oneline", "-5"],
    ["reset", "--soft", "HEAD~1"],
    ["branch", "-D", "vieja"],  # borra rama local, no historial
    ["clean", "-n"],
    ["gc"],
]


@pytest.mark.parametrize("args", PELIGROSOS)
def test_comandos_peligrosos_bloqueados(args):
    assert git_denial(args) is not None


@pytest.mark.parametrize("args", SEGUROS)
def test_comandos_seguros_permitidos(args):
    assert git_denial(args) is None


def test_guard_git_command_detecta_peligro_en_linea_completa():
    assert guard_git_command("git push origin main --force") is not None
    assert guard_git_command("git commit --amend -m x") is not None


def test_guard_git_command_no_aplica_a_otros_comandos():
    assert guard_git_command("rm -rf scratch") is None
    assert guard_git_command("ls -la") is None


def test_guard_git_command_fail_closed_en_comillas_rotas():
    # comillas sin cerrar: el parser falla y el guard bloquea (fail-closed)
    assert guard_git_command("git commit -m 'sin cerrar") is not None


def test_parse_command_divide_tokens():
    assert parse_command('git add "maxocontracts/ oracles"') == [
        "git", "add", "maxocontracts/ oracles",
    ]


def test_ejecutor_permite_git_normal(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    eventos = []
    ejecutor = EjecutorGuardado(str(repo), on_event=eventos.append)
    r = ejecutor.run("git status")
    assert r.returncode == 0
    assert any(e.get("evento") == "resultado" for e in eventos)
    assert all(e.get("guard_git") != "bloqueado" for e in eventos)


def test_ejecutor_bloquea_reset_hard(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    eventos = []
    ejecutor = EjecutorGuardado(str(repo), on_event=eventos.append)
    with pytest.raises(GuardDeniedError, match="reset --hard"):
        ejecutor.run("git reset --hard HEAD~1")
    assert any(e.get("evento") == "GUARD_DENIED" for e in eventos)


def test_guard_bloquea_antes_de_ejecutar_nada(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    (repo / "trabajo.txt").write_text("datos", encoding="utf-8")
    eventos = []
    ejecutor = EjecutorGuardado(str(repo), on_event=eventos.append)
    with pytest.raises(GuardDeniedError):
        ejecutor.run("git clean -fd")
    assert (repo / "trabajo.txt").exists()  # nada se tocó


# --- Pre-push hook (historial remoto) ---


def test_check_ancestor_permite_fast_forward():
    # dos commits en la misma línea: el remoto es ancestro del local
    repo = _repo_con_commits(2)
    local = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True
    ).stdout.strip()
    remoto = subprocess.run(
        ["git", "rev-parse", "HEAD~1"], cwd=repo, capture_output=True, text=True
    ).stdout.strip()
    assert check_ancestor(local, remoto, str(repo)) is None


def test_check_ancestor_bloquea_reescritura():
    repo = _repo_con_commits(2)  # c0, c1
    first = subprocess.run(
        ["git", "rev-parse", "HEAD~1"], cwd=repo, capture_output=True, text=True
    ).stdout.strip()
    head = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True
    ).stdout.strip()
    # sha remoto inexistente: nada que proteger (el remoto validará)
    assert check_ancestor(first, "9" * 40, str(repo)) is None
    # borrado de ref remota (local zeros, remoto real): bloqueado
    motivo_borrado = check_ancestor("0" * 40, head, str(repo))
    assert motivo_borrado is not None and "BORRADA" in motivo_borrado
    # historial divergente: remoto = c1, local = c0 (c1 no es ancestro de c0): bloqueado
    motivo_rewrite = check_ancestor(first, head, str(repo))
    assert motivo_rewrite is not None


def _repo_con_commits(n):
    import tempfile

    repo = Path(tempfile.mkdtemp())
    subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "t@t.t"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=repo, check=True)
    for i in range(n):
        (repo / f"f{i}.txt").write_text(f"{i}", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-qm", f"c{i}"], cwd=repo, check=True)
    return repo


def test_parse_push_lines():
    lineas = [
        "refs/heads/main aaaa refs/heads/main bbbb",
        "refs/heads/x cccc refs/heads/x 0000000000000000000000000000000000000000",
    ]
    parsed = list(parse_push_lines(lineas))
    assert len(parsed) == 2
    assert parsed[0][0] == "refs/heads/main"


def test_guard_bloquea_push_con_plus_y_borrado():
    assert git_denial(["push", "origin", "+main"]) is not None
    assert git_denial(["push", "origin", ":main"]) is not None
