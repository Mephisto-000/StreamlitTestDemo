import random
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class Schelling:
    """
    謝林隔離模型 (Schelling Segregation Model)。
    這是一個用來模擬城市中多種族隔離現象的代理人基模型 (Agent-based model)。
    """
    
    def __init__(self, size, empty_ratio, similarity_threshold, n_neighbors):
        """
        初始化 Schelling 模型的參數。
        
        參數:
        - size: 城市中的房屋數量 (The number of houses in the city)。
        - empty_ratio: 城市中空房屋的比例 (The ratio of empty houses in the city)。
        - similarity_threshold: 相似度門檻 (Similarity Threshold)。用來決定一個人在其社群中是否快樂。
                                如果相似鄰居佔整個社群人口的比例低於此門檻，該人就會搬到空房屋。
        - n_neighbors: 每個方向（上、下、左、右）的鄰居數量。
        """
        self.size = size 
        self.empty_ratio = empty_ratio
        self.similarity_threshold = similarity_threshold
        self.n_neighbors = n_neighbors
        
        # 決定各種族 (-1, 1) 以及空房屋 (0) 的比例
        # Ratio of races (-1, 1) and empty houses (0)
        p = [(1-empty_ratio)/2, (1-empty_ratio)/2, empty_ratio]
        
        # 根據房屋數量計算城市的網格大小 (確保為完全平方數，以便轉換為二維矩陣)
        city_size = int(np.sqrt(self.size))**2
        
        # 根據給定的比例 p，隨機將 -1 (種族A), 1 (種族B), 0 (空屋) 分配到城市的一維陣列中
        self.city = np.random.choice([-1, 1, 0], size=city_size, p=p)
        
        # 將一維陣列重塑為二維陣列 (網格)，代表城市的空間結構
        self.city = np.reshape(self.city, (int(np.sqrt(city_size)), int(np.sqrt(city_size))))
    
    def run(self):
        """
        執行一次 Schelling 模型的模擬迭代。
        對於城市中的每個人，我們會根據 similarity_ratio (相似度比例) 和 similarity_threshold (相似度門檻) 
        來檢查他/她是否快樂。如果不快樂，就會將他/她搬到一個空房屋。
        """
        # 遍歷城市網格中的每一個座標 (row, col) 以及對應的值 value (居民或空屋)
        for (row, col), value in np.ndenumerate(self.city):
            race = self.city[row, col]
            
            # 如果目前位置是有居民的 (race != 0)
            if race != 0:
                # 取得該居民周圍的社區 (neighborhood)，範圍由 n_neighbors 決定
                neighborhood = self.city[row-self.n_neighbors:row+self.n_neighbors, col-self.n_neighbors:col+self.n_neighbors]
                
                # 計算社區的大小 (包含的總房屋數)
                neighborhood_size = np.size(neighborhood)
                
                # 計算社區內的空房屋數量
                n_empty_houses = len(np.where(neighborhood == 0)[0])
                
                # 確保社區內不只有該居民自己 (總房屋數不等於空屋數 + 居民自己1棟)
                if neighborhood_size != n_empty_houses + 1:
                    # 計算社區內相似（同種族）的鄰居數量 (減 1 是為了扣除居民自己)
                    n_similar = len(np.where(neighborhood == race)[0]) - 1
                    
                    # 計算相似度比例 = 相似鄰居數 / (社區總大小 - 空屋數 - 1)
                    similarity_ratio = n_similar / (neighborhood_size - n_empty_houses - 1.)
                    
                    # 判斷該居民是否因為相似度比例低於門檻而不快樂
                    is_unhappy = (similarity_ratio < self.similarity_threshold)
                    
                    # 如果不快樂，則隨機選擇一個空房屋搬家
                    if is_unhappy:
                        # 找出目前城市中所有空房屋 (0) 的座標列表
                        empty_houses = list(zip(np.where(self.city == 0)[0], np.where(self.city == 0)[1]))
                        
                        # 隨機挑選一個空房屋的座標
                        random_house = random.choice(empty_houses)
                        
                        # 將該居民移至隨機挑選的空房屋
                        self.city[random_house] = race
                        
                        # 將該居民原本的位置設為空房屋 (0)
                        self.city[row,col] = 0

    def get_mean_similarity_ratio(self):
        """
        計算整個城市的平均相似度比例 (Average Similarity Ratio)。
        這能用來評估整個城市的隔離程度。
        """
        count = 0
        similarity_ratio = 0
        
        # 遍歷城市網格中的每一個位置
        for (row, col), value in np.ndenumerate(self.city):
            race = self.city[row, col]
            
            # 針對有居民的房屋計算其各自的相似度比例
            if race != 0:
                # 取得該居民周圍的社區
                neighborhood = self.city[row-self.n_neighbors:row+self.n_neighbors, col-self.n_neighbors:col+self.n_neighbors]
                neighborhood_size = np.size(neighborhood)
                n_empty_houses = len(np.where(neighborhood == 0)[0])
                
                if neighborhood_size != n_empty_houses + 1:
                    n_similar = len(np.where(neighborhood == race)[0]) - 1
                    
                    # 累加每位居民的相似度比例
                    similarity_ratio += n_similar / (neighborhood_size - n_empty_houses - 1.)
                    count += 1
                    
        # 回傳總相似度比例除以計算的人數，即為整個城市的平均相似度比例
        return similarity_ratio / count


def main():
    """
    主程式進入點，實作 Streamlit UI 與圖表繪製邏輯。
    """
    # 將網頁版面設定為最大寬度以放大顯示區域
    st.set_page_config(layout="wide")
    
    # 設定網頁標題
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

    # 繪製初始狀態的圖表
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

    # 將繪製好的 Matplotlib 圖表顯示在 Streamlit 畫面上，並設定配合頁面寬度放大
    city_plot = st.pyplot(fig, width="stretch")

    # 建立進度條
    progress_bar = st.progress(0)

    # 當按下側邊欄的「執行模擬」按鈕時
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
            
            # 更新進度條
            progress_bar.progress((i + 1.) / int(n_iterations))

if __name__ == "__main__":
    main()
