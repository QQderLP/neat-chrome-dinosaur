import pygame
import os
import random
import math
import sys
import neat

pygame.init()
generation_scores = []  # 放在程式最前面

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoRun2.png"))]

JUMPING = pygame.image.load(os.path.join("Assets/Dino", "DinoJump.png"))

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]
DUCKING = [pygame.image.load(os.path.join("Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("Assets/Dino", "DinoDuck2.png"))]


BIRD =[pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
           pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

FONT = pygame.font.Font('freesansbold.ttf', 20)


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self, img=RUNNING[0]):
        self.image = img
        self.duck_img = DUCKING
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.jump_vel = self.JUMP_VEL
        self.rect = pygame.Rect(self.X_POS, self.Y_POS, img.get_width(), img.get_height())
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.step_index = 0

    def update(self):
        if self.dino_jump:
            self.jump()
        elif self.dino_duck:
            self.rect.y = self.Y_POS_DUCK
            self.duck()
        else:
            self.rect.y = self.Y_POS
            self.run()

        if self.step_index >= 10:
            self.step_index = 0

    def jump(self):
        self.image = JUMPING
        if self.dino_jump:
            self.rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel <= -self.JUMP_VEL:
            self.dino_jump = False
            self.dino_run = True
            self.jump_vel = self.JUMP_VEL

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.step_index += 1

    def run(self):
        self.image = RUNNING[self.step_index // 5]
        self.step_index += 1

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(SCREEN, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.height), 2)
        for obstacle in obstacles:
            pygame.draw.line(SCREEN, self.color, (self.rect.x + 54, self.rect.y + 12), obstacle.rect.center, 2)


class Obstacle:
    def __init__(self, image, number_of_cacti):
        self.image = image
        self.type = number_of_cacti
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)


class SmallCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 325


class LargeCactus(Obstacle):
    def __init__(self, image, number_of_cacti):
        super().__init__(image, number_of_cacti)
        self.rect.y = 300

class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = random.choice([250, 270, 300])
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1
def remove(index):
    dinosaurs.pop(index)
    ge.pop(index)
    nets.pop(index)


def distance(pos_a, pos_b):
    dx = pos_a[0]-pos_b[0]
    dy = pos_a[1]-pos_b[1]
    return math.sqrt(dx**2+dy**2)


def eval_genomes(genomes, config):
    global game_speed, x_pos_bg, y_pos_bg, obstacles, dinosaurs, ge, nets, points
    clock = pygame.time.Clock()
    points = 0

    obstacles = []
    dinosaurs = []
    ge = []
    nets = []

    x_pos_bg = 0
    y_pos_bg = 380
    game_speed = 20

    for genome_id, genome in genomes:
        dinosaurs.append(Dinosaur())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0

    def score():
        global points, game_speed, run
        points += 1
        if points % 100 == 0:
            game_speed = min(game_speed + 1, 40)  # 加入最大速度限制
        text = FONT.render(f'Points:  {str(points)}', True, (0, 0, 0))
        SCREEN.blit(text, (950, 50))

        # 當達到3000分，關閉程式
        if points >= 10000:
            print("目標達成：3000分，關閉程式。")
            pygame.quit()
            sys.exit()

    def statistics():
        text_1 = FONT.render(f'Dinosaurs Alive:  {str(len(dinosaurs))}', True, (0, 0, 0))
        text_2 = FONT.render(f'Generation:  {pop.generation+1}', True, (0, 0, 0))
        text_3 = FONT.render(f'Game Speed:  {str(game_speed)}', True, (0, 0, 0))

        SCREEN.blit(text_1, (50, 450))
        SCREEN.blit(text_2, (50, 480))
        SCREEN.blit(text_3, (50, 510))

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            x_pos_bg = 0
        x_pos_bg -= game_speed

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        SCREEN.fill((255, 255, 255))

        if len(obstacles) == 0:
            rand_int = random.randint(0, 2)
            if rand_int == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS, random.randint(0, 2)))
            elif rand_int == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS, random.randint(0, 2)))
            else:
                obstacles.append(Bird(BIRD))

        # 對每隻恐龍做行為決策
        for i, dinosaur in enumerate(dinosaurs):
            dinosaur.update()
            dinosaur.draw(SCREEN)
            ge[i].fitness += 0.1

            if len(obstacles) > 0:
                obstacle = obstacles[0]
                dx = obstacle.rect.x - dinosaur.rect.x
                obstacle_type = 0 if isinstance(obstacle, SmallCactus) else (
                    1 if isinstance(obstacle, LargeCactus) else 2)

                inputs = (
                    dinosaur.rect.y,
                    dx,
                    obstacle_type,
                    obstacle.rect.y,
                    obstacle.rect.width,
                    game_speed
                )

                output = nets[i].activate(inputs)

                if output[0] > 0.5 and dinosaur.rect.y == dinosaur.Y_POS:  # 跳躍
                    dinosaur.dino_jump = True
                    dinosaur.dino_run = False
                    dinosaur.dino_duck = False
                elif output[1] > 0.5 and not dinosaur.dino_jump:  # 蹲下
                    dinosaur.dino_duck = True
                    dinosaur.dino_run = False
                else:
                    dinosaur.dino_duck = False
                    dinosaur.dino_run = True

        # 移動與繪製障礙物
        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            for i, dinosaur in enumerate(dinosaurs):
                if dinosaur.rect.colliderect(obstacle.rect):
                    ge[i].fitness -= 1
                    remove(i)
            # 只需要檢查第一個障礙物即可
            break

        statistics()
        score()
        background()
        clock.tick(30)
        pygame.display.update()

        if len(dinosaurs) == 0:
            run = False

            # 統計這一代的分數並即時畫圖
            scores = [genome.fitness for genome_id, genome in genomes]
            max_score = max(scores)
            avg_score = sum(scores) / len(scores)
            generation_scores.append((max_score, avg_score))
            print(f"Generation done. Max: {max_score}, Avg: {avg_score}")
            import visualize
            import pickle
            import os

            # 儲存最佳 genome
            winner = max(genomes, key=lambda g: g[1].fitness)[1]
            with open("best_genome.pkl", "wb") as f:
                pickle.dump(winner, f)

            # 畫出神經網路
            node_names = {
                -1: "Y",
                -2: "dx",
                -3: "Type",
                -4: "obsY",
                -5: "obsW",
                -6: "Speed",
                0: "Jump",
                1: "Duck"
            }

            # 建立圖檔資料夾
            output_dir = "networks"
            os.makedirs(output_dir, exist_ok=True)

            # 自動編號：找出目前最大檔名數字
            existing_files = [f for f in os.listdir(output_dir) if f.startswith("network_") and f.endswith(".png")]
            numbers = [int(f.split("_")[1].split(".")[0]) for f in existing_files if
                       f.split("_")[1].split(".")[0].isdigit()]
            next_num = max(numbers) + 1 if numbers else 1
            filename = os.path.join(output_dir, f"network_{next_num}")

            # 畫圖（儲存圖檔但不打開）
            visualize.draw_net(config, winner, filename=filename, view=False, node_names=node_names)

            # 畫圖
            import matplotlib.pyplot as plt

            max_scores = [score[0] for score in generation_scores]
            avg_scores = [score[1] for score in generation_scores]
            generations = list(range(1, len(generation_scores) + 1))

            plt.plot(generations, max_scores, label='', color='blue', marker='o')
            plt.plot(generations, avg_scores, label='', color='orange', marker='x')

            plt.xlabel('Generation')
            plt.ylabel('Score')
            plt.title('NEAT AI Learning Progress')
            plt.grid(True)
            plt.legend()
            plt.savefig('neat_progress.png')
            plt.show(block=False)
# 畫出神經網路結構圖


# Setup the NEAT Neural Network
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes)

import subprocess

def auto_git_command():
    try:
        # 設定 Git 自動執行指令，這裡假設你的 Git 指令已經正確設置
        subprocess.run(['git', 'add', '--all'], check=True)
        subprocess.run(['git', 'commit', '-m', '"Automatic commit"'], check=True)
        subprocess.run(['git', 'push'], check=True)
        print("Git 操作已自動執行")
    except subprocess.CalledProcessError as e:
        print(f"Git 命令執行失敗：{e}")

auto_git_command()

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
