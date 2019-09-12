import edu.princeton.cs.algs4.In;
import edu.princeton.cs.algs4.MinPQ;
import edu.princeton.cs.algs4.Stack;
import edu.princeton.cs.algs4.StdOut;

public class Solver {

    private SearchNode currentTwinNode;
    private SearchNode currentNode;
    private Stack<Board> result;

    private class SearchNode implements Comparable<SearchNode> {
        private final Board board;
        private SearchNode preSearchNode = null;
        private final int moves;
        private final int priority;

        public SearchNode(Board board, SearchNode pNode) {
            this.board = board;
            this.preSearchNode = pNode;
            if (null == preSearchNode)
                moves = 0;
            else
                moves = preSearchNode.getMoves() + 1;
            priority = board.manhattan() + getMoves();
        }

        @Override
        public int compareTo(SearchNode otherNode) {
            return Integer.compare(this.getPriority(), otherNode.getPriority());
        }

        public int getMoves() {
            return moves;
        }

        public int getPriority() {
            return priority;
        }

        public Board getBoard() {
            return board;
        }

        public SearchNode getPreSearchNode() {
            return preSearchNode;
        }
    }

    // find a solution to the initial board (using the A* algorithm)
    public Solver(Board initial) {
        if (null == initial)
            throw new IllegalArgumentException();
        currentNode = new SearchNode(initial, null);
        MinPQ<SearchNode> minInitialPQ = new MinPQ<>();
        MinPQ<SearchNode> minTwinNode = new MinPQ<>();
        minInitialPQ.insert(currentNode);
        currentTwinNode = new SearchNode(initial.twin(), null);
        minTwinNode.insert(currentTwinNode);
        while (true) {
            currentNode = minInitialPQ.delMin();
            if (currentNode.getBoard().isGoal())
                break;
            else
                putNeighborsBoardToPQ(minInitialPQ, currentNode);

            currentTwinNode = minTwinNode.delMin();
            if (currentTwinNode.getBoard().isGoal())
                break;
            else
                putNeighborsBoardToPQ(minTwinNode, currentTwinNode);

        }
    }

    private void putNeighborsBoardToPQ(MinPQ<SearchNode> pq, SearchNode currentNode) {
        for (Board b : currentNode.getBoard().neighbors()) {
            if (null == currentNode.getPreSearchNode() ||
                    !b.equals(currentNode.getPreSearchNode().getBoard()))
                pq.insert(new SearchNode(b, currentNode));
        }
    }

    // is the initial board solvable? (see below)
    public boolean isSolvable() {
        return currentNode.getBoard().isGoal();
    }

    // min number of moves to solve initial board
    public int moves() {
        if (isSolvable())
            return currentNode.getMoves();
        else
            return -1;
    }

    // sequence of boards in a shortest solution
    public Iterable<Board> solution() {
        if (!isSolvable())
            return null;
        result = new Stack<Board>();
        SearchNode indexNode = currentNode;
        while (null != indexNode) {
            result.push(indexNode.getBoard());
            indexNode = indexNode.getPreSearchNode();
        }
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
