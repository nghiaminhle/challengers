#include <stdio.h>
#include <time.h>
int a[9][9];
int rows[9];
int cols[9];
int areas[9];
int cell_i[81];
int cell_j[81];
int cell_number = 0;
int best_candidate_threshold = 1;
int recursive_number = 0;


int getBestCandidates(int cell)
{
    int bestCandidates = 0;
    int bestCellIdx = -1;
    int bestCandidatesCount = 10;

    for (int idx = cell; idx < cell_number; idx++)
    {
        int i = cell_i[idx];
        int j = cell_j[idx];
        int candidates = 0;
        int candidatesCount = 0;

        for (int k=1; k<=9; k++)
        {
            int bits = 1<<k;
            if( ((rows[i] & bits)==0) && ((cols[j] & bits)==0) && ((areas[3*(i/3)+j/3] & bits)==0))
            {
                candidates |= bits;
                candidatesCount +=1;
            }
        }

        if (candidatesCount <= bestCandidatesCount)
        {
            bestCandidates = candidates;
            bestCellIdx = idx;
            bestCandidatesCount = candidatesCount;
            if (bestCandidatesCount < best_candidate_threshold)
                break;
        }
    }

    int tmpI = cell_i[cell];
    int tmpJ = cell_j[cell];
    cell_i[cell] = cell_i[bestCellIdx];
    cell_j[cell] = cell_j[bestCellIdx];
    cell_i[bestCellIdx] = tmpI;
    cell_j[bestCellIdx] = tmpJ;

    return bestCandidates;
}

void flag(int i, int j, int bitPos)
{
    int bits = 1<<bitPos;
    rows[i] |= bits;
    cols[j] |= bits;
    areas[3*(i/3) + j/3] |= bits;
}

void unflag(int i, int j, int bitPos)
{
    int bits = ~(1<<bitPos);
    rows[i] &= bits;
    cols[j] &= bits;
    areas[3*(i/3) + j/3] &= bits;
}

void print_result(int matrix[9][9])
{
    for(int i = 0; i<9; i++)
    {
        for (int j = 0; j<9; j++)
        {
            printf("%3d",matrix[i][j]);
        }
        printf("\n");
    }
}

int solve(int cell)
{
    recursive_number +=1;
    if (cell > cell_number - 1)
        return 1;
    int candidates = getBestCandidates(cell);
    int i = cell_i[cell];
    int j = cell_j[cell];
    for (int v= 1; v<=9; v++)
    {
        if ((candidates & (1<<v)))
        {
            a[i][j] = v;
            flag(i, j, v);
            if (solve(cell+1) == 1)
                return 1;
            unflag(i, j, v);
        }
    }

    a[i][j] = 0;
    return 0;
}

void sudokuRun()
{
    solve(0);
}

void init()
{
    int example[9][9] = {
        {0,0,0,0,0,6,0,0,0},
        {0,5,9,0,0,0,0,0,8},
        {2,0,0,0,0,8,0,0,0},
        {0,4,5,0,0,0,0,0,0},
        {0,0,3,0,0,0,0,0,0},
        {0,0,6,0,0,3,0,5,4},
        {0,0,0,3,2,5,0,0,6},
        {0,0,0,0,0,0,0,0,0},
        {0,0,0,0,0,0,0,0,0}
        };

    for (int i = 0; i<9; i++)
    {
        for(int j = 0; j<9; j++)
        {
            a[i][j] = example[i][j];
            if(a[i][j]==0)
            {
                cell_i[cell_number] = i;
                cell_j[cell_number] = j;
                cell_number +=1;
            }
            else
            {
                int bits = 1<<a[i][j];
                rows[i] |= bits;
                cols[j] |= bits;
                areas[3*(i/3)+j/3] |= bits;
            }
        }
    }
}

int main()
{
    init();

    print_result(a);

    printf("-------------\n");
    
    clock_t t1, t2;  
    t1 = clock(); 

    sudokuRun();
    
    t2 = clock();   

    float diff = ((float)(t2 - t1) / 1000000.0F ) * 1000;   
    

    print_result(a);

    printf("%f %d \n",diff, recursive_number);  
    
    return 0;
}