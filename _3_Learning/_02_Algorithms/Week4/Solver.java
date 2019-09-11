import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.MinPQ;
import edu.princeton.cs.algs4.StdOut;

import java.util.ArrayList;

public class Solver {
    private Board current;
    private MinPQ<Board> pq = new MinPQ<Board>(1, Board::compareTo);
    private ArrayList<Board> result = new ArrayList<Board>();
    private int moves;

    // find a solution to the initial board (using the A* algorithm)
    public Solver(Board initial) {
        if (initial == null)
            throw new IllegalArgumentException();
        pq.insert(initial);
        moves = -1;
        while (!isSolvable()) {
            result.add(pq.min());
            current = pq.min();
            pq.delMin();
            moves++;
            for (Board board : current.neighbors()) {
                pq.insert(board);
            }

        }
    }

    // is the initial board solvable? (see below)
    public boolean isSolvable() {
        if (result.isEmpty())
            return false;
        Board min = result.get(result.size() - 1);
        return min.isGoal();
    }

    // min number of moves to solve initial board
    public int moves() {
        return moves;
    }

    // sequence of boards in a shortest solution
    public Iterable<Board> solution() {
        return result;
    }

    // test client (see below)
    public static void main(String[] args) {
        // create initial board from file
        In in = new In(args[0]);
        int n = in.readInt();
        int[][] tiles = new int[n][n];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < n; j++)
                tiles[i][j] = in.readInt();
        Board initial = new Board(tiles);

        // solve the puzzle
        Solver solver = new Solver(initial);

        // print solution to standard output
        if (!solver.isSolvable())
            StdOut.println("No solution possible");
        else {
            StdOut.println("Minimum number of moves = " + solver.moves());
            for (Board board : solver.solution())
                StdOut.println(board);
        }

    }

}
