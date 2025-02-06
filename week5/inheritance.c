// Simulate genetic inheritance of blood type

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Each person has two parents and two alleles
typedef struct person
{
    struct person *parents[2];
    char alleles[2];
} person;

const int GENERATIONS = 3;
const int INDENT_LENGTH = 4;

person *create_family(int generations);
void print_family(person *p, int generation);
void free_family(person *p);
char random_allele();

int main(void)
{
    // Seed random number generator
    srand(time(0));

    // Create a new family with three generations
    person *p = create_family(GENERATIONS);

    // Print family tree of blood types
    print_family(p, 0);

    // Free memory
    free_family(p);
}

// Create a new individual with `generations`
person *create_family(int generations)
{
    //创建一个新人
    person *new_person = malloc(sizeof(person));
    

    // 如果还有世代需要创建
    if (generations > 1)
    {
        // 通过递归调用create_family为当前的人创建两个新的父母
        person *parent0 = create_family(generations - 1);
        person *parent1 = create_family(generations - 1);

        // TODO: 设置当前人的父母指针
        new_person->parents[0] = parent0;
        new_person->parents[1] = parent1;

        // TODO: 基于父母的等位基因随机分配当前人的等位基因
        new_person->alleles[0] = parent0->alleles[rand() % 2];
        new_person->alleles[1] = parent1->alleles[rand() % 2];
    }

    // 如果没有更多世代需要创建
    else
    {
        // 将父母指针设置为NULL
        new_person->parents[0] = NULL;
        new_person->parents[1] = NULL;

        // 随机分配等位基因
        new_person->alleles[0] = random_allele();
        new_person->alleles[1] = random_allele();
    }

    // 返回新创建的人
    return new_person;
}

// Free `p` and all ancestors of `p`.
void free_family(person *p)
{
    // TODO: 处理基本情况
    if (p == NULL)
    {
        return;
    }

    // 递归释放父母
    free_family(p->parents[0]);
    free_family(p->parents[1]);

    // 释放子代
    free(p);
}

// Print each family member and their alleles.
void print_family(person *p, int generation)
{
    // Handle base case
    if (p == NULL)
    {
        return;
    }

    // Print indentation
    for (int i = 0; i < generation * INDENT_LENGTH; i++)
    {
        printf(" ");
    }

    // Print person
    if (generation == 0)
    {
        printf("Child (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    }
    else if (generation == 1)
    {
        printf("Parent (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    }
    else
    {
        for (int i = 0; i < generation - 2; i++)
        {
            printf("Great-");
        }
        printf("Grandparent (Generation %i): blood type %c%c\n", generation, p->alleles[0], p->alleles[1]);
    }

    // Print parents of current generation
    print_family(p->parents[0], generation + 1);
    print_family(p->parents[1], generation + 1);
}

// Randomly chooses a blood type allele.
char random_allele()
{
    int r = rand() % 3;
    if (r == 0)
    {
        return 'A';
    }
    else if (r == 1)
    {
        return 'B';
    }
    else
    {
        return 'O';
    }
}

