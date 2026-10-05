"""竞速检查点：按顺序通过检查点，统计用时与可疑抄近路。

缺陷：不校验通过顺序、重复通过同一检查点重复计数、不检查相邻通过的间隔、
同一个 pass_id 重复记录、排名统计全扫通过记录。
"""


class Track:
    """赛道台账。"""

    def __init__(self, checkpoints, min_gap_ms):
        self.checkpoints = list(checkpoints)
        self.min_gap_ms = min_gap_ms
        self.passes = []
        self.work = 0

    def record(self, pass_id, player, index, at_ms):
        """记录一次通过。缺陷：不看顺序、不查 pass_id、不查间隔。"""
        self.passes.append((player, index, at_ms))
        return True

    def record_count(self):
        return len(self.passes)

    def standings(self):
        """返回按用时升序的 (player, time_ms, skipped, suspicious)。缺陷：全扫、乱序也算完赛。"""
        self.work += len(self.passes)
        players = {}
        for player, _, at_ms in self.passes:
            entry = players.setdefault(player, {"first": at_ms, "last": at_ms})
            entry["last"] = at_ms
        rows = []
        for player, entry in players.items():
            rows.append((player, entry["last"] - entry["first"], 0, 0))
        rows.sort(key=lambda row: (row[1], row[0]))
        return rows

    def work_count(self):
        return self.work
