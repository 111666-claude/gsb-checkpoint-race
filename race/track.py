"""竞速检查点：按顺序通过检查点，统计用时与可疑抄近路。

口径见 README：按 checkpoints 顺序通过，跳号记 skipped；过最后一个检查点才算完赛；
相邻通过间隔小于 min_gap_ms 记 suspicious；同一个 pass_id 只记一次；
standings 增量维护并缓存，不全扫通过记录。
"""


class Track:
    """赛道台账。"""

    def __init__(self, checkpoints, min_gap_ms):
        self.checkpoints = list(checkpoints)
        self.min_gap_ms = min_gap_ms
        self.work = 0
        self._seen_ids = set()
        self._players = {}
        self._cache = None

    def record(self, pass_id, player, index, at_ms):
        """记录一次通过；重复 pass_id、重复检查点、越界序号直接忽略。"""
        if pass_id in self._seen_ids:
            return False
        self._seen_ids.add(pass_id)
        self.work += 1
        if index < 0 or index >= len(self.checkpoints):
            return False
        entry = self._players.get(player)
        if entry is None:
            entry = {"next": 0, "first": None, "last": None, "skipped": 0, "suspicious": 0}
            self._players[player] = entry
        if index < entry["next"]:
            return True
        if index > entry["next"]:
            entry["skipped"] += 1
        entry["next"] = index + 1
        if entry["last"] is not None and at_ms - entry["last"] < self.min_gap_ms:
            entry["suspicious"] += 1
        if entry["first"] is None:
            entry["first"] = at_ms
        entry["last"] = at_ms
        self._cache = None
        return True

    def record_count(self):
        return len(self._seen_ids)

    def standings(self):
        """返回按用时升序的 (player, time_ms, skipped, suspicious)；只统计完赛者，结果缓存。"""
        if self._cache is None:
            self.work += len(self._players)
            last_index = len(self.checkpoints) - 1
            rows = []
            for player, entry in self._players.items():
                if entry["next"] > last_index and entry["first"] is not None:
                    rows.append((player, entry["last"] - entry["first"], entry["skipped"], entry["suspicious"]))
            rows.sort(key=lambda row: (row[1], row[0]))
            self._cache = rows
        return list(self._cache)

    def work_count(self):
        return self.work
