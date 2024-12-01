#include <stdio.h>
#include <string.h>
#include <stdbool.h>

#define MAX_CANDIDATES 9
#define MAX_VOTERS 100
#define MAX 9

// 记录候选人名字
char *candidates[MAX_CANDIDATES];
int candidate_count;

// 记录每个选民的偏好排序
// preferences[i][j] 表示第i个选民的第j偏好的候选人的索引
int preferences[MAX_VOTERS][MAX_CANDIDATES];
int voter_count;

// Move function declaration outside main
bool has_path(int start, int end, bool visited[]);  // Function prototype
bool creates_cycle(int from, int to);  // Add this near the has_path declaration

bool graph[MAX][MAX] = {false}; // Move this to global scope, near other global variables

int main(void)
{
    // Initialize counts
    voter_count = 9;
    candidate_count = 3;
    
    // Initialize candidates
    candidates[0] = "Alice";
    candidates[1] = "Bob";
    candidates[2] = "Charlie";
    
    // Initialize preferences
    // 前3张选票: Alice > Bob > Charlie
    preferences[0][0] = 0; // Alice
    preferences[0][1] = 1; // Bob
    preferences[0][2] = 2; // Charlie

    preferences[1][0] = 0;
    preferences[1][1] = 1;
    preferences[1][2] = 2;

    preferences[2][0] = 0;
    preferences[2][1] = 1;
    preferences[2][2] = 2;

    // 接下来2张选票: Bob > Charlie > Alice
    preferences[3][0] = 1; // Bob
    preferences[3][1] = 2; // Charlie
    preferences[3][2] = 0; // Alice

    preferences[4][0] = 1;
    preferences[4][1] = 2;
    preferences[4][2] = 0;

    // 最后4张选票: Charlie > Alice > Bob
    preferences[5][0] = 2; // Charlie
    preferences[5][1] = 0; // Alice
    preferences[5][2] = 1; // Bob

    preferences[6][0] = 2;
    preferences[6][1] = 0;
    preferences[6][2] = 1;

    preferences[7][0] = 2;
    preferences[7][1] = 0;
    preferences[7][2] = 1;

    preferences[8][0] = 2;
    preferences[8][1] = 0;
    preferences[8][2] = 1;
    
    // 创建一个二维数组记录候选人之间的胜负关系
    int wins[3][3] = {0}; // 初始化为0
    
    // 遍历每张选票
    for (int i = 0; i < voter_count; i++)
    {
        // 遍历并比较该选票中的每对候选人
        for (int j = 0; j < candidate_count - 1; j++)
        {
            for (int k = j + 1; k < candidate_count; k++)
            {
                // preferences[i][j]的候选人排名比preferences[i][k]靠前
                // 说明preferences[i][j]战胜了preferences[i][k]
                int winner = preferences[i][j];
                int loser = preferences[i][k];
                wins[winner][loser]++;
            }
        }
    }

    // 找出真正的优势对
    int pairs[3][2]; // 存储优势对 [winner, loser]
    int pair_count = 0;
    
    // 比较每对候选人
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            int candidate_i_wins = wins[i][j];
            int candidate_j_wins = wins[j][i];
            
            if (candidate_i_wins > candidate_j_wins)
            {
                pairs[pair_count][0] = i;
                pairs[pair_count][1] = j;
                pair_count++;
            }
            else if (candidate_j_wins > candidate_i_wins)
            {
                pairs[pair_count][0] = j;
                pairs[pair_count][1] = i;
                pair_count++;
            }
        }
    }
    
    // 按照优势大小排序
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = 0; j < pair_count - i - 1; j++)
        {
            int strength1 = wins[pairs[j][0]][pairs[j][1]] - wins[pairs[j][1]][pairs[j][0]];
            int strength2 = wins[pairs[j+1][0]][pairs[j+1][1]] - wins[pairs[j+1][1]][pairs[j+1][0]];
            
            if (strength1 < strength2)
            {
                // 交换
                int temp_winner = pairs[j][0];
                int temp_loser = pairs[j][1];
                pairs[j][0] = pairs[j+1][0];
                pairs[j][1] = pairs[j+1][1];
                pairs[j+1][0] = temp_winner;
                pairs[j+1][1] = temp_loser;
            }
        }
    }

    // 按优势顺序添加边
    for (int i = 0; i < pair_count; i++)
    {
        if (!creates_cycle(pairs[i][0], pairs[i][1]))
        {
            graph[pairs[i][0]][pairs[i][1]] = true;
            printf("添加边: %s -> %s (优势: %d)\n", 
                   candidates[pairs[i][0]], 
                   candidates[pairs[i][1]], 
                   wins[pairs[i][0]][pairs[i][1]] - wins[pairs[i][1]][pairs[i][0]]);
        }
    }
    
    // 找到入度为0的点作为起点(胜利者)
    int in_degrees[MAX] = {0};
    
    // 计算每个点的入度
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (graph[j][i])
            {
                in_degrees[i]++;
            }
        }
    }
    
    // 找到并输出所有入度为0的点(获胜者)
    bool found_winner = false;
    for (int i = 0; i < candidate_count; i++)
    {
        if (in_degrees[i] == 0)
        {
            printf("%s\n", candidates[i]);
            found_winner = true;
        }
    }
    
    // 如果没有入度为0的点,说明存在环路
    if (!found_winner)
    {
        printf("No winner found - cycle detected\n");
    }
    
}

// Move function definition after main
bool has_path(int start, int end, bool visited[])
{
    if (start == end)
    {
        return true;
    }
    
    visited[start] = true;
    
    for (int i = 0; i < candidate_count; i++)
    {
        if (graph[start][i] && !visited[i])
        {
            if (has_path(i, end, visited))
            {
                return true;
            }
        }
    }
    
    return false;
}

// Add the function definition here, after main (near has_path function)
bool creates_cycle(int from, int to)
{
    bool visited[MAX] = {false};
    graph[from][to] = true;  // 临时添加边
    
    bool has_cycle = has_path(to, from, visited);
    
    if (has_cycle)
    {
        graph[from][to] = false;  // 如果有环,撤销添加的边
    }
    
    return has_cycle;
}


