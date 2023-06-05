#include <stdio.h>
#include <stdbool.h>
#include <time.h>


int sudo[9][9] = {
    {8, 0, 0, 0, 0, 0, 0, 0, 9},
    {0, 0, 3, 6, 0, 0, 0, 0, 0},
    {0, 7, 0, 0, 9, 0, 2, 0, 0},
    {0, 5, 0, 0, 0, 7, 0, 0, 0},
    {0, 0, 0, 0, 4, 5, 7, 0, 0},
    {0, 0, 0, 1, 0, 0, 0, 3, 0},
    {0, 0, 1, 0, 0, 0, 0, 6, 8},
    {0, 0, 8, 5, 0, 0, 0, 1, 0},
    {0, 9, 0, 0, 0, 0, 4, 0, 0},
};
// int sudo[9][9] = {
//     {0, 0, 0, 0, 0, 0, 0, 0, 0},
//     {0, 0, 0, 0, 0, 3, 0, 8, 5},
//     {0, 0, 1, 0, 2, 0, 0, 0, 0},
//     {0, 0, 0, 5, 0, 7, 0, 0, 0},
//     {0, 0, 4, 0, 0, 0, 1, 0, 0},
//     {0, 9, 0, 0, 0, 0, 0, 0, 0},
//     {5, 0, 0, 0, 0, 0, 0, 7, 3},
//     {0, 0, 2, 0, 1, 0, 0, 0, 0},
//     {0, 0, 0, 0, 4, 0, 0, 0, 9},
// };
// int sudo[9][9] = {
//     {1, 0, 0, 4, 0, 0, 8, 0, 0},
//     {0, 4, 0, 0, 3, 0, 0, 0, 9},
//     {0, 0, 9, 0, 0, 6, 0, 5, 0},
//     {0, 5, 0, 3, 0, 0, 0, 0, 0},
//     {0, 0, 0, 0, 0, 1, 6, 0, 0},
//     {0, 0, 0, 0, 7, 0, 0, 0, 2},
//     {0, 0, 4, 0, 1, 0, 9, 0, 0},
//     {7, 0, 0, 8, 0, 0, 0, 0, 4},
//     {0, 2, 0, 0, 0, 4, 0, 8, 0},
// };

int cacheValues[82][10], cacheKeys[82][3], coordinate;
bool legalR[10][9];
bool legalC[10][9];
bool legalB[10][9];

bool Legal(int value, int row, int col)
{
    for (int rc = 0; rc <= 8; rc++) {
        if (sudo[rc][col] == value || sudo[row][rc] == value) {
            return false;
        }
    }
    for (int r = 3*(row/3); r <= 3*(row/3)+2; r++) {
        for (int c = 3*(col/3); c <= 3*(col/3)+2; c++) {
            if (sudo[r][c] == value){
                return false;
            }
        }
    }
    return true;
}

bool Check(void)
{
    int tmp;
    for (int r = 0; r <= 8; r++) {
        for (int c = 0; c <= 8; c++) {
            if (sudo[r][c]) {
                tmp = sudo[r][c];
                sudo[r][c] = 0;
                if (Legal(tmp, r, c)) {
                    sudo[r][c] = tmp;
                } else {
                    return false;
                }
            }
        }
    }
    return true;
}

void Fill(void)
{
    bool key = true, sameNumber = false;
    int signNumber = 0, signR = 0, signC = 0;
    while (key) {
        key = false;
        for (int number = 1; number <= 9; number++) {
            // Row and column
            for (int r = 0; r <= 8; r++) {
                for (int c = 0; c <= 8; c++) {
                    // Row
                    if (!sudo[r][c] && Legal(number, r, c)) {
                        if (sameNumber) {
                            sameNumber = false;
                            break;
                        }
                        signR = r;
                        signC = c;
                        sameNumber = true;
                    }
                }
                if (sameNumber) {
                    key = true;
                    sameNumber = false;
                    sudo[signR][signC] = number;
                }
                // Column
                for (int c = 0; c <= 8; c++) {
                    if (!sudo[c][r] && Legal(number, c, r)) {
                        if (sameNumber) {
                            sameNumber = false;
                            break;
                        }
                        signR = c;
                        signC = r;
                        sameNumber = true;
                    }
                }
                if (sameNumber) {
                    key = true;
                    sameNumber = false;
                    sudo[signR][signC] = number;
                }
            }
            // Block
            for (int bloR = 0; bloR<= 6; bloR += 3) {
                for (int bloC = 0; bloC <= 6; bloC += 3) {
                    for (int r = bloR;r <= bloR+2 && sameNumber; r++) {
                        for (int c = bloC; c <= bloC+2; c++) {
                            if (!sudo[r][c] && Legal(number, r, c)) {
                                if (sameNumber) {
                                    sameNumber = false;
                                    break;
                                }
                                signR = r;
                                signC = c;
                                sameNumber = true;
                            }
                        }
                    }
                    if (sameNumber) {
                        key = true;
                        sameNumber = false;
                        sudo[signR][signC] = number;
                    }
                }
            }
        }

        // Only one number
        for (int r = 0; r <= 8; r++) {
            for (int c = 0; c <= 8; c++) {
                if (!sudo[r][c]) {
                    for (int number = 1; number <= 9; number++) {
                        if (Legal(number, r, c)) {
                            if (sameNumber) {
                                sameNumber = false;
                                break;
                            }
                            signNumber = number;
                            sameNumber = true;
                        }
                    }
                    if (sameNumber) {
                        key = true;
                        sameNumber = false;
                        sudo[r][c] = signNumber;
                    }
                }
            }
        }
    }
}

void getCache(void)
{
    int valuesSize;
    //Get all legal values
    coordinate = 0;
    for (int r = 0; r <= 8; r++) {
        for (int c = 0; c <= 8; c++) {
            if (!sudo[r][c]) {
                valuesSize = 0;
                coordinate++;
                cacheKeys[coordinate][0] = r;
                cacheKeys[coordinate][1] = c;
                cacheKeys[coordinate][2] = 3 * (r / 3) + c / 3;
                for (int number = 1; number <= 9; number++) {
                    if (Legal(number, r, c)) {
                        cacheValues[coordinate][valuesSize] = number;
                        valuesSize++;
                    }
                }
            }
        }
    }
}

bool Solve(void)
{
    if (!coordinate) {
        return true;
    }
    int row = cacheKeys[coordinate][0];
    int col = cacheKeys[coordinate][1];
    int blo = cacheKeys[coordinate][2];
    for (int i = 0; cacheValues[coordinate][i]; i++) {
        int value = cacheValues[coordinate][i];
        if (legalR[row][value] && legalC[col][value] && legalB[blo][value]) {
            legalR[row][value] = false;
            legalC[col][value] = false;
            legalB[blo][value] = false;
            coordinate--;
            if (Solve()) {
                sudo[row][col] = value;
                return true;
            }
            legalR[row][value] = true;
            legalC[col][value] = true;
            legalB[blo][value] = true;
            coordinate++;
        }
    }
    return false;
}

void Output(void)
{
    printf("---------------------------\n");
    for (int r = 0; r <= 8; r++) {
        for (int c = 0; c <= 8; c++) {
            printf(" %d ", sudo[r][c]);
        }
        printf("\n");
    }
    printf("---------------------------\n");
}

int main(void)
{
    clock_t start, end;
    start = clock();
    for (int i = 0; i <= 9; i++) {
        for (int j = 0; j <= 8; j++) {
            legalR[i][j] = true;
            legalC[i][j] = true;
            legalB[i][j] = true;
        }
    }

    if (Check()) {
        Fill();
        getCache();
        Solve();
        Output();
    } else {
        printf("sudoError\n");
    }
    end = clock();
    printf("Time=%.1fms\n", (float)(end-start)/1000);

    return 0;
}
