import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.StdRandom;

import java.util.ArrayList;
import java.util.Arrays;


// import edu.princeton.cs.algs4.In;
//
// import java.util.Arrays;
//
// import static java.lang.Math.abs;
//
// public class Board {
//
//     private final int n;
//     private final char[] blocks;
//     private int blankIndex;  // where is the blankIndex tile
//
//     // create a board from an n-by-n array of blocks,
//     // where blocks[row][col] = tile at (row, col)
//     public Board(int[][] blocks) {
//         n = blocks.length;
//         this.blocks = new char[n * n];
//         int k = 0;
//         for (int i = 0; i < n; i++) {
//             for (int j = 0; j < n; j++) {
//                 this.blocks[k] = (char) blocks[i][j];
//                 if (blocks[i][j] == 0)
//                     blankIndex = k;
//                 k++;
//             }
//         }
//
//     }
//
//     // string representation of this board
//     public String toString() {
//         StringBuilder sb = new StringBuilder();
//         sb.append(n + "\n");
//         int k = 0;
//         for (int i = 0; i < n; i++) {
//             for (int j = 0; j < n; j++) {
//                 sb.append(String.format("%2d ", (int) blocks[k]));
//                 k++;
//             }
//             sb.append("\n");
//         }
//
//         return sb.toString();
//     }
//
//     // board dimension n
//     public int dimension() {
//         return n;
//     }
//
//     // number of blocks out of place
//     public int hamming() {
//         int result = 0;
//         for (int i = 0; i < n * n; i++) {
//             if (blocks[i] != i + 1 && blocks[i] != 0)
//                 result++;
//         }
//         return result;
//     }
//
//     // sum of Manhattan distances between blocks and goal
//     public int manhattan() {
//         int result = 0;
//         for (int i = 0; i < n; i++) {
//             if (blocks[i] != 0)
//                 result += distance(blocks[i],i);
//         }
//
//         return result;
//     }
//
//     private int distance(int block, int i) {
//         // int row = block / n;
//         // int col = block % n - 1;
//         return abs(row(block)-row(i))+abs(col(block)-col(i));
//     }
//
//     private int row(int x) {
//         return x / n;
//     }
//
//     private int col(int x) {
//         return x % n - 1;
//     }
//
//
//     // is this board the goal board?
//     public boolean isGoal() {
//         if (blocks[n * n - 1] != 0)
//             return false;
//         // return is ordered?
//         for (int i = 0; i < n * n - 2; i++) {
//             if (blocks[i] > blocks[i + 1])
//                 return false;
//         }
//         return true;
//     }
//
//     // does this board equal y?
//     public boolean equals(Object y) {
//         if (y == null || y.getClass() != this.getClass())
//             return false;
//         if (y == this)
//             return true;
//         Board that = (Board) y;
//         return Arrays.equals(this.blocks, that.blocks);
//     }
//
//     // all neighboring boards
//     public Iterable<Board> neighbors() {
//         return null;
//     }
//
//     // a board that is obtained by exchanging any pair of blocks
//     public Board twin() {
//         return null;
//     }
//
//     // unit testing (not graded)
//     public static void main(String[] args) {
//         In in = new In(args[0]);
//         int n = in.readInt();
//         int[][] blocks = new int[n][n];
//         for (int i = 0; i < n; i++) {
//             for (int j = 0; j < n; j++) {
//                 blocks[i][j] = in.readInt();
//             }
//         }
//
//         Board b = new Board(blocks);
//         // System.out.println(b.toString());
//         System.out.println(b.hamming());
//         // System.out.println(b.isGoal());
//         System.out.println(b.manhattan());
//     }
//
// }
public class Board {

    private final int[][] blocks;
    private final int n;
    private int blankposx;
    private int blankposy;

    // create a board from an n-by-n array of blocks,
    // where blocks[row][col] = tile at (row, col)
    public Board(int[][] tiles) {
        // Storing a copy of the object is better approach in many situations
        this.n = tiles.length;
        this.blocks = Arrays.copyOf(tiles, n);  // deep copy
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (blocks[i][j] == 0)
                {
                    this.blankposx = i;
                    this.blankposy = j;
                    break;
                }
            }
        }
    }

    // string representation of this board
    public String toString() {
        StringBuilder sb = new StringBuilder();
        sb.append(n + "\n");
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                sb.append(String.format("%2d ", blocks[i][j]));
            }
            sb.append("\n");
        }
        return sb.toString();
    }

    // board dimension n
    public int dimension() {
        return n;
    }

    // number of blocks out of place
    public int hamming() {
        int result = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (blocks[i][j] != 0 && blocks[i][j] != index(i, j))
                    result++;
            }
        }
        return result;

    }

    private int index(int i, int j) {
        if ((i * n + j + 1) < (n * n))
            return i * n + j + 1;
        return 0;
    }


    // sum of Manhattan distances between blocks and goal
    public int manhattan() {
        int result = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (blocks[i][j] != 0) {
                    result += abs(i - row(blocks[i][j])) + abs(j - col(blocks[i][j]));
                }
            }
        }
        return result;
    }

    private int abs(int a) {
        return (a < 0) ? -a : a;
    }


    private int row(int x) {
        return (x - 1) / n;
    }

    private int col(int x) {
        return (x - 1) % n;
    }

    // is this board the goal board?
    public boolean isGoal()
    {
        return manhattan() == 0 && blocks[n - 1][n - 1] == 0;
    }

    // does this board equal y?
    public boolean equals(Object y)
    {
        if (y == null || y.getClass() != this.getClass())
            return false;
        if (y == this)
            return true;
        Board that = (Board) y;
        return Arrays.equals(this.blocks, that.blocks);
    }

    // all neighboring boards
    public Iterable<Board> neighbors() {
        // swap 0 and up/down/left/right
        ArrayList<Board> neighbor = new ArrayList<Board>();
        if (blankposx > 0) {
            int[][] arr = exchage(blankposx - 1, blankposy);
            Board tmpb = new Board(arr);
            neighbor.add(tmpb);
            // System.out.println(tmpb.toString());
        }
        if (blankposx < n-1) {
            int[][] arr = exchage(blankposx + 1, blankposy);
            Board tmpb = new Board(arr);
            neighbor.add(tmpb);
        }
        if (blankposy > 0) {
            int[][] arr = exchage(blankposx, blankposy - 1);
            Board tmpb = new Board(arr);
            neighbor.add(tmpb);
        }
        if (blankposx < n-1) {
            int[][] arr = exchage(blankposx, blankposy + 1);
            Board tmpb = new Board(arr);
            neighbor.add(tmpb);
        }
        return neighbor;
    }

    private int[][] exchage(int targetx, int targety) {
        int arr[][] = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                arr[i][j] = blocks[i][j];
            }
        }
        arr[blankposx][blankposy] = arr[targetx][targety];
        arr[targetx][targety] = 0;
        return arr;
    }


    // a board that is obtained by exchanging any pair of blocks
    public Board twin()
    {
        ArrayList<Board> neibor = (ArrayList<Board>) neighbors();
        int uniform = StdRandom.uniform(neibor.size());
        return neibor.get(uniform);

    }

    // unit testing (not graded)
    public static void main(String[] args) {
        In in = new In(args[0]);
        int n = in.readInt();
        int[][] blocks = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                blocks[i][j] = in.readInt();
            }
        }

        Board b = new Board(blocks);
        // Board bsame = new Board(blocks);
        // System.out.println(b.equals(bsame));
        // System.out.println(b.toString());
        // System.out.println(b.neighbors());
        System.out.println(b.twin());
        // System.out.println(b.dimension());

        // System.out.println(b.goal());

        // System.out.println(b.hamming());
        // System.out.println(b.isGoal());
        // System.out.println(b.manhattan());
        // b.manhattan();
    }

}
