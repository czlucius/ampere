from dataclasses import dataclass
from typing import Any

from pyston.models import RunStage, CompileStage


@dataclass
class OutputInfo:
    output: str
    exit_code: int
    signal: Any
    language: str

    raw_run_stage: RunStage
    raw_compile_stage: CompileStage