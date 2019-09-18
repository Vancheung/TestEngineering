# 【Python3】【LeetCode】【10】Valid Sudoku

 

### 题目

*Determine if a 9x9 Sudoku board is valid. Only the filled cells need to be validated **according to the following rules**:*

1. *Each row must contain the digits `1-9` without repetition.*
2. *Each column must contain the digits `1-9` without repetition.*
3. *Each of the 9 `3x3` sub-boxes of the grid must contain the digits `1-9` without repetition.*

*![img](https://upload.wikimedia.org/wikipedia/commons/thumb/f/ff/Sudoku-by-L2G-20050714.svg/250px-Sudoku-by-L2G-20050714.svg.png)*
*A partially filled sudoku which is valid.*

*The Sudoku board could be partially filled, where empty cells are filled with the character `'.'`.*

***Example 1:***

```
Input:
[
  ["5","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
Output: true
```

***Example 2:***

```
Input:
[
  ["8","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
Output: false
Explanation: Same as Example 1, except with the 5 in the top left corner being 
    modified to 8. Since there are two 8's in the top left 3x3 sub-box, it is invalid.
```

***Note:***

- *A Sudoku board (partially filled) could be valid but is not necessarily solvable.*
- *Only the filled cells need to be validated according to the mentioned rules.*
- *The given board contain only digits `1-9` and the character `'.'`.*
- *The given board size is always `9x9`.*

### Version1

判断一个表格是否符合数独的规则：

（1）行无重复

（2）列无重复

（3）3x3小格子无重复

转换成代码：

```python
class Solution:
    def isValidSudoku(self, board):
        if not checkBoard(board):
            return False
        for i in range(9):
            if not isSingle(board[i]):
                return False
            if not isSingle(col(board, i)):
                return False
            if not isSingle(rect(board, i)):
                return False

        return True


def col(board, x):
    res = []
    for i in range(9):
        res.append(board[i][x])
    return res


def rect(board, order):
    x = int(order / 3) * 3
    y = order % 3 * 3
    res = []
    for i in range(3):
        for j in range(3):
            res.append(board[x + i][y + j])
    return res


def checkBoard(nums):
    for j in nums:
        for i in j:
            if i == '.' or (i.isdigit() and len(i) == 1):
                continue
            else:
                return False
    return True


def isSingle(nums):
    nums = list(filter(lambda a: a != '.', nums))
    return len(nums) == len(set(nums))

```

### 抄作业

这个答案从实现上化简了一下上面的思路，值得借鉴。

使用一个set作为额外的存储，每个格子对应在set存储三个值：

(行，值) ，（值，列），（小方块行，小方块列，值）

遍历每个元素，检查这个元素的三个值是否在set中，在则说明有重复，直接返回true，不在则插入这个元素的三个值。

查询、插入操作的复杂度都是O(n)，整体的最坏复杂度~7n （n==9*9）。

```python
class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        big = set()
        for i in range(0,9):
            for j in range(0,9):
                if board[i][j]!='.':
                    cur = board[i][j]
                    if (i,cur) in big or (cur,j) in big or (i//3,j//3,cur) in big:
                        return False
                    big.add((i,cur))
                    big.add((cur,j))
                    big.add((i//3,j//3,cur))
        return True
```

