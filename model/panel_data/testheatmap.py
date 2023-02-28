# import plotly.figure_factory as ff
# import pandas as pd
# import plotly
# import numpy as np
# testdf = pd.read_csv(r'D:/file/digital_server/model/panel_data/distance_test.csv', index_col=0)
# heatmap_value = np.round(testdf.values,3)  # 数据框数组转换
#
# fig = ff.create_annotated_heatmap(
#         heatmap_value,
#         x=testdf.columns.tolist(),
#         y=testdf.columns.tolist(),
#         colorscale='Viridis',
#     )
# fig.update_layout(xaxis_tickangle=90)
# plotly.offline.plot(fig, filename='file1.html')

import plotly.graph_objects as go
import numpy as np
import plotly
import pandas as pd
testdf = pd.read_csv(r'D:/file/digital_server/model/panel_data/distance_test.csv', index_col=0)
heatmap_value = np.round(testdf.values,3)  # 数据框数组转换
fig = go.Figure(data=go.Heatmap(
                   z=heatmap_value,
                   x=testdf.columns.tolist(),
                   y=testdf.index.tolist(),
                   ))  # 缺失值处理参数
# fig.show()
fig.update_layout(xaxis_tickangle=90)
plotly.offline.plot(fig, filename='file1.html')