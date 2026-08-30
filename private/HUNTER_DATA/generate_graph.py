import os
import re
import json

def main():
    base_dir = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/private/HUNTER_DATA"
    out_dir = "/Users/yu/Antigravity_workspace/HUNTERHUNTER-FANSITE/public/hunterdata/glaph"
    out_file = os.path.join(out_dir, "index.html")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    exclude_files = {'index.md', 'README_WIKI_MAINTENANCE.md', '検討中キーワード.md'}
    
    nodes_data = []
    edges_data = []
    
    node_id_map = {}
    current_id = 1
    
    # 1. ノード（各ページ）の収集とグループ分け
    for root, dirs, files in os.walk(base_dir):
        if "venv" in root or "build_src" in root: 
            continue
        for f in files:
            if f.endswith('.md') and f not in exclude_files:
                term = f[:-3]
                if term not in node_id_map:
                    node_id_map[term] = current_id
                    
                    category = os.path.basename(root)
                    if category == "HUNTER_DATA":
                        category = "その他"
                        
                    # カテゴリごとに色を変える
                    color = "#97c2fc"
                    if category == "登場人物": color = "#ff9999"      # 赤系
                    elif category == "念能力": color = "#99ff99"      # 緑系
                    elif category == "用語集": color = "#ffff99"      # 黄色系
                    elif category == "グリードアイランド_カード": color = "#e0b0ff" # 紫系
                    elif category == "ストーリー": color = "#ffb366"  # オレンジ系
                        
                    nodes_data.append({
                        "id": current_id, 
                        "label": term, 
                        "group": category,
                        "color": {"background": color, "border": "#555"}
                    })
                    current_id += 1

    # 2. エッジ（リンク関係）の抽出
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
                
                # ファイル内のマークダウンリンクを抽出
                matches = link_pattern.findall(content)
                for label, target_path in matches:
                    target_term = os.path.basename(target_path)[:-3]
                    target_id = node_id_map.get(target_term)
                    
                    if target_id and source_id != target_id:
                        # 双方向リンクを重複して描画しないための処理
                        edge_tuple = (min(source_id, target_id), max(source_id, target_id))
                        if edge_tuple not in edge_set:
                            edge_set.add(edge_tuple)
                            edges_data.append({
                                "from": source_id,
                                "to": target_id
                            })

    # 3. HTMLテンプレートにデータを埋め込んで出力
    html_template = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HUNTER×HUNTER ナレッジグラフ</title>
    <!-- vis.js CDN -->
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style type="text/css">
        body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; margin: 0; padding: 0; background-color: #121212; color: #fff; overflow: hidden;}
        #mynetwork { width: 100vw; height: 100vh; border: none; }
        #legend {
            position: absolute; top: 20px; left: 20px; z-index: 10;
            background: rgba(0,0,0,0.8); padding: 15px; border-radius: 8px; font-size: 14px;
        }
        h1 { margin: 0 0 10px 0; font-size: 1.2rem; }
        .legend-item { display: flex; align-items: center; margin-bottom: 5px; }
        .color-box { width: 15px; height: 15px; border-radius: 50%; margin-right: 10px; border: 1px solid #555; }
    </style>
</head>
<body>
<div id="legend">
    <h1>HUNTER×HUNTER ネットワークグラフ</h1>
    <div class="legend-item"><div class="color-box" style="background:#ff9999;"></div>登場人物</div>
    <div class="legend-item"><div class="color-box" style="background:#99ff99;"></div>念能力</div>
    <div class="legend-item"><div class="color-box" style="background:#ffff99;"></div>用語集</div>
    <div class="legend-item"><div class="color-box" style="background:#e0b0ff;"></div>グリードアイランド</div>
    <div class="legend-item"><div class="color-box" style="background:#ffb366;"></div>ストーリー</div>
    <div style="margin-top:10px; font-size:12px; color:#aaa;">※ノードをドラッグして動かせます<br>※マウスホイールで拡大縮小</div>
</div>
<div id="mynetwork"></div>

<script type="text/javascript">
    var nodes = new vis.DataSet(__NODES_DATA__);
    var edges = new vis.DataSet(__EDGES_DATA__);

    var container = document.getElementById('mynetwork');
    var data = { nodes: nodes, edges: edges };
    var options = {
        nodes: {
            shape: 'dot', size: 25,
            font: { size: 16, color: '#ffffff', strokeWidth: 3, strokeColor: '#000000' },
            borderWidth: 2, shadow: true
        },
        edges: {
            width: 1.5,
            color: { inherit: 'from', opacity: 0.7 },
            smooth: { type: 'continuous' }
        },
        physics: {
            forceAtlas2Based: { gravitationalConstant: -150, centralGravity: 0.01, springLength: 120, springConstant: 0.08 },
            maxVelocity: 50, solver: 'forceAtlas2Based', timestep: 0.35,
            stabilization: { iterations: 150 }
        },
        interaction: { hover: true, tooltipDelay: 200 }
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
