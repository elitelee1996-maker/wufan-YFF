"""CPM调度引擎 - 关键路径法计算"""
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, deque
from datetime import datetime, timedelta

class CPMEngine:
    """关键路径法计算引擎"""
    
    @staticmethod
    def forward_pass(tasks: Dict[str, Dict], dependencies: List[Dict]) -> Dict[str, Dict]:
        """
        前推法：计算最早开始时间(ES)和最早结束时间(EF)
        
        Args:
            tasks: {task_id: {duration, constraint_type, constraint_date}}
            dependencies: [{from_id, to_id, type, lag}]
        
        Returns:
            {task_id: {ES, EF, predecessors}}
        """
        # 构建邻接表
        successors = defaultdict(list)
        predecessors = defaultdict(list)
        
        for dep in dependencies:
            from_id = dep['from_id']
            to_id = dep['to_id']
            lag = dep.get('lag', 0)
            dep_type = dep.get('type', 'FS')
            
            successors[from_id].append((to_id, dep_type, lag))
            predecessors[to_id].append((from_id, dep_type, lag))
        
        # 拓扑排序
        in_degree = {tid: len(predecessors[tid]) for tid in tasks}
        queue = deque([tid for tid, deg in in_degree.items() if deg == 0])
        topo_order = []
        
        while queue:
            tid = queue.popleft()
            topo_order.append(tid)
            for succ, _, _ in successors[tid]:
                in_degree[succ] -= 1
                if in_degree[succ] == 0:
                    queue.append(succ)
        
        if len(topo_order) != len(tasks):
            raise ValueError("循环依赖检测失败")
        
        # 计算ES/EF
        result = {}
        for tid in topo_order:
            task = tasks[tid]
            duration = task['duration']
            
            # 计算ES
            if not predecessors[tid]:
                es = 0
            else:
                es = 0
                for pred_id, dep_type, lag in predecessors[tid]:
                    pred_ef = result[pred_id]['EF']
                    if dep_type == 'FS':
                        es = max(es, pred_ef + lag)
                    elif dep_type == 'SS':
                        pred_es = result[pred_id]['ES']
                        es = max(es, pred_es + lag)
                    elif dep_type == 'FF':
                        pred_ef = result[pred_id]['EF']
                        es = max(es, pred_ef + lag - duration)
                    elif dep_type == 'SF':
                        pred_es = result[pred_id]['ES']
                        es = max(es, pred_es + lag - duration)
            
            # 应用约束
            constraint_type = task.get('constraint_type', 'ASAP')
            constraint_date = task.get('constraint_date')
            
            if constraint_type == 'MSO' and constraint_date:
                es = max(es, constraint_date)
            elif constraint_type == 'SNET' and constraint_date:
                es = max(es, constraint_date)
            
            ef = es + duration
            
            result[tid] = {
                'ES': es,
                'EF': ef,
                'predecessors': [p[0] for p in predecessors[tid]]
            }
        
        return result
    
    @staticmethod
    def backward_pass(tasks: Dict[str, Dict], dependencies: List[Dict],
                     forward_result: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        后推法：计算最晚开始时间(LS)和最晚结束时间(LF)
        """
        # 构建邻接表
        successors = defaultdict(list)
        predecessors = defaultdict(list)
        
        for dep in dependencies:
            from_id = dep['from_id']
            to_id = dep['to_id']
            lag = dep.get('lag', 0)
            dep_type = dep.get('type', 'FS')
            
            successors[from_id].append((to_id, dep_type, lag))
            predecessors[to_id].append((from_id, dep_type, lag))
        
        # 逆拓扑排序
        in_degree = {tid: len(successors[tid]) for tid in tasks}
        queue = deque([tid for tid, deg in in_degree.items() if deg == 0])
        reverse_topo = []
        
        while queue:
            tid = queue.popleft()
            reverse_topo.append(tid)
            for pred, _, _ in predecessors[tid]:
                in_degree[pred] -= 1
                if in_degree[pred] == 0:
                    queue.append(pred)
        
        reverse_topo.reverse()
        
        # 计算项目总工期
        project_duration = max(r['EF'] for r in forward_result.values())
        
        # 计算LS/LF
        result = {}
        for tid in reverse_topo:
            task = tasks[tid]
            duration = task['duration']
            
            # 计算LF
            if not successors[tid]:
                lf = project_duration
            else:
                lf = float('inf')
                for succ_id, dep_type, lag in successors[tid]:
                    succ_ls = result[succ_id]['LS']
                    if dep_type == 'FS':
                        lf = min(lf, succ_ls - lag)
                    elif dep_type == 'SS':
                        succ_ls = result[succ_id]['LS']
                        lf = min(lf, succ_ls - lag + duration)
                    elif dep_type == 'FF':
                        succ_lf = result[succ_id]['LF']
                        lf = min(lf, succ_lf - lag)
                    elif dep_type == 'SF':
                        succ_lf = result[succ_id]['LF']
                        lf = min(lf, succ_lf - lag + duration)
            
            # 应用约束
            constraint_type = task.get('constraint_type', 'ASAP')
            constraint_date = task.get('constraint_date')
            
            if constraint_type == 'MFO' and constraint_date:
                lf = min(lf, constraint_date)
            elif constraint_type == 'SNLT' and constraint_date:
                lf = min(lf, constraint_date)
            
            ls = lf - duration
            
            result[tid] = {
                'LS': ls,
                'LF': lf,
                'successors': [s[0] for s in successors[tid]]
            }
        
        return result
    
    @staticmethod
    def calculate_float(forward_result: Dict[str, Dict],
                       backward_result: Dict[str, Dict]) -> Dict[str, Dict]:
        """计算浮动时间"""
        result = {}
        for tid in forward_result:
            es = forward_result[tid]['ES']
            ef = forward_result[tid]['EF']
            ls = backward_result[tid]['LS']
            lf = backward_result[tid]['LF']
            
            tf = ls - es  # 总浮动时间
            ff = min(backward_result.get(succ, {}).get('LS', float('inf')) 
                    for succ in backward_result[tid].get('successors', [])) - ef if backward_result[tid].get('successors') else 0
            
            result[tid] = {
                'ES': es, 'EF': ef,
                'LS': ls, 'LF': lf,
                'TF': tf,  # 总浮动时间
                'FF': max(0, ff),  # 自由浮动时间
                'is_critical': tf == 0,
                'has_conflict': tf < 0
            }
        
        return result
    
    @staticmethod
    def detect_cycle(tasks: List[str], dependencies: List[Dict]) -> Optional[List[str]]:
        """检测循环依赖，返回环路路径或None"""
        graph = defaultdict(list)
        for dep in dependencies:
            graph[dep['from_id']].append(dep['to_id'])
        
        visited = set()
        rec_stack = set()
        path = []
        
        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            path.append(node)
            
            for neighbor in graph[node]:
                if neighbor not in visited:
                    cycle = dfs(neighbor)
                    if cycle:
                        return cycle
                elif neighbor in rec_stack:
                    # 找到环路
                    cycle_start = path.index(neighbor)
                    return path[cycle_start:] + [neighbor]
            
            path.pop()
            rec_stack.remove(node)
            return None
        
        for task in tasks:
            if task not in visited:
                cycle = dfs(task)
                if cycle:
                    return cycle
        
        return None
