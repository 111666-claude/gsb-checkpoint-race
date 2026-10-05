# checkpoint-race

竞速检查点：按顺序通过检查点，统计用时与可疑抄近路，结果写进 `out/report.txt`，只用 Python 标准库。

```
python3 -m race.report --sample order
python3 -m race.report --sample dup
python3 -m race.report --sample shortcut
python3 -m race.report --sample work
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **顺序**：必须按 `checkpoints` 的顺序通过；跳号一次 `skipped` 加一；同一个检查点重复通过只算第一次。
- **完赛**：通过最后一个检查点才算完赛，用时等于最后一次通过减第一次通过。
- **抄近路**：相邻两次通过的间隔小于 `min_gap_ms` 记一次 `suspicious`。
- **幂等**：同一个 `pass_id` 只记一次，重复上报不改变任何统计。
- **代价**：`standings` 不许全扫全部通过记录，`work_count()` 不随通过数乘统计次数增长；
  100 万次通过、每秒 10 万次统计。

## 输出契约（不改格式）

```
skipped=..
records=..
suspicious=..
work=..
```

报告文件 `out/report.txt` 每行是 `player  time_ms  skipped  suspicious`，首行是表头。

## 目录

```
race/track.py       顺序校验、用时与抄近路
race/report.py      样例入口与报告文件
tests/test_track.py unittest 用例
```
