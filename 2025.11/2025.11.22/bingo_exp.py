import itertools
from sympy import isprime

def is_composite(n):
    return n > 3 and not isprime(n)

def has_2x2_square(grid):
    for i in range(4):
        for j in range(4):
            if (grid[i][j] + grid[i + 1][j] + grid[i][j + 1] + grid[i + 1][j + 1] == 4):
                return True
    
    return False

def line_has_three(grid):
    p = False
    for i in range(3):
        for j in range(5):
            if (grid[i][j] + grid[i+1][j] + grid[i+2][j] == 3):
                p = True
                break
        if p: break
    
    q = False
    for i in range(5):
        for j in range(3):
            if (grid[i][j] + grid[i][j+1] + grid[i][j+2] == 3):
                q = True
                break
        if q: break
    
    return p and q

def main():
    for mat in itertools.product([0,1], repeat=25):
        grid = [list(mat[i*5:(i+1)*5]) for i in range(5)]
        row_sum = [sum(r) for r in grid]
        col_sum = [sum(grid[i][j] for i in range(5)) for j in range(5)]
        total_one = sum(row_sum)
        diag1_sum = sum(grid[i][i] for i in range(5))
        diag2_sum = sum(grid[i][4-i] for i in range(5))
        
        # --- 条件枚举，逐条判定，建议依据题目每条写断言 ---
        # | 第1行: 此格为1，且总勾数为素数
        if (grid[0][0] == 1) and not (grid[0][0] == 1 and isprime(total_one)):
            continue
        if (grid[0][0] == 0) and (grid[0][0] == 1 and isprime(total_one)):
            continue

        # | 第1行: 总勾数>=12
        if (grid[0][1] == 1) and not (total_one >= 12):
            continue
        if (grid[0][1] == 0) and (total_one >= 12):
            continue

        # | 第1行: 第2列勾数<=第3列勾数，且第2列与第3列奇偶相同
        if (grid[0][2] == 1) and not (col_sum[1] <= col_sum[2] and col_sum[1] % 2 == col_sum[2] % 2):
            continue
        if (grid[0][2] == 0) and (col_sum[1] <= col_sum[2] and col_sum[1] % 2 == col_sum[2] % 2):
            continue

        # | 第1行: 第1行勾数<第4列勾数
        if (grid[0][3] == 1) and not (row_sum[0] < col_sum[3]):
            continue
        if (grid[0][3] == 0) and (row_sum[0] < col_sum[3]):
            continue

        # | 第1行: 存在一行被填满
        if (grid[0][4] == 1) and not (5 in row_sum):
            continue
        if (grid[0][4] == 0) and (5 in row_sum):
            continue

        # | 第2行: 此格为1

        # | 第2行: total<=13 XOR 至少两行为奇数
        if (grid[1][1] == 1) and not ((total_one <= 13) ^ (sum(1 for i in range(5) if row_sum[i] % 2 == 1) >= 2)):
            continue
        if (grid[1][1] == 0) and ((total_one <= 13) ^ (sum(1 for i in range(5) if row_sum[i] % 2 == 1) >= 2)):
            continue

        # | 第2行: 恰好存在1行完全为空
        if (grid[1][2] == 1) and not (sum(1 for i in range(5) if row_sum[i] == 0) == 1):
            continue
        if (grid[1][2] == 0) and (sum(1 for i in range(5) if row_sum[i] == 0) == 1):
            continue

        # | 第2行: 1不是质数
        if (grid[1][3] == 0):
            continue 

        # | 第2行: 存在某个2*2区域全为1
        if (grid[1][4] == 1) and not (has_2x2_square(grid)):
            continue
        if (grid[1][4] == 0) and (has_2x2_square(grid)):
            continue

        # | 第3行: 中心格为1，且两条对角线上1数为合数
        # if (grid[2][0] == 0) and (grid[2][2] == 1 and (is_composite(diag1_sum + diag2_sum - grid[2][2]))):
        #     continue
        # if (grid[2][0] == 0) and (grid[2][2] == 1 and (is_composite(diag1_sum + diag2_sum - grid[2][2]))):
        #     continue

        # | 第3行: 左上3x3区至少5个为1
        if (grid[2][1] == 1) and not (sum(grid[i][j] for i in range(3) for j in range(3)) >= 5):
            continue
        if (grid[2][1] == 0) and (sum(grid[i][j] for i in range(3) for j in range(3)) >= 5):
            continue

        # | 第3行: 上下相邻均为1的格对不少于四对
        vertical_pairs = sum([grid[i][j]==1 and grid[i+1][j]==1 for j in range(5) for i in range(4)])
        if (grid[2][2] == 1) and not (vertical_pairs >= 4):
            continue
        if (grid[2][2] == 0) and (vertical_pairs >= 4):
            continue

        # | 第3行: 上下相邻均为1的格对不多于六对
        if (grid[2][3] == 1) and not (vertical_pairs <= 6):
            continue
        if (grid[2][3] == 0) and (vertical_pairs <= 6):
            continue

        # | 第3行: 答案不是对角线
        if (grid[2][4] == 1) and not (diag1_sum != 5 and diag2_sum != 5):
            continue
        if (grid[2][4] == 0) and (diag1_sum != 5 and diag2_sum != 5):
            continue

        # | 第4行: 此格相邻三格勾数为偶数
        # 找第4行第1列相邻三格
        if (grid[3][0] == 1) and not (grid[2][0] + grid[3][1] + grid[4][0] % 2 == 0):
            continue
        if (grid[3][0] == 0) and (grid[2][0] + grid[3][1] + grid[4][0] % 2 == 0):
            continue

        # | 第4行: 令a=第4行和,b=第2列和,要求(a*a+b)%5<=3 且 a<=b
        a = row_sum[3]
        b = col_sum[1]
        if (grid[3][1] == 1) and not ((a*a+b)%5<=3 and a<=b):
            continue
        if (grid[3][1] == 0) and ((a*a+b)%5<=3 and a<=b):
            continue

        # | 第4行: 全体勾重心不偏右
        # if (grid[3][2] == 1) and (right_gravity(grid)):
        #     continue
        # if (grid[3][2] == 0) and not (right_gravity(grid)):
        #     continue

        # | 第4行: 此行不是正确答案
        # 意思是本行非满1
        # if (grid[3][3] == 1) and (all(cell==1 for cell in grid[3])):
        #     continue
        # if (grid[3][3] == 0) and not (all(cell==1 for cell in grid[3])):
        #     continue
        if (grid[3][3] == 0):
            continue
        

        # | 第4行: 没有"请先将本格打勾"的逻辑起点,此题不可解
        # if (grid[3][4] == 1) and (grid[3][0]!=1):
        #     continue

        # | 第5行: 第4列和第2列勾数之和为合数
        if (grid[4][0] == 1) and not (is_composite(col_sum[3]+col_sum[1])):
            continue
        if (grid[4][0] == 0) and (is_composite(col_sum[3]+col_sum[1])):
            continue

        # | 第5行: 1不是合数 XOR 此列是正确答案
        # if (grid[4][1] == 1) and (not ((not is_composite(1)) ^ all(grid[i][4]==1 for i in range(5)))):
        #     continue
        # if (grid[4][1] == 0) and not (not ((not is_composite(1)) ^ all(grid[i][4]==1 for i in range(5)))):
        #     continue
        if (grid[4][1] == 0):
            continue

        # | 第5行: 此列是勾数唯一最少的列
        if (grid[4][2] == 1) and not (col_sum[0] > col_sum[2] and col_sum[1] > col_sum[2] and col_sum[3] > col_sum[2] and col_sum[4] > col_sum[2]):
            continue
        if (grid[4][2] == 0) and (col_sum[0] > col_sum[2] and col_sum[1] > col_sum[2] and col_sum[3] > col_sum[2] and col_sum[4] > col_sum[2]):
            continue

        # | 第5行: 至少某行连续三个格子打勾且至少某列连续三个格子打勾
        if (grid[4][3] == 1) and not (line_has_three(grid)):
            continue
        if (grid[4][3] == 0) and (line_has_three(grid)):
            continue
        # | 第5行: 不存在某一对角线有至少三个格子打勾
        if (grid[4][4] == 1) and not (diag1_sum >= 3 or diag2_sum >= 3):
            continue
        if (grid[4][4] == 0) and (diag1_sum >= 3 or diag2_sum >= 3):
            continue

        # | 注：答案唯一，且某格打勾等价于为1、陈述为真，且仅有唯一一条满1行/列/对角线
        count = 0
        if (diag1_sum == 5):
            count += 1
        if (diag2_sum == 5):
            count += 1
        count += sum(1 for i in range(5) if row_sum[i] == 5)
        count += sum(1 for i in range(5) if col_sum[i] == 5)
        if (count != 1):
            continue

        # 若满足所有条件
        ans = "_".join("".join(str(x) for x in row) for row in grid)
        print(f"ZJUCTF{{{ans}}}")
        # break # 若答案唯一只需输出一次

if __name__ == "__main__":
    main()