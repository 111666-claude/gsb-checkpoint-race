"""竞速检查点：按顺序通过检查点，统计用时与可疑抄近路。

口径（见 README）：必须按 checkpoints 顺序通过，跳号一次 skipped 加一；
同一个检查点重复通过只算第一次；通过最后一个检查点才算完赛，用时等于
最后一次通过减第一次通过；相邻两次通过间隔小于 min_gap_ms 记一次
suspicious；同一个 pass_id 只记一次；standings 增量维护，不全扫通过记录。
"""


class Track:
    """赛道台账。"""

    def __init__(self, checkpoints, min_gap_ms):
        self.checkpoints = list(checkpoints)
        self.min_gap_ms = min_gap_ms
        self._seen_ids = set()
        self._players = {}
        self._records = 0
        self._standings_cache = None
        self.work = 0

    def record(self, pass_id, player, index, at_ms):
        """记录一次通过；同一 pass_id 只记一次，重复上报不改变任何统计。"""
        if pass_id in self._seen_ids:
            return False
        self._seen_ids.add(pass_id)
        self._records += 1
        self.work += 1
        state = self._players.get(player)
        if state is None:
            state = {"next": 0, "first": None, "last": None, "skipped": 0, "suspicious": 0}
            self._players[player] = state
        if index < state["next"]:
            return True
        if index > state["next"]:
            state["skipped"] += 1
        state["next"] = index + 1
        if state["last"] is not None and at_ms - state["last"] < self.min_gap_ms:
            state["suspicious"] += 1
        if state["first"] is None:
            state["first"] = at_ms
        state["last"] = at_ms
        self._standings_cache = None
        return True

    def record_count(self):
        return self._records

    def standings(self):
        """返回按用时升序的 (player, time_ms, skipped, suspicious)；只含完赛者。"""
        if self._standings_cache is None:
            rows = []
            for player, state in self._players.items():
                if state["first"] is not None and state["next"] >= len(self.checkpoints):
                    rows.append((player, state["last"] - state["first"],
                                 state["skipped"], state["suspicious"]))
            rows.sort(key=lambda row: (row[1], row[0]))
            self._standings_cache = rows
        return list(self._standings_cache)

    def work_count(self):
        return self.work
