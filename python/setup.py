from pathlib import Path
import shutil
from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.sdist import sdist


def resolve_common_rules_source(project_dir: Path) -> Path:
    local_copy = project_dir / "common_rules"
    if local_copy.is_dir():
        return local_copy
    repo_common = project_dir.parent / "common" / "rules"
    if repo_common.is_dir():
        return repo_common
    raise FileNotFoundError(f"Common rules directory not found at {local_copy} or {repo_common}")


class BuildPyWithCommonRules(build_py):
    def run(self) -> None:
        super().run()
        project_dir = Path(__file__).resolve().parent
        src_common = resolve_common_rules_source(project_dir)
        dest_common = Path(self.build_lib) / "semgrep_rules" / "common_rules"
        if dest_common.exists():
            shutil.rmtree(dest_common)
        shutil.copytree(src_common, dest_common)


class SdistWithCommonRules(sdist):
    def make_release_tree(self, base_dir: str, files: list[str]) -> None:
        super().make_release_tree(base_dir, files)
        project_dir = Path(__file__).resolve().parent
        src_common = resolve_common_rules_source(project_dir)
        dest_common = Path(base_dir) / "common_rules"
        if dest_common.exists():
            shutil.rmtree(dest_common)
        shutil.copytree(src_common, dest_common)


setup(
    cmdclass={
        "build_py": BuildPyWithCommonRules,
        "sdist": SdistWithCommonRules,
    }
)
