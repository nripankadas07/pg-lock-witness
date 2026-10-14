"""Offline bounded pg-lock-witness analyzer. No operational writes."""

from collections import deque

def analyze(d):
    if not isinstance(d,dict) or set(d)!={'sessions'}: raise ValueError('expected sessions only')
    rows=d['sessions']
    if not isinstance(rows,list) or len(rows)>256: raise ValueError('at most 256 sessions')
    graph={}
    for row in rows:
        if not isinstance(row,dict) or set(row)!={'pid','blocking_pids'}: raise ValueError('expected pid and blocking_pids')
        pid=row['pid']; blockers=row['blocking_pids']
        if type(pid)!=int or pid<=0 or pid in graph: raise ValueError('unique positive session pid required')
        if not isinstance(blockers,list) or len(blockers)>256 or any(type(x)!=int or x<0 for x in blockers): raise ValueError('invalid blocking_pids')
        graph[pid]=sorted(set(blockers))
    # Reachability over the captured graph, without inventing rows for unseen blockers.
    reach={}
    for pid in graph:
        seen=set(); queue=deque(graph[pid])
        while queue:
            x=queue.popleft()
            if x in seen: continue
            seen.add(x); queue.extend(graph.get(x,[]))
        reach[pid]=seen
    groups=[];used=set()
    for pid in sorted(graph):
        if pid in used or pid not in reach[pid]: continue
        group=sorted(x for x in graph if x in reach[pid] and pid in reach[x]);used.update(group)
        # A shortest concrete cycle anchored at the smallest member. A BFS avoids recursion.
        start=group[0]; queue=deque([[start]]); seen={start}; cycle=None
        while queue and cycle is None:
            path=queue.popleft()
            for nxt in graph[path[-1]]:
                if nxt==start: cycle=path+[start];break
                if nxt in group and nxt not in seen: seen.add(nxt);queue.append(path+[nxt])
        groups.append({'members':group,'cycle':cycle,'edges':[{'waiter':a,'blocker':b} for a,b in zip(cycle,cycle[1:])]})
    cycle_members=set(used)
    return {'cycles':groups,'blocked_by_cycle':sorted(p for p in graph if p not in used and reach[p]&cycle_members),
            'terminal_observed_blockers':sorted(p for p in graph if not graph[p] and any(p in v for v in graph.values())),
            'unobserved_blockers':sorted({b for v in graph.values() for b in v if b and b not in graph}),
            'prepared_transaction_waiters':sorted(p for p in graph if 0 in reach[p]),
            'snapshot_cycle_only':True,'sessions':len(graph),'edges':sum(map(len,graph.values()))}

def _pairs(pairs):
    result={}
    for key,val in pairs:
        if key in result:raise ValueError('duplicate JSON key: '+key)
        result[key]=val
    return result

def main():
    import argparse,json,sys
    from pathlib import Path
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',help='JSON input path; - for stdin')
    args=parser.parse_args()
    try:
        raw=sys.stdin.buffer.read(1048577) if args.input=='-' else Path(args.input).open('rb').read(1048577)
        if len(raw)>1048576:raise ValueError('input exceeds 1 MiB')
        data=json.loads(raw,object_pairs_hook=_pairs,parse_constant=lambda x:(_ for _ in ()).throw(ValueError('nonfinite JSON number')))
        print(json.dumps(analyze(data),ensure_ascii=True,indent=2));return 0
    except (ValueError,TypeError,KeyError,OverflowError,RecursionError,OSError) as exc:
        print(json.dumps({'error':str(exc)}),file=sys.stderr);return 2

if __name__=='__main__':raise SystemExit(main())
