"""
measure.py

Ham dung chung de do Runtime va Memory Usage cho tat ca thuat toan,
theo dung chuan da thong nhat trong tai lieu du an:
    - Runtime: do bang time.perf_counter().
    - Memory Usage: do bang psutil (RSS - Resident Set Size) truoc/sau khi chay.

Tat ca thuat toan (ILP, 2-opt, ...) deu goi qua ham run_with_metrics()
de dam bao ket qua Output dong nhat: Tour, Tour Length, Runtime, Memory Usage.
"""

from __future__ import annotations
import time
import os
from typing import Callable, Any, Dict

try:
    import psutil
    _PROCESS = psutil.Process(os.getpid())
except ImportError:  # psutil chua duoc cai, van cho chay nhung khong co memory usage
    psutil = None
    _PROCESS = None


def _current_memory_mb() -> float:
    """Tra ve memory (RSS) hien tai cua tien trinh, don vi MB."""
    if _PROCESS is None:
        return 0.0
    return _PROCESS.memory_info().rss / (1024 ** 2)


def run_with_metrics(algorithm_fn: Callable[..., Any], *args, **kwargs) -> Dict[str, Any]:
    """
    Chay mot ham thuat toan va do Runtime + Memory Usage.

    Args:
        algorithm_fn: ham thuat toan, phai tra ve dict co it nhat 2 khoa "tour" va "tour_length".
        *args, **kwargs: tham so truyen cho algorithm_fn.

    Returns:
        dict chuan hoa gom:
            tour, tour_length, runtime_seconds, memory_usage_mb
        (cong them cac field khac ma algorithm_fn tra ve, neu co, vi du "status").
    """
    mem_before = _current_memory_mb()
    start = time.perf_counter()

    result = algorithm_fn(*args, **kwargs)

    elapsed = time.perf_counter() - start
    mem_after = _current_memory_mb()

    output = dict(result)  # copy de khong sua doi ket qua goc
    output["runtime_seconds"] = elapsed
    # Memory usage uoc luong: chenh lech RSS truoc/sau (co the = 0 voi bai toan rat nho)
    output["memory_usage_mb"] = max(mem_after - mem_before, 0.0)
    return output
