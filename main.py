import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from SchellingModel import Schelling


def main():

    st.set_page_config(layout="wide")
    st.title("Schelling's Model of Segregation (謝林隔離模型)")

    # 側邊欄：設定 Schelling 模型的參數
    population_size = st.sidebar.slider("Population Size (人口總數)", 500, 10000, 2500)
    empty_ratio = st.sidebar.slider("Empty Houses Ratio (空屋比例)", 0., 1., .2)
    similarity_threshold = st.sidebar.slider("Similarity Threshold (相似度門檻)", 0., 1., .4)
    n_iterations = st.sidebar.number_input("Number of Iterations (模擬迭代次數)", 50)

    # 初始化 Schelling 模型
    schelling = Schelling(population_size, empty_ratio, similarity_threshold, 3)
    mean_similarity_ratio = []
    mean_similarity_ratio.append(schelling.get_mean_similarity_ratio())

    plt.style.use("ggplot")
    
    # 設定字體以支援繁體中文顯示
    plt.rcParams['font.sans-serif'] = ['PingFang HK', 'Heiti TC', 'Arial Unicode MS', 'sans-serif']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig = plt.figure(figsize=(14, 6))
    
    # 左側圖表：城市空間的網格狀態
    cmap = ListedColormap(['red', 'white', 'royalblue'])
    ax1 = fig.add_subplot(121)
    ax1.axis('off')
    ax1.pcolor(schelling.city, cmap=cmap, edgecolors='w', linewidths=1)
    
    # 右側圖表：平均相似度比例的變化圖
    ax2 = fig.add_subplot(122)
    ax2.set_xlabel("Iterations (迭代次數)")
    ax2.set_xlim([0, n_iterations])
    ax2.set_ylim([0.4, 1])
    ax2.set_title("Mean Similarity Ratio", fontsize=15)
    ax2.text(1, 0.95, "Similarity Ratio: %.4f" % schelling.get_mean_similarity_ratio(), fontsize=10)

    city_plot = st.pyplot(fig, width="stretch")

    progress_bar = st.progress(0)

    if st.sidebar.button('Run Simulation (執行模擬)'):
        for i in range(int(n_iterations)):
            schelling.run()
            mean_similarity_ratio.append(schelling.get_mean_similarity_ratio())
            
            fig = plt.figure(figsize=(14, 6))
            
            # 更新左側城市空間圖
            ax1 = fig.add_subplot(121)
            ax1.axis('off')
            ax1.pcolor(schelling.city, cmap=cmap, edgecolors='w', linewidths=1)
            
            # 更新右側平均相似度比例圖
            ax2 = fig.add_subplot(122)
            ax2.set_xlabel("Iterations")
            ax2.set_xlim([0, n_iterations])
            ax2.set_ylim([0.4, 1])
            ax2.set_title("Mean Similarity Ratio", fontsize=15)
            ax2.plot(range(1, len(mean_similarity_ratio)+1), mean_similarity_ratio)
            ax2.text(1, 0.95, "Similarity Ratio: %.4f" % schelling.get_mean_similarity_ratio(), fontsize=10)
            
            city_plot.pyplot(fig, width="stretch")
            plt.close(fig)
            
            progress_bar.progress((i + 1.) / int(n_iterations))

if __name__ == "__main__":
    main()
