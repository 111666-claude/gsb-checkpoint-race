"""报告入口：跑样例或生成 out/report.txt。"""

import argparse
import os

from .track import Track

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(HERE, "out", "report.txt")


def build_parser():
    parser = argparse.ArgumentParser(prog="checkpoint-race", description="竞速检查点")
    parser.add_argument("--sample", default="order", help="order / dup / shortcut / work")
    parser.add_argument("--out", default=DEFAULT_OUT, help="报告文件路径")
    return parser


def write_report(path, track):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    lines = ["player  time_ms  skipped  suspicious"]
    for player, time_ms, skipped, suspicious in track.standings():
        lines.append("%s  %d  %d  %d" % (player, time_ms, skipped, suspicious))
    text = "\n".join(lines) + "\n"
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    return text


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample == "order":
        track = Track(["c0", "c1", "c2"], 0)
        track.record("m1", "p", 2, 100)
        track.record("m2", "p", 0, 0)
        track.record("m3", "p", 1, 50)
        track.record("m4", "p", 2, 200)
        write_report(args.out, track)
        print("skipped=%d" % track.standings()[0][2])
    elif args.sample == "dup":
        track = Track(["c0", "c1"], 0)
        track.record("m1", "p", 0, 0)
        track.record("m1", "p", 1, 10)
        print("records=%d" % track.record_count())
    elif args.sample == "shortcut":
        track = Track(["c0", "c1"], 100)
        track.record("m1", "p", 0, 0)
        track.record("m2", "p", 1, 50)
        print("suspicious=%d" % track.standings()[0][3])
    elif args.sample == "work":
        track = Track(["c0", "c1"], 0)
        for index in range(3000):
            track.record("m-%d" % index, "p-%d" % index, 0, index)
        for _ in range(3000):
            track.standings()
        print("work=%d" % track.work_count())
    else:
        raise SystemExit("需要 --sample order|dup|shortcut|work")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
