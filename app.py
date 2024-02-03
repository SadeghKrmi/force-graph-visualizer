import streamlit as st
import pandas as pd
import json
import streamlit.components.v1 as components

# Streamlit app
def main():
    st.subheader("Excel to Force Graph App", divider=True)

    with st.sidebar:
        # File upload
        uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

    if uploaded_file is not None:
        # Read Excel file into DataFrame
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        
        tab1, tab2, tab3 = st.tabs(["📈 Graph", "🗃 Data", "JSON"])


        # Display DataFrame
        with tab2:
            st.write(df)

        with tab1:
            # jdata = {"nodes": [{"id": 1},...], "links": [{"source": "1", "target": "2"}]}
            nodes = []
            links = []
            for index, row in df.iterrows():
                activity = str(row['activity'])
                nodes.append({"id": activity})
                time = row['time']
                dependency = row['dependency']
                if not pd.isna(dependency):
                    dependencies = [dep.strip() for dep in str(dependency).split(',') if not pd.isna(dep)]
        
                    for dep in dependencies:
                        links.append({"source": dep, "target": activity})

            json_data = {"nodes": nodes, "links": links}
            
            with st.container(border=True):
                components.html(
                f"""
                <div class="contianer">
                    <div class="row my-2 pb-3" id="graph"></div>
                </div>
                <script src="https://cdn.jsdelivr.net/npm/force-graph@1.43.4/dist/force-graph.min.js"></script>
                <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    const getColor = n => '#' + ((n * 1234567) % Math.pow(2, 24)).toString(16).padStart(6, '0');
                    const Graph = ForceGraph()
                    (document.getElementById('graph'))
                        .graphData({json_data})
                        .onNodeDragEnd(node => {{
                            node.fx = node.x;
                            node.fy = node.y;
                        }})
                        .nodeVal(7)
                        .nodeCanvasObject((node, ctx) => nodePaint(node, getColor(node.id), ctx))
                        .linkColor('black')
                        .linkDirectionalArrowLength(4);

                    function nodePaint({{ id, x, y }}, color, ctx) {{
                        ctx.fillStyle = 'black';
                        ctx.beginPath(); ctx.arc(x, y, 5, 0, 2 * Math.PI, false); ctx.fill();
                        ctx.fillStyle = 'white';
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.font = '5px Sans-Serif';
                        ctx.fillText(id, x, y);
                    }}
                }});
                </script>
                """,
                height=400
                )

        with tab3:
            st.json(json_data, expanded=False)


if __name__ == "__main__":
    main()
