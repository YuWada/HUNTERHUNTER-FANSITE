import os
import re
import json

def main():
    base_dir = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/HUNTER_DATA"
    out_dir = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/hunterdataglaph"
    out_file = os.path.join(out_dir, "index.html")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    exclude_files = {'index.md', 'README_WIKI_MAINTENANCE.md', '検討中キーワード.md'}
    
    nodes_data = []
    edges_data = []
    
    node_id_map = {}
    current_id = 1
    
    in_degrees = {}
    
    # 1. First Pass: Collect nodes and determine categories properly
    for root, dirs, files in os.walk(base_dir):
        if "venv" in root or "build_src" in root: 
            continue
        for f in files:
            if f.endswith('.md') and f not in exclude_files:
                term = f[:-3]
                if term not in node_id_map:
                    node_id_map[term] = current_id
                    in_degrees[current_id] = 0
                    
                    # More robust category detection based on path
                    category = "その他"
                    if "/登場人物" in root or root.endswith("登場人物"): category = "登場人物"
                    elif "/念能力" in root or root.endswith("念能力"): category = "念能力"
                    elif "/用語集" in root or root.endswith("用語集"): category = "用語集"
                    elif "グリードアイランド" in root: category = "グリードアイランド"
                    elif "/ストーリー" in root or root.endswith("ストーリー"): category = "ストーリー"
                        
                    # 念能力を赤、登場人物を青などに変更
                    color = "#cccccc"
                    if category == "念能力": color = "#ff6666"        # 赤系
                    elif category == "登場人物": color = "#66b3ff"    # 青系
                    elif category == "用語集": color = "#ffcc66"      # オレンジ/黄系
                    elif category == "グリードアイランド": color = "#d279a6" # 紫/ピンク系
                    elif category == "ストーリー": color = "#66cc99"  # 緑系
                        
                    nodes_data.append({
                        "id": current_id, 
                        "label": term, 
                        "group": category,
                        "color": {"background": color, "border": "#333"}
                    })
                    current_id += 1

    # 2. Second Pass: Extract edges and calculate in-degrees
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')
    edge_set = set()

    for root, dirs, files in os.walk(base_dir):
        if "venv" in root or "build_src" in root: 
            continue
        for f in files:
            if f.endswith('.md') and f not in exclude_files:
                source_term = f[:-3]
                source_id = node_id_map.get(source_term)
                if not source_id:
                    continue
                
                filepath = os.path.join(root, f)
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                matches = link_pattern.findall(content)
                for label, target_path in matches:
                    target_term = os.path.basename(target_path)[:-3]
                    target_id = node_id_map.get(target_term)
                    
                    if target_id and source_id != target_id:
                        # For directed visualization, we keep directed edges, but avoid exact duplicates
                        edge_tuple = (source_id, target_id)
                        if edge_tuple not in edge_set:
                            edge_set.add(edge_tuple)
                            edges_data.append({
                                "from": source_id,
                                "to": target_id
                            })
                            in_degrees[target_id] += 1

    # Apply scaling value based on in-degree + out-degree or just in-degree
    # This will make highly referenced nodes much larger.
    for node in nodes_data:
        # base value 1, plus number of incoming links
        node["value"] = in_degrees.get(node["id"], 0) + 1

    # 3. Generate HTML with dynamic scaling configured
    html_template = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HUNTER×HUNTER ナレッジグラフ</title>
    <!-- vis.js CDN -->
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style type="text/css">
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 0; background-color: #1a1a1a; color: #fff; overflow: hidden;}
        #mynetwork { width: 100vw; height: 100vh; border: none; }
        #legend {
            position: absolute; top: 20px; left: 20px; z-index: 10;
            background: rgba(0,0,0,0.85); padding: 15px; border-radius: 8px; font-size: 14px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }
        h1 { margin: 0 0 10px 0; font-size: 1.2rem; }
        .legend-item { display: flex; align-items: center; margin-bottom: 5px; }
        .color-box { width: 16px; height: 16px; border-radius: 50%; margin-right: 10px; border: 1px solid #555; }
    </style>
</head>
<body>
<div id="legend">
    <h1>HUNTER×HUNTER ネットワークグラフ</h1>
    <div class="legend-item"><div class="color-box" style="background:#ff6666;"></div>念能力</div>
    <div class="legend-item"><div class="color-box" style="background:#66b3ff;"></div>登場人物</div>
    <div class="legend-item"><div class="color-box" style="background:#ffcc66;"></div>用語集</div>
    <div class="legend-item"><div class="color-box" style="background:#d279a6;"></div>グリードアイランド</div>
    <div class="legend-item"><div class="color-box" style="background:#66cc99;"></div>ストーリー</div>
    <div class="legend-item"><div class="color-box" style="background:#cccccc;"></div>その他</div>
    <div style="margin-top:12px; font-size:12px; color:#aaa; line-height: 1.4;">
        ※ノードをドラッグして動かせます<br>
        ※マウスホイールで拡大・縮小<br>
        ※円の大きさは「参照されている数」に比例します
    </div>
</div>
<div id="mynetwork"></div>

<script type="text/javascript">
    var nodes = new vis.DataSet(__NODES_DATA__);
    var edges = new vis.DataSet(__EDGES_DATA__);

    var container = document.getElementById('mynetwork');
    var data = { nodes: nodes, edges: edges };
    var options = {
        nodes: {
            shape: 'dot',
            scaling: {
                min: 10,
                max: 70,
                label: {
                    min: 10,
                    max: 40,
                    drawThreshold: 8,
                    maxVisible: 30
                }
            },
            font: { color: '#ffffff', strokeWidth: 3, strokeColor: '#000000' },
            borderWidth: 2, shadow: true
        },
        edges: {
            width: 0.8,
            arrows: {
                to: { enabled: true, scaleFactor: 0.5 }
            },
            color: { inherit: 'from', opacity: 0.5 },
            smooth: { type: 'continuous' }
        },
        physics: {
            forceAtlas2Based: { gravitationalConstant: -200, centralGravity: 0.01, springLength: 150, springConstant: 0.05, damping: 0.8 },
            maxVelocity: 5, solver: 'forceAtlas2Based', timestep: 0.05,
            stabilization: { iterations: 200 }
        },
        interaction: { hover: true, tooltipDelay: 100 }
    };
    var network = new vis.Network(container, data, options);
</script>
</body>
</html>
"""
    
    html_template = html_template.replace("__NODES_DATA__", json.dumps(nodes_data))
    html_template = html_template.replace("__EDGES_DATA__", json.dumps(edges_data))

    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(html_template)
        
    print(f"✅ 生成完了: {out_file} (ノード数: {len(nodes_data)}, エッジ数: {len(edges_data)})")

if __name__ == "__main__":
    main()
