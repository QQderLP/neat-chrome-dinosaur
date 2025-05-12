import matplotlib.pyplot as plt

plt.show()
# 預留空間給數據
max_scores = []
avg_scores = []
generations = []

# 假設你有最大世代數（請自己設定這個變數）
max_generations = 50  # 範例：50 代

# 模擬演算法迴圈
for gen in range(1, max_generations + 1):
    # 這裡請改為你的實際演算法邏輯
    new_max_score = gen * 2 + 10  # 假資料
    new_avg_score = gen + 5  # 假資料

    max_scores.append(new_max_score)
    avg_scores.append(new_avg_score)
    generations.append(gen)

# 畫圖
plt.plot(generations, max_scores, label='Max Score', color='blue', marker='o')
plt.plot(generations, avg_scores, label='Avg Score', color='orange', marker='x')
plt.xlabel('Generation')
plt.ylabel('Score')
plt.title('NEAT AI Learning Progress')
plt.grid(True)
plt.legend()
plt.savefig('neat_progress.png')
plt.show()